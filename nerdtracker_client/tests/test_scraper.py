import pytest
from bs4 import BeautifulSoup

import nerdtracker_client.constants.stats as ntc_stats
from nerdtracker_client.scraper import (
    create_scraper,
    parse_tracker_html,
    retrieve_page_from_tracker,
    retrieve_stats,
    retrieve_stats_multiple,
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
    def test_parse_tracker_html(
        self, html_page: str, joy_stats: ntc_stats.StatColumns
    ) -> None:
        soup = BeautifulSoup(html_page, "html.parser")
        stats = parse_tracker_html(soup)
        # TODO: Find a better way to type: ignore this
        assert stats == joy_stats


class TestRetrieve:
    def test_retrieve_stats(
        self,
        valid_activision_user_string: str,
        joy_stats: ntc_stats.StatColumns,
    ) -> None:
        stats = retrieve_stats(valid_activision_user_string, cold_war_flag=True)
        if stats == {}:
            pytest.skip("Cloudflare challenge detected, skipping test")
        assert stats == joy_stats
