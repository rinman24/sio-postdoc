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
        [
            "05051652.BARO.ncdf",
            "05060025.BARO.ncdf",
            "05060845.BARO.ncdf",
            "05061705.BARO.ncdf",
            "05070001.BARO.ncdf",
        ],
    ),
    (
        builder.raw_data_request(
            start="1997-12-29-00:00",
            end="1997-12-29-23:59",
            location="sheba",
            name="lidar",
        ),
        [
            "12290000.BARO.ncdf",
            "12290820.BARO.ncdf",
            "12291640.BARO.ncdf",
            "12300033.BARO.ncdf",
        ],
    ),
    (
        builder.raw_data_request(
            start="1997-12-29-09:00",
            end="1997-12-29-23:59",
            location="sheba",
            name="lidar",
        ),
        [
            "12290820.BARO.ncdf",
            "12291640.BARO.ncdf",
            "12300033.BARO.ncdf",
        ],
    ),
    (
        builder.raw_data_request(
            start="1998-06-01-00:00",
            end="1998-06-02-23:59",
            location="sheba",
            name="lidar",
        ),
        [
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
    ),
    (
        builder.raw_data_request(
            start="1998-01-01-00:00",
            end="1998-01-02-23:59",
            location="sheba",
            name="lidar",
        ),
        [
            "12311731.BARO.ncdf",
            "01010027.BARO.ncdf",
            "01010847.BARO.ncdf",
            "01011707.BARO.ncdf",
            "01020024.BARO.ncdf",
            "01020844.BARO.ncdf",
            "01021704.BARO.ncdf",
            "01030020.BARO.ncdf",
        ],
    ),
    (
        builder.raw_data_request(
            start="1998-01-07-00:00",
            end="1998-01-07-18:34",
            location="sheba",
            name="lidar",
        ),
        [
            "01061648.BARO.ncdf",
            "01070002.BARO.ncdf",
            "01071014.BARO.ncdf",
            "01071834.BARO.ncdf",
        ],
    ),
    (
        builder.raw_data_request(
            start="1998-05-31-12:00",
            end="1998-06-01-12:00",
            location="sheba",
            name="lidar",
        ),
        [
            "05310827.BARO.ncdf",
            "05311648.BARO.ncdf",
            "06010035.BARO.ncdf",
            "06010855.BARO.ncdf",
            "06011715.BARO.ncdf",
        ],
    ),
    (
        builder.raw_data_request(
            start="1997-12-31-12:00",
            end="1998-01-01-12:00",
            location="sheba",
            name="lidar",
        ),
        [
            "12310911.BARO.ncdf",
            "12311731.BARO.ncdf",
            "01010027.BARO.ncdf",
            "01010847.BARO.ncdf",
            "01011707.BARO.ncdf",
        ],
    ),
]


@pytest.mark.parametrize("raw_data_request, expected", IDENTIFY_LIDAR_FILES)
def test_identify_files(raw_data_request, expected):
    response: FilterResponse = access._identify_files(raw_data_request)
    assert len(expected) == len(response.paths)
    for exp, res in zip(expected, response.paths):
        assert str(res).endswith(exp)
