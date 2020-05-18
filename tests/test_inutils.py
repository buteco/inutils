from inutils import chunkify


def test_chunkify():
    assert list(chunkify([1], chunk_size=2)) == [[1]]
    assert list(chunkify([1, 2], chunk_size=2)) == [[1, 2]]
    assert list(chunkify([1, 2, 3], chunk_size=2)) == [[1, 2], [3]]
    assert list(chunkify([1, 2, 3, 4, 5], chunk_size=2)) == [[1, 2], [3, 4], [5]]

    assert list(chunkify([1, 2, 3], chunk_size=3)) == [[1, 2, 3]]
    assert list(chunkify([1, 2, 3, 4, 5], chunk_size=3)) == [[1, 2, 3], [4, 5]]
    assert list(chunkify([1, 2, 3, 4, 5, 6, 7], chunk_size=3)) == [[1, 2, 3], [4, 5, 6], [7]]
