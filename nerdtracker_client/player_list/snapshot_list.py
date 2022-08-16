import time
from typing import TypeVar

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
        for i, snapshot_row in enumerate(initial_snapshot):
            if (snapshot_row == "") or (snapshot_row is None):
                listing: Listing | EmptyListing = EmptyListing()
            else:
                listing = Listing(snapshot_row)
            fed_snapshot.append(listing)
        return SnapshotList(fed_snapshot, max_list_length, max_list_age)
