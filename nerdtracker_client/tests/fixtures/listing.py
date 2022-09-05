import pytest
from freezegun import freeze_time

import nerdtracker_client.constants.stats as ntc_stats
from nerdtracker_client.player_list import EmptyListing, Listing
from nerdtracker_client.tests.constants import DATE_FLOAT, DATE_STRING


@pytest.fixture
def listing() -> Listing:
    """Returns a listing object

    Returns:
        Listing: A listing object
    """
    with freeze_time(DATE_STRING):
        return Listing("5")


@pytest.fixture
def listing_true() -> Listing:
    """Returns a listing object with full_match set to True

    Returns:
        Listing: A listing object
    """
    with freeze_time(DATE_STRING):
        return Listing("5", full_match=True)


@pytest.fixture
def listing_with_stats(fake_stats: ntc_stats.StatColumns) -> Listing:
    """Returns a listing object with stats

    Args:
        fake_stats (ntc_stats.StatColumns): The stats for the listing

    Returns:
        Listing: A listing object
    """
    with freeze_time(DATE_STRING):
        return Listing("5", stats=fake_stats)


@pytest.fixture
def empty_listing() -> EmptyListing:
    """Returns an empty listing object

    Returns:
        EmptyListing: An empty listing object
    """
    with freeze_time(DATE_STRING):
        return EmptyListing()
