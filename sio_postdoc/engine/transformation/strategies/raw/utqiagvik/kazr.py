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


class UtqiagvikKazrRaw(TransformationStrategy):
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
        self._dimensions["layer"] = Dimension(
            name=Dimensions.LAYER,
            size=dataset.dimensions["layer"].size,
        )

    def _add_variables(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_variables`."""
        self._add_epoch(path)
        # self._add_mean_dopp_vel(dataset)
        self._add_offset(dataset)
        self._add_range(dataset)
        # self._add_refl(dataset)
        # self._add_spec_width(dataset)
        # self._add_snr(dataset)
        # self._add_cloud_source_flag(dataset)
        # self._add_precip_mean(dataset)
        self._add_cloud_layer_base_height(dataset)
        self._add_cloud_layer_top_height(dataset)
        # self._add_mwr_lwp(dataset)
        # self._add_cloud_mask_mplzwang(dataset)

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

    def _add_cloud_source_flag(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="cloud_source_flag",
            name="cloud_source_flag",
            long_name="Cloud Source Flag",
            # 0 'No detection due to missing radar and micropulse lidar data'
            # 1 'Clear according to radar and lidar'
            # 2 'Cloud detected by radar and lidar'
            # 3 'Cloud detected by radar only'
            # 4 'Cloud detected by lidar only'
            # 5 'Cloud detected by radar but lidar data missing'
            # 6 'Cloud detected by lidar but radar data missing'
            units=Units.NONE,
            scale=Scales.ONE,
            dtype=DType.U1,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_cloud_layer_base_height(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="cloud_layer_base_height",
            name="cloud_layer_base_height",
            long_name="Cloud Layer Base Height",
            units=Units.METERS,
            scale=Scales.ONE,
            dtype=DType.U4,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["layer"]),
        )
        self._add_single_variable(dataset, value_request)
    
    def _add_cloud_layer_top_height(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="cloud_layer_top_height",
            name="cloud_layer_top_height",
            long_name="Cloud Layer Top Height",
            units=Units.METERS,
            scale=Scales.ONE,
            dtype=DType.U4,
            flag=NINES,
            dimensions=(self._dimensions["time"], self._dimensions["layer"]),
        )
        self._add_single_variable(dataset, value_request)


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
