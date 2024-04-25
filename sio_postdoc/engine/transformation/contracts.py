"""Instrument Access Contracts."""

from datetime import datetime
from typing import Union

from pydantic import BaseModel

from sio_postdoc.engine import Dimensions, DType, Scales, Units

Vector = tuple[int, ...]
Matrix = tuple[Vector, ...]
Values = Union[int, Vector, Matrix]


class DateTime(BaseModel):
    """Define a custom `DateTime`."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

    @property
    def unix(self) -> int:
        """Seconds since Unix Epoch."""
        return int(
            datetime(
                year=self.year,
                month=self.month,
                day=self.day,
                hour=self.hour,
                minute=self.minute,
                second=self.second,
            ).timestamp()
        )

    @property
    def initial(self) -> datetime:
        """Return `datetime` of initial observation."""
        return datetime.fromtimestamp(self.unix)


class Dimension(BaseModel):
    """Container describing a dimension."""

    name: Dimensions
    size: int


class Variable(BaseModel):
    """Container describing a variable.

    NOTE: A variable can have zero, one, two, or many dimensions.
    """

    dimensions: tuple[Dimension, ...]
    dtype: DType
    long_name: str
    scale: Scales
    units: Units
    values: Values


class HorizontalCoordinate(BaseModel):
    """Define a horizontal coordinate."""


class InstrumentData(BaseModel):
    """Container for data from an instrument."""

    dimensions: dict[str, Dimension]
    variables: dict[str, Variable]


class VariableRequest(BaseModel):
    """Request values from a `DataSet`."""

    variable: str
    name: str
    long_name: str
    units: Units
    scale: Scales
    dtype: DType
    flag: int
    dimensions: tuple[Dimension, ...]
    conversion_scale: Scales = Scales.ONE
