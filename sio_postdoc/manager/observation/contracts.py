"""Define contracts for the `ObservationManager`."""

from pydantic import BaseModel

from sio_postdoc.manager import FileType, Instrument, Month, Observatory, Product


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
    month: Month | None = None
    year: int


class FileRequest(BaseModel):
    """Encapsulate requests for the request of daily files."""

    product: Product
    observatory: Observatory
    year: int
    month: Month
    day: int
    type: FileType


class RequestResponse(BaseModel):
    """Encapsulate response to a request."""

    status: bool
    message: str
    items: tuple


class BlobRequest(BaseModel):
    """Encapsulate request for a blob."""

    container: str
    prefix: str = ""
