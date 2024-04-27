"""Test the create daily files workflow."""

import pytest
from dotenv import load_dotenv

from sio_postdoc.manager import Instrument, Month, Observatory
from sio_postdoc.manager.observation.contracts import DailyRequest
from sio_postdoc.manager.observation.service import ObservationManager


@pytest.fixture(scope="module")
def manager() -> ObservationManager:
    """Yield module level service for testing."""
    load_dotenv(override=True)
    return ObservationManager()


@pytest.mark.skip(reason="Used for User Acceptance Testing.")
def test_workflow(manager):
    request = DailyRequest(
        instrument=Instrument.DABUL,
        observatory=Observatory.SHEBA,
        month=Month.FEB,
        year=1998,
    )
    manager.create_daily_files(request)
