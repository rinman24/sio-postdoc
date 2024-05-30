"""Define strategy to extract raw Utqiagvik MPLCMASKML data."""

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

NINES: int = -9999


class MplCmaskMlRaw(TransformationStrategy):
    """Engine logic for raw Utqiagvik KAZR data."""

    def _add_dimensions(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_dimensions`."""
        self._dimensions["time"] = Dimension(
            name=Dimensions.TIME,
            size=dataset.dimensions["time"].size,
        )
        self._dimensions["level"] = Dimension(
            name=Dimensions.LEVEL,
            size=dataset.dimensions["height"].size,
        )

    def _add_variables(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_variables`."""
        self._add_epoch(path)
        self._add_offset(dataset)
        self._add_range(dataset)
        self._add_cloud_mask(dataset)
        self._add_linear_depolarization_ratio(dataset)

    def _add_epoch(self, path: Path) -> None:
        # Change this to base: it should not be epoch
        extracted: DateTime = utility.extract_datetime(path.name)
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

    def _add_offset(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="time",
            name="offset",
            long_name="Seconds Since Initial Timestamp",
            units=Units.SECONDS,
            scale=Scales.ONE,
            dtype=DType.I4,
            flag=NINES,
            dimensions=(self._dimensions["time"],),
        )
        self._add_single_variable(dataset, value_request)

    def _add_range(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="height",
            name="range",
            long_name="Return Range",
            units=Units.METERS,
            scale=Scales.ONE,
            conversion_scale=Scales.THOUSAND,
            dtype=DType.U2,
            flag=NINES,
            dimensions=(self._dimensions["level"],),
        )
        self._add_single_variable(dataset, value_request)

    def _add_cloud_mask(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="cloud_mask",
            name="lidar_mask",
            long_name="Lidar Mask",
            units=Units.NONE,
            scale=Scales.ONE,
            dtype=DType.I1,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_linear_depolarization_ratio(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="linear_depol_ratio",
            name="depol",
            long_name="Linear Depolarization Ratio",
            units=Units.NONE,
            scale=Scales.THOUSAND,
            conversion_scale=Scales.THOUSAND,
            dtype=DType.I2,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)
