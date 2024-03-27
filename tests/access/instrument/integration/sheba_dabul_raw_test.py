"""Test ShebaDabulRaw implementation of AbstractDataStrategy"""

import os
from datetime import datetime
from pathlib import Path

import pytest

from sio_postdoc.access.instrument.contracts import InstrumentData
from sio_postdoc.access.instrument.strategies.data import ShebaDabulRaw

DATA_DIRECTORY: Path = Path(
    os.getcwd() + "/tests/access/instrument/integration/netCDF4_files/"
)
PATH: str = str(DATA_DIRECTORY / "D1997-11-04T00-31-00.BHAR.ncdf")


# pylint: disable=missing-function-docstring, redefined-outer-name


@pytest.fixture(scope="module")
def result() -> InstrumentData:
    return ShebaDabulRaw().extract(PATH)


def test_time_units(result):
    assert result.time.initial == datetime(1997, 11, 4, 0, 31)
    assert result.time.offsets == (1910, 1920, 1930)
    assert result.time.units == "seconds"
    assert result.time.name == "offsets"
    assert result.time.long_name == "seconds since initial time"
    assert result.time.scale == 1
    assert result.time.flag == -999
    assert result.time.dtype == "i4"


def test_axis(result):
    assert len(result.axis) == 1
    assert result.axis[0].values == (0.0, 30.0)
    assert result.axis[0].units == "meters"
    assert result.axis[0].name == "range"
    assert result.axis[0].long_name == "vertical range of measurement"
    assert result.axis[0].scale == 1
    assert result.axis[0].flag == 2**16 - 1
    assert result.axis[0].dtype == "u2"


def test_vectors(result):
    expected: list[str] = [
        "latitude",
        "longitude",
        "altitude",
        "elevation",
        "azimuth",
        "scanmode",
    ]
    assert len(result.vectors) == len(expected)
    assert [vec.name for vec in result.vectors] == expected


def test_matrices(result):
    expected: list[str] = [
        "depolarization",
        "far_parallel",
    ]
    assert len(result.matrices) == len(expected)
    assert [mat.name for mat in result.matrices] == expected


def test_notes(result):
    assert result.notes == str(DATA_DIRECTORY) + "/.BHAR"
