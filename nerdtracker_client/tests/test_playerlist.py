from datetime import timedelta

import pytest
from freezegun import freeze_time

from nerdtracker_client.player_list import EmptyListing, Listing, SnapshotList

DATE_STRING = "2022-07-21 12:00:01"
DATE_FLOAT = 1658404801.0


class TestSnapshotList:
    @freeze_time(DATE_STRING)
    def test_init(self) -> None:
        """Tests the init method of the snapshot list class"""

        snapshot_list = SnapshotList([], 10, 300.0)

        assert snapshot_list.list == []
        assert snapshot_list.last_update == DATE_FLOAT
        assert snapshot_list.max_list_length == 10
        assert snapshot_list.max_list_age == 300

    @freeze_time(DATE_STRING)
    def test_repr(self) -> None:
        """Tests the repr method of the snapshot list class"""

        snapshot_list = SnapshotList([], 10, 300.0)

        expected = (
            "SnapshotList(\n"
            + "\tNo. Listings: 0,\n"
            + f"\tLast Update: {DATE_FLOAT},\n"
            + "\tMax Age: 300.0,\n"
            + "\tMax Length: 10,\n"
            + ")"
        )
        assert repr(snapshot_list) == expected

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

    def test_stale_override(self, ten_listings_no_empty: list[Listing]) -> None:
        """Tests the stale_override method of the snapshot list class"""

        with freeze_time(DATE_STRING) as frozen_datetime:
            snapshot_list = SnapshotList([Listing("99")], 10, 300.0)
            frozen_datetime.tick(delta=timedelta(seconds=301))
            snapshot_list.new_snapshot(ten_listings_no_empty)

        assert snapshot_list.list == ten_listings_no_empty
        assert snapshot_list.last_update == DATE_FLOAT + 301

    def test_drop(self, ten_listings_no_empty: list[Listing]) -> None:
        """Tests the drop method of the snapshot list class"""

        expected_order = ten_listings_no_empty[:8]
        initial_snapshot = ten_listings_no_empty

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_list.drop(8)

        assert snapshot_list.list == expected_order

    def test_insert(
        self,
        ten_listings_no_empty: list[Listing],
        nine_listings_removed_6: list[Listing],
    ) -> None:
        """Tests the insert method of the snapshot list class"""

        expected_order = ten_listings_no_empty
        initial_snapshot = nine_listings_removed_6

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_list.insert([Listing("7")], 6)

        assert snapshot_list.list == expected_order

    def test_sequential_forward_no_drops_no_overlap_no_empty(
        self, ten_listings_no_empty: list[Listing]
    ) -> None:
        """Tests the sequential_forward method of the snapshot list class with
        no drops"""

        expected_order = ten_listings_no_empty
        initial_snapshot = [listing.copy() for listing in expected_order[:4]]
        new_snapshot = [listing.copy() for listing in expected_order[4:]]

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_list.new_snapshot(new_snapshot)

        assert snapshot_list.list == expected_order

    def test_sequential_forward_no_drops_w_overlap_no_empty(
        self, ten_listings_no_empty: list[Listing]
    ) -> None:
        """Tests the sequential_forward method of the snapshot list class with
        no drops and an overlap"""

        expected_order = ten_listings_no_empty
        initial_snapshot = [listing.copy() for listing in expected_order[:4]]
        new_snapshot = [listing.copy() for listing in expected_order[2:]]

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_list.new_snapshot(new_snapshot)

        assert snapshot_list.list == expected_order

    def test_sequential_forward_no_drops_no_overlap_w_empty(
        self, twelve_listings_two_empty: list[Listing | EmptyListing]
    ) -> None:
        """Tests the sequential_forward method of the snapshot list class with
        drops"""

        expected_order = twelve_listings_two_empty
        initial_snapshot = [listing.copy() for listing in expected_order[:5]]
        new_snapshot = [listing.copy() for listing in expected_order[5:]]

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_list.new_snapshot(new_snapshot)

        assert snapshot_list.list == expected_order

    def test_sequential_forward_no_drops_w_overlap_w_empty(
        self, twelve_listings_two_empty: list[Listing | EmptyListing]
    ) -> None:
        """Tests the sequential_forward method of the snapshot list class with
        drops and an overlap"""

        expected_order = twelve_listings_two_empty
        initial_snapshot = [listing.copy() for listing in expected_order[:7]]
        new_snapshot = [listing.copy() for listing in expected_order[5:]]

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_list.new_snapshot(new_snapshot)

        assert snapshot_list.list == expected_order

    def test_sequential_forward_w_drops_w_overlap_no_empty(
        self,
        ten_listings_no_empty: list[Listing],
        nine_listings_removed_6: list[Listing],
    ) -> None:
        """Tests the sequential_forward method of the snapshot list class with
        drops"""

        expected_order = nine_listings_removed_6
        initial_snapshot = [
            listing.copy() for listing in ten_listings_no_empty[:8]
        ]

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_without_index_4 = [
            listing.copy()
            for index, listing in enumerate(ten_listings_no_empty)
            if index != 6 and index >= 4
        ]
        snapshot_list.new_snapshot(snapshot_without_index_4)

        assert snapshot_list.list == expected_order

    def test_sequential_backwards_w_drops_w_overlap_no_empty(
        self,
        ten_listings_no_empty: list[Listing],
        nine_listings_removed_6: list[Listing],
    ) -> None:
        """Tests the sequential_forward method of the snapshot list class with
        drops"""

        expected_order = nine_listings_removed_6
        initial_snapshot = [
            listing.copy() for listing in ten_listings_no_empty[3:]
        ]

        snapshot_list = SnapshotList(initial_snapshot, 10, 300.0)
        snapshot_without_index_4 = [
            listing.copy()
            for index, listing in enumerate(ten_listings_no_empty)
            if index != 6 and index <= 7
        ]
        snapshot_list.new_snapshot(snapshot_without_index_4)

        assert snapshot_list.list == expected_order
