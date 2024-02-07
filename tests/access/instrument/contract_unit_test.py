import pytest

from sio_postdoc.utility.builders import AccessContractsBuilder

builder: AccessContractsBuilder = AccessContractsBuilder()


@pytest.fixture
def text_start() -> str:
    return "2018-03-20-08:45"


@pytest.fixture
def text_end() -> str:
    return "2018-03-20-21:45"


@pytest.fixture
def valid_location() -> str:
    return "sheba"


@pytest.fixture
def invalid_location() -> str:
    return "not-a-valid-location"


@pytest.fixture
def valid_name() -> str:
    return "lidar"


@pytest.fixture
def invalid_name() -> str:
    return "not-a-valid-name"


def test_daterange_start_cannot_be_before_end(text_start, text_end):
    with pytest.raises(ValueError) as excinfo:
        builder.daterange(start=text_end, end=text_start)
    assert "start cannot be before end" in str(excinfo.value)


def test_daterange_start_and_end_cannot_be_equal(text_start):
    with pytest.raises(ValueError) as excinfo:
        builder.daterange(start=text_start, end=text_start)
    assert "start and end cannot be equal" in str(excinfo.value)


def test_instrument_has_invalid_location(invalid_location, valid_name):
    with pytest.raises(ValueError) as excinfo:
        builder.instrument(location=invalid_location, name=valid_name)
    assert invalid_location in str(excinfo.value)


def test_instrument_has_invalid_name(valid_location, invalid_name):
    with pytest.raises(ValueError) as excinfo:
        builder.instrument(location=valid_location, name=invalid_name)
    assert invalid_name in str(excinfo.value)
