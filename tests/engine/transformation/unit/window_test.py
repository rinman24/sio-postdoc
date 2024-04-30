"""Test the `GridWindow`."""

import pytest

from sio_postdoc.engine.transformation.window import GridWindow


@pytest.fixture(scope="module", params=[1, 2, 3, 4, 5, 6, 7, 8])
def size(request) -> int:
    """Define parametrized size for testing."""
    return request.param


def test_get_padding(size):
    window: GridWindow = GridWindow()
    expected: tuple[int, int]
    match size:
        case 1:
            expected = (0, 0)
        case 2:
            expected = (0, 1)
        case 3:
            expected = (1, 1)
        case 4:
            expected = (1, 2)
        case 5:
            expected = (2, 2)
        case 6:
            expected = (2, 3)
        case 7:
            expected = (3, 3)
        case 8:
            expected = (3, 4)
    result: int = window._get_padding(size)
    assert result == expected
