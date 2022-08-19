from typing import Union

import pytest

from nerdtracker_client.player_list import EmptyListing, Listing


@pytest.fixture
def ten_listings_no_empty() -> list[Listing]:
    """Returns a list of 10 listings with no empty listings"""
    return [
        Listing("1"),
        Listing("2"),
        Listing("3"),
        Listing("4"),
        Listing("5"),
        Listing("6"),
        Listing("7"),
        Listing("8"),
        Listing("9"),
        Listing("10"),
    ]


@pytest.fixture
def twelve_listings_two_empty() -> list[Union[Listing, EmptyListing]]:
    """Returns a list of 12 listings with two empty listings"""
    return [
        EmptyListing(),
        Listing("1"),
        Listing("2"),
        Listing("3"),
        Listing("4"),
        EmptyListing(),
        Listing("5"),
        Listing("6"),
        Listing("7"),
        Listing("8"),
        Listing("9"),
        Listing("10"),
    ]
