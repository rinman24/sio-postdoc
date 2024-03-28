"""Test ShebaMmchRaw implementation of AbstractDataStrategy"""

import os
from datetime import datetime
from pathlib import Path

import pytest

from sio_postdoc.access.instrument.contracts import InstrumentData, PhysicalMatrix
from sio_postdoc.access.instrument.strategies.data import ShebaMmcrRaw

DATA_DIRECTORY: Path = Path(
    os.getcwd() + "/tests/access/instrument/integration/netCDF4_files/"
)
PATH: str = str(DATA_DIRECTORY / "D1997-10-30T12-00-00.mrg.corrected.nc")


# pylint: disable=missing-function-docstring, redefined-outer-name


@pytest.fixture(scope="module")
def result() -> InstrumentData:
    return ShebaMmcrRaw().extract(PATH)


def test_time(result):
    assert result.time.initial == datetime(1997, 10, 30, 12, 1, 10)
    assert result.time.offsets == (0, 10, 20)
    assert result.time.units == "seconds"
    assert result.time.name == "offsets"
    assert result.time.long_name == "seconds since initial time"
    assert result.time.scale == 1
    assert result.time.flag == -999
    assert result.time.dtype == "i4"


def test_axis(result):
    assert result.axis.values == (105, 150)
    assert result.axis.units == "meters"
    assert result.axis.name == "range"
    assert result.axis.long_name == "Height of Measured Value; agl"
    assert result.axis.scale == 1
    assert result.axis.flag == 2**16 - 1
    assert result.axis.dtype == "u2"


def test_vectors(result):
    expected: list[str] = []
    assert len(result.vectors) == len(expected)
    assert sorted(result.vectors.keys()) == expected


def test_matrices(result):
    expected: list[str] = [
        "mean_doppler_velocity",
        "mode_id",
        "qc",
        "reflectivity",
        "signal_to_noise",
        "spectral_width",
    ]
    assert len(result.matrices) == len(expected)
    assert sorted(result.matrices.keys()) == expected


def test_mean_doppler_velocity(result):
    matrix: PhysicalMatrix = result.matrices["mean_doppler_velocity"]
    assert matrix.values == (
        (590, 586),
        (590, 586),
        (504, 527),
    )
    assert matrix.units == "m/s"
    assert matrix.name == "mean_doppler_velocity"
    assert matrix.long_name == "Mean Doppler Velocity"
    assert matrix.scale == 1000
    assert matrix.flag == -int(2**16 / 2)
    assert matrix.dtype == "i2"


def test_mode_id(result):
    matrix: PhysicalMatrix = result.matrices["mode_id"]
    assert matrix.values == (
        (3, 3),
        (3, 3),
        (3, 3),
    )
    assert matrix.units == "unitless"
    assert matrix.name == "mode_id"
    assert matrix.long_name == "Mode I.D. for Merged Time-Height Moments Data"
    assert matrix.scale == 1
    assert matrix.flag == 0
    assert matrix.dtype == "S1"


def test_qc(result):
    matrix: PhysicalMatrix = result.matrices["qc"]
    assert matrix.values == (
        (1, 1),
        (1, 1),
        (1, 1),
    )
    assert matrix.units == "unitless"
    assert matrix.name == "qc"
    assert matrix.long_name == "Quality Control Flags"
    assert matrix.scale == 1
    assert matrix.flag == 0
    assert matrix.dtype == "S1"


@pytest.mark.skip(reason="Not Implemented")
def test_reflectivity(result):
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_signal_to_noise(result):
    pass


@pytest.mark.skip(reason="Not Implemented")
def test_spectral_width(result):
    pass
