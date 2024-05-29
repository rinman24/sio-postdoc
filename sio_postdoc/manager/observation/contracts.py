"""Define contracts for the `ObservationManager`."""

from pydantic import BaseModel

from sio_postdoc.manager import Instrument, Month, Observatory, Product


class DailyRequest(BaseModel):
    """Encapsulate requests for the creation of daily files."""

    instrument: Instrument
    observatory: Observatory
    month: Month
    year: int


class DailyProductRequest(BaseModel):
    """Encapsulate requests for the creation of daily files."""

    product: Product
    observatory: Observatory
    month: Month
    year: int


class ObservatoryRequest(BaseModel):
    """Encapsulate requests for the creation of daily files."""

    observatory: Observatory
    month: Month
    year: int
