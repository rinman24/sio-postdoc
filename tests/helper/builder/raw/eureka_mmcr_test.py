"""Test the creation of netCDF files."""

import os
from typing import Generator

import pytest
from numpy import allclose

from sio_postdoc.access.instrument.types import Dataset
from tests.helper.builder.raw.context import RawDataContext
from tests.helper.builder.raw.strategies import EurekaMmcrRaw
from tests.helper.builder.raw.types import Instrument, Observatory

BASE_TIME: float = 1221955209.0


@pytest.fixture(scope="module")
def dataset() -> Generator[Dataset, None, None]:
    # Arrange
    data = RawDataContext(Observatory.EUREKA, Instrument.MMCR)
    data.hydrate()
    dataset = Dataset(data.filename)
    # Test
    yield dataset
    # Cleanup
    dataset.close()
    os.remove(data.filename)


def test_attributes(dataset):
    assert dataset.Source == "20080921.000000"
    assert dataset.Version == "***1.0***"
    assert dataset.Input_Platforms == ""
    assert dataset.Contact == "***ETL***"
    assert (
        dataset.commenta
        == "At each height and time, the MMCR reflectivity, velocity, spectral width and signal-to-noise ratio always come from the same mode. The mode in indicated by ModeId."
    )
    assert (
        dataset.commentb
        == "Missing (i.e., does not exist) data for a particular time period are indicated by a value of 10 for the ModeId. The geophysical variables should contain a value of -32768 at these times."
    )
    assert (
        dataset.commentc
        == "Nore that -32768 is also used for the geophysical variables when there are no significant detections, in which case ModeId is 0."
    )


def test_dimensions(dataset):
    assert dataset.dimensions["time"].size == EurekaMmcrRaw.time
    assert dataset.dimensions["nheights"].size == EurekaMmcrRaw.nheights
    assert dataset.dimensions["numlayers"].size == EurekaMmcrRaw.numlayers


def test_base_time(dataset):
    assert str(dataset["base_time"].dtype) == "float64"
    assert dataset["base_time"].long_name == "Beginning Time of File"
    assert dataset["base_time"].units == "seconds since 1970-01-01 00:00 UTC"
    assert dataset["base_time"].calendar_date == "20080921_00:00:09"
    assert int(dataset["base_time"][:].data) == BASE_TIME


def test_time_offset(dataset):
    assert str(dataset["time_offset"].dtype) == "float64"
    assert dataset["time_offset"].long_name == "Time Offset from base_time"
    assert dataset["time_offset"].units == "seconds"
    assert dataset["time_offset"].comment == "none"
    assert allclose(dataset["time_offset"][:].data, [0.0, 10.0, 20.0, 30.0, 40.0, 50.0])


def test_heights(dataset):
    assert str(dataset["heights"].dtype) == "float32"
    assert dataset["heights"].long_name == "Height of Measured Value"
    assert dataset["heights"].units == "m AGL"
    assert dataset["heights"].comment == "none"
    assert allclose(dataset["heights"][:].data, [54.0, 97.0, 140.0])


def test_Reflectivity(dataset):
    assert str(dataset["Reflectivity"].dtype) == "int16"
    assert dataset["Reflectivity"].long_name == "MMCR Reflectivity"
    assert dataset["Reflectivity"].units == "dBZ(x100)"
    assert dataset["Reflectivity"].comment == "Divide Reflectivity by 100 to get dBZ"
    assert allclose(
        dataset["Reflectivity"][:].data,
        [
            [-32768, -32768, -32768],
            [-3438, -3730, -5072],
            [-4511, -4802, -6151],
            [-4540, -4831, -6183],
            [-4303, -4595, -5946],
            [-4400, -4688, -5924],
        ],
    )


def test_MeanDopplerVelocity(dataset):
    assert str(dataset["MeanDopplerVelocity"].dtype) == "int16"
    assert dataset["MeanDopplerVelocity"].long_name == "MMCR MeanDopplerVelocity"
    assert dataset["MeanDopplerVelocity"].units == "m/s(x1000)"
    assert (
        dataset["MeanDopplerVelocity"].comment
        == "Divide MeanDopplerVelocity by 1000 to get m/s"
    )
    assert allclose(
        dataset["MeanDopplerVelocity"][:].data,
        [
            [-32768, -32768, -32768],
            [77, 69, 61],
            [-4057, -1847, 363],
            [-4111, -2629, -1148],
            [-4460, -1692, 1076],
            [-4284, -1676, 931],
        ],
    )


def test_SpectralWidth(dataset):
    assert str(dataset["SpectralWidth"].dtype) == "int16"
    assert dataset["SpectralWidth"].long_name == "MMCR SpectralWidth"
    assert dataset["SpectralWidth"].units == "m/s(x1000)"
    assert dataset["SpectralWidth"].comment == "Divide SpectralWidth by 1000 to get m/s"
    assert allclose(
        dataset["SpectralWidth"][:].data,
        [
            [-32768, -32768, -32768],
            [470, 300, 130],
            [593, 353, 113],
            [513, 296, 80],
            [1013, 552, 91],
            [727, 466, 205],
        ],
    )


def test_SignalToNoiseRatio(dataset):
    assert str(dataset["SignalToNoiseRatio"].dtype) == "int16"
    assert dataset["SignalToNoiseRatio"].long_name == "MMCR Signal-To-Noise Ratio"
    assert dataset["SignalToNoiseRatio"].units == "dB(x100)"
    assert (
        dataset["SignalToNoiseRatio"].comment
        == "Divide SignalToNoiseRatio by 100 to get dB"
    )
    assert allclose(
        dataset["SignalToNoiseRatio"][:].data,
        [
            [-32768, -32768, -32768],
            [2044, 1753, 405],
            [602, 312, -1002],
            [588, 297, -1035],
            [768, 477, -859],
            [712, 424, -793],
        ],
    )


def test_ModeId(dataset):
    assert str(dataset["ModeId"].dtype) == "int16"
    assert dataset["ModeId"].long_name == "MMCR ModeId"
    assert dataset["ModeId"].units == "unitless"
    assert allclose(
        dataset["ModeId"][:].data,
        [
            [0, 0, 0],
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2],
        ],
    )


def test_CloudLayerBottomHeight(dataset):
    assert str(dataset["CloudLayerBottomHeight"].dtype) == "float32"
    assert dataset["CloudLayerBottomHeight"].long_name == "Bottom Height of Echo Layer"
    assert dataset["CloudLayerBottomHeight"].units == "m AGL"
    assert dataset["CloudLayerTopHeight"].comment == "none"
    assert allclose(
        dataset["CloudLayerBottomHeight"][:].data,
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [54.0, 1731.0, 4268.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [54.0, 1645.0, 4268.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [54.0, 1645.0, 4268.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [54.0, 1645.0, 4268.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [54.0, 1645.0, 4354.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
    )


def test_CloudLayerTopHeight(dataset):
    assert str(dataset["CloudLayerTopHeight"].dtype) == "float32"
    assert dataset["CloudLayerTopHeight"].long_name == "Top Height of Echo Layer"
    assert dataset["CloudLayerTopHeight"].units == "m AGL"
    assert dataset["CloudLayerTopHeight"].comment == "none"

    assert allclose(
        dataset["CloudLayerTopHeight"][:].data,
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [226.0, 1860.0, 6246.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [226.0, 1860.0, 6246.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [226.0, 1860.0, 6246.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [226.0, 1860.0, 6160.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [226.0, 1860.0, 6160.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
    )
