import time
from typing import Optional

from fuzzywuzzy import fuzz

import nerdtracker_client.constants.stats as ntc_stats

# Constants
SIMILARITY_THRESHOLD = 80


class Listing:
    """Listing class is a class that represents a single listing on the
    SnapshotList class"""

    def __init__(
        self,
        listing_id: str | int,
        full_match: bool = False,
        stats: Optional[ntc_stats.StatColumns] = None,
    ) -> None:
        """Constructor for the Listing class

        Arguments:
            listing_id (str | int): The identifier for the listing
            full_match (bool): Whether the listing id is a full match or not
            stats (Optional[ntc_stats.StatColumns]): The stats for the listing.
        """

        self.listing_id: str | int | None = listing_id
        self.full_match = full_match
        self.stats = stats
        self.listing_time = time.time()

    def __repr__(self) -> str:
        """Returns a string representation of the listing object. Purposefully
        different from __str__

        Returns:
            str: The string representation of the listing
        """

        if self.has_stats:
            kdr_string = self.stats[ntc_stats.KD_RATIO]  # type: ignore
        else:
            kdr_string = "N/A"

        out = (
            "Listing("
            + f"{self.listing_id}, "
            + f"KDR: {kdr_string}, "
            + f"Threshold: {SIMILARITY_THRESHOLD}, "
            + f"Time: {self.time_since_listing()}"
            + ")"
        )
        return out

    def __str__(self) -> str:
        """When stringified, returns the listing id. Purposefully different from
        __repr__

        Returns:
            str: The string representation of the listing
        """

        return str(self.listing_id)

    def __eq__(self, other: object) -> bool:
        """Returns whether the two listings are equal through fuzzywuzzy

        Arguments:
            other (object): The other listing to compare to

        Returns:
            bool: Whether the two listings are equal...ish
        """
        if not isinstance(other, Listing):
            return False
        self_id = str(self.listing_id)
        other_id = str(other.listing_id)
        return fuzz.ratio(self_id, other_id) > SIMILARITY_THRESHOLD

    def time_since_listing(self) -> str:
        """Returns the time since the listing was created

        Returns:
            str: The time since the listing was created
        """

        seconds = time.time() - self.listing_time
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes):02d}m:{int(seconds):02d}s"

    def update(self, other: "Listing") -> None:
        """Updates the listing with another listing

        Given another listing, transforms the current listing into the other
        listing. If the current listing is a full match, then this function
        does nothing.

        Args:
            other (Listing): The other listing
        """
        if self.full_match:
            return

        self.listing_id = other.listing_id
        self.stats = other.stats
        self.full_match = other.full_match
        self.listing_time = other.listing_time

    def update_time(self, new_time: float | None) -> None:
        """Updates the listing time.

        Updates the listing time to the new time if the new time is provided.

        Args:
            new_time (float | None): The new time to update to, or None to use
                the current time
        """

        self.listing_time = time.time() if new_time is None else new_time

    def update_id_full_match(self, new_id: str | int) -> None:
        """Updates the listing id if a full match has been found

        Args:
            new_id (str | int): The new listing id to update to
        """
        # If full match is already true, don't update
        if self.full_match:
            return

        self.listing_id = new_id
        self.full_match = True

    def copy(self) -> "Listing":
        """Returns a copy of the listing

        Returns:
            Listing: A copy of the listing
        """
        if self.listing_id is None:
            return EmptyListing()
        new_listing = Listing(self.listing_id, self.full_match)
        new_listing.listing_time = self.listing_time
        return new_listing

    @property
    def is_empty(self) -> bool:
        """Whether the listing is empty or not

        Returns:
            bool: Whether the listing is empty or not
        """

        return self.listing_id is None

    @property
    def has_stats(self) -> bool:
        """Whether the listing has stats or not

        Returns:
            bool: Whether the listing has stats or not
        """

        return self.stats is not None


class EmptyListing(Listing):
    """EmptyListing class is necessary in case the OCR unit fails and there is
    no listing"""

    def __init__(self) -> None:
        """Constructor for the EmptyListing class"""

        self.listing_id = None
        self.stats = None
        self.full_match = False
        self.listing_time = 0.0

    def __repr__(self) -> str:
        """Returns a string representation of the listing object. Purposefully
        different from __str__

        Returns:
            str: The string representation of the listing
        """

        return "EmptyListing()"

    def __str__(self) -> str:
        """When stringified, returns the listing id. Purposefully different from
        __repr__

        Returns:
            str: The string representation of the listing
        """

        return ""

    def __eq__(self, other: object) -> bool:
        """Returns whether the two listings are equal.

        Since this is an EmptyListing, it will always return True if the other
        object is also an EmptyListing, and False otherwise.

        Arguments:
            other (object): The other listing to compare to

        Returns:
            bool: Whether the two listings are equal...ish
        """
        return isinstance(other, EmptyListing)

    def time_since_listing(self) -> str:
        """Returns the time since the listing was created

        Returns:
            str: The time since the listing was created
        """

        return ""

    def update_time(self, new_time: float | None) -> None:
        """Updates the listing time.

        Updates the listing time to the new time if the new time is provided.

        Args:
            new_time (float | None): For EmptyListing, this does nothing. This
                is just here to override the parent class method.
        """
        pass

    def update_id_full_match(self, new_id: str | int) -> None:
        """Updates the listing id if a full match has been found

        Args:
            new_id (str | int): For EmptyListing, this does nothing. This is
                just here to override the parent class method.
        """
        pass
