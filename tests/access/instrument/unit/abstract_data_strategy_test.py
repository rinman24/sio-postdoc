"""Test methods used for InstrumentDataStrategy."""

import pytest

import sio_postdoc.access.instrument.strategies.data as service

# pylint: disable=missing-function-docstring, redefined-outer-name, protected-access


@pytest.fixture(params=["hours", "seconds"])
def units(request) -> str:
    return request.param


@pytest.fixture(params=["prefix-only", "suffix-only", "both", "neither"])
def notes(request) -> str:
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
    result: tuple[float, ...] = service._monotonic_times(
        times=times,
        units=units,
    )
    # Assert
    assert result == expected


def test_get_notes(notes):
    # Arrange
    name: str
    expected: str
    prefix: str = "prefix.test1.test2"
    date: str = "D2024-03-20T09-24-00"
    suffix: str = "test.suffix"
    extension: str = "ncdf"
    match notes:
        case "prefix-only":
            name = f"{prefix}.{date}.{extension}"
            expected = prefix
        case "suffix-only":
            name = f"{date}.{suffix}.{extension}"
            expected = suffix
        case "both":
            name = f"{prefix}.{date}.{suffix}.{extension}"
            expected = f"{prefix}.{suffix}"
        case "neither":
            name = f"{date}.{extension}"
            expected = ""
    # Act
    notes: str = service._get_notes(name)
    # Assert
    assert notes == expected
