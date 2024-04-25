"""Test the creation of `InstrumentData` from raw SHEBA DABUL `Dataset`."""

import os
from pathlib import Path
from typing import Generator

import pytest

from sio_postdoc.access import DataSet
from sio_postdoc.engine import Dimensions, Scales, Signs, Units
from sio_postdoc.engine.transformation.context.service import TransformationContext
from sio_postdoc.engine.transformation.contracts import (
    Dimension,
    DType,
    InstrumentData,
    Variable,
)
from sio_postdoc.engine.transformation.strategies.raw.sheba.dabul import ShebaDabulRaw

DIRECTORY: str = "/tests/access/instrument/integration/netCDF4_files/"
FILENAME: str = "D1998-05-06T00-25-00.BARO.sheba_dabul_test.ncdf"
PATH: Path = Path(os.getcwd() + DIRECTORY + FILENAME)


@pytest.fixture(scope="module")
def context() -> TransformationContext:
    context: TransformationContext = TransformationContext()
    context.strategy = ShebaDabulRaw()
    return context


@pytest.fixture(scope="module")
def dataset() -> Generator[DataSet, None, None]:
    data: DataSet = DataSet(PATH)
    yield data
    data.close()


@pytest.fixture(scope="module")
def data(context, dataset) -> InstrumentData:
    return context.instrument_data(dataset, PATH)


def test_init(context):
    assert isinstance(context, TransformationContext)
    assert isinstance(context.strategy, ShebaDabulRaw)


def test_instrument_data(data):
    assert isinstance(data, InstrumentData)


def test_dimensions(data):
    assert len(data.dimensions) == 3


def test_time_dimension(data):
    assert data.dimensions["time"] == Dimension(name=Dimensions.TIME, size=6)


def test_level_dimension(data):
    assert data.dimensions["level"] == Dimension(name=Dimensions.LEVEL, size=3)


def test_degrees_dimension(data):
    assert data.dimensions["angle"] == Dimension(name=Dimensions.ANGLE, size=4)


def test_variables(data):
    assert len(data.variables) == 9


def test_azimuth_variable(data):
    var: Variable = data.variables["azimuth"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.ANGLE, size=4)
    assert var.dtype == DType.U1
    assert var.long_name == "Beam Azimuth Angle"
    assert var.scale == Scales.ONE
    assert var.units == Units.DEGREES
    assert var.values == (
        (-1, 165, 37, 10),
        (-1, 165, 37, 10),
        (-1, 165, 37, 11),
        (-1, 165, 37, 11),
        (-1, 165, 37, 11),
        (-1, 165, 37, 12),
    )


def test_depol_variable(data):
    var: Variable = data.variables["depol"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.I2
    assert var.long_name == "Depolarization Ratio"
    assert var.scale == Scales.THOUSAND
    assert var.units == Units.NONE
    assert var.values == (
        (1544, 1398, 361),
        (1387, 1660, 401),
        (1477, 1337, 427),
        (1409, 1128, 397),
        (1385, 1123, 263),
        (1575, 1016, 300),
    )


def test_epoch_variable(data):
    var: Variable = data.variables["epoch"]
    assert len(var.dimensions) == 0
    assert var.dtype == DType.I4
    assert var.long_name == "Unix Epoch 1970 of Initial Timestamp"
    assert var.scale == Scales.ONE
    assert var.units == Units.SECONDS
    assert var.values == 894439500


def test_far_par_variable(data):
    var: Variable = data.variables["far_par"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.I2
    assert var.long_name == "Lidar Returned Power"
    assert var.scale == Scales.HUNDRED
    assert var.units == Units.UNSPECIFIED
    assert var.values == (
        (-32768, -32768, 5902),
        (-32768, -32768, 6212),
        (-32768, -32768, 6031),
        (-32768, -32768, 6039),
        (-32768, -32768, 5835),
        (-32768, -32768, 5921),
    )


def test_latitude_variable(data):
    var: Variable = data.variables["latitude"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.ANGLE, size=4)
    assert var.dtype == DType.U1
    assert var.long_name == "Platform Latitude [North]"
    assert var.scale == Scales.ONE
    assert var.units == Units.DEGREES
    assert var.values == (
        (1, 76, 2, 14),
        (1, 76, 2, 14),
        (1, 76, 2, 14),
        (1, 76, 2, 14),
        (1, 76, 2, 14),
        (1, 76, 2, 14),
    )


def test_longitude_variable(data):
    var: Variable = data.variables["longitude"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.ANGLE, size=4)
    assert var.dtype == DType.U1
    assert var.long_name == "Platform Longitude [East]"
    assert var.scale == Scales.ONE
    assert var.units == Units.DEGREES
    assert var.values == (
        (-1, 165, 15, 14),
        (-1, 165, 15, 14),
        (-1, 165, 15, 14),
        (-1, 165, 15, 14),
        (-1, 165, 15, 13),
        (-1, 165, 15, 13),
    )


def test_offset_variable(data):
    var: Variable = data.variables["offset"]
    assert len(var.dimensions) == 1
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dtype == DType.I4
    assert var.long_name == "Seconds Since Initial Timestamp"
    assert var.scale == Scales.ONE
    assert var.units == Units.SECONDS
    assert var.values == (1500, 1510, 1520, 1530, 1540, 1550)


def test_range_variable(data):
    var: Variable = data.variables["range"]
    assert len(var.dimensions) == 1
    assert var.dimensions[0] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.U2
    assert var.long_name == "Return Range"
    assert var.scale == Scales.ONE
    assert var.units == Units.METERS
    assert var.values == (0, 30, 60)


def test_scan_mode_variable(data):
    var: Variable = data.variables["scan_mode"]
    assert len(var.dimensions) == 1
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dtype == DType.I4
    assert var.long_name == "Scan Mode"
    assert var.scale == Scales.ONE
    assert var.units == Units.NONE
    assert var.values == (
        -2147483648,
        -2147483648,
        -2147483648,
        -2147483648,
        -2147483648,
        -2147483648,
    )
