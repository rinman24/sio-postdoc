from datetime import datetime, timedelta
from pathlib import Path

import pytest

import sio_postdoc.access.instrument.service as access
from sio_postdoc.access.instrument.contracts import (
    DateRange,
    Instrument,
    LidarData,
    RawDataRequest,
    RawDataResponse,
    TimeHeightData,
)


@pytest.fixture
def request_() -> RawDataRequest:
    return RawDataRequest(
        daterange=DateRange(
            start=datetime.now(),
            end=datetime.now() + timedelta(1),
        ),
        instrument=Instrument(
            location="sheba",
            name="lidar",
        ),
    )


def test_identify_files_call(monkeypatch, request_):
    # Arrange
    def mock_identify_files(request: RawDataRequest) -> RawDataResponse:
        return RawDataResponse(
            paths=[Path("test_path")],
            datetimes=[datetime(2024, 1, 1)],
        )

    def mock_concatinate_raw_data(response: RawDataResponse) -> LidarData:
        return LidarData(
            far_parallel=TimeHeightData(
                datetimes=[datetime(2024, 1, 1)],
                elevations=[1],
                values=[[1]],
            ),
            depolarization=TimeHeightData(
                datetimes=[datetime(2024, 1, 1)],
                elevations=[2],
                values=[[2]],
            ),
        )

    monkeypatch.setattr(
        access,
        "_identify_files",
        mock_identify_files,
    )
    monkeypatch.setattr(
        access,
        "_concatinate_raw_data",
        mock_concatinate_raw_data,
    )
    # Act
    result: LidarData = access.process(request_)
    # Assert
    assert result == mock_concatinate_raw_data(mock_identify_files(request_))
