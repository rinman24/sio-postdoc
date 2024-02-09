import math
from datetime import datetime

import numpy as np
import pytest

import sio_postdoc.engine.transformation.service as engine
from sio_postdoc.access.instrument.contracts import DateRange, TimeHeightData

# TODO: This is also copy and paste from remove_flagged_data_test
# You need to move these to conftest.py

datetimes = [
    datetime(2024, 1, 1, 1, 10),
    datetime(2024, 1, 1, 1, 20),
    datetime(2024, 1, 1, 1, 30),
    datetime(2024, 1, 1, 1, 40),
]

elevations = [0.5, 1, 1.5]

values = [
    [np.nan, 2, 3],
    [4, np.nan, 6],
    [5, 4, np.nan],
    [2, np.nan, 0],
]

data = TimeHeightData(
    datetimes=datetimes,
    elevations=elevations,
    values=values,
)

date_range = DateRange(
    start=datetimes[1],
    end=datetimes[2],
)

no_cropping_date_range = DateRange(
    start=datetimes[0],
    end=datetimes[-1],
)


@pytest.fixture
def expected() -> TimeHeightData:
    return TimeHeightData(
        datetimes=datetimes[1:3],
        elevations=elevations,
        values=values[1:3],
    )


@pytest.fixture
def result() -> TimeHeightData:
    return engine._crop(data, date_range)


def test_cropping(result, expected):
    assert result.datetimes == expected.datetimes


def test_no_cropping():
    result: TimeHeightData = engine._crop(data, no_cropping_date_range)
    assert result.datetimes == data.datetimes


def test_columns_not_changed(result, expected):
    assert result.elevations == expected.elevations


def test_values_are_unchanged(result, expected):
    # TODO: This is a copy and paster from remove_flagged_data_test.py
    # TODO: Move this to a helper
    for res, exp in zip(result.values, expected.values):
        assert len(res) == len(exp)
        for r, e in zip(res, exp):
            if math.isnan(r):
                assert math.isnan(e)
            else:
                assert r == e
