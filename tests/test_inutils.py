import pytest

from inutils import chunkify


@pytest.mark.parametrize(
    "iterable, expected",
    (
        ([1], [[1]]),
        ([1, 2], [[1, 2]]),
        ([1, 2, 3], [[1, 2], [3]]),
        ([1, 2, 3, 4, 5], [[1, 2], [3, 4], [5]]),
        (range(1, 7), [[1, 2], [3, 4], [5, 6]]),
    ),
)
def test_chunkify_size_2(iterable, expected):
    assert list(chunkify(iterable, chunk_size=2)) == expected


@pytest.mark.parametrize(
    "iterable, expected",
    (
        ([1, 2], [[1, 2]]),
        ([1, 2, 3], [[1, 2, 3]]),
        ([1, 2, 3, 4, 5], [[1, 2, 3], [4, 5]]),
        (range(1, 7), [[1, 2, 3], [4, 5, 6]]),
        ([1, 2, 3, 4, 5, 6, 7], [[1, 2, 3], [4, 5, 6], [7]]),
    ),
)
def test_chunkify_size_3(iterable, expected):
    assert list(chunkify(iterable, chunk_size=3)) == expected
