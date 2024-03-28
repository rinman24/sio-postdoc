"""Test byte conversion in instrument access."""

from sio_postdoc.access.instrument.strategies.constants import _convert_bytes


def test_successful_conversion():  # noqa: D103
    assert _convert_bytes(b"\xbd") == 189  # noqa: PLR2004


def test_float_to_zero():  # noqa : D103
    assert _convert_bytes(3.14) == 0


def test_nan_to_zero():  # noqa: D103
    assert _convert_bytes(float("nan")) == 0
