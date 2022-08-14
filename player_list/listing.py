import time
from typing import Union
from fuzzywuzzy import fuzz

# Constants
SIMILARITY_THRESHOLD = 80


class Listing:
    """Listing class is a class that represents a single listing on the SnapshotList class"""

    def __init__(self, listing_id: Union[str, int], full_match: bool = False) -> None:
        """Constructor for the Listing class

        Arguments:
            listing_id (Union[str, int]): The identifier for the listing
            full_match (bool): Whether the listing id is a full match or not
        """

        self.listing_id = listing_id
        self.full_match = full_match
        self.listing_time = time.time()

    def __repr__(self) -> str:
        """Returns a string representation of the listing object. Purposefully different from __str__

        Returns:
            str: The string representation of the listing
        """

        return f"Listing({self.listing_id}, Threshold: {SIMILARITY_THRESHOLD}, Time: {self.time_since_listing()})"

    def __str__(self) -> str:
        """When stringified, returns the listing id. Purposefully different from __repr__

        Returns:
            str: The string representation of the listing
        """

        return str(self.listing_id)

    def __eq__(self, other: "Listing") -> bool:
        """Returns whether the two listings are equal through fuzzywuzzy

        Arguments:
            other (Listing): The other listing to compare to

        Returns:
            bool: Whether the two listings are equal...ish
        """
        self_id = str(self.listing_id)
        other_id = str(other.listing_id)
        return fuzz.ratio(self_id, other_id) > SIMILARITY_THRESHOLD

    def time_since_listing(self) -> str:
        """Returns the time since the listing was created

        Returns:
            str: The time since the listing was created
        """

        seconds = time.time() - self.listing_id
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes):02d}m:{int(seconds):02d}s"

    def update_time(self, new_time: float) -> None:
        """Updates the listing time to the current time"""

        self.listing_time = time.time() if new_time is None else new_time
        return None

    def update_id_full_match(self, new_id: Union[str, int]) -> None:
        """Updates the listing id if a full match has been found

        Args:
            new_id (Union[str, int]): The new listing id to update to
        """

        self.listing_id = new_id
        self.full_match = True
        return None


class SnapshotList:
    """SnapshotList class is a class that tries to keep a real-time list based on the snapshot fed to it. More formally,
    it keeps a list of length n based on a snapshot fed to it of length k. It will then attempt to update the list based
    on the snapshot and assumptions fed to it.
    """

    def __init__(
        self,
        initial_snapshot: list,
        max_list_length: int = 12,
        max_list_age: float = 5.0 * 60.0,
    ) -> None:
        """Constructor for the Listing class.

        Args:
            initial_snapshot (list): The initial snapshot to use to initialize the list.
            max_list_length (int, optional): Maximum length the list will attempt to keep. Defaults to 12.
            max_list_age (float, optional): Maximum age before the list is considered stale. Defaults to 5 minutes.
        """
        self.list = initial_snapshot
        self.last_update = time.time()
        self.max_list_length = max_list_length
        self.max_list_age = max_list_age
