"""Define strategy to extract raw Utqiagvik KAZR data."""

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


class Arscl1Cloth(TransformationStrategy):
    """Engine logic for raw Utqiagvik KAZR data.

    NOTE: The private methods are shared across these classes.
    NOTE: The private methods should be moved to TransformationStrategy (base)

    """

    def _add_dimensions(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_dimensions`."""
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
        self._add_epoch(dataset)
        self._add_mean_dopp_vel(dataset)
        self._add_offset(dataset)
        self._add_range(dataset)
        self._add_refl(dataset)
        self._add_spec_width(dataset)

    def _add_epoch(self, dataset: DataSet) -> None:
        # Change this to base: it should not be epoch
        self._variables["epoch"] = Variable(
            dtype=DType.I4,
            long_name="Unix Epoch 1970 of Initial Timestamp",
            scale=Scales.ONE,
            units=Units.SECONDS,
            dimensions=(),
            values=int(dataset["epoch"][0].data),
        )

    def _add_mean_dopp_vel(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="mean_dopp_vel",
            name="mean_dopp_vel",
            long_name="Mean Doppler Velocity",
            units=Units.METERS_PER_SECOND,
            scale=Scales.THOUSAND,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
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
            flag=DType.U2.min,
            dimensions=(self._dimensions["level"],),
        )
        self._add_single_variable(dataset, value_request)

    def _add_refl(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="refl",
            name="refl",
            long_name="Reflectivity",
            units=Units.DBZ,
            scale=Scales.HUNDRED,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_spec_width(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="spec_width",
            name="spec_width",
            long_name="Spectral Width",
            units=Units.METERS_PER_SECOND,
            scale=Scales.THOUSAND,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)


class ArsclKazr1Kollias(TransformationStrategy):
    """Engine logic for raw Utqiagvik KAZR data."""

    def _add_dimensions(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_dimensions`."""
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
        self._add_epoch(path)
        self._add_mean_dopp_vel(dataset)
        self._add_offset(dataset)
        self._add_range(dataset)
        self._add_refl(dataset)
        self._add_spec_width(dataset)

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

    def _add_mean_dopp_vel(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="mean_dopp_vel",
            name="mean_dopp_vel",
            long_name="Mean Doppler Velocity",
            units=Units.METERS_PER_SECOND,
            scale=Scales.THOUSAND,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
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
            flag=DType.U2.min,
            dimensions=(self._dimensions["level"],),
        )
        self._add_single_variable(dataset, value_request)

    def _add_refl(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="refl",
            name="refl",
            long_name="Reflectivity",
            units=Units.DBZ,
            scale=Scales.HUNDRED,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_spec_width(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="spec_width",
            name="spec_width",
            long_name="Spectral Width",
            units=Units.METERS_PER_SECOND,
            scale=Scales.THOUSAND,
            dtype=DType.I2,
            flag=DType.I2.min,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)


class ArsclKazr1KolliasMwr(TransformationStrategy):
    """Engine logic for liquid water path from the ArsclKazr1Kollias product."""

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
        self._add_mwr_lwp(dataset)

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
