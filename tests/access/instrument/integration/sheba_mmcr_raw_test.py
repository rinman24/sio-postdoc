"""Test ShebaMmchRaw implementation of AbstractDataStrategy"""

import os
from datetime import datetime
from pathlib import Path

import pytest

from sio_postdoc.access.instrument.contracts import InstrumentData
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
