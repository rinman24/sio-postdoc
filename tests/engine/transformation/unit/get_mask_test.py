"""Test the get_mask method from the transformation engine."""

import pytest

from sio_postdoc.engine.transformation.contracts import DType, MaskRequest
from sio_postdoc.engine.transformation.service import TransformationEngine


@pytest.fixture(scope="module")
def engine() -> TransformationEngine:
    return TransformationEngine()


def test_get_mask_large(engine):
    request: MaskRequest = MaskRequest(
        values=(
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
        ),
        length=3,
        height=2,
        threshold=1,
        scale=1,
        dtype=DType.U1,
    )
    assert engine.get_mask(request) == (
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


def test_get_mask_small(engine):
    request = MaskRequest(
        values=(
            (0, 0, 0, 0),
            (0, 1, 1, 0),
            (0, 1, 1, 0),
            (0, 1, 1, 0),
            (0, 0, 0, 0),
        ),
        length=3,
        height=2,
        threshold=1,
        scale=1,
        dtype=DType.U1,
    )
    assert engine.get_mask(request) == (
        (False, False, False, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, True, True, False),
        (False, False, False, False),
    )
