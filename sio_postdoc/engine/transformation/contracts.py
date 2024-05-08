"""Instrument Access Contracts."""

from datetime import datetime, timezone
from enum import Enum, auto
from typing import Union

from pydantic import BaseModel

from sio_postdoc.engine import Dimensions, DType, Scales, Units

Vector = tuple[int, ...]
Matrix = tuple[Vector, ...]
Values = Union[int, Vector, Matrix]
EPOCH: datetime = datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc)


class DateTime(BaseModel):
    """Define a custom `DateTime`."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

    @property
    def datetime(self) -> datetime:
        """Return a `datetime`."""
        return datetime(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            tzinfo=timezone.utc,
        )

    @property
    def unix(self) -> int:
        """Seconds since Unix Epoch."""
        return int((self.datetime - EPOCH).total_seconds())


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
    flag: int | float
    dimensions: tuple[Dimension, ...]
    conversion_scale: Scales = Scales.ONE


class Direction(Enum):
    """Define directions for thresholds.

    Specifies whether valid values less than or greater than the threshold.
    """

    LESS_THAN = auto()
    GREATER_THAN = auto()


class Threshold(BaseModel):
    """Container for a threshold."""

    value: int
    direction: Direction


class MaskRequest(BaseModel):
    """Request a binary cloud mask from a `DataSet`."""

    values: tuple[tuple[int, ...], ...]
    length: int
    height: int
    threshold: Threshold
    scale: int
    dtype: DType


class MaskCode(BaseModel):
    """Container for mask codes for bases and tops of masked objects."""

    bottom: int
    top: int


class VerticalTransition(BaseModel):
    """Container for the base of a masked object."""

    elevation: int  # meters
    code: MaskCode


class VerticalExtent(BaseModel):
    """Container for the vertical extent of masked objects."""

    # NOTE: Each datetime could have several bases and tops
    # So there is one datetime with these
    # And then you keep a list of these things.

    datetimes: tuple[datetime, ...]
    bases: tuple[VerticalTransition, ...]  # meters
    tops: tuple[VerticalTransition, ...]  # meters
