"""Test the creation of netCDF files."""

import os
from typing import Generator

import pytest
from numpy import allclose

from sio_postdoc.access.instrument.types import Dataset
from tests.helper.builder.raw.context import RawDataContext
from tests.helper.builder.raw.strategies import ShebaDabulRaw
from tests.helper.builder.raw.types import Instrument, Observatory


@pytest.fixture(scope="module")
def dataset() -> Generator[Dataset, None, None]:
    # Arrange
    data = RawDataContext(Observatory.SHEBA, Instrument.DABUL)
    data.hydrate()
    dataset = Dataset(data.filename)
    # Test
    yield dataset
    # Cleanup
    dataset.close()
    os.remove(data.filename)


def test_attributes(dataset):
    assert dataset.instrument_name == "dabul"
    assert dataset.experiment_name == "sheba"
    assert dataset.site_name == "arctic"
    assert dataset.netcdf_filename == "D1998-05-06T00-25-00.BARO.sheba_dabul_test.ncdf"
    assert dataset.netcdf_file_creation == "012201"


def test_dimensions(dataset):
    assert dataset.dimensions["record"].size == ShebaDabulRaw._records
    assert dataset.dimensions["level"].size == ShebaDabulRaw._levels
    assert dataset.dimensions["filename_size"].size == len(dataset.netcdf_filename)


def test_range(dataset):
    assert dataset["range"].long_name == "range"
    assert dataset["range"].units == "meter"
    assert str(dataset["range"].dtype) == "float32"
    assert list(dataset["range"][:].data) == [0.0, 30.0, 60.0]


def test_time(dataset):
    assert dataset["time"].long_name == "time"
    assert dataset["time"].units == "seconds since 1970-01-01 00:00 UTC"
    assert str(dataset["range"].dtype) == "float32"
    assert allclose(
        list(dataset["time"][:].data),
        [
            0.41666666,
            0.41944444,
            0.42222223,
            0.42499998,
            0.42777777,
            0.43055555,
        ],
    )


def test_latitude(dataset):
    assert dataset["latitude"].long_name == "platform latitude"
    assert dataset["latitude"].units == "degrees_north"
    assert str(dataset["latitude"].dtype) == "float32"
    assert allclose(
        list(dataset["latitude"][:].data),
        [
            76.03717,
            76.03717,
            76.03718,
            76.03718,
            76.037186,
            76.037186,
        ],
    )


def test_longitude(dataset):
    assert dataset["longitude"].long_name == "platform longitude"
    assert dataset["longitude"].units == "degrees_east"
    assert str(dataset["longitude"].dtype) == "float32"
    assert allclose(
        list(dataset["longitude"][:].data),
        [
            -165.25378,
            -165.25378,
            -165.25377,
            -165.25375,
            -165.25374,
            -165.25372,
        ],
    )


def test_altitude(dataset):
    assert dataset["altitude"].long_name == "platform altitude"
    assert dataset["altitude"].units == "meter"
    assert str(dataset["altitude"].dtype) == "float32"
    assert allclose(list(dataset["altitude"][:].data), [10.0] * 6)


def test_elevation(dataset):
    assert dataset["elevation"].long_name == "beam elevation angle"
    assert dataset["elevation"].units == "degrees"
    assert str(dataset["elevation"].dtype) == "float32"
    assert allclose(
        list(dataset["elevation"][:].data),
        [
            95.043205,
            95.167625,
            94.96686,
            94.948654,
            95.03751,
            95.015335,
        ],
    )


def test_azimuth(dataset):
    assert dataset["azimuth"].long_name == "beam azimuth angle"
    assert dataset["azimuth"].units == "degrees"
    assert str(dataset["azimuth"].dtype) == "float32"
    assert allclose(
        list(dataset["azimuth"][:].data),
        [
            194.38048,
            194.38042,
            194.38037,
            194.38025,
            194.38014,
            194.38008,
        ],
    )


def test_scanmode(dataset):
    assert dataset["scanmode"].long_name == "scan mode"
    assert str(dataset["scanmode"].dtype) == "int16"
    assert list(dataset["scanmode"][:].data) == [-999] * 6


def test_depolarization(dataset):
    assert dataset["depolarization"].long_name == "far parallel channel"
    assert str(dataset["depolarization"].dtype) == "float32"
    assert allclose(
        dataset["depolarization"][:].data,
        [
            [1.5441344, 1.3981241, 0.3610639],
            [1.3873776, 1.6597508, 0.40076607],
            [1.477456, 1.3367455, 0.42651573],
            [1.4093928, 1.1275327, 0.39695445],
            [1.3849448, 1.1230909, 0.2626472],
            [1.5751007, 1.0160526, 0.29984418],
        ],
    )


def test_far_parallel(dataset):
    assert str(dataset["far_parallel"].dtype) == "float32"
    assert allclose(
        dataset["far_parallel"][:].data,
        [
            [-999.0, -999.0, 59.016533],
            [-999.0, -999.0, 62.122227],
            [-999.0, -999.0, 60.314087],
            [-999.0, -999.0, 60.391975],
            [-999.0, -999.0, 58.352943],
            [-999.0, -999.0, 59.214672],
        ],
    )
