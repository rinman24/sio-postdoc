"""Define contracts for the `ObservationManager`."""

from datetime import date

from pydantic import BaseModel

from sio_postdoc.manager import (
    FileType,
    Instrument,
    Month,
    Observatory,
    Process,
    Product,
)


class ObservatoryRequest(BaseModel):
    """Encapsulate an request for an observatory."""

    observatory: Observatory
    month: Month
    year: int


class DailyRequest(ObservatoryRequest):
    """Encapsulate requests for the creation of daily files."""

    instrument: Instrument


class DailyProductRequest(ObservatoryRequest):
    """Encapsulate requests for the creation of daily files."""

    product: Product


class ContainerContentRequest(BaseModel):
    """Encapsulate requests for blobs in a container."""

    observatory: Observatory
    product: Product
    type: FileType
    year: int


class FileRequest(ObservatoryRequest):
    """Encapsulate requests for the request of daily files."""

    product: Product
    day: int
    type: FileType
    content: tuple[str, ...]
    inclusive: bool
    time: bool


class DownloadInfo(BaseModel):
    """Encapsulate requsts to download files to the local disk."""

    product: Product
    type: FileType
    inclusive: bool
    time: bool
    target: date


class PlotRequest(BaseModel):
    """Encapsulate requests for the request of daily files."""

    filename: str
    product: Product


class ProcessRequest(ObservatoryRequest):
    """Encapsulate the request of processing steps."""

    process: Process


class RequestResponse(BaseModel):
    """Encapsulate response to a request."""

    status: bool
    message: str = ""
    items: tuple = tuple()


class BlobRequest(BaseModel):
    """Encapsulate request for a blob."""

    container: str
    prefix: str = ""
