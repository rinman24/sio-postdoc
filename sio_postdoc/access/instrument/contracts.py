"""Instrument Access Contracts"""

from datetime import datetime

from pydantic import BaseModel


class Data(BaseModel):
    """Base data model for other contracts to extend."""

    units: str
    name: str
    scale: float
    flag: float
    dtype: str


class PhysicalVector(Data):
    """Container for one-dimensional data."""

    values: tuple[float, ...]


class TemporalVector(Data):
    """
    Container for one-dimensional temporal data.

    NOTE: `offsets` should always be in seconds.
    """

    initial: datetime
    offsets: tuple[float, ...]


class PhysicalMatrix(Data):
    """Container for two-dimensional data."""

    values: tuple[tuple[float, ...], ...]


class InstrumentData(BaseModel):
    """Container for data from an instrument."""

    time: TemporalVector
    axis: tuple[PhysicalVector, ...]
    matrices: tuple[PhysicalMatrix, ...]
    vectors: tuple[PhysicalVector, ...]
    name: str
    observatory: str
    notes: str
