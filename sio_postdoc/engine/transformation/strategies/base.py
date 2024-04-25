"""Define the Abstract Base Class of Transformation Strategies."""

from abc import ABC, abstractmethod
from pathlib import Path

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
SECONDS_PER_HOUR: int = 3600
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

    @staticmethod
    def get_deg_min_sec(angle: float) -> tuple[int, int, int]:
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

    def extract_values(self, dataset: DataSet, req: VariableRequest) -> None:
        """Extract the data from a `DataSet`."""
        data: np.ndarray = dataset[req.variable][:].data
        dimensions: int = len(data.shape)
        if req.units == Units.DEGREES:
            return tuple(map(self.get_deg_min_sec, data))
        if dimensions == 1:
            return tuple(
                (
                    req.dtype.min
                    if i == req.flag
                    else round(i * req.conversion_scale.value)
                )
                for i in data
            )
        else:  # dimensions == 2
            return tuple(
                tuple(
                    (
                        req.dtype.min
                        if i == req.flag
                        else round(i * req.conversion_scale.value)
                    )
                    for i in row
                )
                for row in data
            )

    def monotonic_times(times: list[float], units: str) -> tuple[int, ...]:
        """TODO: Docstring."""
        # Convert to seconds (potentially non-monotonic)
        scale: int
        match units:
            case "hours":
                scale = 3600
            case "seconds":
                scale = 1
        seconds = [round(i * scale) for i in times]
        # Convert to monotonic seconds
        previous: float = float(-999)  # Large negative number
        datum: int = 0  # Initially on same day
        monotonic_seconds: list[float] = []
        for item in seconds:
            if item < previous:
                datum += SECONDS_PER_DAY
            monotonic_seconds.append(int(datum + item))
            previous = item
        return tuple(monotonic_seconds)

    def _add_single_variable(self, dataset: DataSet, req: VariableRequest) -> None:
        self._variables[req.name] = Variable(
            dtype=req.dtype,
            long_name=req.long_name,
            scale=req.scale,
            units=req.units,
            dimensions=req.dimensions,
            values=self.extract_values(dataset, req),
        )
