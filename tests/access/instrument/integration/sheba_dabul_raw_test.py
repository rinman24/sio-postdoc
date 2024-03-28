"""Test ShebaDabulRaw implementation of AbstractDataStrategy"""

import os
from datetime import datetime
from pathlib import Path

import pytest

from sio_postdoc.access.instrument.contracts import InstrumentData, PhysicalVector
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
    assert result.axis.values == (0, 30)
    assert result.axis.units == "meters"
    assert result.axis.name == "range"
    assert result.axis.long_name == "vertical range of measurement"
    assert result.axis.scale == 1
    assert result.axis.flag == 2**16 - 1
    assert result.axis.dtype == "u2"


def test_vectors(result):
    expected: list[str] = [
        "altitude",
        "azimuth",
        "elevation",
        "latitude",
        "longitude",
        "scanmode",
    ]
    assert len(result.vectors) == len(expected)
    assert sorted(result.vectors.keys()) == expected


def test_matrices(result):
    expected: list[str] = [
        "depolarization",
        "far_parallel",
    ]
    assert len(result.matrices) == len(expected)
    assert sorted(result.matrices.keys()) == expected


def test_altitude(result):
    vector: PhysicalVector = result.vectors["altitude"]
    assert vector.values == (10, 10, 10)
    assert vector.units == "meters"
    assert vector.name == "altitude"
    assert vector.long_name == "platform altitude"
    assert vector.scale == 1
    assert vector.flag == -999
    assert vector.dtype == "i2"


def test_azimuth(result):
    vector: PhysicalVector = result.vectors["azimuth"]
    assert vector.values == (34001232, 34001235, 34001242)
    assert vector.units == "degrees"
    assert vector.name == "azimuth"
    assert vector.long_name == "beam azimuth angle"
    assert vector.scale == 1e5
    assert vector.flag == 360 * 1e5
    assert vector.dtype == "i4"


def test_elevation(result):
    vector: PhysicalVector = result.vectors["elevation"]
    assert vector.values == (9546252, 9544544, 9544687)
    assert vector.units == "degrees"
    assert vector.name == "elevation"
    assert vector.long_name == "beam elevation angle"
    assert vector.scale == 1e5
    assert vector.flag == 360 * 1e5
    assert vector.dtype == "i4"


def test_latitude(result):
    vector: PhysicalVector = result.vectors["latitude"]
    assert vector.values == (7595036, 7595037, 7595037)
    assert vector.units == "degrees north"
    assert vector.name == "latitude"
    assert vector.long_name == "platform latitude"
    assert vector.scale == 1e5
    assert vector.flag == 360 * 1e5
    assert vector.dtype == "i4"


def test_longitude(result):
    vector: PhysicalVector = result.vectors["longitude"]
    assert vector.values == (-14410420, -14410421, -14410423)
    assert vector.units == "degrees east"
    assert vector.name == "longitude"
    assert vector.long_name == "platform longitude"
    assert vector.scale == 1e5
    assert vector.flag == 360 * 1e5
    assert vector.dtype == "i4"


def test_scanmode(result):
    vector: PhysicalVector = result.vectors["scanmode"]
    assert vector.values == (-999, -999, -999)
    assert vector.units == "unitless"
    assert vector.name == "scanmode"
    assert vector.long_name == "scan mode"
    assert vector.scale == 1
    assert vector.flag == -999
    assert vector.dtype == "i2"


def test_depolarization(result):
    matrix: PhysicalVector = result.matrices["depolarization"]
    assert matrix.values == (
        (-999, 591),
        (-999, 587),
        (-999, 553),
    )
    assert matrix.units == "unitless"
    assert matrix.name == "depolarization"
    assert matrix.long_name == "depolarization ratio"
    assert matrix.scale == 1000
    assert matrix.flag == -999
    assert matrix.dtype == "i2"


def test_far_parallel(result):
    matrix: PhysicalVector = result.matrices["far_parallel"]
    assert matrix.values == (
        (-999, 63688),
        (-999, 64665),
        (-999, 63777),
    )
    assert matrix.units == "unknown"
    assert matrix.name == "far_parallel"
    assert matrix.long_name == "far parallel reflected power"
    assert matrix.scale == 1000
    assert matrix.flag == -999
    assert matrix.dtype == "i4"


def test_notes(result):
    assert result.notes == str(DATA_DIRECTORY) + "/.BHAR"
