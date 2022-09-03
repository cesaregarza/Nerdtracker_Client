from typing import TypeVar, cast

T = TypeVar("T")


def identify_chunks(data: list[T]) -> list[list[T]]:
    """Identifies chunks of consecutive items in a list of items separated by
    None.

    Args:
        data (list[T]): The list of items to identify chunks in.

    Returns:
        list[list[T]]: The list of chunks in the list, without Nones.
    """
    out: list[list[T]] = []
    chunk: list[T] = []
    for item in data:
        if item is None:
            if len(chunk) > 0:
                out.append(chunk)
                chunk = []
        else:
            chunk.append(item)
    if len(chunk) > 0:
        out.append(chunk)
    return out


def identify_chunks_alternating_indices(data: list[T]) -> list[int]:
    """Identifies chunks of consecutive items in a list of items separated by
    None. The indices of the items in the chunk are alternating between data and
    None. For example,
    >>> data = [1, 2, 3, None, 4, 5, 6, None, None, 7, 8, 9, 10]

    can expect a return value of
    >>> [3, 4, 7, 9]

    because the index of the first
    None is 3, the index of the next item is 4, the index of the next None is 7,
    and the index of the next item is 9. A list with no Nones will return an
    empty list. A list with all Nones will return [0].

    Args:
        data (list[T]): The list of items to identify chunks in.

    Returns:
        list[int]: The list of alternating indices of the items in the chunks.
    """
    out: list[int] = []
    none_chunk: bool = False
    for index, item in enumerate(data):
        if item is None and not none_chunk:
            out.append(index)
            none_chunk = True
        elif item is not None and none_chunk:
            out.append(index)
            none_chunk = False
    return out


def identify_missing_values(data: list[int | None]) -> list[int]:
    """Identifies and returns the missing values in the list.

    Given a monotonically increasing list, where None is used as a placeholder,
    identify and return the missing values in the list. For example:
    >>> data = [1, 2, 3, None, 5, 7]

    will have None as a placeholder for 4, while 6 will be returned.
    >>> identify_missing_values(data)
    [6]

    Args:
        data (list[int  |  None]): The list of integers to identify missing
            values in. None is used as a placeholder, assumes the first value is
            not None.

    Raises:
        TypeError: If the first value in the list is None.

    Returns:
        list[int]: The list of missing values.
    """
    if not isinstance(data[0], int):
        raise TypeError("First value in data must be an integer.")

    out: list[int] = []
    smallest_value: int = cast(int, data[0])
    # Find the largest value that is not None. Must be done this way since there
    # probably are missing values, so the largest value is not necessarily the
    # smallest value plus the length of the list.
    largest_value: int = 0
    ending_nones: int = 0
    for value in data[::-1]:
        if value is not None:
            largest_value = value + ending_nones
            break
        else:
            ending_nones += 1

    # Impute the None values assuming it's one more than the previous value
    new_data: list[int] = []
    previous_value: int = smallest_value
    for value in data:
        if value is None:
            new_value: int = previous_value + 1
            new_data.append(new_value)
            previous_value = new_value
        else:
            new_data.append(value)
            previous_value = value

    # Find the missing values
    for value in range(smallest_value, largest_value + 1):
        if value not in new_data:
            out.append(value)
    return out
