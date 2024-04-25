"""Test the creation of `InstrumentData` from raw SHEBA DABUL `Dataset`."""

import os
from pathlib import Path
from typing import Generator

import pytest

from sio_postdoc.access import DataSet
from sio_postdoc.engine import Dimensions, Scales, Units
from sio_postdoc.engine.transformation.context.service import TransformationContext
from sio_postdoc.engine.transformation.contracts import (
    Dimension,
    DType,
    InstrumentData,
    Variable,
)
from sio_postdoc.engine.transformation.strategies.raw.sheba.mmcr import ShebaMmcrRaw

DIRECTORY: str = "/tests/access/instrument/integration/netCDF4_files/"
FILENAME: str = "D1997-11-20T00-00-00.mrg.corrected.sheba_mmcr_test.nc"
PATH: Path = Path(os.getcwd() + DIRECTORY + FILENAME)


@pytest.fixture(scope="module")
def context() -> TransformationContext:
    context: TransformationContext = TransformationContext()
    context.strategy = ShebaMmcrRaw()
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
    assert isinstance(context.strategy, ShebaMmcrRaw)


def test_instrument_data(data):
    assert isinstance(data, InstrumentData)


def test_dimensions(data):
    assert len(data.dimensions) == 2


def test_time_dimension(data):
    assert data.dimensions["time"] == Dimension(name=Dimensions.TIME, size=6)


def test_level_dimension(data):
    assert data.dimensions["level"] == Dimension(name=Dimensions.LEVEL, size=3)


# def test_variables(data):
#     assert len(data.variables) == 9


def test_epoch_variable(data):
    var: Variable = data.variables["epoch"]
    assert len(var.dimensions) == 0
    assert var.dtype == DType.I4
    assert var.long_name == "Unix Epoch 1970 of Initial Timestamp"
    assert var.scale == Scales.ONE
    assert var.units == Units.SECONDS
    assert var.values == 880012800


def test_mean_dopp_vel_variable(data):
    var: Variable = data.variables["mean_dopp_vel"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.I2
    assert var.long_name == "Mean Doppler Velocity"
    assert var.scale == Scales.THOUSAND
    assert var.units == Units.METERS_PER_SECOND
    assert var.values == (
        (-826, -299, -32768),
        (-826, -299, -32768),
        (-826, -299, -32768),
        (-821, -303, -32768),
        (-816, -308, -32768),
        (-810, -313, -32768),
    )


def test_offset_variable(data):
    var: Variable = data.variables["offset"]
    assert len(var.dimensions) == 1
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dtype == DType.I4
    assert var.long_name == "Seconds Since Initial Timestamp"
    assert var.scale == Scales.ONE
    assert var.units == Units.SECONDS
    assert var.values == (0, 10, 20, 30, 40, 50)


def test_range_variable(data):
    var: Variable = data.variables["range"]
    assert len(var.dimensions) == 1
    assert var.dimensions[0] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.U2
    assert var.long_name == "Return Range"
    assert var.scale == Scales.ONE
    assert var.units == Units.METERS
    assert var.values == (105, 150, 195)


def test_refl_variable(data):
    var: Variable = data.variables["refl"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.I2
    assert var.long_name == "Reflectivity"
    assert var.scale == Scales.HUNDRED
    assert var.units == Units.DBZ
    assert var.values == (
        (-4713, -3745, -32768),
        (-4713, -3745, -32768),
        (-4713, -3745, -32768),
        (-4725, -3727, -32768),
        (-4738, -3709, -32768),
        (-4751, -3692, -32768),
    )


def test_spec_width_variable(data):
    var: Variable = data.variables["spec_width"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.I2
    assert var.long_name == "Spectral Width"
    assert var.scale == Scales.THOUSAND
    assert var.units == Units.METERS_PER_SECOND
    assert var.values == (
        (101, 116, -32768),
        (101, 116, -32768),
        (101, 116, -32768),
        (173, 180, -32768),
        (244, 244, -32768),
        (316, 308, -32768),
    )
