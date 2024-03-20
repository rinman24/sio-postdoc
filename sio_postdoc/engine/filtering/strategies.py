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

ContentType = Union[str, bool, InstrumentData]
Content = tuple[ContentType, ...]
Mask = tuple[bool, ...]

Matrix = list[list[float]]
Vector = list[float]


FLAG: int = -999


class AbstractDateStrategy(ABC):
    @abstractmethod
    def apply(self, target: date, content: Content) -> Content: ...


class NamesByDate(AbstractDateStrategy):

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
                results.append(entry)
                break
            else:
                previous_entry = entry
        return tuple(sorted(results))


class IndicesByDate(AbstractDateStrategy):

    def apply(
        self, target: date, content: tuple[InstrumentData, ...]
    ) -> InstrumentData:
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
                    for matrix in data.matrices:
                        data_2d[matrix.name].append(matrix.values[i])
                    for vector in data.vectors:
                        data_1d[vector.name].append(vector.values[i])
        # Convert to corresponding contracts
        matrices: list[PhysicalMatrix] = []
        vectors: list[PhysicalVector] = []
        for matrix in prototype.matrices:
            item: PhysicalMatrix = PhysicalMatrix(
                values=tuple(data_2d[matrix.name]),
                units=matrix.units,
                name=matrix.name,
                scale=matrix.scale,
                flag=matrix.flag,
            )
            matrices.append(item)
        for vector in prototype.vectors:
            item: PhysicalVector = PhysicalVector(
                values=tuple(data_1d[vector.name]),
                units=vector.units,
                name=vector.name,
                scale=vector.scale,
                flag=vector.flag,
            )
            vectors.append(item)
        time: TemporalVector = TemporalVector(
            initial=datetime.combine(target, time()),
            offsets=offsets,
            units=prototype.time.units,
            name=prototype.time.name,
            scale=prototype.time.scale,
            flag=prototype.time.flag,
        )
        # Construct the result
        result: InstrumentData = InstrumentData(
            time=time,
            axis=prototype.axis,
            matrices=matrices,
            vectors=vectors,
            name=prototype.name,
            observatory=prototype.observatory,
            notes=prototype.notes,
        )
        return result
