"""TODO: Docstring."""

from datetime import datetime

from pydantic import BaseModel


class Data(BaseModel):
    """TODO: Docstring."""

    units: str
    name: str
    scale: float
    flag: float
    dtype: str


class PhysicalVector(Data):
    """TODO: Docstring."""

    values: tuple[float, ...]


class TemporalVector(Data):
    """TODO: Docstring."""

    initial: datetime
    offsets: tuple[float, ...]


class PhysicalMatrix(Data):
    """TODO: Docstring."""

    values: tuple[tuple[float, ...], ...]


class InstrumentData(BaseModel):
    """TODO: Docstring."""

    time: TemporalVector
    axis: tuple[PhysicalVector, ...]
    matrices: tuple[PhysicalMatrix, ...]
    vectors: tuple[PhysicalVector, ...]
    name: str
    observatory: str
    notes: str
