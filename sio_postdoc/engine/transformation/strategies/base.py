"""Define the Abstract Base Class of Transformation Strategies."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator

import numpy as np

from sio_postdoc.access import DataSet
from sio_postdoc.engine import Units
from sio_postdoc.engine.transformation.contracts import (
    Dimension,
    InstrumentData,
    Variable,
    VariableRequest,
)

ONE_EIGHTY: int = 180
SECONDS_PER_DAY: int = 86400
THREE_SIXTY: int = 360
NINES: int = -999


class TransformationStrategy(ABC):
    """Encapsulate the base transformation class."""

    def __init__(self) -> None:
        """Initialize `TransformationStrategy` parameters."""
        self._dimensions: dict[str, Dimension] = {}
        self._variables: dict[str, Variable] = {}

    @abstractmethod
    def _add_dimensions(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_dimensions`."""

    @abstractmethod
    def _add_variables(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_variables`."""

    def hydrate(self, dataset: DataSet, path: Path) -> InstrumentData:
        """Use a `DataSet` to hydrate `InstrumentData`."""
        self._add_dimensions(dataset, path)
        self._add_variables(dataset, path)
        return InstrumentData(
            dimensions=self._dimensions,
            variables=self._variables,
        )

    def _add_single_variable(self, dataset: DataSet, req: VariableRequest) -> None:
        self._variables[req.name] = Variable(
            dtype=req.dtype,
            long_name=req.long_name,
            scale=req.scale,
            units=req.units,
            dimensions=req.dimensions,
            values=self._extract_values(dataset, req),
        )

    def _extract_values(self, dataset: DataSet, req: VariableRequest) -> None:
        """Extract the data from a `DataSet`."""
        data: np.ndarray = dataset[req.variable][:].data
        if req.units == Units.DEGREES:
            return tuple(map(self._get_deg_min_sec, data))
        elif req.units == Units.SECONDS:
            seconds: list[int] = list(self._generate_values(data, req))
            return self._monotonic_times(seconds)
        return tuple(self._generate_values(data, req))

    def _generate_values(
        self, data: np.ndarray, req: VariableRequest
    ) -> Generator[int, None, None]:
        dimensions: int = len(data.shape)
        if dimensions == 1:
            for i in data:
                yield self._convert_with_rails(i, req)
        else:  # dimensions == 2
            for row in data:
                yield tuple(self._convert_with_rails(i, req) for i in row)

    @staticmethod
    def _get_deg_min_sec(angle: float) -> tuple[int, int, int]:
        """Convert decimal degrees into degrees, minutes, and seconds.

        NOTE: This always returns a positve angle and InstrumentData.

        Angles in `InstrumentData` must always be accompanied by a sign variable.

        Angles will not have absolute value greater than 180
        Therefore, an angle of 190 is represented as -170
        """
        # Remove full rotations
        angle = angle % 360
        # Map angles greater than 180 to negative angles
        if angle > ONE_EIGHTY:
            angle = angle - THREE_SIXTY
        # Get the sign
        sign: int = 1 if 0 <= angle else -1
        # Now use absolute value
        angle = abs(angle)
        # Derive minutes and seconds
        minutes, seconds = divmod(angle * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        return (sign, int(degrees), int(minutes), round(seconds))

    @staticmethod
    def _convert_with_rails(element: float, req: VariableRequest) -> tuple[int, ...]:
        if element == req.flag:
            return req.dtype.min
        else:
            value: float = element * req.conversion_scale.value
            too_small: bool = value < req.dtype.min
            too_large: bool = req.dtype.max < value
            is_nan: bool = np.isnan(value)
            if too_small or too_large or is_nan:
                return req.dtype.min
        return round(value)

    @staticmethod
    def _monotonic_times(seconds: list[float]) -> tuple[int, ...]:
        previous: float = float(NINES)  # Large negative number
        datum: int = 0  # Initially on same day
        monotonic_seconds: list[float] = []
        for item in seconds:
            if item < previous:
                datum += SECONDS_PER_DAY
            monotonic_seconds.append(int(datum + item))
            previous = item
        return tuple(monotonic_seconds)
