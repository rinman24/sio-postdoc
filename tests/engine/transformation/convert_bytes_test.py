"""Test byte conversion in instrument access."""

from sio_postdoc.engine.transformation import _convert_bytes

# TODO: MOVE THIS TO THE CORRECT TEST DIRECTORY


def test_successful_conversion():
    assert _convert_bytes(b"\xbd") == 189


def test_float_to_zero():
    assert _convert_bytes(3.14) == 0


def test_nan_to_zero():
    assert _convert_bytes(float("nan")) == 0
