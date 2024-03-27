"""Test methods in AbstractDataStrategy."""

import pytest

from sio_postdoc.access.instrument.strategies.data import AbstractDataStrategy

# pylint: disable=missing-function-docstring, redefined-outer-name


@pytest.fixture(params=["hours", "seconds"])
def units(request) -> str:
    return request.param


def test_monotonic_times(units):
    # Arrange
    times: list[float]
    expected: tuple[float, ...]
    match units:
        case "hours":
            times = [23, 23.5, 0, 0.5]
            expected = (82800, 84600, 86400, 88200)
        case "seconds":
            times = [86380, 86390, 0, 10, 20]
            expected = (86380, 86390, 86400, 86410, 86420)
    # Act
    result: tuple[float, ...] = AbstractDataStrategy.monotonic_times(
        times=times,
        units=units,
    )
    # Assert
    assert result == expected
