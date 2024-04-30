"""Test the get_mask method from the transformation engine."""

from sio_postdoc.engine.transformation.service import TransformationEngine
from sio_postdoc.engine.transformation.window import GridWindow

THRESHOLD: int = 1
Mask = tuple[tuple[bool, ...]]


def test_get_mask():
    engine: TransformationEngine = TransformationEngine()
    window: GridWindow = GridWindow(length=3, height=2)
    values: tuple[tuple[int, ...]] = (
        (1, 0, 0, 0, 0, 0, 1, 0, 0, 0),
        (0, 0, 1, 1, 0, 1, 0, 1, 0, 0),
        (0, 0, 1, 1, 0, 1, 1, 0, 1, 1),
        (0, 0, 1, 1, 0, 1, 0, 1, 1, 1),
        (0, 0, 1, 1, 0, 0, 1, 0, 1, 1),
        (0, 0, 1, 0, 0, 0, 1, 1, 0, 0),
        (0, 1, 1, 1, 0, 0, 1, 1, 1, 0),
        (1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
        (1, 1, 0, 1, 0, 1, 0, 1, 1, 0),
        (1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    )
    mask: Mask = engine.get_mask(values, window, THRESHOLD)
    assert mask == (
        (False, False, False, False, False, False, False, False, False, False),
        (False, False, True, True, False, False, False, False, False, False),
        (False, False, True, True, False, False, False, False, True, True),
        (False, False, True, True, False, False, False, False, True, True),
        (False, False, True, True, False, False, False, False, True, True),
        (False, False, False, False, False, False, True, True, False, False),
        (False, False, False, False, False, False, True, True, True, False),
        (True, True, False, False, False, False, True, True, True, False),
        (True, True, False, False, False, False, False, True, True, False),
        (True, True, False, False, False, False, False, False, False, False),
    )


def test_get_mask2():
    engine: TransformationEngine = TransformationEngine()
    window: GridWindow = GridWindow(length=3, height=2)
    values = (
        (0, 0, 0, 0),
        (0, 1, 1, 0),
        (0, 1, 1, 0),
        (0, 1, 1, 0),
        (0, 0, 0, 0),
    )
    mask: Mask = engine.get_mask(values, window, THRESHOLD)
    assert mask == (
        (False, False, False, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, False, False, False),
    )
