import pytest
from freezegun import freeze_time

from nerdtracker_client.player_list import EmptyListing, Listing, SnapshotList
from nerdtracker_client.player_list.listing import SIMILARITY_THRESHOLD

DATE_STRING = "2022-07-21 12:00:01"
DATE_FLOAT = 1658404801.0


class TestListing:
    @freeze_time(DATE_STRING)
    def test_init(self) -> None:
        """Tests the init method of the listing class"""

        listing = Listing("5")

        assert listing.listing_id == "5"
        assert listing.full_match is False
        assert isinstance(listing.listing_time, float)
        assert listing.listing_time == DATE_FLOAT

    @freeze_time(DATE_STRING)
    def test_repr(self) -> None:
        """Tests the __repr__ method of the listing class"""

        listing = Listing("5")

        expected_string = (
            "Listing(5, "
            + f"Threshold: {SIMILARITY_THRESHOLD}, "
            + "Time: 00m:00s"
            + ")"
        )

        assert repr(listing) == expected_string

    @freeze_time(DATE_STRING)
    def test_str(self) -> None:
        """Tests the __str__ method of the listing class"""

        listing = Listing("5")

        assert str(listing) == "5"

    @freeze_time(DATE_STRING)
    def test_eq(self) -> None:
        """Tests the __eq__ method of the listing class"""

        listing = Listing("5")
        equal_listing = Listing("5")
        unequal_listing = Listing("6")

        assert listing == equal_listing
        assert listing != unequal_listing

    @freeze_time(DATE_STRING)
    def test_time_since_listing(self) -> None:
        """Tests the time_since_listing method of the listing class"""

        listing = Listing("5")

        assert listing.time_since_listing() == "00m:00s"

    @freeze_time(DATE_STRING)
    def test_update_time(self) -> None:
        """Tests the update_time method of the listing class"""

        listing = Listing("5")
        listing.update_time(DATE_FLOAT + 1)

        assert listing.listing_time == DATE_FLOAT + 1

    @freeze_time(DATE_STRING)
    def test_update_time_with_none(self) -> None:
        """Tests the update_time method of the listing class with None"""

        listing = Listing("5")
        listing.update_time(None)

        assert listing.listing_time == DATE_FLOAT

    @freeze_time(DATE_STRING)
    def test_is_empty_property(self) -> None:
        """Tests the is_empty property of the listing class"""

        listing = Listing("5")
        assert listing.is_empty is False


class TestEmptyListing:
    def test_init(self) -> None:
        """Tests the init method of the empty listing class"""

        listing = EmptyListing()

        assert listing.listing_id is None
        assert listing.full_match is False
        assert isinstance(listing.listing_time, float)
        assert listing.listing_time == 0.0

    def test_repr(self) -> None:
        """Tests the __repr__ method of the empty listing class"""

        listing = EmptyListing()

        expected_string = "EmptyListing()"

        assert repr(listing) == expected_string

    def test_str(self) -> None:
        """Tests the __str__ method of the empty listing class"""

        listing = EmptyListing()

        assert str(listing) == ""

    def test_eq(self) -> None:
        """Tests the __eq__ method of the empty listing class"""

        listing = EmptyListing()
        second_listing = EmptyListing()

        assert listing != second_listing

    def test_time_since_listing(self) -> None:
        """Tests the time_since_listing method of the empty listing class"""

        listing = EmptyListing()

        assert listing.time_since_listing() == ""

    def test_update_time(self) -> None:
        """Tests the update_time method of the empty listing class"""

        listing = EmptyListing()
        listing.update_time(DATE_FLOAT)

        assert listing.listing_time == 0.0

    def test_update_time_with_none(self) -> None:
        """Tests the update_time method of the empty listing class with None"""

        listing = EmptyListing()
        listing.update_time(None)

        assert listing.listing_time == 0.0

    def test_is_empty_property(self) -> None:
        """Tests the is_empty property of the empty listing class"""

        listing = EmptyListing()

        assert listing.is_empty is True
