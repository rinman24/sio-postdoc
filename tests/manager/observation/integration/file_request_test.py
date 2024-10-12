"""TODO: Docstring."""

import pytest
from dotenv import load_dotenv

from sio_postdoc.manager import FileType, Month, Observatory, Product
from sio_postdoc.manager.observation.contracts import FileRequest
from sio_postdoc.manager.observation.service import ObservationManager


@pytest.fixture(scope="module")
def manager() -> ObservationManager:
    """Yield module level service for testing."""
    load_dotenv(override=True)
    return ObservationManager()


def test_request_file(manager):
    request = FileRequest(
        product=Product.ARSCLKAZR1KOLLIAS,
        observatory=Observatory.UTQIAGVIK,
        year=2019,
        month=Month.JAN,
        day=1,
        type=FileType.DAILY,
    )
    response = manager.process(request)
    assert response.status
    assert response.message == (
        f"D{request.year}"
        f"-{str(request.month.value).zfill(2)}"
        f"-{str(request.day).zfill(2)}"
        f"-{request.observatory.name.lower()}"
        f"-{request.product.name.lower()}"
        ".ncdf"
    )
    assert response.items == tuple()


def test_negative_day(manager):
    request = FileRequest(
        product=Product.ARSCLKAZR1KOLLIAS,
        observatory=Observatory.UTQIAGVIK,
        year=2019,
        month=Month.JAN,
        day=-1,
        type=FileType.DAILY,
    )
    response = manager.process(request)
    assert not response.status
    assert response.message == "day is out of range for month"
    assert response.items == tuple()


def test_large_day(manager):
    request = FileRequest(
        product=Product.ARSCLKAZR1KOLLIAS,
        observatory=Observatory.UTQIAGVIK,
        year=2019,
        month=Month.JAN,
        day=100,
        type=FileType.DAILY,
    )
    response = manager.process(request)
    assert not response.status
    assert response.message == "day is out of range for month"
    assert response.items == tuple()


def test_file_not_found(manager):
    request = FileRequest(
        product=Product.ARSCLKAZR1KOLLIAS,
        observatory=Observatory.UTQIAGVIK,
        year=1970,
        month=Month.JAN,
        day=1,
        type=FileType.DAILY,
    )
    response = manager.process(request)
    assert not response.status
    assert response.message == "file not found"
    assert response.items == tuple()
