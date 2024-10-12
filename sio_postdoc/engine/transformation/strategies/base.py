"""Define the Abstract Base Class of Transformation Strategies."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator

import numpy as np

import sio_postdoc.utility.service as utility
from sio_postdoc.access import DataSet
from sio_postdoc.engine import Scales, Units
from sio_postdoc.engine.transformation.contracts import (
    DateTime,
    Dimension,
    DType,
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
            if data.size == 1:
                return self._get_deg_min_sec(float(data))
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

    def _add_epoch(self, path: Path) -> None:
        # Change this to base: it should not be epoch
        extracted: DateTime = utility.extract_datetime(path.name, time=False)
        value: int = DateTime(
            year=extracted.year,
            month=extracted.month,
            day=extracted.day,
            hour=0,
            minute=0,
            second=0,
        ).unix
        self._variables["epoch"] = Variable(
            dtype=DType.I4,
            long_name="Unix Epoch 1970 of Initial Timestamp",
            units=Units.SECONDS,
            dimensions=(),
            values=value,
        )

    def _add_offset(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="offset",
            name="offset",
            long_name="Seconds Since Initial Timestamp",
            units=Units.SECONDS,
            dtype=DType.I4,
            flag=DType.I4.min,
            dimensions=(self._dimensions["time"],),
        )
        self._add_single_variable(dataset, value_request)

    def _add_range(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="range",
            name="range",
            long_name="Return Range",
            units=Units.METERS,
            dtype=DType.U2,
            flag=DType.U2.min,
            dimensions=(self._dimensions["level"],),
        )
        self._add_single_variable(dataset, value_request)

    def _add_lidar_mask(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="lidar_mask",
            name="lidar_mask",
            long_name="Lidar Mask",
            units=Units.NONE,
            dtype=DType.I1,
            flag=DType.I1.min,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_linear_depolarization_ratio(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="depol",
            name="depol",
            long_name="Linear Depolarization Ratio",
            units=Units.NONE,
            scale=Scales.THOUSAND,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_mwr_lwp(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="mwr_lwp",
            name="mwr_lwp",
            long_name="Liquid Water Path",
            units=Units.GRAMS_PER_METER_SQUARE,
            scale=Scales.TEN,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"],),
        )
        self._add_single_variable(dataset, value_request)

    def _add_dlr(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="dlr",
            name="dlr",
            long_name="Downwelling Longwave Radiation Hemispherical",
            units=Units.WATTS_PER_METER_SQUARE,
            scale=Scales.TEN,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"],),
        )
        self._add_single_variable(dataset, value_request)

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
    def _convert_with_rails(element: float, req: VariableRequest) -> int:
        if element == req.flag:
            return req.dtype.min
        else:
            offset: float = req.offset * req.conversion_scale.value
            value: float = offset + (element * req.conversion_scale.value)
            too_small: bool = value <= req.dtype.min
            too_large: bool = req.dtype.max < value
            is_nan: bool = np.isnan(value)
            if any([too_small, too_large, is_nan]):
                return req.dtype.min
            if req.binary:
                midpoint: float = sum(req.binary) / 2
                if (value < req.binary[0]) | (req.binary[1] < value):
                    return req.dtype.min
                elif req.binary[0] <= value < midpoint:
                    return int(req.binary[0])
                elif midpoint <= value <= req.binary[1]:
                    return int(req.binary[1])
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
