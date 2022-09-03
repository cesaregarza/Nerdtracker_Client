import pytest
from bs4 import BeautifulSoup

import nerdtracker_client.constants.stats as ntc_stats
from nerdtracker_client.scraper import (
    create_scraper,
    parse_tracker_html,
    retrieve_page_from_tracker,
)


class TestScraper:
    def test_retrieve_page_from_tracker(
        self, valid_activision_user_string
    ) -> None:
        scraper = create_scraper()
        soup = retrieve_page_from_tracker(
            scraper, valid_activision_user_string, cold_war_flag=True
        )
        # Check that the soup object does not contain a failed request message
        failed_string = "Enable JavaScript and cookies to continue"
        assert failed_string not in soup.text

    def test_retrieve_invalid_page_from_tracker(
        self, invalid_activision_user_string
    ) -> None:
        scraper = create_scraper()
        soup = retrieve_page_from_tracker(
            scraper, invalid_activision_user_string, cold_war_flag=True
        )
        # Check that the soup object contains a failed stats message
        failed_string = "stats not found"
        assert failed_string in soup.text

    def test_retrieve_empty_page_from_tracker(
        self, empty_activision_user_string
    ) -> None:
        scraper = create_scraper()
        soup = retrieve_page_from_tracker(
            scraper, empty_activision_user_string, cold_war_flag=True
        )
        # Check that the soup object contains a failed stats message
        failed_string = "404 Page not Found"
        assert failed_string in soup.text


class TestParseTrackerHtml:
    def test_parse_tracker_html(self, html_page) -> None:
        soup = BeautifulSoup(html_page, "html.parser")
        stats = parse_tracker_html(soup)
        # TODO: Find a better way to type: ignore this
        assert stats[ntc_stats.KD_RATIO] == "1.79"  # type: ignore
        assert stats[ntc_stats.WIN_PERC] == "52.9%"  # type: ignore
        assert stats[ntc_stats.SCORE_PER_MIN] == "742.72"  # type: ignore
        assert stats[ntc_stats.KILLS] == "52,349"  # type: ignore
        assert stats[ntc_stats.DEATHS] == "29,297"  # type: ignore
        assert stats[ntc_stats.WINS] == "793"  # type: ignore
        assert stats[ntc_stats.LOSSES] == "535"  # type: ignore
        assert stats[ntc_stats.TIES] == "8"  # type: ignore
        assert stats[ntc_stats.ASSISTS] == "3,252"  # type: ignore
        assert stats[ntc_stats.BEST_KILLSTREAK] == "31"  # type: ignore
        assert stats[ntc_stats.AVG_LIFESPAN] == "27.5s"  # type: ignore
        assert stats[ntc_stats.TOTAL_SCORE] == "9,973,255"  # type: ignore
