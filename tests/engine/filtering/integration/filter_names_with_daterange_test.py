"""Test that you can use a range of dates to filter formatted timestamps in filenames."""

from datetime import date

from sio_postdoc.engine.filtering.context import FilterContext
from sio_postdoc.engine.filtering.strategies import NamesByDate

Content = tuple[str, ...]


def test_filter_01():
    # Arrange
    service: FilterContext = FilterContext()
    filenames: Content = (
        "D1998-03-24T00-00-00.mrg.corrected.nc",
        "D1998-03-24T12-00-00.mrg.corrected.nc",
        "D1998-03-25T00-00-00.mrg.corrected.nc",
        "D1998-03-25T12-00-00.mrg.corrected.nc",
        "D1998-03-26T00-00-00.mrg.corrected.nc",
        "D1998-03-26T12-00-00.mrg.corrected.nc",
    )
    target = date(1998, 3, 25)
    # Act
    response: Content = service.apply(target, filenames, strategy=NamesByDate())
    # Assert
    assert response == (
        "D1998-03-25T00-00-00.mrg.corrected.nc",
        "D1998-03-25T12-00-00.mrg.corrected.nc",
    )


def test_filter_02():
    # Arrange
    service: FilterContext = FilterContext()
    filenames: Content = (
        "D1998-05-03T08-25-00.BARO.ncdf",
        "D1998-05-03T16-45-00.BARO.ncdf",
        "D1998-05-04T00-33-00.BARO.ncdf",
        "D1998-05-04T08-53-00.BARO.ncdf",
        "D1998-05-04T17-14-00.BARO.ncdf",
        "D1998-05-05T00-12-00.BARO.ncdf",
        "D1998-05-05T08-32-00.BARO.ncdf",
        "D1998-05-05T16-52-00.BARO.ncdf",
    )
    target = date(1998, 5, 4)
    # Act
    response: Content = service.apply(target, filenames, strategy=NamesByDate())
    # Assert
    assert response == (
        "D1998-05-03T16-45-00.BARO.ncdf",
        "D1998-05-04T00-33-00.BARO.ncdf",
        "D1998-05-04T08-53-00.BARO.ncdf",
        "D1998-05-04T17-14-00.BARO.ncdf",
        "D1998-05-05T00-12-00.BARO.ncdf",
    )
