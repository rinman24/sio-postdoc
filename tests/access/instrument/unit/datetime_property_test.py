"""Test the various properties of `DateTime`."""

from datetime import datetime

import pytest

from sio_postdoc.engine.transformation.contracts import DateTime


@pytest.fixture(scope="module")
def date_time() -> DateTime:
    return DateTime(
        year=1984,
        month=9,
        day=24,
        hour=1,
        minute=7,
        second=24,
    )


BASE: int = 464836044
INITIAL: datetime = datetime.fromtimestamp(BASE)


def test_base_property(date_time: DateTime) -> None:
    assert date_time.base == BASE


def test_initial_property(date_time: DateTime) -> None:
    assert date_time.initial == INITIAL
