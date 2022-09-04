import pytest
from freezegun import freeze_time

from nerdtracker_client.player_list import EmptyListing, Listing
from nerdtracker_client.player_list.listing import SIMILARITY_THRESHOLD
from nerdtracker_client.tests.constants import DATE_FLOAT, DATE_STRING


class TestListing:
    def test_init(self, listing: Listing) -> None:
        """Tests the init method of the listing class"""

        assert listing.listing_id == "5"
        assert listing.full_match is False
        assert isinstance(listing.listing_time, float)
        assert listing.listing_time == DATE_FLOAT

    @freeze_time(DATE_STRING)
    def test_repr(self, listing: Listing) -> None:
        """Tests the __repr__ method of the listing class"""

        expected_string = (
            "Listing(5, "
            + "KDR: N/A, "
            + f"Threshold: {SIMILARITY_THRESHOLD}, "
            + "Time: 00m:00s"
            + ")"
        )

        assert repr(listing) == expected_string

    def test_str(self, listing: Listing) -> None:
        """Tests the __str__ method of the listing class"""

        assert str(listing) == "5"

    @freeze_time(DATE_STRING)
    def test_eq(self, listing: Listing) -> None:
        """Tests the __eq__ method of the listing class"""

        equal_listing = Listing("5")
        unequal_listing = Listing("6")

        assert listing == equal_listing
        assert listing != unequal_listing
        assert listing != 5
        assert listing != "5"

    @freeze_time(DATE_STRING)
    def test_time_since_listing(self, listing: Listing) -> None:
        """Tests the time_since_listing method of the listing class"""

        assert listing.time_since_listing() == "00m:00s"

    @freeze_time(DATE_STRING)
    def test_update_time(self, listing: Listing) -> None:
        """Tests the update_time method of the listing class"""

        listing.update_time(DATE_FLOAT + 1)

        assert listing.listing_time == DATE_FLOAT + 1

    @freeze_time(DATE_STRING)
    def test_update_time_with_none(self, listing: Listing) -> None:
        """Tests the update_time method of the listing class with None"""

        listing.update_time(None)

        assert listing.listing_time == DATE_FLOAT

    def test_is_empty_property(self, listing: Listing) -> None:
        """Tests the is_empty property of the listing class"""

        assert listing.is_empty is False

    def test_update_id_full_match(self, listing: Listing) -> None:
        """Tests the update_id_full_match method of the listing class"""

        assert listing.full_match is False

        listing.update_id_full_match("6")
        assert listing.listing_id == "6"
        assert listing.full_match is True

    def test_update_id_full_match_attempt_update_again(
        self, listing_true: Listing
    ) -> None:
        """Tests the update_id_full_match method on a listing with an already
        full match"""

        assert listing_true.full_match is True

        listing_true.update_id_full_match("6")
        assert listing_true.listing_id == "5"
        assert listing_true.full_match is True

    def test_update_full_match_attempt_update_again(
        self, listing_true: Listing
    ) -> None:
        """Tests the update_full_match method on a listing with an already
        full match"""
        assert listing_true.full_match is True

        new_listing = Listing("6")
        listing_true.update(new_listing)
        assert listing_true.listing_id == "5"
        assert listing_true.full_match is True


class TestEmptyListing:
    def test_init(self, empty_listing: EmptyListing) -> None:
        """Tests the init method of the empty listing class"""

        assert empty_listing.listing_id is None
        assert empty_listing.full_match is False
        assert isinstance(empty_listing.listing_time, float)
        assert empty_listing.listing_time == 0.0

    def test_repr(self, empty_listing: EmptyListing) -> None:
        """Tests the __repr__ method of the empty listing class"""

        expected_string = "EmptyListing()"

        assert repr(empty_listing) == expected_string

    def test_str(self, empty_listing: EmptyListing) -> None:
        """Tests the __str__ method of the empty listing class"""

        assert str(empty_listing) == ""

    def test_eq(self, empty_listing: EmptyListing) -> None:
        """Tests the __eq__ method of the empty listing class"""

        second_listing = EmptyListing()

        assert empty_listing == second_listing

    def test_time_since_listing(self, empty_listing: EmptyListing) -> None:
        """Tests the time_since_listing method of the empty listing class"""

        assert empty_listing.time_since_listing() == ""

    def test_update_time(self, empty_listing: EmptyListing) -> None:
        """Tests the update_time method of the empty listing class"""

        empty_listing.update_time(DATE_FLOAT)

        assert empty_listing.listing_time == 0.0

    def test_update_time_with_none(self, empty_listing: EmptyListing) -> None:
        """Tests the update_time method of the empty listing class with None"""

        empty_listing.update_time(None)

        assert empty_listing.listing_time == 0.0

    def test_is_empty_property(self, empty_listing: EmptyListing) -> None:
        """Tests the is_empty property of the empty listing class"""

        assert empty_listing.is_empty is True

    def test_update_id_full_match(self, empty_listing: EmptyListing) -> None:
        """Tests the update_id_full_match method of the empty listing class"""

        assert empty_listing.full_match is False

        empty_listing.update_id_full_match("6")
        assert empty_listing.listing_id is None
        assert empty_listing.full_match is False
