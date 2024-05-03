"""Test the create daily files workflow."""

import pytest
from dotenv import load_dotenv

from sio_postdoc.manager import Instrument, Month, Observatory
from sio_postdoc.manager.observation.contracts import DailyRequest
from sio_postdoc.manager.observation.service import ObservationManager

# load_dotenv(override=True)
# manager = ObservationManager()

# for month in [Month.OCT, Month.NOV, Month.DEC]:
#     request = DailyRequest(
#         instrument=Instrument.MMCR,
#         observatory=Observatory.SHEBA,
#         month=month,
#         year=1998,
#     )
#     manager.create_daily_masks(request, threshold=-5, name="refl")


# load_dotenv(override=True)


# manager = ObservationManager()

# request = DailyRequest(
#     instrument=Instrument.MMCR,
#     observatory=Observatory.SHEBA,
#     month=Month.NOV,
#     year=1998,
# )
# manager.create_daily_files(request)


@pytest.fixture(scope="module")
def manager() -> ObservationManager:
    """Yield module level service for testing."""
    load_dotenv(override=True)
    return ObservationManager()


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_create_daily_files(manager):
    request = DailyRequest(
        instrument=Instrument.DABUL,
        observatory=Observatory.SHEBA,
        month=Month.NOV,
        year=1997,
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
