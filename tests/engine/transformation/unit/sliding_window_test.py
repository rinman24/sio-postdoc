import math
from datetime import datetime

import numpy as np
import pytest

import sio_postdoc.engine.transformation.service as engine
from sio_postdoc.access.instrument.contracts import TimeHeightData

datetimes = [
    datetime(2024, 1, 1, 1, 0),
    datetime(2024, 1, 1, 1, 10),
    datetime(2024, 1, 1, 1, 20),
    datetime(2024, 1, 1, 1, 30),
    datetime(2024, 1, 1, 1, 40),
    datetime(2024, 1, 1, 1, 50),
    datetime(2024, 1, 1, 2, 0),
    datetime(2024, 1, 1, 2, 10),
    datetime(2024, 1, 1, 2, 20),
    datetime(2024, 1, 1, 2, 30),
    datetime(2024, 1, 1, 2, 40),
    datetime(2024, 1, 1, 2, 50),
    datetime(2024, 1, 1, 3, 0),
    datetime(2024, 1, 1, 3, 10),
    datetime(2024, 1, 1, 3, 20),
    datetime(2024, 1, 1, 3, 30),
    datetime(2024, 1, 1, 3, 40),
    datetime(2024, 1, 1, 3, 50),
    datetime(2024, 1, 1, 4, 0),
    datetime(2024, 1, 1, 4, 10),
    datetime(2024, 1, 1, 4, 20),
    datetime(2024, 1, 1, 4, 30),
    datetime(2024, 1, 1, 4, 40),
    datetime(2024, 1, 1, 4, 50),
    datetime(2024, 1, 1, 5, 0),
    datetime(2024, 1, 1, 5, 10),
    datetime(2024, 1, 1, 5, 20),
    datetime(2024, 1, 1, 5, 30),
    datetime(2024, 1, 1, 5, 40),
    datetime(2024, 1, 1, 5, 50),
]

elevations = [0.03, 0.06, 0.09, 0.12, 0.15]

single_pulse_values = [
    [0, 0, 0, 0, 0],  # 1
    [0, 0, 0, 0, 0],  # 2
    [0, 0, 0, 0, 0],  # 3
    [0, 0, 0, 0, 0],  # 4
    [0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 0],  # 7
    [0, 0, 0, 0, 0],  # 8
    [0, 0, 0, 0, 0],  # 9
    [0, 0, 0, 0, 0],  # 10
    [1, 0, 0, 0, 0],  # 11
    [1, 1, 0, 0, 0],  # 12
    [1, 1, 1, 0, 0],  # 13
    [1, 1, 1, 1, 0],  # 14
    [1, 1, 1, 1, 1],  # 15
    [1, 1, 1, 1, 0],  # 16
    [1, 1, 1, 0, 0],  # 17
    [1, 1, 0, 0, 0],  # 18
    [1, 0, 0, 0, 0],  # 19
    [0, 0, 0, 0, 0],  # 20
    [0, 0, 0, 0, 0],  # 21
    [0, 0, 0, 0, 0],  # 22
    [0, 0, 0, 0, 0],  # 23
    [0, 0, 0, 0, 0],  # 24
    [0, 0, 0, 0, 0],  # 25
    [0, 0, 0, 0, 0],  # 26
    [0, 0, 0, 0, 0],  # 27
    [0, 0, 0, 0, 0],  # 28
    [0, 0, 0, 0, 0],  # 29
    [0, 0, 0, 0, 0],  # 30
]

double_pulse_values = [
    [0, 0, 0, 0, 0],  # 1
    [0, 0, 0, 0, 0],  # 2
    [0, 0, 0, 0, 0],  # 3
    [0, 0, 0, 0, 0],  # 4
    [0, 0, 0, 0, 0],  # 5
    [1, 0, 0, 0, 0],  # 6
    [1, 1, 0, 0, 0],  # 7
    [1, 1, 1, 0, 0],  # 8
    [1, 1, 1, 1, 0],  # 9
    [1, 1, 1, 1, 1],  # 10
    [1, 1, 1, 1, 0],  # 11
    [1, 1, 1, 0, 0],  # 12
    [1, 1, 0, 0, 0],  # 13
    [1, 0, 0, 0, 0],  # 14
    [0, 0, 0, 0, 0],  # 15
    [1, 0, 0, 0, 0],  # 16
    [1, 1, 0, 0, 0],  # 17
    [1, 1, 1, 0, 0],  # 18
    [1, 1, 1, 1, 0],  # 19
    [1, 1, 1, 1, 1],  # 20
    [1, 1, 1, 1, 0],  # 21
    [1, 1, 1, 0, 0],  # 22
    [1, 1, 0, 0, 0],  # 23
    [1, 0, 0, 0, 0],  # 24
    [0, 0, 0, 0, 0],  # 25
    [0, 0, 0, 0, 0],  # 26
    [0, 0, 0, 0, 0],  # 27
    [0, 0, 0, 0, 0],  # 28
    [0, 0, 0, 0, 0],  # 29
    [0, 0, 0, 0, 0],  # 30
]

expected_single_pule_values = [
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 1
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 2
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 3
    [0, 0, 0, 0, 0],  # 4
    [0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 0],  # 7
    [10, 0, 0, 0, 0],  # 8
    [20, 10, 0, 0, 0],  # 9
    [30, 20, 10, 0, 0],  # 10
    [40, 30, 20, 10, 0],  # 11
    [50, 40, 30, 20, 10],  # 12
    [60, 50, 40, 30, 10],  # 13
    [70, 60, 50, 30, 10],  # 14
    [70, 70, 50, 30, 10],  # 15
    [70, 60, 50, 30, 10],  # 16
    [60, 50, 40, 30, 10],  # 17
    [50, 40, 30, 20, 10],  # 18
    [40, 30, 20, 10, 0],  # 19
    [30, 20, 10, 0, 0],  # 20
    [20, 10, 0, 0, 0],  # 21
    [10, 0, 0, 0, 0],  # 22
    [0, 0, 0, 0, 0],  # 23
    [0, 0, 0, 0, 0],  # 24
    [0, 0, 0, 0, 0],  # 25
    [0, 0, 0, 0, 0],  # 26
    [0, 0, 0, 0, 0],  # 27
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 28
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 29
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 30
]


expected_double_pule_values = [
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 1
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 2
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 3
    [20, 10, 0, 0, 0],  # 4
    [30, 20, 10, 0, 0],  # 5
    [40, 30, 20, 10, 0],  # 6
    [50, 40, 30, 20, 10],  # 7
    [60, 50, 40, 30, 10],  # 8
    [70, 60, 50, 30, 10],  # 9
    [70, 70, 50, 30, 10],  # 10
    [70, 60, 50, 30, 10],  # 11
    [60, 50, 40, 30, 10],  # 12
    [60, 40, 30, 20, 10],  # 13
    [60, 40, 20, 10, 0],  # 14
    [60, 40, 20, 0, 0],  # 15
    [60, 40, 20, 10, 0],  # 16
    [60, 40, 30, 20, 10],  # 17
    [60, 50, 40, 30, 10],  # 18
    [70, 60, 50, 30, 10],  # 19
    [70, 70, 50, 30, 10],  # 20
    [70, 60, 50, 30, 10],  # 21
    [60, 50, 40, 30, 10],  # 22
    [50, 40, 30, 20, 10],  # 23
    [40, 30, 20, 10, 0],  # 24
    [30, 20, 10, 0, 0],  # 25
    [20, 10, 0, 0, 0],  # 26
    [10, 0, 0, 0, 0],  # 27
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 28
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 29
    [np.nan, np.nan, np.nan, np.nan, np.nan],  # 30
]


single_pulse_data: TimeHeightData = TimeHeightData(
    datetimes=datetimes,
    elevations=elevations,
    values=single_pulse_values,
)

double_pulse_data: TimeHeightData = TimeHeightData(
    datetimes=datetimes,
    elevations=elevations,
    values=double_pulse_values,
)

single_pulse_expected: TimeHeightData = TimeHeightData(
    datetimes=datetimes,
    elevations=elevations,
    values=expected_single_pule_values,
)

double_pulse_expected: TimeHeightData = TimeHeightData(
    datetimes=datetimes,
    elevations=elevations,
    values=expected_double_pule_values,
)


@pytest.mark.parametrize(
    "data, expected",
    [
        (single_pulse_data, single_pulse_expected),
        (double_pulse_data, double_pulse_expected),
    ],
)
def test_sliding_window(data, expected):
    # Act
    result: TimeHeightData = engine._rolling_apply(
        data=data,
        func=lambda array: 10 * sum(array),
        window=7,
    )
    # Assert
    assert result.datetimes == expected.datetimes
    assert result.elevations == expected.elevations
    assert len(result.values) == len(expected.values)
    # TODO: This should be a helper
    for res, exp in zip(result.values, expected.values):
        assert len(res) == len(exp)
        for r, e in zip(res, exp):
            if math.isnan(r):
                assert math.isnan(e)
            else:
                assert r == e
