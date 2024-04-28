"""Test the creation of `InstrumentData` from raw SHEBA DABUL `Dataset`."""

import os
from datetime import datetime
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
from sio_postdoc.engine.transformation.strategies.raw.eureka.ahsrl import EurekaAhsrlRaw

DIRECTORY: str = "/tests/access/instrument/integration/netCDF4_files/"
FILENAME: str = "ahsrl_D2008-09-21T00-00-00_30s_30m.eureka_ahsrl_test.nc"
PATH: Path = Path(os.getcwd() + DIRECTORY + FILENAME)


@pytest.fixture(scope="module")
def context() -> TransformationContext:
    context: TransformationContext = TransformationContext()
    context.strategy = EurekaAhsrlRaw()
    return context


@pytest.fixture(scope="module")
def dataset() -> Generator[DataSet, None, None]:
    data: DataSet = DataSet(PATH)
    yield data
    data.close()


@pytest.fixture(scope="module")
def data(context, dataset) -> InstrumentData:
    return context.hydrate(dataset, PATH)


def test_init(context):
    assert isinstance(context, TransformationContext)
    assert isinstance(context.strategy, EurekaAhsrlRaw)


# def test_dimensions(data):
#     assert len(data.dimensions) == 3


def test_time_dimension(data):
    assert data.dimensions["time"] == Dimension(name=Dimensions.TIME, size=6)


def test_level_dimension(data):
    assert data.dimensions["level"] == Dimension(name=Dimensions.LEVEL, size=3)


def test_degrees_dimension(data):
    assert data.dimensions["angle"] == Dimension(name=Dimensions.ANGLE, size=4)


# def test_variables(data):
#     assert len(data.variables) == 9


def test_counts_lo_variable(data):
    var: Variable = data.variables["counts_lo"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.I4
    assert var.long_name == "Low Gain Combined Photon Counts"
    assert var.scale == Scales.ONE
    assert var.units == Units.NONE
    assert var.values == (
        (557654, 56641, 1980),
        (557940, 57206, 2093),
        (558454, 57456, 1992),
        (604798, 61537, 2027),
        (558429, 57499, 1769),
        (558247, 57274, 2026),
    )


def test_counts_hi_variable(data):
    var: Variable = data.variables["counts_hi"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.I4
    assert var.long_name == "High Gain Combined Photon Counts"
    assert var.scale == Scales.ONE
    assert var.units == Units.NONE
    assert var.values == (
        (793186, 225421, 36897),
        (793750, 224982, 37594),
        (794103, 225480, 36914),
        (860080, 242103, 36056),
        (793712, 222074, 30974),
        (794443, 227433, 38366),
    )


def test_cross_counts_variable(data):
    var: Variable = data.variables["cross_counts"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.I4
    assert var.long_name == "Cross Polarized Photon Counts"
    assert var.scale == Scales.ONE
    assert var.units == Units.NONE
    assert var.values == (
        (3259673, 765202, 0),
        (3257464, 761927, 0),
        (3256298, 765139, 0),
        (3528099, 828282, 0),
        (3255033, 767666, 0),
        (3253180, 769465, 0),
    )


def test_depol_variable(data):
    var: Variable = data.variables["depol"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.I2
    assert var.long_name == "Circular depolarization ratio for particulate"
    assert var.scale == Scales.THOUSAND
    assert var.units == Units.NONE
    assert var.values == (
        (-32768, 891, -11),
        (-32768, 877, -9),
        (-32768, 874, -11),
        (-32768, 885, -11),
        (-32768, 876, -14),
        (-32768, 884, -10),
    )


def test_epoch_variable(data):
    var: Variable = data.variables["epoch"]
    assert len(var.dimensions) == 0
    assert var.dtype == DType.I4
    assert var.long_name == "Unix Epoch 1970 of Initial Timestamp"
    assert var.scale == Scales.ONE
    assert var.units == Units.SECONDS
    assert var.values == 1221980400
    # TODO: Add this to other tests
    assert datetime.fromtimestamp(var.values) == datetime(2008, 9, 21, 0, 0)


def test_latitude(data):
    var: Variable = data.variables["latitude"]
    assert len(var.dimensions) == 0
    assert var.dtype == DType.U1
    assert var.long_name == "Platform Latitude [North]"
    assert var.scale == Scales.ONE
    assert var.units == Units.DEGREES
    assert var.values == (1, 79, 59, 25)


def test_longitude(data):
    var: Variable = data.variables["longitude"]
    assert len(var.dimensions) == 0
    assert var.dtype == DType.U1
    assert var.long_name == "Platform Longitude [East]"
    assert var.scale == Scales.ONE
    assert var.units == Units.DEGREES
    assert var.values == (1, 85, 56, 20)


def test_molecular_counts(data):
    var: Variable = data.variables["molecular_counts"]
    assert len(var.dimensions) == 2
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dimensions[1] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.I4
    assert var.long_name == "Molecular Photon Counts"
    assert var.scale == Scales.ONE
    assert var.units == Units.NONE
    assert var.values == (
        (941193, 17500, 31942),
        (940739, 17726, 31574),
        (941563, 17342, 32121),
        (1016112, 18831, 34467),
        (938971, 17644, 32128),
        (943866, 17841, 32346),
    )


def test_offset_variable(data):
    var: Variable = data.variables["offset"]
    assert len(var.dimensions) == 1
    assert var.dimensions[0] == Dimension(name=Dimensions.TIME, size=6)
    assert var.dtype == DType.I4
    assert var.long_name == "Seconds Since Initial Timestamp"
    assert var.scale == Scales.ONE
    assert var.units == Units.SECONDS
    assert var.values == (-1, 29, 59, 88, 121, 151)


def test_range_variable(data):
    var: Variable = data.variables["range"]
    assert len(var.dimensions) == 1
    assert var.dimensions[0] == Dimension(name=Dimensions.LEVEL, size=3)
    assert var.dtype == DType.U2
    assert var.long_name == "Return Range"
    assert var.scale == Scales.ONE
    assert var.units == Units.METERS
    assert var.values == (11, 41, 71)
