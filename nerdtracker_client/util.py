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
    None. The indices of the items in the chunk are alternating.

    Args:
        data (list[T]): The list of items to identify chunks in.

    Returns:
        list[int]: The list of alternating indices of the chunks in the list.
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
