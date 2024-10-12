"""Test date formatting strategies."""

import pytest

from sio_postdoc.engine.formatting.service import FormattingContext
from sio_postdoc.engine.formatting.strategies import (
    DDMMMYYYYdothhColonmmDashhhColonmm,
    MMDDhhmm,
    YYYYMMDDdothhmmss,
)


@pytest.fixture(scope="module")
def context() -> FormattingContext:
    return FormattingContext()


def test_MMDDhhmm(context):
    assert (
        context.format(
            "11020820.BHAR.ncdf",
            "1997",
            strategy=MMDDhhmm(),
        )
        == "D1997-11-02T08-20-00.BHAR.ncdf"
    )


def test_YYYYMMDDdothhmmss(context):
    assert (
        context.format(
            "eurmmcrmerge.C1.c1.20240924.200822.nc",
            "2024",
            strategy=YYYYMMDDdothhmmss(),
        )
        == "eurmmcrmerge.C1.c1.D2024-09-24T20-08-22.nc"
    )


def test_DDMMMYYYYdothhColonmmDashhhColonmm(context):
    assert (
        context.format(
            "01sep1998.12:00-24:00.mrg.corrected.nc",
            "1998",
            strategy=DDMMMYYYYdothhColonmmDashhhColonmm(),
        )
        == "D1998-09-01T12-00-00.mrg.corrected.nc"
    )


def test_no_match(context):
    raw: str = "nopattern"
    with pytest.raises(ValueError) as excinfo:
        context.format(raw, "2024", strategy=YYYYMMDDdothhmmss())
    assert f"No match found: '{raw}'" in str(excinfo.value)
