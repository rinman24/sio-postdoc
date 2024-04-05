"""TODO: Docstring."""

from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import date, datetime, time, timedelta
from typing import Union

import sio_postdoc.utility.service as utility
from sio_postdoc.access.instrument.contracts import (
    InstrumentData,
    PhysicalMatrix,
    PhysicalVector,
    TemporalVector,
)
from sio_postdoc.access.instrument.constants import REFERENCE_TIME

ContentType = Union[str, bool, InstrumentData]
Content = tuple[ContentType, ...]
Mask = tuple[bool, ...]

Matrix = list[list[float]]
Vector = list[float]


FLAG: int = -999


class AbstractDateStrategy(ABC):
    """TODO: Docstring."""

    @abstractmethod
    def apply(  # pylint: disable=missing-function-docstring
        self,
        target: date,
        content: Content,
    ) -> Content: ...


class NamesByDate(AbstractDateStrategy):
    """TODO: Docstring."""

    def apply(self, target: date, content: Content) -> Content:
        """TODO: Implement."""
        results: list[str] = []
        start: datetime = datetime(
            year=target.year,
            month=target.month,
            day=target.day,
            hour=0,
            minute=0,
            second=0,
        )
        end: datetime = start + timedelta(days=1)
        previous_entry: str = ""
        for entry in content:
            current: datetime = utility.extract_datetime(entry)
            if current == start:
                results.append(entry)
            elif start < current < end:
                if not results and previous_entry:
                    results.append(previous_entry)
                results.append(entry)
            elif current == end:
                break
            elif current > end:
                if results:
                    results.append(entry)
                break
            else:
                previous_entry = entry
        return tuple(sorted(results))


class IndicesByDate(AbstractDateStrategy):
    """TODO: Docstring."""

    def apply(
        self, target: date, content: tuple[InstrumentData, ...]
    ) -> InstrumentData:
        # TODO: Too many local variables. You need to break this up.
        masks: list[Mask] = []
        prototype: InstrumentData | None = None
        # Determine which times correspond with the target
        for item in content:
            reference: datetime = datetime(
                year=item.time.initial.year,
                month=item.time.initial.month,
                day=item.time.initial.day,
                hour=0,
                minute=0,
                second=0,
            )
            mask: list[bool] = []
            for offset in item.time.offsets:
                timestamp: datetime = reference + timedelta(seconds=offset)
                if prototype is None and reference.date() == target:
                    prototype = item
                mask.append(timestamp.date() == target)
            masks.append(tuple(mask))
        # Reconstruct a single filtered result
        offsets: list[float] = []
        data_2d: dict[str, list[Matrix]] = defaultdict(list)
        data_1d: dict[str, list[Vector]] = defaultdict(list)
        for data, mask in zip(content, masks):
            for i, item in enumerate(mask):
                if item:
                    offsets.append(data.time.offsets[i])
                    for matrix in data.matrices.values():
                        data_2d[matrix.name].append(matrix.values[i])
                    for vector in data.vectors.values():
                        data_1d[vector.name].append(vector.values[i])
        # Convert to corresponding contracts
        matrices: dict[str, PhysicalMatrix] = {}
        vectors: dict[str, PhysicalVector] = {}
        for matrix in prototype.matrices.values():
            item: PhysicalMatrix = PhysicalMatrix(
                values=tuple(data_2d[matrix.name]),
                units=matrix.units,
                name=matrix.name,
                scale=matrix.scale,
                flag=matrix.flag,
                dtype=matrix.dtype,
                long_name=matrix.long_name,
            )
            matrices[matrix.name] = item
        for vector in prototype.vectors.values():
            item: PhysicalVector = PhysicalVector(
                values=tuple(data_1d[vector.name]),
                units=vector.units,
                name=vector.name,
                scale=vector.scale,
                flag=vector.flag,
                dtype=vector.dtype,
                long_name=vector.long_name,
            )
            vectors[vector.name] = item
        initial: datetime = datetime.combine(target, time())
        time_: TemporalVector = TemporalVector(
            initial=initial,
            offsets=offsets,
            units=prototype.time.units,
            name=prototype.time.name,
            scale=prototype.time.scale,
            flag=prototype.time.flag,
            dtype=prototype.time.dtype,
            base_time=int((initial - REFERENCE_TIME).total_seconds()),
            long_name=prototype.time.long_name,
        )
        # Construct the result
        result: InstrumentData = InstrumentData(
            time=time_,
            axis=prototype.axis,
            matrices=matrices,
            vectors=vectors,
            name=prototype.name,
            observatory=prototype.observatory,
            notes=prototype.notes,
        )
        return result
