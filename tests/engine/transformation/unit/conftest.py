from datetime import datetime

import pytest

from sio_postdoc.access.instrument.contracts import TimeHeightData


@pytest.fixture(params=["single", "double"])
def _pf_pulse_key(request) -> str:
    return request.param


@pytest.fixture
def _f_datetimes() -> list[datetime]:
    return [
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


@pytest.fixture
def _f_elevations() -> list[float:]:
    return [0.03, 0.06, 0.09, 0.12, 0.15]


@pytest.fixture
def _f_pulse_values() -> dict[str, list[list[float]]]:
    return dict(
        single=[
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
        ],
        double=[
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
        ],
    )


@pytest.fixture
def _f_pulse_data(
    _f_datetimes, _f_elevations, _f_pulse_values
) -> dict[str, TimeHeightData]:
    return dict(
        single=TimeHeightData(
            datetimes=_f_datetimes,
            elevations=_f_elevations,
            values=_f_pulse_values["single"],
        ),
        double=TimeHeightData(
            datetimes=_f_datetimes,
            elevations=_f_elevations,
            values=_f_pulse_values["double"],
        ),
    )
