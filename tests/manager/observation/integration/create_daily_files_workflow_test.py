"""Test the create daily files workflow."""

from pathlib import Path

import pytest
from dotenv import load_dotenv

from sio_postdoc.manager import Instrument, Month, Observatory
from sio_postdoc.manager.observation.contracts import DailyRequest, ObservatoryRequest
from sio_postdoc.manager.observation.service import ObservationManager

# load_dotenv(override=True)
# manager = ObservationManager()

# request = ObservatoryRequest(
#     observatory=Observatory.SHEBA,
#     month=Month.SEP,
#     year=1998,
# )
# manager.merge_daily_masks(request)


# request = DailyRequest(
#     instrument=Instrument.MMCR,
#     observatory=Observatory.SHEBA,
#     month=Month.NOV,
#     year=1998,
# )
# manager.create_daily_masks(request)


# for month in [Month.JAN, Month.FEB, Month.MAR, Month.APR, Month.MAY, Month.JUN, Month.JUL, Month.AUG, Month.SEP, Month.OCT, Month.NOV, Month.DEC]:
#     request = DailyRequest(
#         instrument=Instrument.MMCR,
#         observatory=Observatory.EUREKA,
#         month=month,
#         year=2014,
#     )
#     manager.create_daily_files(request)


@pytest.fixture(scope="module")
def manager() -> ObservationManager:
    """Yield module level service for testing."""
    load_dotenv(override=True)
    return ObservationManager()


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_format_dir(manager):
    directory: Path = Path("/Users/richardinman/Code/sio-postdoc/KAZR-TEST")
    manager.format_dir(directory=directory, suffix=".nc", year="2023")


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_files(manager):
    request = DailyRequest(
        instrument=Instrument.AHSRL,
        observatory=Observatory.EUREKA,
        month=Month.AUG,
        year=2005,
    )
    manager.create_daily_files(request)


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_masks(manager):
    request = DailyRequest(
        instrument=Instrument.MMCR,
        observatory=Observatory.SHEBA,
        month=Month.NOV,
        year=1997,
    )
    manager.create_daily_masks(request, threshold=-5, name="refl")
