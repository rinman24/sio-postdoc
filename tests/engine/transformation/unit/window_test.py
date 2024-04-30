"""Test the `GridWindow`."""

import pytest

from sio_postdoc.engine.transformation.window import GridWindow


@pytest.fixture(scope="module", params=[1, 2, 3, 4, 5, 6, 7, 8])
def size(request) -> int:
    """Define parametrized size for testing."""
    return request.param


def test_get_padding(size):
    window: GridWindow = GridWindow(length=size, height=size)
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


def test_horizontal_window(size):
    window: GridWindow = GridWindow(length=size, height=1)
    position: tuple[int, int]
    padding: dict[str, int] = {}
    match size:
        case 1:
            position = (0, 0)
            padding["left"] = 0
            padding["right"] = 0
        case 2:
            position = (0, 0)
            padding["left"] = 0
            padding["right"] = 1
        case 3:
            position = (1, 0)
            padding["left"] = 1
            padding["right"] = 1
        case 4:
            position = (1, 0)
            padding["left"] = 1
            padding["right"] = 2
        case 5:
            position = (2, 0)
            padding["left"] = 2
            padding["right"] = 2
        case 6:
            position = (2, 0)
            padding["left"] = 2
            padding["right"] = 3
        case 7:
            position = (3, 0)
            padding["left"] = 3
            padding["right"] = 3
        case 8:
            position = (3, 0)
            padding["left"] = 3
            padding["right"] = 4
    assert window.position == position
    assert window.padding["left"] == padding["left"]
    assert window.padding["right"] == padding["right"]
    assert window.padding["bottom"] == 0
    assert window.padding["top"] == 0


def test_vertical_window(size):
    window: GridWindow = GridWindow(length=1, height=size)
    position: tuple[int, int]
    padding: dict[str, int] = {}
    match size:
        case 1:
            position = (0, 0)
            padding["bottom"] = 0
            padding["top"] = 0
        case 2:
            position = (0, 0)
            padding["bottom"] = 0
            padding["top"] = 1
        case 3:
            position = (0, 1)
            padding["bottom"] = 1
            padding["top"] = 1
        case 4:
            position = (0, 1)
            padding["bottom"] = 1
            padding["top"] = 2
        case 5:
            position = (0, 2)
            padding["bottom"] = 2
            padding["top"] = 2
        case 6:
            position = (0, 2)
            padding["bottom"] = 2
            padding["top"] = 3
        case 7:
            position = (0, 3)
            padding["bottom"] = 3
            padding["top"] = 3
        case 8:
            position = (0, 3)
            padding["bottom"] = 3
            padding["top"] = 4
    assert window.position == position
    assert window.padding["left"] == 0
    assert window.padding["right"] == 0
    assert window.padding["bottom"] == padding["bottom"]
    assert window.padding["top"] == padding["top"]
