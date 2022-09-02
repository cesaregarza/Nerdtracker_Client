import pytest

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
