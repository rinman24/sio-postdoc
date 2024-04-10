"""Test the creation of netCDF files."""

import os
from typing import Generator

import pytest
from numpy import allclose

from sio_postdoc.access.instrument.types import Dataset
from tests.helper.builder.raw.context import RawDataContext
from tests.helper.builder.raw.strategies import ShebaMmcrRaw
from tests.helper.builder.raw.types import Instrument, Observatory

BASE_TIME: int = 879984050


@pytest.fixture(scope="module")
def dataset() -> Generator[Dataset, None, None]:
    # Arrange
    data = RawDataContext(Observatory.SHEBA, Instrument.MMCR)
    data.hydrate()
    dataset = Dataset(data.filename)
    # Test
    yield dataset
    # Cleanup
    dataset.close()
    os.remove(data.filename)


def test_attributes(dataset):
    assert (
        dataset.contact
        == "Eugene E. Clothiaux, Gerald. G. Mace, Thomas A. Ackerman, 503 Walker Building, University Park, PA, 16802; Phone: , FAX: , E-mail: cloth,mace,ackerman@essc.psu.edu"
    )
    assert (
        dataset.comment
        == "Divide Reflectivity by 100 to get dBZ, SignaltoNoiseRatio by 100 to get dB and MeanDopplerVelocity and SpectralWidth by 1000 to get m/s!"
    )
    assert (
        dataset.commenta
        == "For each merged range gate reflectivity, velocity and width always come from the same mode."
    )
    assert (
        dataset.commentb
        == "Quality Control Flags: 0 - No Data, 1 - Good Data, 2 - Second Trip Echo Problems, 3 - Coherent Integration Problems, 4 - Second Trip Echo and Coherent Integration Problems"
    )


def test_dimensions(dataset):
    assert dataset.dimensions["time"].size == ShebaMmcrRaw._time
    assert dataset.dimensions["nheights"].size == ShebaMmcrRaw._nheights


def test_base_time(dataset):
    assert str(dataset["base_time"].dtype) == "int32"
    assert dataset["base_time"].long_name == "Beginning Time of File"
    assert dataset["base_time"].units == "seconds since 1970-01-01 00:00:00 00:00"
    assert dataset["base_time"].calendar_date == "Year 1997 Month 11 Day 20 00:00:50"
    assert int(dataset["base_time"][:].data) == BASE_TIME


def test_time_offset(dataset):
    assert str(dataset["time_offset"].dtype) == "float64"
    assert dataset["time_offset"].long_name == "Time Offset from base_time"
    assert dataset["time_offset"].units == "seconds"
    assert dataset["time_offset"].comment == "none"
    assert list(dataset["time_offset"][:].data) == [0.0, 10.0, 20.0, 30.0, 40.0, 50.0]


def test_Heights(dataset):
    assert str(dataset["Heights"].dtype) == "float32"
    assert dataset["Heights"].long_name == "Height of Measured Value; agl"
    assert dataset["Heights"].units == "m"
    assert list(dataset["Heights"][:].data) == [105.0, 150.0, 195.0]


def test_Qc(dataset):
    assert str(dataset["Qc"].dtype) == "|S1"
    assert dataset["Qc"].long_name == "Quality Control Flags"
    assert dataset["Qc"].units == "unitless"
    for row in dataset["Qc"][:].data:
        assert list(row) == [b"\x01", b"\x01", b""]


def test_Reflectivity(dataset):
    assert str(dataset["Reflectivity"].dtype) == "int16"
    assert dataset["Reflectivity"].long_name == "Reflectivity"
    assert dataset["Reflectivity"].units == "dBZ (X100)"
    assert allclose(
        dataset["Reflectivity"][:].data,
        [
            [-4713, -3745, -32768],
            [-4713, -3745, -32768],
            [-4713, -3745, -32768],
            [-4725, -3727, -32768],
            [-4738, -3709, -32768],
            [-4751, -3692, -32768],
        ],
    )


def test_MeanDopplerVelocity(dataset):
    assert str(dataset["MeanDopplerVelocity"].dtype) == "int16"
    assert dataset["MeanDopplerVelocity"].long_name == "Mean Doppler Velocity"
    assert dataset["MeanDopplerVelocity"].units == "m/s (X1000)"
    assert allclose(
        dataset["MeanDopplerVelocity"][:].data,
        [
            [-826, -299, -32768],
            [-826, -299, -32768],
            [-826, -299, -32768],
            [-821, -303, -32768],
            [-816, -308, -32768],
            [-810, -313, -32768],
        ],
    )


def test_SpectralWidth(dataset):
    assert str(dataset["SpectralWidth"].dtype) == "int16"
    assert dataset["SpectralWidth"].long_name == "Spectral Width"
    assert dataset["SpectralWidth"].units == "m/s (X1000)"
    assert allclose(
        dataset["SpectralWidth"][:].data,
        [
            [101, 116, -32768],
            [101, 116, -32768],
            [101, 116, -32768],
            [173, 180, -32768],
            [244, 244, -32768],
            [316, 308, -32768],
        ],
    )


def test_ModeId(dataset):
    assert str(dataset["ModeId"].dtype) == "|S1"
    assert (
        dataset["ModeId"].long_name == "Mode I.D. for Merged Time-Height Moments Data"
    )
    assert dataset["ModeId"].units == "unitless"
    for row in dataset["ModeId"][:].data:
        assert list(row) == [b"\x03", b"\x03", b""]


def test_SignaltoNoiseRatio(dataset):
    assert str(dataset["SignaltoNoiseRatio"].dtype) == "int16"
    assert dataset["SignaltoNoiseRatio"].long_name == "Signal-to-Noise Ratio"
    assert dataset["SignaltoNoiseRatio"].units == "dB (X100)"
    assert allclose(
        dataset["SignaltoNoiseRatio"][:].data,
        [
            [1376, 1219, -32768],
            [1376, 1219, -32768],
            [1376, 1219, -32768],
            [1356, 1212, -32768],
            [1336, 1205, -32768],
            [1314, 1197, -32768],
        ],
    )
