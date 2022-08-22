import pytest

from nerdtracker_client.util import (
    identify_chunks,
    identify_chunks_alternating_indices,
    identify_missing_values,
)


def test_identify_chunks() -> None:
    """Tests the identify_chunks function"""

    data = [1, 2, 3, None, 4, 5, 6, None, 7, 8, 9, 10]
    expected_output = [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10]]

    assert identify_chunks(data) == expected_output


def test_identify_chunks_multiple_nones() -> None:
    """Tests the identify_chunks function with multiple Nones"""

    data = [1, 2, 3, None, None, 4, 5, 6, None, None, 7, 8, 9, 10]
    expected_output = [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10]]

    assert identify_chunks(data) == expected_output


def test_identify_chunks_all_nones() -> None:
    """Tests the identify_chunks function with all Nones"""

    data = [None] * 10
    expected_output: list[int] = []

    assert identify_chunks(data) == expected_output


def test_identify_chunks_alternating_indices() -> None:
    """Tests the identify_chunks_alternating_indices function"""

    data = [1, 2, 3, None, 4, 5, 6, None, None, 7, 8, 9, 10]
    expected_output = [3, 4, 7, 9]

    assert identify_chunks_alternating_indices(data) == expected_output


def test_identify_chunks_alternating_indices_all_nones() -> None:
    """Tests the identify_chunks_alternating_indices function with all Nones"""

    data = [None] * 10
    expected_output: list[int] = [0]

    assert identify_chunks_alternating_indices(data) == expected_output


def test_identify_chunks_alternating_indices_no_nones() -> None:
    """Tests the identify_chunks_alternating_indices function with no Nones"""

    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected_output: list[int] = []

    assert identify_chunks_alternating_indices(data) == expected_output


def test_missing_values_with_nones() -> None:
    """Tests the identify_missing_values function if there are Nones but no
    missing values"""

    data = [1, 2, 3, None, 5, 6, None, None, 9, 10]
    expected_output: list[int] = []

    assert identify_missing_values(data) == expected_output


def test_missing_values_with_nones_and_drops() -> None:
    """Tests the identify_missing_values function if there are Nones and missing
    values"""

    data = [1, 2, 3, None, 6, 7, None, 9, 10, None]
    expected_output: list[int] = [5]

    assert identify_missing_values(data) == expected_output
