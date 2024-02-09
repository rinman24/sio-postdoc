from datetime import datetime
from pathlib import Path
from typing import Union

import pytest

import sio_postdoc.access.instrument.service as access
from sio_postdoc.access.instrument.contracts import (
    LidarData,
    RawDataResponse,
    RawTimeHeightData,
)

PREFIX: str = (
    "/Users/richardinman/Code/sio-postdoc/sio_postdoc/data/sheba/lidar/"  # noqa
)
SUFFIX: str = ".BARO.ncdf"


@pytest.fixture
def raw_data_response_1() -> RawDataResponse:
    return RawDataResponse(
        paths=[
            Path(PREFIX + "1997/12-december/12290820" + SUFFIX),
            Path(PREFIX + "1997/12-december/12291640" + SUFFIX),
            Path(PREFIX + "1997/12-december/12300033" + SUFFIX),
        ],
        datetimes=[
            datetime(1997, 12, 29, 8, 20),
            datetime(1997, 12, 29, 16, 40),
            datetime(1997, 12, 30, 0, 33),
        ],
    )


@pytest.fixture
def expected_1() -> dict[str, list[Union[datetime, float]]]:
    return dict(
        datetimes=[
            datetime(1997, 12, 29, 8, 20, 19, 997406),
            datetime(1997, 12, 29, 8, 20, 29, 998398),
            datetime(1997, 12, 29, 8, 20, 39, 999390),
            datetime(1997, 12, 29, 8, 20, 50, 382),
            datetime(1997, 12, 29, 8, 21, 00, 1374),
            datetime(1997, 12, 29, 8, 21, 10, 2366),
            datetime(1997, 12, 29, 8, 21, 19, 999925),
            datetime(1997, 12, 29, 8, 21, 30, 917),
            datetime(1997, 12, 29, 8, 21, 40, 1909),
            datetime(1997, 12, 29, 8, 21, 50, 2901),
        ],
        elevations=[
            0,
            0.03,
            0.06,
            0.09,
            0.12,
            0.15,
            0.18,
            0.21,
            0.24,
            0.27,
        ],
    )


@pytest.fixture
def raw_data_response_2() -> RawDataResponse:
    return RawDataResponse(
        paths=[
            Path(PREFIX + "1998/03-march/03311658" + SUFFIX),
            Path(PREFIX + "1998/04-april/04010001" + SUFFIX),
        ],
        datetimes=[
            datetime(1998, 3, 31, 16, 58),
            datetime(1998, 4, 1, 0, 1),
        ],
    )


@pytest.fixture
def expected_2() -> dict[str, list[Union[datetime, float]]]:
    return dict(
        datetimes=[
            datetime(1998, 3, 31, 16, 58, 50, 3357),
            datetime(1998, 3, 31, 16, 59, 0, 916),
            datetime(1998, 3, 31, 16, 59, 9, 998475),
            datetime(1998, 3, 31, 16, 59, 20, 2900),
            datetime(1998, 3, 31, 16, 59, 30, 459),
            datetime(1998, 3, 31, 16, 59, 39, 998018),
            datetime(1998, 3, 31, 16, 59, 50, 2443),
            datetime(1998, 3, 31, 17, 0, 0, 2),
            datetime(1998, 3, 31, 17, 0, 9, 997561),
            datetime(1998, 3, 31, 17, 0, 20, 1986),
        ],
        elevations=[
            0,
            0.03,
            0.06,
            0.09,
            0.12,
            0.15,
            0.18,
            0.21,
            0.24,
            0.27,
        ],
    )


def test_concatinate_raw_data_1(raw_data_response_1, expected_1):
    # Act
    data: RawTimeHeightData
    data = access._concatinate_raw_data(raw_data_response_1)
    # Assert
    assert isinstance(data, LidarData)

    assert len(data.far_parallel.datetimes) == 8616
    assert len(data.far_parallel.elevations) == 417
    assert len(data.far_parallel.values) == 8616
    assert sum([len(i) for i in data.far_parallel.values]) / 417 == 8616
    assert round(sum(sum(i) for i in data.far_parallel.values)) == -729800285

    assert len(data.depolarization.datetimes) == 8616
    assert len(data.depolarization.elevations) == 417
    assert len(data.depolarization.values) == 8616
    assert sum([len(i) for i in data.depolarization.values]) / 417 == 8616
    assert round(sum(sum(i) for i in data.depolarization.values)) == 318180

    for i in range(10):
        assert data.far_parallel.datetimes[i] == expected_1["datetimes"][i]
        assert data.far_parallel.elevations[i] == expected_1["elevations"][i]
        assert data.depolarization.datetimes[i] == expected_1["datetimes"][i]
        assert data.depolarization.elevations[i] == expected_1["elevations"][i]


def test_concatinate_raw_data_2(raw_data_response_2, expected_2):
    # Act
    data: RawTimeHeightData
    data = access._concatinate_raw_data(raw_data_response_2)
    # Assert
    assert isinstance(data, LidarData)

    assert len(data.far_parallel.datetimes) == 5387
    assert len(data.far_parallel.elevations) == 417
    assert len(data.far_parallel.values) == 5387
    assert sum([len(i) for i in data.far_parallel.values]) / 417 == 5387
    assert round(sum(sum(i) for i in data.far_parallel.values)) == -426267291

    assert len(data.depolarization.datetimes) == 5387
    assert len(data.depolarization.elevations) == 417
    assert len(data.depolarization.values) == 5387
    assert sum([len(i) for i in data.depolarization.values]) / 417 == 5387
    assert round(sum(sum(i) for i in data.depolarization.values)) == -4041182

    for i in range(10):
        assert data.far_parallel.datetimes[i] == expected_2["datetimes"][i]
        assert data.far_parallel.elevations[i] == expected_2["elevations"][i]
        assert data.depolarization.datetimes[i] == expected_2["datetimes"][i]
        assert data.depolarization.elevations[i] == expected_2["elevations"][i]
