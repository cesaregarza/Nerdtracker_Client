from typing import TypeVar

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
