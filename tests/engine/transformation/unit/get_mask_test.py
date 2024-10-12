"""Test the get_mask method from the transformation engine."""

import pytest

from sio_postdoc.engine.transformation.contracts import (
    Direction,
    DType,
    MaskRequest,
    Threshold,
)
from sio_postdoc.engine.transformation.service import TransformationEngine


@pytest.fixture(scope="module")
def threshold() -> Threshold:
    return Threshold(
        value=1,
        direction=Direction.LESS_THAN,
    )


@pytest.fixture(scope="module")
def engine() -> TransformationEngine:
    return TransformationEngine()


def test_get_mask_large(engine, threshold):
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
        threshold=threshold,
        scale=1,
        dtype=DType.U1,
    )
    assert engine.get_mask(request) == (
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 1, 1, 0, 0, 0, 0, 0, 0),
        (0, 0, 1, 1, 0, 0, 0, 0, 1, 1),
        (0, 0, 1, 1, 0, 0, 0, 0, 1, 1),
        (0, 0, 1, 1, 0, 0, 0, 0, 1, 1),
        (0, 0, 0, 0, 0, 0, 1, 1, 0, 0),
        (0, 0, 0, 0, 0, 0, 1, 1, 1, 0),
        (1, 1, 0, 0, 0, 0, 1, 1, 1, 0),
        (1, 1, 0, 0, 0, 0, 0, 1, 1, 0),
        (1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    )


def test_get_mask_small(engine, threshold):
    request: MaskRequest = MaskRequest(
        values=(
            (0, 0, 0, 0),
            (0, 1, 1, 0),
            (0, 1, 1, 0),
            (0, 1, 1, 0),
            (0, 0, 0, 0),
        ),
        length=3,
        height=2,
        threshold=threshold,
        scale=1,
        dtype=DType.U1,
    )
    assert engine.get_mask(request) == (
        (0, 0, 0, 0),
        (0, 1, 1, 0),
        (0, 1, 1, 0),
        (0, 1, 1, 0),
        (0, 0, 0, 0),
    )
