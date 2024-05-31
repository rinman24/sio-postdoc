"""TODO: Docstring."""

from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone

import sio_postdoc.utility.service as utility
from sio_postdoc.engine import Dimensions, Units
from sio_postdoc.engine.filtering import Content, Mask
from sio_postdoc.engine.transformation.contracts import (
    DateTime,
    Dimension,
    InstrumentData,
    Values,
    Variable,
)


class AbstractDateStrategy(ABC):
    """TODO: Docstring."""

    @staticmethod
    @abstractmethod
    def apply(target: date, content: Content) -> Content: ...


class NamesByDate(AbstractDateStrategy):
    """TODO: Docstring."""

    @staticmethod
    def apply(target: date, content: Content, time: bool = True) -> Content:
        """TODO: Implement."""
        results: list[str] = []
        start: datetime = DateTime(
            year=target.year,
            month=target.month,
            day=target.day,
            hour=0,
            minute=0,
            second=0,
        ).datetime
        end: datetime = start + timedelta(days=1)
        previous_entry: str = ""
        for entry in content:
            current: datetime = utility.extract_datetime(entry, time=time).datetime
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

    @staticmethod
    def _get_variables(
        masks: list[tuple[bool, ...]], content: tuple[InstrumentData, ...]
    ) -> dict[str, Values]:
        var_values: dict[str, Values] = defaultdict(list)
        # Variables not indexed by time
        for mask, data in zip(masks, content):
            if not any(mask):
                continue
            for name, var in data.variables.items():
                if not var.dimensions:
                    var_values[name] = var.values
                elif var.dimensions[0].name != Dimensions.TIME:
                    var_values[name] = var.values
            break  # stop going through the masks and data
        # Variables indexed by time
        for mask, data in zip(masks, content):
            if not any(mask):
                continue
            for name, var in data.variables.items():
                # You're really just checking the the length is less than 2 and
                if not var.dimensions:
                    continue
                if var.dimensions[0].name != Dimensions.TIME:
                    continue
                if var.units == Units.SECONDS:
                    initial: datetime = datetime.fromtimestamp(
                        data.variables["epoch"].values
                    )
                    var_values[name] += tuple(
                        int(
                            (initial + timedelta(seconds=offset)).timestamp()
                            - var_values["epoch"]
                        )
                        for flag, offset in zip(mask, var.values)
                        if flag
                    )
                    continue
                var_values[name] += list(
                    value for flag, value in zip(mask, var.values) if flag
                )
        return var_values

    @staticmethod
    def _get_unique_dimensions(
        data: InstrumentData, var_values: dict[str, Variable]
    ) -> dict[str, Dimension]:
        data_dims: dict[str, Dimension] = {}
        for required in data.dimensions.keys():
            match required:
                case "time":
                    name = Dimensions.TIME
                    size = len(var_values["offset"])
                case "level":
                    name = Dimensions.LEVEL
                    size = len(var_values["range"])
                case "layer":
                    name = Dimensions.LAYER
                    size = 10
                case "angle":
                    name = Dimensions.ANGLE
                    size = 4
                case _:
                    continue
            data_dims[required] = Dimension(name=name, size=size)
        return data_dims

    @staticmethod
    def _get_dimensions(
        data: InstrumentData, data_dims: dict[str, Dimension]
    ) -> dict[str, Dimension]:
        var_dims: dict[str, tuple[Dimension, ...]] = {}
        for key, value in data.variables.items():
            current_dimensions: list[Dimension] = []
            for dimension in value.dimensions:
                match dimension.name:
                    case Dimensions.TIME:
                        name: str = "time"
                    case Dimensions.LAYER:
                        name: str = "layer"
                    case Dimensions.LEVEL:
                        name: str = "level"
                    case Dimensions.ANGLE:
                        name: str = "angle"
                    case _:
                        continue
                current_dimensions.append(data_dims[name])
            var_dims[key] = tuple(current_dimensions)
        return var_dims

    def apply(
        self, target: date, content: tuple[InstrumentData, ...]
    ) -> InstrumentData:
        """Apply the filtering strategy."""
        # Get the masks
        data = content[0]
        masks: list[tuple[int, ...]] = self._get_masks(target, content)
        # If the masks are all false, then return None
        if not any(any(m) for m in masks):
            return None
        var_values: dict[str, Values] = self._get_variables(masks, content)
        data_dims: dict[str, Dimension] = self._get_unique_dimensions(data, var_values)
        var_dims: dict[str, tuple[Dimension, ...]] = self._get_dimensions(
            data,
            data_dims,
        )
        variables: dict[str, Variable] = {
            key: Variable(
                dimensions=var_dims[key],
                dtype=value.dtype,
                long_name=value.long_name,
                scale=value.scale,
                units=value.units,
                values=var_values[key],
            )
            for key, value in data.variables.items()
        }
        new_data: InstrumentData = InstrumentData(
            dimensions=data_dims,
            variables=variables,
        )
        return new_data

    @staticmethod
    def _get_masks(
        target: date, content: tuple[InstrumentData, ...]
    ) -> tuple[tuple[int, ...], ...]:
        masks: list[Mask] = []
        epoch: datetime = datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc)
        for data in content:
            initial: datetime = epoch + timedelta(
                seconds=data.variables["epoch"].values
            )
            masks.append(
                tuple(
                    (
                        True
                        if (initial + timedelta(seconds=offset)).date() == target
                        else False
                    )
                    for offset in data.variables["offset"].values
                )
            )
        return tuple(masks)
