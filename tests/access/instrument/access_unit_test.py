from datetime import datetime

import pytest

import sio_postdoc.access.instrument.service as access
from sio_postdoc.access.instrument.contracts import FilterResponse, RawDataRequest
from sio_postdoc.utility.builders import AccessContractsBuilder

builder: AccessContractsBuilder = AccessContractsBuilder()


IDENTIFY_LIDAR_FILES: list[tuple[RawDataRequest, list[str]]] = [
    (
        builder.raw_data_request(
            start="1998-05-06-00:00",
            end="1998-05-06-23:59",
            location="sheba",
            name="lidar",
        ),
        dict(
            paths=[
                "05051652.BARO.ncdf",
                "05060025.BARO.ncdf",
                "05060845.BARO.ncdf",
                "05061705.BARO.ncdf",
                "05070001.BARO.ncdf",
            ],
            datetimes=[
                datetime(1998, 5, 5, 16, 52),
                datetime(1998, 5, 6, 0, 25),
                datetime(1998, 5, 6, 8, 45),
                datetime(1998, 5, 6, 17, 5),
                datetime(1998, 5, 7, 0, 1),
            ],
        ),
    ),
    (
        builder.raw_data_request(
            start="1997-12-29-00:00",
            end="1997-12-29-23:59",
            location="sheba",
            name="lidar",
        ),
        dict(
            paths=[
                "12290000.BARO.ncdf",
                "12290820.BARO.ncdf",
                "12291640.BARO.ncdf",
                "12300033.BARO.ncdf",
            ],
            datetimes=[
                datetime(1997, 12, 29, 0, 0),
                datetime(1997, 12, 29, 8, 20),
                datetime(1997, 12, 29, 16, 40),
                datetime(1997, 12, 30, 0, 33),
            ],
        ),
    ),
    (
        builder.raw_data_request(
            start="1997-12-29-09:00",
            end="1997-12-29-23:59",
            location="sheba",
            name="lidar",
        ),
        dict(
            paths=[
                "12290820.BARO.ncdf",
                "12291640.BARO.ncdf",
                "12300033.BARO.ncdf",
            ],
            datetimes=[
                datetime(1997, 12, 29, 8, 20),
                datetime(1997, 12, 29, 16, 40),
                datetime(1997, 12, 30, 0, 33),
            ],
        ),
    ),
    (
        builder.raw_data_request(
            start="1998-06-01-00:00",
            end="1998-06-02-23:59",
            location="sheba",
            name="lidar",
        ),
        dict(
            paths=[
                "05311648.BARO.ncdf",
                "06010035.BARO.ncdf",
                "06010855.BARO.ncdf",
                "06011715.BARO.ncdf",
                "06020035.BARO.ncdf",
                "06020536.BARO.ncdf",
                "06021036.BARO.ncdf",
                "06021536.BARO.ncdf",
                "06022037.BARO.ncdf",
                "06030003.BARO.ncdf",
            ],
            datetimes=[
                datetime(1998, 5, 31, 16, 48),
                datetime(1998, 6, 1, 0, 35),
                datetime(1998, 6, 1, 8, 55),
                datetime(1998, 6, 1, 17, 15),
                datetime(1998, 6, 2, 0, 35),
                datetime(1998, 6, 2, 5, 36),
                datetime(1998, 6, 2, 10, 36),
                datetime(1998, 6, 2, 15, 36),
                datetime(1998, 6, 2, 20, 37),
                datetime(1998, 6, 3, 0, 3),
            ],
        ),
    ),
    (
        builder.raw_data_request(
            start="1998-01-01-00:00",
            end="1998-01-02-23:59",
            location="sheba",
            name="lidar",
        ),
        dict(
            paths=[
                "12311731.BARO.ncdf",
                "01010027.BARO.ncdf",
                "01010847.BARO.ncdf",
                "01011707.BARO.ncdf",
                "01020024.BARO.ncdf",
                "01020844.BARO.ncdf",
                "01021704.BARO.ncdf",
                "01030020.BARO.ncdf",
            ],
            datetimes=[
                datetime(1997, 12, 31, 17, 31),
                datetime(1998, 1, 1, 0, 27),
                datetime(1998, 1, 1, 8, 47),
                datetime(1998, 1, 1, 17, 7),
                datetime(1998, 1, 2, 0, 24),
                datetime(1998, 1, 2, 8, 44),
                datetime(1998, 1, 2, 17, 4),
                datetime(1998, 1, 3, 0, 20),
            ],
        ),
    ),
    (
        builder.raw_data_request(
            start="1998-01-07-00:00",
            end="1998-01-07-18:34",
            location="sheba",
            name="lidar",
        ),
        dict(
            paths=[
                "01061648.BARO.ncdf",
                "01070002.BARO.ncdf",
                "01071014.BARO.ncdf",
                "01071834.BARO.ncdf",
            ],
            datetimes=[
                datetime(1998, 1, 6, 16, 48),
                datetime(1998, 1, 7, 0, 2),
                datetime(1998, 1, 7, 10, 14),
                datetime(1998, 1, 7, 18, 34),
            ],
        ),
    ),
    (
        builder.raw_data_request(
            start="1998-05-31-12:00",
            end="1998-06-01-12:00",
            location="sheba",
            name="lidar",
        ),
        dict(
            paths=[
                "05310827.BARO.ncdf",
                "05311648.BARO.ncdf",
                "06010035.BARO.ncdf",
                "06010855.BARO.ncdf",
                "06011715.BARO.ncdf",
            ],
            datetimes=[
                datetime(1998, 5, 31, 8, 27),
                datetime(1998, 5, 31, 16, 48),
                datetime(1998, 6, 1, 0, 35),
                datetime(1998, 6, 1, 8, 55),
                datetime(1998, 6, 1, 17, 15),
            ],
        ),
    ),
    (
        builder.raw_data_request(
            start="1997-12-31-12:00",
            end="1998-01-01-12:00",
            location="sheba",
            name="lidar",
        ),
        dict(
            paths=[
                "12310911.BARO.ncdf",
                "12311731.BARO.ncdf",
                "01010027.BARO.ncdf",
                "01010847.BARO.ncdf",
                "01011707.BARO.ncdf",
            ],
            datetimes=[
                datetime(1997, 12, 31, 9, 11),
                datetime(1997, 12, 31, 17, 31),
                datetime(1998, 1, 1, 0, 27),
                datetime(1998, 1, 1, 8, 47),
                datetime(1998, 1, 1, 17, 7),
            ],
        ),
    ),
]


@pytest.mark.parametrize("raw_data_request, expected", IDENTIFY_LIDAR_FILES)
def test_identify_files(raw_data_request, expected):
    response: FilterResponse = access._identify_files(raw_data_request)
    assert len(expected["paths"]) == len(response.paths)
    assert len(expected["datetimes"]) == len(response.datetimes)
    for exp, res in zip(expected["paths"], response.paths):
        assert str(res).endswith(exp)
    for exp, res in zip(expected["datetimes"], response.datetimes):
        assert exp == res
