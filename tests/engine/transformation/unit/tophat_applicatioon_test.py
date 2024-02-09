import math
from typing import Union

import numpy as np
import pytest

import sio_postdoc.engine.transformation.service as engine
from sio_postdoc.access.instrument.contracts import TimeHeightData

EXPECTED_SINGLE_PULSE_VALUES: list[Union[float, np.nan]] = [
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [-0.25, 0.0, 0.0, 0.0, 0.0],
    [-0.5, -0.25, 0.0, 0.0, 0.0],
    [-0.25, -0.5, -0.25, 0.0, 0.0],
    [0.0, -0.25, -0.5, -0.25, 0.0],
    [0.25, 0.0, -0.25, -0.5, -0.25],
    [0.5, 0.25, 0.0, -0.25, -0.25],
    [0.25, 0.5, 0.25, 0.25, 0.25],
    [0.0, 0.25, 0.75, 0.75, 0.25],
    [0.0, 0.25, 0.75, 0.75, 0.25],
    [0.25, 0.5, 0.25, 0.25, 0.25],
    [0.5, 0.25, 0.0, -0.25, -0.25],
    [0.25, 0.0, -0.25, -0.5, -0.25],
    [0.0, -0.25, -0.5, -0.25, 0.0],
    [-0.25, -0.5, -0.25, 0.0, 0.0],
    [-0.5, -0.25, 0.0, 0.0, 0.0],
    [-0.25, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
]

EXPECTED_DOUBLE_PULSE_VALUES: list[Union[float, np.nan]] = [
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [-0.25, -0.5, -0.25, 0.0, 0.0],
    [0.0, -0.25, -0.5, -0.25, 0.0],
    [0.25, 0.0, -0.25, -0.5, -0.25],
    [0.5, 0.25, 0.0, -0.25, -0.25],
    [0.25, 0.5, 0.25, 0.25, 0.25],
    [0.0, 0.25, 0.75, 0.75, 0.25],
    [0.0, 0.25, 0.75, 0.75, 0.25],
    [0.25, 0.5, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0.0, -0.25, -0.25],
    [-0.25, -0.25, -0.25, -0.5, -0.25],
    [-0.25, -0.75, -0.75, -0.25, 0.0],
    [-0.25, -0.75, -0.75, -0.25, 0.0],
    [-0.25, -0.25, -0.25, -0.5, -0.25],
    [0.25, 0.25, 0.0, -0.25, -0.25],
    [0.25, 0.5, 0.25, 0.25, 0.25],
    [0.0, 0.25, 0.75, 0.75, 0.25],
    [0.0, 0.25, 0.75, 0.75, 0.25],
    [0.25, 0.5, 0.25, 0.25, 0.25],
    [0.5, 0.25, 0.0, -0.25, -0.25],
    [0.25, 0.0, -0.25, -0.5, -0.25],
    [0.0, -0.25, -0.5, -0.25, 0.0],
    [-0.25, -0.5, -0.25, 0.0, 0.0],
    [-0.5, -0.25, 0.0, 0.0, 0.0],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan],
]


@pytest.fixture
def _f_expected(_f_datetimes, _f_elevations) -> dict[str, TimeHeightData]:
    return dict(
        single=TimeHeightData(
            datetimes=_f_datetimes,
            elevations=_f_elevations,
            values=EXPECTED_SINGLE_PULSE_VALUES,
        ),
        double=TimeHeightData(
            datetimes=_f_datetimes,
            elevations=_f_elevations,
            values=EXPECTED_DOUBLE_PULSE_VALUES,
        ),
    )


def test_tophat_application(_pf_pulse_key, _f_expected, _f_pulse_data):
    # Arrange
    expected: TimeHeightData = _f_expected[_pf_pulse_key]
    # Act
    result: TimeHeightData = engine._rolling_apply(
        data=_f_pulse_data[_pf_pulse_key],
        func=engine._wavelet,
        window=8,
        kwargs={"kind": "tophat"},
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
