"""Define contracts for the `ObservationManager`."""

from pydantic import BaseModel

from sio_postdoc.manager import Instrument, Month, Observatory


class DailyRequest(BaseModel):
    """Encapsulate requests for the creation of daily files."""

    instrument: Instrument
    observatory: Observatory
    month: Month
    year: int
