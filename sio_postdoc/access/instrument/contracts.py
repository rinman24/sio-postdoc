from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, field_validator, model_validator

from sio_postdoc.access.instrument.constants import VALID_LOCATIONS, VALID_NAMES  # noqa


class AccessResponse(BaseModel):
    success: bool
    message: str


class DateRange(BaseModel):
    start: datetime
    end: datetime

    @model_validator(mode="after")
    def end_must_be_at_least_one_minute_after_start(self) -> "DateRange":
        if self.end < self.start:
            raise ValueError("start cannot be before end")
        elif self.start == self.end:
            raise ValueError("start and end cannot be equal")
        return self


class Instrument(BaseModel):
    location: str
    name: str

    @field_validator("location")
    @classmethod
    def location_must_be_valid(cls, location: str) -> str:
        if location not in VALID_LOCATIONS:
            message: str
            message = f"'{location}' not a valid location; "
            message += f"valid locations include {VALID_LOCATIONS}"
            raise ValueError(message)
        return location

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, name: str) -> str:
        if name not in VALID_NAMES:
            message: str
            message = f"'{name}' not a valid name; "
            message += f"valid names include {VALID_NAMES}"
            raise ValueError(message)
        return name

    # TODO: Add a model validator for valid location and name
    # combinations once you have more locations in that may not
    # have all the equipment


class RawDataRequest(BaseModel):
    daterange: DateRange
    instrument: Instrument

    @property
    def start(self) -> datetime:
        return self.daterange.start

    @property
    def end(self) -> datetime:
        return self.daterange.end

    @property
    def location(self) -> str:
        return self.instrument.location

    @property
    def instr_name(self) -> str:
        return self.instrument.name


class MonthRange(BaseModel):
    years: list[int]
    months: dict[int, list[int]]  # keys are years: values are months


class DayRange(BaseModel):
    years: list[int]
    months: dict[int, list[int]]  # keys are years: values are months
    days: dict[str, set[int]]  # keys are 'year-month': values are days


class RawDataResponse(BaseModel):
    paths: list[Path]
    datetimes: list[datetime]


class FilterRequest(BaseModel):
    start: datetime
    end: datetime
    path: Path
    valid_days: list[int]
    year: int
    response: RawDataResponse


class RawTimeHeightData(BaseModel):
    datetimes: list[datetime]  # This is the first index (rows)
    elevations: list[float]  # This is the second index (column)
    # The inner list is at constant time (elevation varies)
    values: list[list[float]]


class TimeHeightData(BaseModel):
    datetimes: list[datetime]
    elevations: list[float]  # km
    values: list[list[float]]


class LidarData(BaseModel):
    far_parallel: TimeHeightData
    depolarization: TimeHeightData


class UploadRequest(BaseModel):
    site: str
    instrument: str
    year: int
    month: int
    directory: str
    format: str


# Here are the new ones


class RICHBASE(BaseModel):
    units: str
    name: str
    scale: float
    flag: float


class PhysicalVector(RICHBASE):
    values: tuple[float, ...]


class TemporalVector(RICHBASE):
    initial: datetime
    offsets: tuple[float, ...]
    # Make sure that the units are in a subset of what we want


class PhysicalMatrix(RICHBASE):
    values: tuple[tuple[float, ...], ...]


class InstrumentData(BaseModel):
    time: TemporalVector
    axis: tuple[PhysicalVector, ...]
    matrices: tuple[PhysicalMatrix, ...]
    vectors: tuple[PhysicalVector, ...]
    name: str
    observatory: str
    notes: str
