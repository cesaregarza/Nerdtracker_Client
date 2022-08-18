import time
from typing import TypeVar, Union

from nerdtracker_client.player_list.listing import EmptyListing, Listing

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
        """Constructor for the Listing class.

        Args:
            initial_snapshot (list[Listing]): The initial snapshot to use to
            initialize the list.
            max_list_length (int, optional): Maximum length the list will
            attempt to keep. Defaults to 12.
            max_list_age (float, optional): Maximum age in seconds before the
            list is considered stale. Defaults to 5 minutes.
        """
        self.list: list[T] = initial_snapshot
        self.last_update = time.time()
        self.max_list_length = max_list_length
        self.max_list_age = max_list_age

    @property
    def __is_list_stale(self) -> bool:
        """Returns whether the list is stale or not"""
        return (time.time() - self.last_update) > self.max_list_age

    @staticmethod
    def from_list_of_strings(
        initial_snapshot: list,
        max_list_length: int = 12,
        max_list_age: float = 5.0 * 60.0,
    ) -> "SnapshotList":
        """Creates a SnapshotList from a list of strings. If the string fed is
        empty or None, an empty Listing is created. Otherwise, the string is
        used to create a new Listing.

        Args:
            initial_snapshot (list): The initial snapshot to use to initialize
            max_list_length (int, optional): Max length the list will attempt to
            keep. Defaults to 12.
            max_list_age (float, optional): Maximum age in seconds before the
            list is considered stale. Defaults to 5 minutes.

        Returns:
            SnapshotList: _description_
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
        """Returns whether the listing is in the list or not"""
        return listing in self.list

    def new_snapshot(self, new_snapshot: list[T]) -> None:
        """Updates the list with a new snapshot.

        Args:
            new_snapshot (list[Listing]): The new snapshot to use to update the
            list.
        """
        # If the list is stale, update it.
        if self.__is_list_stale:
            self.list = new_snapshot
            self.last_update = time.time()
            return None

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
        # 2. Only the first is found. Add the new entries to the end.
        elif first_listing_found and not last_listing_found:
            overlap_indices = self.__new_snapshot_overlap(new_snapshot)
            index_of_first_none = overlap_indices.index(None)
            self.list += new_snapshot[index_of_first_none:]
        return None

    def __new_snapshot_overlap(
        self, new_snapshot: list[T]
    ) -> list[Union[int, None]]:
        """Returns a list of indices of the new snapshot that overlap with the
        current list, or None if there is no overlap.

        Args:
            new_snapshot (list[Listing]): The new snapshot to use to update the
            list.

        Returns:
            list[Union[int, None]]: The indices of the new snapshot that overlap
            with the current list or None if no overlap.
        """
        overlap: list[Union[int, None]] = []
        for index, listing in enumerate(new_snapshot):
            if listing in self.list:
                overlap.append(index)
            else:
                overlap.append(None)
        return overlap

    def __update_existing_listing(self, new_listing: T, index: int) -> None:
        """Updates an existing listing in the list.

        Args:
            new_listing (Listing): The new listing to use to update the list.
            index (int): The index of the listing to update.
        """
        old_listing = self.list[index]
        if isinstance(old_listing, EmptyListing):
            self.list[index] = new_listing
            return None

        if isinstance(new_listing, EmptyListing):
            return None

        if old_listing.full_match:
            return None

        if new_listing.full_match:
            self.list[index] = new_listing
            return None

        # TODO: Add logic to Listing to use all data from the listings.
        self.list[index] = new_listing
        return None
