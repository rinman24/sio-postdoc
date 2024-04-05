"""Test ShebaMmchRaw implementation of AbstractDataStrategy."""

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
BASE_TIME: int = 883828870
TIME_FLAG: int = -999
ONE_HUNDRED: int = 100
ONE_THOUSAND: int = 1000


@pytest.fixture(scope="module")
def result() -> InstrumentData:  # noqa: D103
    return ShebaMmcrRaw().extract(PATH)


def test_time(result):  # noqa: D103
    assert result.time.base_time == BASE_TIME
    assert result.time.initial == datetime(1998, 1, 3, 12, 1, 10)
    assert result.time.offsets == (0, 10, 20, 30, 40, 50)
    assert result.time.units == "seconds"
    assert result.time.name == "offsets"
    assert result.time.long_name == "Seconds Since Initial Time"
    assert result.time.scale == 1
    assert result.time.flag == TIME_FLAG
    assert result.time.dtype == "i4"


def test_axis(result):  # noqa: D103
    assert result.axis.values == (105, 150, 195)
    assert result.axis.units == "meters"
    assert result.axis.name == "range"
    assert result.axis.long_name == "Height of Measured Value; agl"
    assert result.axis.scale == 1
    assert result.axis.flag == int(2**16 - 1)
    assert result.axis.dtype == "u2"


def test_vectors(result):  # noqa: D103
    expected: list[str] = []
    assert len(result.vectors) == len(expected)
    assert sorted(result.vectors.keys()) == expected


def test_matrices(result):  # noqa: D103
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


def test_mean_doppler_velocity(result):  # noqa: D103
    matrix: PhysicalMatrix = result.matrices["mean_doppler_velocity"]
    assert matrix.values == (
        (-865, -296, 273),
        (-865, -296, 273),
        (-864, -288, 288),
        (-863, -275, 312),
        (-861, -262, 337),
        (-860, -251, 358),
    )
    assert matrix.units == "m/s"
    assert matrix.name == "mean_doppler_velocity"
    assert matrix.long_name == "Mean Doppler Velocity"
    assert matrix.scale == ONE_THOUSAND
    assert matrix.flag == -int(2**16 / 2)
    assert matrix.dtype == "i2"


def test_mode_id(result):  # noqa: D103
    matrix: PhysicalMatrix = result.matrices["mode_id"]
    assert matrix.values == (
        (3, 3, 3),
        (3, 3, 3),
        (3, 3, 3),
        (3, 3, 3),
        (3, 3, 3),
        (3, 3, 3),
    )
    assert matrix.units == "unitless"
    assert matrix.name == "mode_id"
    assert matrix.long_name == "Mode I.D. for Merged Time-Height Moments Data"
    assert matrix.scale == 1
    assert matrix.flag == 0
    assert matrix.dtype == "S1"


def test_qc(result):  # noqa: D103
    matrix: PhysicalMatrix = result.matrices["qc"]
    assert matrix.values == (
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
        (1, 1, 1),
    )
    assert matrix.units == "unitless"
    assert matrix.name == "qc"
    assert matrix.long_name == "Quality Control Flags"
    assert matrix.scale == 1
    assert matrix.flag == 0
    assert matrix.dtype == "S1"


def test_reflectivity(result):  # noqa: D103
    matrix: PhysicalMatrix = result.matrices["reflectivity"]
    assert matrix.values == (
        (-6408, -2450, -2149),
        (-6408, -2450, -2149),
        (-6422, -2446, -2145),
        (-6448, -2439, -2138),
        (-6475, -2432, -2131),
        (-6498, -2427, -2126),
    )
    assert matrix.units == "dBZ"
    assert matrix.name == "reflectivity"
    assert matrix.long_name == "Reflectivity"
    assert matrix.scale == ONE_HUNDRED
    assert matrix.flag == -int(2**16 / 2)
    assert matrix.dtype == "i2"


def test_signal_to_noise(result):  # noqa: D103
    matrix: PhysicalMatrix = result.matrices["signal_to_noise"]
    assert matrix.values == (
        (475, 2745, 3045),
        (475, 2745, 3045),
        (462, 2749, 3049),
        (439, 2757, 3057),
        (415, 2764, 3064),
        (394, 2769, 3069),
    )
    assert matrix.units == "dB"
    assert matrix.name == "signal_to_noise"
    assert matrix.long_name == "Signal-to-Noise Ratio"
    assert matrix.scale == ONE_HUNDRED
    assert matrix.flag == -int(2**16 / 2)
    assert matrix.dtype == "i2"


def test_spectral_width(result):  # noqa: D103
    matrix: PhysicalMatrix = result.matrices["spectral_width"]
    assert matrix.values == (
        (104, 165, 225),
        (104, 165, 225),
        (104, 167, 230),
        (105, 171, 237),
        (106, 175, 245),
        (106, 179, 251),
    )
    assert matrix.units == "m/s"
    assert matrix.name == "spectral_width"
    assert matrix.long_name == "Spectral Width"
    assert matrix.scale == ONE_THOUSAND
    assert matrix.flag == -int(2**16 / 2)
    assert matrix.dtype == "i2"


def test_notes(result):  # noqa: D103
    assert result.notes == str(DATA_DIRECTORY) + "/.mrg.corrected"
