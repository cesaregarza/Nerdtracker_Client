import urllib.parse
from typing import Generator

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from cloudscraper import CloudScraper

import nerdtracker_client.constants.stats as ntc_stats


def retrieve_page_from_tracker(
    scraper: CloudScraper, activision_user_string: str
) -> BeautifulSoup:
    """Retrieve page from tracker.gg, returning a BeautifulSoup object

    Args:
        scraper (CloudScraper): CloudScraper object
        activision_user_string (str): Activision user string

    Returns:
        BeautifulSoup: BeautifulSoup object
    """
    # Retrieve page from tracker.gg using the activision user ID
    activision_user_string = urllib.parse.quote(activision_user_string)
    base_url = "https://cod.tracker.gg/modern-warfare/profile/atvi/"
    tracker_url = base_url + activision_user_string + "/mp"
    request = scraper.get(tracker_url)

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
        temp_stats_dict[name] = value

    # Remove stats not in ntc_stats.STAT_COLUMNS
    temp_stats_dict = {
        key: value
        for key, value in temp_stats_dict.items()
        if key in ntc_stats.STAT_COLUMNS
    }

    # The below has not been resolved in mypy. See:
    # https://github.com/python/mypy/issues/8890
    stat_dict = ntc_stats.StatColumns(**temp_stats_dict)  # type: ignore

    return stat_dict
