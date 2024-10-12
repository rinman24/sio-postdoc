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
    Wavelet,
    WaveletOrder,
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
    process: Process | None = None
    product: Product | None = None
    type: FileType
    year: int
    seconds: int | None = None
    meters: int | None = None
    wavelet: Wavelet | None = None
    wavelet_order: WaveletOrder | None = None


class FileRequest(ObservatoryRequest):
    """Encapsulate requests for the request of daily files."""

    process: Process | None = None
    product: Product | None = None
    day: int
    type: FileType
    content: tuple[str, ...]
    inclusive: bool
    time: bool
    filename_day: bool = True


class DownloadInfo(BaseModel):
    """Encapsulate requsts to download files to the local disk."""

    product: Product | None = None
    process: Process | None = None
    type: FileType
    inclusive: bool
    time: bool
    target: date
    seconds: int | None = None
    meters: int | None = None


class ProductPlotRequest(ObservatoryRequest):
    """Encapsulate requests for the request of daily product plots."""

    day: int
    product: Product
    left: float | None = None
    right: float | None = None
    bottom: float | None = None
    top: float | None = None


class ProcessPlotRequest(ObservatoryRequest):
    """Encapsulate requests for the request of daily product plots."""

    day: int
    process: Process
    left: float | None = None
    right: float | None = None
    bottom: float | None = None
    top: float | None = None


class ProcessRequest(ObservatoryRequest):
    """Encapsulate the request of processing steps."""

    process: Process
    seconds: int | None = None
    meters: int | None = None
    wavelet: Wavelet | None = None
    wavelet_order: WaveletOrder | None = None

    @property
    def resolution_description(self) -> str:
        """Return a description of the process resolution."""
        if self.seconds and self.meters:
            return f"{self.seconds}_seconds_{self.meters}_meters"
        return ""

    @property
    def shape(self) -> str:
        """Return the name of the wavelet."""
        if self.wavelet:
            return self.wavelet.name.lower()
        return ""

    @property
    def order(self) -> str:
        """Return the zero-padded order of the wavelet."""
        if self.wavelet_order:
            return str(self.wavelet_order.value).zfill(2)
        return ""

    @property
    def wavelet_description(self):
        """Return a description of the process wavelet."""
        if self.wavelet and self.wavelet_order:
            return f"{self.shape}_order_{self.order}"
        return ""

    @property
    def wavelet_dir(self):
        """Return the directory describing the process wavelet."""
        if self.wavelet and self.wavelet_order:
            return f"{self.shape}/order_{self.order}"
        return ""


class RequestResponse(BaseModel):
    """Encapsulate response to a request."""

    status: bool
    message: str = ""
    items: tuple = tuple()


class BlobRequest(BaseModel):
    """Encapsulate request for a blob."""

    container: str
    prefix: str = ""
