import concurrent.futures
import urllib.parse
from typing import Generator

import cloudscraper
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from cloudscraper import CloudScraper
from cloudscraper.exceptions import CloudflareChallengeError

import nerdtracker_client.constants.stats as ntc_stats


def create_scraper() -> CloudScraper:
    """Create a CloudScraper object

    Returns:
        CloudScraper: CloudScraper object
    """
    scraper = cloudscraper.create_scraper()
    return scraper


def retrieve_page_from_tracker(
    scraper: CloudScraper,
    activision_user_string: str,
    cold_war_flag: bool = False,
) -> BeautifulSoup:
    """Retrieve page from tracker.gg using the activision user ID

    Given a scraper object and an activision user ID, retrieve the page from
    tracker.gg and return a BeautifulSoup object

    Args:
        scraper (CloudScraper): CloudScraper object. Could theoretically be
            any object that has a get method, but CloudScraper is the only
            object that so far works with tracker.gg
        activision_user_string (str): Activision user string
        cold_war_flag (bool): Flag to indicate whether to retrieve stats from
            Cold War or Modern Warfare. Defaults to False, which retrieves
            stats from Modern Warfare. True is mostly for testing purposes.

    Returns:
        BeautifulSoup: BeautifulSoup object
    """
    # Retrieve page from tracker.gg using the activision user ID
    activision_user_string = urllib.parse.quote(activision_user_string)
    mw_url = "modern-warfare"
    cw_url = "cold-war"
    selected_url = mw_url if not cold_war_flag else cw_url
    base_url = "https://cod.tracker.gg/" + selected_url + "/profile/atvi/"
    tracker_url = base_url + activision_user_string + "/mp"
    try:
        request = scraper.get(tracker_url)
    except CloudflareChallengeError:
        # In case of Cloudflare challenge, retry only once
        try:
            request = scraper.get(tracker_url)
        except CloudflareChallengeError:
            return BeautifulSoup("", "html.parser")

    # Parse the tracker.gg page using BeautifulSoup
    soup = BeautifulSoup(request.content, "html.parser")

    return soup


def parse_tracker_html(soup: BeautifulSoup) -> ntc_stats.StatColumns:
    """Parse tracker.gg page using BeautifulSoup, returning a dictionary of
    stats

    Args:
        soup (BeautifulSoup): BeautifulSoup object

    Returns:
        dict: Dictionary of stats
    """

    def soup_find_all() -> Generator[Tag, None, None]:
        """Generator function that extracts all relevant stats from the
        BeautifulSoup object

        Yields:
            bs4.element.Tag: BeautifulSoup Tag object
        """
        tag_set: ResultSet[Tag] = soup.find_all("div", {"class": "numbers"})
        for tag in tag_set:
            yield tag

    def extract_stat(tag: Tag) -> tuple[str, str]:
        """Extract stat from a Tag object, returning a tuple of the stat name
        and value

        Args:
            tag (bs4.element.Tag): BeautifulSoup Tag object

        Returns:
            tuple[str, str]: Tuple of stat name and value
        """
        name = tag.find(class_="name").string
        value = tag.find(class_="value").string
        return name, value

    temp_stats_dict: dict[str, str | None] = {}
    # If the page is found, fill the dictionary with the stats
    for stat_soup in soup_find_all():
        name, value = extract_stat(stat_soup)
        # Takes only the first value if there are multiple values to leverage
        # the design of the webpage
        if (name in ntc_stats.STAT_COLUMNS) and (name not in temp_stats_dict):
            temp_stats_dict[name] = value

    # The below has not been resolved in mypy. See:
    # https://github.com/python/mypy/issues/8890
    stat_dict = ntc_stats.StatColumns(**temp_stats_dict)  # type: ignore

    return stat_dict


def retrieve_stats(
    activision_user_string: str, cold_war_flag: bool = False
) -> ntc_stats.StatColumns:
    """Retrieve stats from tracker.gg using the activision user ID

    Given an activision user ID, retrieve the stats from tracker.gg and return
    a dictionary of stats

    Args:
        activision_user_string (str): Activision user string
        cold_war_flag (bool): Flag to indicate whether to retrieve stats from
            Cold War or Modern Warfare. Defaults to False, which retrieves
            stats from Modern Warfare. True is mostly for testing purposes.

    Returns:
        dict: Dictionary of stats
    """
    scraper = create_scraper()
    soup = retrieve_page_from_tracker(
        scraper, activision_user_string, cold_war_flag=cold_war_flag
    )
    stat_dict = parse_tracker_html(soup)
    return stat_dict


def retrieve_stats_multiple(
    user_list: list[str],
    cold_war_flag: bool = False,
) -> list[ntc_stats.StatColumns | None]:
    """Retrieve stats from tracker.gg for multiple users using concurrency

    Given a list of activision user IDs, retrieve the stats from tracker.gg
    and return a list of StatColumns objects in the same order as the input. If
    a user is not found, the corresponding entry in the list will be None. This
    function uses concurrency to speed up the process.

    Args:
        user_list (list[str]): List of activision user IDs
        cold_war_flag (bool): Flag to indicate whether to retrieve stats from
            Cold War or Modern Warfare. Defaults to False, which retrieves
            stats from Modern Warfare. True is mostly for testing purposes.

    Returns:
        list[dict]: List of dictionaries of stats
    """
    scraper = create_scraper()
    stat_list: list[ntc_stats.StatColumns | None] = [None] * len(user_list)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_user = {
            executor.submit(
                retrieve_page_from_tracker, scraper, user, cold_war_flag
            ): user
            for user in user_list
            if user is not None and user != ""
        }
        for future in concurrent.futures.as_completed(future_to_user):
            user = future_to_user[future]
            try:
                soup = future.result()
            except Exception as exc:
                print(f"{user} generated an exception: {exc}")
            else:
                stat_dict = parse_tracker_html(soup)
                stat_list[user_list.index(user)] = stat_dict

    return stat_list
