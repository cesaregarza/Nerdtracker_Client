import time
from typing import Optional, TypeVar, cast

from nerdtracker_client.player_list.listing import EmptyListing, Listing
from nerdtracker_client.util import identify_missing_values

T = TypeVar("T", bound=Listing)


class SnapshotList:
    """SnapshotList class is a class that tries to keep a real-time list based
    on the snapshot fed to it. More formally, it keeps a list of length n based
    on a snapshot fed to it of length k. It will then attempt to update the list
    based on the snapshot and assumptions fed to it.
    """

    def __init__(
        self,
        initial_snapshot: list[T],
        max_list_length: int = 12,
        max_list_age: float = 5.0 * 60.0,
    ) -> None:
        """Initializes the SnapshotList class.

        Args:
            initial_snapshot (list[T]): The initial snapshot to use to create
                the list.
            max_list_length (int): Maximum length to attempt to keep. Defaults
                to 12.
            max_list_age (float): Maximum age, in seconds, before the
                SnapshotList is considered stale. Defaults to 300 seconds.
        """
        self.list: list[T] = initial_snapshot
        self.last_update = time.time()
        self.max_list_length = max_list_length
        self.max_list_age = max_list_age

    def __repr__(self) -> str:
        out_str = (
            "SnapshotList(\n"
            + f"\tNo. Listings: {len(self.list)},\n"
            + f"\tLast Update: {self.last_update},\n"
            + f"\tMax Age: {self.max_list_age},\n"
            + f"\tMax Length: {self.max_list_length},\n"
            + ")"
        )
        return out_str

    @property
    def __is_list_stale(self) -> bool:
        """Whether the list is stale

        Checks whether the list is stale based on the last update time and the
        maximum age of the list.

        Returns:
            bool: Whether the list is stale
        """
        return (time.time() - self.last_update) > self.max_list_age

    @staticmethod
    def from_list_of_strings(
        initial_snapshot: list[str | None],
        max_list_length: int = 12,
        max_list_age: float = 5.0 * 60.0,
    ) -> "SnapshotList":
        """Creates a SnapshotList from a list of strings.

        Given a list of strings, creates a SnapshotList with the strings as the
        listings. If the string is empty or None, it will be converted to an
        EmptyListing. Otherwise, the string will be used to create a new
        Listing.

        Args:
            initial_snapshot (list [str | None]): The initial snapshot to use to
                create the SnapshotList.
            max_list_length (int): Max length the list will attempt to keep.
                Defaults to 12.
            max_list_age (float): Maximum age, in seconds, before the
                SnapshotList is considered stale. Defaults to 300 seconds.

        Returns:
            SnapshotList: The SnapshotList created from the list of strings.
        """

        fed_snapshot = []
        for snapshot_row in initial_snapshot:
            if (snapshot_row == "") or (snapshot_row is None):
                listing: Listing | EmptyListing = EmptyListing()
            else:
                listing = Listing(snapshot_row)
            fed_snapshot.append(listing)
        return SnapshotList(fed_snapshot, max_list_length, max_list_age)

    def __contains__(self, listing: T) -> bool:
        """Checks whether the fed listing is in the SnapshotList.

        Args:
            listing (T): The listing to check, where T is a subclass of Listing.

        Returns:
            bool: Whether the listing is in the SnapshotList.
        """
        return listing in self.list

    def new_snapshot(self, new_snapshot: list[T]) -> None:
        """Updates the list based on a new snapshot.

        Given a new snapshot of Listings, updates the list with a few
        assumptions. First, if there is no overlap between the new snapshot and
        the current list, the list will be appended with the new snapshot. If
        there is an overlap, then depending on where the overlap is, the shared
        listings will be updated and the rest will be either appended or
        prepended. Missing listings from the current list will be dropped. If
        the list is stale, it will be replaced with the new snapshot.

        Args:
            new_snapshot (list[T]): The new snapshot to use to update the list.
        """
        # If the list is stale, update it.
        if self.__is_list_stale:
            self.list = new_snapshot
            self.last_update = time.time()
            return

        # Find the first and last listing that are not empty
        first_listing: Listing | None = None
        last_listing: Listing | None = None
        for new_listing in new_snapshot:
            if (first_listing is None) and (not new_listing.is_empty):
                first_listing = new_listing

            if not new_listing.is_empty:
                last_listing = new_listing

        # Assume the order never changes. Find where the new snapshot fits in.
        first_listing_found: bool = False
        last_listing_found: bool = False
        for listing in self.list:
            if listing.is_empty:
                continue
            if listing == first_listing:
                first_listing_found = True
            if listing == last_listing:
                last_listing_found = True

        # Four cases:
        # 1. Neither are found. Append the new snapshot to the end.
        if not first_listing_found and not last_listing_found:
            self.list += new_snapshot
        # 2. Either case is found. Calculate overlaps, drops, and appends. Then,
        # use whether first OR last is found to determine whether to append or
        # prepend for new entries. The case where both are found is handled by
        # the overlap and drop case in its entirety.
        elif first_listing_found or last_listing_found:
            (
                overlap_indices_old,
                overlap_indices_new,
            ) = self.__new_snapshot_overlap(new_snapshot)
            dropped_indices = identify_missing_values(overlap_indices_old)
            new_indices = [
                index
                for index, listing in enumerate(new_snapshot)
                if (index not in dropped_indices)
                and (index not in overlap_indices_new)
                and not (listing.is_empty and index == 0)
            ]
            # Go through the overlap indices and update them.
            for new_index, old_index in zip(
                overlap_indices_new, overlap_indices_old
            ):
                if old_index is None:
                    continue
                new_index = cast(int, new_index)
                self.__update_existing_listing(
                    new_snapshot[new_index], old_index
                )

            # Drop the listings that are considered dropped.
            self.drop_list(dropped_indices)

            # Add the listings that are not considered dropped and are not
            # overlapping with the existing listings.
            new_listings = [new_snapshot[index] for index in new_indices]
            self.add_list(new_listings, append=first_listing_found)

    def __new_snapshot_overlap(
        self, new_snapshot: list[T]
    ) -> tuple[list[int | None], list[int | None]]:
        """Calculates the overlap between the new snapshot and the current list.

        Given a new snapshot, calculates the overlap between the new snapshot
        and the current list. Returns two lists, one with the indices of the
        overlap in the current list and one with the indices of the overlap in
        the new snapshot.

        Args:
            new_snapshot (list[T]): A list of Listings to compare to the current
                list.

        Returns:
            tuple[list[int | None], list[int | None]]: A tuple of two lists,
                one with the indices of the overlap in the current list and one
                with the indices of the overlap in the new snapshot. If there is
                no overlap, the index will be None.
        """
        overlap_old_index: list[int | None] = []
        overlap_new_index: list[int | None] = []
        # Go through each listing. If it is in the new snapshot, add its index.
        # If it is an empty listing, add None. Otherwise, do nothing.
        for index, listing in enumerate(new_snapshot):
            if (listing in self.list) and (not listing.is_empty):
                # Find the index of the listing
                overlap_old_index.append(self.list.index(listing))
                overlap_new_index.append(index)
            elif listing.is_empty and (index > 0):
                overlap_old_index.append(None)
                overlap_new_index.append(None)
        return (overlap_old_index, overlap_new_index)

    def __update_existing_listing(self, new_listing: T, index: int) -> None:
        """Updates an existing listing with a new listing.

        Given a new listing and an index, updates the existing listing at that
        index with the new listing.

        Args:
            new_listing (T): The new listing to use to update the existing
                listing at the given index.
            index (int): The index of the existing listing to update.
        """
        old_listing = self.list[index]
        if isinstance(old_listing, EmptyListing):
            self.list[index] = new_listing
            return

        if isinstance(new_listing, EmptyListing):
            return

        if old_listing.full_match:
            return

        if new_listing.full_match:
            self.list[index] = new_listing
            return

        # TODO: Add logic to Listing to use all data from the listings.
        self.list[index].update(new_listing)
        return

    def drop(
        self,
        start_index: int,
        stop_index: Optional[int] = None,
        step: int = 1,
    ) -> None:
        """Drops one or more listings based on the index.

        Given a start index, a stop index, and a step, drops the listings
        between the start and stop index, stepping by the step. If the stop
        index is not given, drops the listing at the start index.

        Args:
            start_index (int): The index of the listing to drop, or start
                dropping from.
            stop_index (int, optional): The index to stop dropping at. If None,
                only the listing at start_index will be dropped. Defaults to
                None.
            step (int): The step size to use when dropping listings. Defaults to
                1.
        """
        if stop_index is None:
            stop_index = len(self.list)
        for _ in range(start_index, stop_index, step):
            self.list.pop(start_index)
        return

    def drop_list(self, indices: list[int]) -> None:
        """Drops one or more listings based on the index.

        Given a list of indices, drops the listings at those indices. In
        practice, this overwrites the existing list with a shallow copy with the
        dropped listings removed.

        Args:
            indices (list[int]): A list of indices to drop.
        """
        new_list = [
            listing
            for index, listing in enumerate(self.list)
            if index not in indices
        ]
        self.list = new_list

    def insert(
        self,
        new_list: list[T],
        start_index: int,
    ) -> None:
        """Inserts a list of listings into the current list.

        Given a list of listings and a start index, inserts the new listings
        into the current list at the start index. Does not support inserting
        listings into specific indices, must insert at the start index.

        Args:
            new_list (list[T]): A list of listings to insert into the current
                list.
            start_index (int): The index to insert the new listings at.
        """
        new_list = [
            *self.list[:start_index],
            *new_list,
            *self.list[start_index:],
        ]
        self.list = new_list

    def add_list(
        self,
        new_list: list[T],
        append: bool = True,
    ) -> None:
        """Adds a list of listings to the list.

        Args:
            new_list (list[Listing]): The new list to add.
            append (bool): Whether to append the new list or prepend it.
        """
        if append:
            self.list += new_list
        else:
            self.list = new_list + self.list

    def replace(
        self,
        new_list: list[T],
        start_index: int,
        stop_index: Optional[int] = None,
        step: int = 1,
    ) -> None:
        """Replaces one or more listings with a new list of listings.

        Given a new list of listings, a start index, a stop index, and a step,
        replaces the listings between the start and stop index, stepping by the
        step, with the new listings. If the stop index is not given, drops all
        listings after the start index and appends the new listings.

        Args:
            new_list (list[T]): The new list of listings to replace the existing
                listings with.
            start_index (int): The index of the listing to start replacing from.
            stop_index (int, optional): The index to stop replacing at. If None,
                all listings after start_index will be dropped and the new
                listings will be appended. Defaults to None.
            step (int): The step size to use when replacing listings.
        """
        if stop_index is None:
            stop_index = len(self.list)

        if len(new_list) != (stop_index - start_index):
            # Some values were dropped.
            self.drop(start_index, stop_index, step)
            self.insert(new_list, start_index)
