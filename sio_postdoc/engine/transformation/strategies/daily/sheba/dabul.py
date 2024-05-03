"""Define strategy to extract raw SHEBA DABUL data."""

from pathlib import Path

import sio_postdoc.utility.service as utility
from sio_postdoc.access import DataSet
from sio_postdoc.engine import Dimensions, Scales, Units
from sio_postdoc.engine.transformation.contracts import (
    DateTime,
    Dimension,
    DType,
    Variable,
    VariableRequest,
)
from sio_postdoc.engine.transformation.strategies.base import TransformationStrategy

NINES: int = -999


class ShebaDabulDaily(TransformationStrategy):
    """Engine logic for daily SHEBA DABUL data."""

    def _add_dimensions(self, dataset: DataSet, path: Path) -> None:
        """Use a `InstrumentData` to set the state of `_dimensions`."""
        self._dimensions["time"] = Dimension(
            name=Dimensions.TIME,
            size=dataset.dimensions["time"].size,
        )
        self._dimensions["level"] = Dimension(
            name=Dimensions.LEVEL,
            size=dataset.dimensions["level"].size,
        )

    def _add_variables(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_variables`."""
        self._add_depol(dataset)
        self._add_epoch(path)
        self._add_far_par(dataset)
        self._add_offset(dataset)
        self._add_range(dataset)

    def _add_azimuth(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="azimuth",
            name="azimuth",
            long_name="Beam Azimuth Angle",
            units=Units.DEGREES,
            scale=Scales.ONE,
            dtype=DType.U1,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["angle"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_depol(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="depol",
            name="depol",
            long_name="Depolarization Ratio",
            units=Units.NONE,
            scale=Scales.THOUSAND,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

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
            scale=Scales.ONE,
            units=Units.SECONDS,
            dimensions=(),
            values=value,
        )

    def _add_far_par(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="far_par",
            name="far_par",
            long_name="Lidar Returned Power",
            units=Units.UNSPECIFIED,
            scale=Scales.HUNDRED,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_latitude(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="latitude",
            name="latitude",
            long_name="Platform Latitude [North]",
            units=Units.DEGREES,
            scale=Scales.ONE,
            dtype=DType.U1,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["angle"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_longitude(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="longitude",
            name="longitude",
            long_name="Platform Longitude [East]",
            units=Units.DEGREES,
            scale=Scales.ONE,
            dtype=DType.U1,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["angle"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_offset(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="offset",
            name="offset",
            long_name="Seconds Since Initial Timestamp",
            units=Units.SECONDS,
            scale=Scales.ONE,
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
            scale=Scales.ONE,
            dtype=DType.U2,
            flag=NINES,
            dimensions=(self._dimensions["level"],),
        )
        self._add_single_variable(dataset, value_request)
