"""Test monotonic times method."""

from sio_postdoc.engine.transformation.strategies.base import TransformationStrategy


def test_monotonic_times():
    # Arrange
    times: list[float] = [86380, 86390, 0, 10, 20]
    expected: tuple[float, ...] = (86380, 86390, 86400, 86410, 86420)
    # Act
    result: tuple[float, ...] = TransformationStrategy._monotonic_times(times)
    # Assert
    assert result == expected
    assert result == expected
