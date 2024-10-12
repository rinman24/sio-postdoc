"""Define strategy to extract raw Utqiagvik MPLCMASKML data."""

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

import sio_postdoc.utility.service as utility
from sio_postdoc.access import DataSet
from sio_postdoc.engine import Dimensions, Scales, Units
from sio_postdoc.engine.transformation.contracts import (
    EPOCH,
    DateTime,
    Dimension,
    DType,
    Variable,
    VariableRequest,
)
from sio_postdoc.engine.transformation.strategies.base import TransformationStrategy

NINES: int = -9999


class MwrLosRaw(TransformationStrategy):
    """Engine logic for raw Utqiagvik KAZR data."""

    def _add_dimensions(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_dimensions`."""
        self._dimensions["time"] = Dimension(
            name=Dimensions.TIME,
            size=dataset.dimensions["time"].size,
        )

    def _add_variables(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_variables`."""
        self._add_epoch(path)
        self._add_offset(dataset)
        self._add_lwp(dataset)

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

    def _add_lwp(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="liq",
            name="mwr_lwp",
            long_name="Liquid Water Path",
            units=Units.GRAMS_PER_METER_SQUARE,
            scale=Scales.TEN,
            conversion_scale=Scales.CM_TO_GM2_X10,
            dtype=DType.I2,
            flag=NINES,
            dimensions=(self._dimensions["time"],),
        )
        self._add_single_variable(dataset, value_request)


class MwrLosRawEureka(TransformationStrategy):
    """Engine logic for raw Utqiagvik KAZR data."""

    def _add_dimensions(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_dimensions`."""
        self._dimensions["time"] = Dimension(
            name=Dimensions.TIME,
            size=dataset.dimensions["time"].size,
        )

    def _add_variables(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_variables`."""
        self._add_epoch(dataset)
        self._add_offset(dataset, path)
        self._add_lwp(dataset)

    def _add_epoch(self, dataset: DataSet) -> None:
        # Change this to base: it should not be epoch
        value = int(dataset["base_time"][:].data)
        self._variables["epoch"] = Variable(
            dtype=DType.I4,
            long_name="Unix Epoch 1970 of Initial Timestamp",
            scale=Scales.ONE,
            units=Units.SECONDS,
            dimensions=(),
            values=value,
        )

    def _add_offset(self, dataset: DataSet, path: Path) -> None:
        extracted: datetime = utility.extract_datetime(path.name).datetime
        base_time = EPOCH + timedelta(seconds=self._variables["epoch"].values)
        offset = (base_time - extracted).seconds
        value_request: VariableRequest = VariableRequest(
            variable="time_offset",
            name="offset",
            long_name="Seconds Since Initial Timestamp",
            units=Units.SECONDS,
            scale=Scales.ONE,
            dtype=DType.I4,
            flag=NINES,
            offset=offset,
            dimensions=(self._dimensions["time"],),
        )
        self._add_single_variable(dataset, value_request)

    def _add_lwp(self, dataset: DataSet) -> None:
        values: pd.Series = pd.Series(dataset["liquid"][:].data)
        # values = values * Scales.CM_TO_GM2.value
        values = values * 10
        # values[values < 0] = DType.I2.min
        self._variables["mwr_lwp"] = Variable(
            dtype=DType.I2,
            long_name="Liquid Water Path",
            scale=Scales.TEN,
            units=Units.GRAMS_PER_METER_SQUARE,
            dimensions=(self._dimensions["time"],),
            values=tuple(values.map(int).values),
        )
