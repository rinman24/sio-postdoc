import math
from datetime import datetime

import numpy as np

import sio_postdoc.engine.transformation.service as engine
from sio_postdoc.access.instrument.contracts import TimeHeightData


def test_replace_flagged_data_neg_999():
    # Arrange
    datetimes = [
        datetime(2024, 1, 1, 1, 10),
        datetime(2024, 1, 1, 1, 20),
        datetime(2024, 1, 1, 1, 30),
        datetime(2024, 1, 1, 1, 40),
    ]
    elevations = [0.5, 1, 1.5]
    input_values = [
        [-999, 2, 3],
        [4, -999, 6],
        [5, 4, -999],
        [2, -999, 0],
    ]
    expected_values = [
        [np.nan, 2, 3],
        [4, np.nan, 6],
        [5, 4, np.nan],
        [2, np.nan, 0],
    ]
    data: TimeHeightData = TimeHeightData(
        datetimes=datetimes,
        elevations=elevations,
        values=input_values,
    )
    expected: TimeHeightData = TimeHeightData(
        datetimes=datetimes,
        elevations=elevations,
        values=expected_values,
    )
    # Act
    clean: TimeHeightData = engine._replace(
        data=data,
        flag=-999,
        value=np.nan,
    )
    # Assert
    assert clean.datetimes == expected.datetimes
    assert clean.elevations == expected.elevations
    assert len(clean.values) == len(expected.values)
    for cln, exp in zip(clean.values, expected.values):
        assert len(cln) == len(exp)
        for c, e in zip(cln, exp):
            if math.isnan(c):
                assert math.isnan(e)
            else:
                assert c == e
