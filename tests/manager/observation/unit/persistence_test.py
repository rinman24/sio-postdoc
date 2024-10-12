"""Test the persistence algorithm."""

import pytest
from dotenv import load_dotenv

from sio_postdoc.manager.observation.service import ObservationManager


@pytest.fixture(scope="module")
def manager() -> ObservationManager:
    """Yield module level service for testing."""
    load_dotenv(override=True)
    return ObservationManager()


def test_cloudiness_filter_01(manager):
    # Arrange
    a = [1] * 30
    b = [0] * 1
    c = [1] * 2
    d = [0] * 40
    data = a + b + c + d
    result = manager._persistence(data)
    assert result == [33]


def test_cloudiness_filter_02(manager):
    # Arrange
    a = [0] * 5
    b = [1] * 30
    c = [0] * 1
    d = [1] * 2
    e = [0] * 40
    data = a + b + c + d + e
    result = manager._persistence(data)
    assert result == [33]


def test_cloudiness_filter_03(manager):
    # Arrange
    a = [1, 0, 1, 1, 0]
    b = [1] * 30
    c = [0] * 1
    d = [1] * 2
    e = [0] * 40
    data = a + b + c + d + e
    result = manager._persistence(data)
    assert result == [33]


def test_cloudiness_filter_04(manager):
    # Arrange
    a = [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0] * 10
    b = [1] * 25
    c = [0] * 10
    d = [1] * 25
    e = [0] * 10
    data = a + b + c + d + e
    result = manager._persistence(data)
    assert result == []


def test_cloudiness_filter_05(manager):
    # Arrange
    a = [1, 0, 1, 1, 0]
    b = [1] * 30
    c = [0] * 20
    d = [1] * 2
    e = [0] * 40
    data = a + b + c + d + e
    result = manager._persistence(data)
    assert result == [52]


def test_cloudiness_filter_06(manager):
    # Arrange
    a = [1, 0, 1, 1, 0]
    b = [1] * 30
    c = [0] * 20
    d = [1] * 2
    e = [0] * 40
    f = [1] * 29
    g = [0] * 20
    h = [1] * 33
    i = [0] * 10
    j = [1] * 40
    k = [0] * 30
    data = a + b + c + d + e + f + g + h + i + j + k
    result = manager._persistence(data)
    assert result == [52, 83]


def test_cloudiness_filter_07(manager):
    # Arrange
    a = [1, 0, 1, 1, 0]
    b = [1] * 30
    c = [0] * 20
    d = [1] * 2
    e = [0] * 40
    f = [1] * 29
    g = [0] * 20
    h = [1] * 33
    i = [0] * 10
    j = [1] * 40
    k = [0] * 31
    data = a + b + c + d + e + f + g + h + i + j + k
    result = manager._persistence(data)
    assert result == [52, 83]


def test_cloudiness_filter_07(manager):
    # Arrange
    a = [1] * 35
    b = [0] * 30
    c = [0] * 20
    d = [1] * 2
    e = [0] * 40
    f = [1] * 29
    g = [0] * 20
    h = [1] * 33
    i = [0] * 10
    j = [1] * 40
    k = [0] * 31
    data = a + b + c + d + e + f + g + h + i + j + k
    result = manager._persistence(data)
    assert result == [52, 83]
