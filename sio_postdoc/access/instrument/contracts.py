"""TODO: Docstring."""

from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator

from sio_postdoc.access.instrument.constants import VALID_LOCATIONS, VALID_NAMES  # noqa


class DateRange(BaseModel):
    """TODO: Docstring."""

    start: datetime
    end: datetime

    @model_validator(mode="after")
    def end_must_be_at_least_one_minute_after_start(self) -> "DateRange":
        """TODO: Docstring."""
        if self.end < self.start:
            raise ValueError("start cannot be before end")
        elif self.start == self.end:
            raise ValueError("start and end cannot be equal")
        return self


class Instrument(BaseModel):
    """TODO: Docstring."""

    location: str
    name: str

    @field_validator("location")
    @classmethod
    def location_must_be_valid(cls, location: str) -> str:
        """TODO: Docstring."""
        if location not in VALID_LOCATIONS:
            message: str
            message = f"'{location}' not a valid location; "
            message += f"valid locations include {VALID_LOCATIONS}"
            raise ValueError(message)
        return location

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, name: str) -> str:
        """TODO: Docstring."""
        if name not in VALID_NAMES:
            message: str
            message = f"'{name}' not a valid name; "
            message += f"valid names include {VALID_NAMES}"
            raise ValueError(message)
        return name


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
    # Make sure that the units are in a subset of what we want


class PhysicalMatrix(Data):
    """TODO: Docstring."""

    values: tuple[tuple[float, ...], ...]


class InstrumentData(BaseModel):
    """TODO: Docstring."""

    time: TemporalVector
    axis: tuple[PhysicalVector, ...]
    # NOTE: Rather than tuples, these should be dictionaries
    matrices: tuple[PhysicalMatrix, ...]
    vectors: tuple[PhysicalVector, ...]
    name: str
    observatory: str
    notes: str
