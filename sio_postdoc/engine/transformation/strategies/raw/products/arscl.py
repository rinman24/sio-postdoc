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


class ArsclKazr1KolliasRaw(TransformationStrategy):
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
        self._add_mean_dopp_vel(dataset)
        self._add_offset(dataset)
        self._add_range(dataset)
        self._add_refl(dataset)
        self._add_spec_width(dataset)
        self._add_mwr_lwp(dataset)
        self._add_cloud_mask_mplzwang(dataset)

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

    def _add_mean_dopp_vel(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="mean_doppler_velocity",
            name="mean_dopp_vel",
            long_name="Mean Doppler Velocity",
            units=Units.METERS_PER_SECOND,
            scale=Scales.THOUSAND,
            dtype=DType.I2,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

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
            dtype=DType.U2,
            flag=NINES,
            dimensions=(self._dimensions["level"],),
        )
        self._add_single_variable(dataset, value_request)

    def _add_refl(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="reflectivity",
            name="refl",
            long_name="Reflectivity",
            units=Units.DBZ,
            scale=Scales.HUNDRED,
            dtype=DType.I2,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_spec_width(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="spectral_width",
            name="spec_width",
            long_name="Spectral Width",
            units=Units.METERS_PER_SECOND,
            scale=Scales.THOUSAND,
            dtype=DType.I2,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_mwr_lwp(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="mwr_lwp",
            name="mwr_lwp",
            long_name="Liquid Water Path",
            units=Units.GRAMS_PER_METER_SQUARE,
            scale=Scales.ONE,
            dtype=DType.I2,
            flag=NINES,
            dimensions=(self._dimensions["time"],),
        )
        self._add_single_variable(dataset, value_request)

    def _add_cloud_mask_mplzwang(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="cloud_mask_mplzwang",
            name="radar_mask",
            long_name="Radar Mask",
            units=Units.NONE,
            scale=Scales.ONE,
            dtype=DType.I1,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)
