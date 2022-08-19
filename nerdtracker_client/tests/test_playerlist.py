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

    def test_is_empty_property(self) -> None:
        """Tests the is_empty property of the listing class"""

        listing = Listing("5")
        assert listing.is_empty is False

    def test_update_id_full_match(self) -> None:
        """Tests the update_id_full_match method of the listing class"""

        listing = Listing("5")
        assert listing.full_match is False

        listing.update_id_full_match("6")
        assert listing.listing_id == "6"
        assert listing.full_match is True

    def test_update_id_full_match_attempt_update_again(self) -> None:
        """Tests the update_id_full_match method on a listing with an already
        full match"""

        listing = Listing("5", True)
        assert listing.full_match is True

        listing.update_id_full_match("6")
        assert listing.listing_id == "5"
        assert listing.full_match is True


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

        assert listing == second_listing

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


class TestSnapshotList:
    @freeze_time(DATE_STRING)
    def test_init(self) -> None:
        """Tests the init method of the snapshot list class"""

        snapshot_list = SnapshotList([], 10, 300.0)

        assert snapshot_list.list == []
        assert snapshot_list.last_update == DATE_FLOAT
        assert snapshot_list.max_list_length == 10
        assert snapshot_list.max_list_age == 300

    def test_in(self) -> None:
        """Tests the __contains__ method of the snapshot list class"""

        listing_1 = Listing("5")
        listing_2 = Listing("55555555555555555555")
        listing_2_close = Listing("55555555555555555556")
        snapshot_list = SnapshotList([listing_1, listing_2], 10, 300.0)

        assert listing_1 in snapshot_list
        assert Listing("5") in snapshot_list
        assert Listing("6") not in snapshot_list
        assert listing_2_close in snapshot_list

    @freeze_time(DATE_STRING)
    def test_from_list_of_strings(self) -> None:
        """Tests the from_list_of_strings method of the snapshot list class"""

        snapshot_list = SnapshotList.from_list_of_strings(
            ["1", "2", "3", "", None]
        )

        one_listing = Listing("1")
        two_listing = Listing("2")
        three_listing = Listing("3")
        empty_listing = EmptyListing()

        expected_order = [
            one_listing,
            two_listing,
            three_listing,
            empty_listing,
            empty_listing,
        ]

        for actual, expected in zip(snapshot_list.list, expected_order):
            assert actual == expected

    def test_sequential_forward_no_drops_no_overlap_no_empty(self) -> None:
        """Tests the sequential_forward method of the snapshot list class with
        no drops"""

        expected_order = [
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
        initial_snapshot = expected_order[:4]

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_list.new_snapshot(expected_order[4:])

        assert snapshot_list.list == expected_order

    def test_sequential_forward_no_drops_w_overlap_no_empty(self) -> None:
        """Tests the sequential_forward method of the snapshot list class with
        no drops and an overlap"""

        expected_order = [
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
        initial_snapshot = expected_order[:4]

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_list.new_snapshot(expected_order[2:])

        assert snapshot_list.list == expected_order

    def test_sequential_forward_no_drops_no_overlap_w_empty(self) -> None:
        """Tests the sequential_forward method of the snapshot list class with
        drops"""

        expected_order = [
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
        initial_snapshot = expected_order[:5]

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_list.new_snapshot(expected_order[5:])

        assert snapshot_list.list == expected_order
