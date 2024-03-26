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

    def __repr__(self) -> str:
        repr_: str = ""
        repr_ += "<class 'sio_postdoc.access.instrument.contracts.PhysicalVector'>\n"
        repr_ += f"    dimensions(sizes): ({len(self.values)},)\n"
        repr_ += f"    units: {self.units}\n"
        repr_ += f"    name: {self.name}\n"
        return repr_


class TemporalVector(Data):
    """
    Container for one-dimensional temporal data.

    NOTE: `offsets` should always be in seconds.
    """

    initial: datetime
    offsets: tuple[float, ...]

    def __repr__(self) -> str:
        repr_: str = ""
        repr_ += "<class 'sio_postdoc.access.instrument.contracts.TemporalVector'>\n"
        repr_ += f"    dimensions(sizes): ({len(self.offsets)},)\n"
        repr_ += f"    units: {self.units}\n"
        repr_ += f"    name: {self.name}\n"
        repr_ += f"    initial time: {self.initial}\n"
        return repr_


class PhysicalMatrix(Data):
    """Container for two-dimensional data."""

    values: tuple[tuple[float, ...], ...]

    def __repr__(self) -> str:
        repr_: str = ""
        repr_ += "<class 'sio_postdoc.access.instrument.contracts.PhysicalMatrix'>\n"
        repr_ += f"    dimensions(sizes): ({len(self.values)}, {len(self.values[0])})\n"
        repr_ += f"    units: {self.units}\n"
        repr_ += f"    name: {self.name}\n"
        return repr_


class InstrumentData(BaseModel):
    """Container for data from an instrument."""

    time: TemporalVector
    axis: tuple[PhysicalVector, ...]
    matrices: tuple[PhysicalMatrix, ...]
    vectors: tuple[PhysicalVector, ...]
    name: str
    observatory: str
    notes: str

    def __repr__(self) -> str:
        first: bool

        repr_: str = ""
        repr_ += "<class 'sio_postdoc.access.instrument.contracts.InstrumentData'>\n"
        repr_ += f"    instrument name: {self.name}\n"
        repr_ += f"    observatory name: {self.observatory}\n"
        repr_ += f"    notes: {self.notes}\n"
        repr_ += f"    initial time: {self.time.initial}\n"
        repr_ += f"    dimensions(sizes): time({len(self.time.offsets)})"
        for dimension in self.axis:
            repr_ += f", {dimension.name}({len(dimension.values)})"
        if self.vectors:
            repr_ += "\n    vectors(dimensions): "
        first = True
        for vector in self.vectors:
            if not first:
                repr_ += ", "
            repr_ += f"{vector.name}(time)"
            first = False
        if self.matrices:
            repr_ += "\n    matrices(dimensions): "
        first = True
        for matrix in self.matrices:
            if not first:
                repr_ += ", "
            repr_ += f"{matrix.name}(time, {self.axis[0].name})"
            first = False

        return repr_
