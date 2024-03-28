"""Instrument Access Contracts."""

from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel

from sio_postdoc.access.instrument.constants import REFERENCE_TIME


class Data(BaseModel):
    """Base data model for other contracts to extend."""

    units: str
    name: str
    long_name: str
    scale: int
    flag: int
    dtype: str


class PhysicalVector(Data):
    """Container for one-dimensional data."""

    values: tuple[int, ...]

    def __repr__(self) -> str:  # noqa: D105
        repr_: str = ""
        repr_ += "<class 'sio_postdoc.access.instrument.contracts.PhysicalVector'>\n"
        repr_ += f"    dimensions(sizes): ({len(self.values)},)\n"
        repr_ += f"    units: {self.units}\n"
        repr_ += f"    name: {self.name}\n"
        return repr_


class TemporalVector(Data):
    """I encapsulate temporal data.

    Parameters
    ----------
    base_time : int
        Seconds since 1970-01-01 00:00:00 00:00.
    offsets : tuple of int
        Seconds since `initial`.

    """

    base_time: int
    offsets: tuple[int, ...]

    def __repr__(self) -> str:  # noqa: D105
        repr_: str = ""
        repr_ += "<class 'sio_postdoc.access.instrument.contracts.TemporalVector'>\n"
        repr_ += f"    dimensions(sizes): ({len(self.offsets)},)\n"
        repr_ += f"    units: {self.units}\n"
        repr_ += f"    name: {self.name}\n"
        repr_ += f"    base_time: {self.base_time}\n"
        repr_ += f"    initial: {self.initial}"
        return repr_

    @property
    def initial(self) -> datetime:
        """Calculate the initial datetime."""
        return REFERENCE_TIME + timedelta(seconds=self.base_time)


class PhysicalMatrix(Data):
    """Container for two-dimensional data."""

    values: tuple[tuple[int, ...], ...]

    def __repr__(self) -> str:  # noqa: D105
        repr_: str = ""
        repr_ += "<class 'sio_postdoc.access.instrument.contracts.PhysicalMatrix'>\n"
        repr_ += f"    dimensions(sizes): ({len(self.values)}, {len(self.values[0])})\n"
        repr_ += f"    units: {self.units}\n"
        repr_ += f"    name: {self.name}\n"
        return repr_


class InstrumentData(BaseModel):
    """Container for data from an instrument."""

    time: TemporalVector
    axis: Optional[PhysicalVector]
    vectors: dict[str, PhysicalVector]
    matrices: dict[str, PhysicalMatrix]
    name: str
    observatory: str
    notes: str

    def __repr__(self) -> str:  # noqa: D105
        first: bool

        repr_: str = ""
        repr_ += "<class 'sio_postdoc.access.instrument.contracts.InstrumentData'>\n"
        repr_ += f"    instrument name: {self.name}\n"
        repr_ += f"    observatory name: {self.observatory}\n"
        repr_ += f"    notes: {self.notes}\n"
        repr_ += f"    initial time: {self.time.initial}\n"
        repr_ += f"    dimensions(sizes): time({len(self.time.offsets)})"
        if self.axis:
            repr_ += f", {self.axis.name}({len(self.axis.values)})"
        if self.vectors:
            repr_ += "\n    vectors(dimensions): "
        first = True
        for vector in self.vectors:
            if not first:
                repr_ += ", "
            repr_ += f"{vector}(time)"
            first = False
        if self.matrices:
            repr_ += "\n    matrices(dimensions): "
        first = True
        for matrix in self.matrices:
            if not first:
                repr_ += ", "
            repr_ += f"{matrix}(time, {self.axis.name})"
            first = False

        return repr_
