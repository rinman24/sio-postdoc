"""Define strategy to extract raw Utiqiagvik KAZR data."""

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


# NOTE: This looks exactly like the SHEBA MMCR Strategy, you probably just have an MMCR strategy.
# If this works without changes, then you do have an a single strategy.
# Why would you only have one, well that is the reason that you made the daily files to begin
# with, all you need is a daily file that already has the correct names, because you did it that way.
class UtqiagvikKazrDaily(TransformationStrategy):
    """Engine logic for daily Utqiagvik KAZR data."""

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
        extracted: DateTime = utility.extract_datetime(path.name, time=False)
        self._variables["epoch"] = Variable(
            dtype=DType.I4,
            long_name="Unix Epoch 1970 of Initial Timestamp",
            scale=Scales.ONE,
            units=Units.SECONDS,
            dimensions=(),
            values=extracted.unix,
        )

    # def _add_mean_dopp_vel(self, dataset: DataSet) -> None:
    #     value_request: VariableRequest = VariableRequest(
    #         variable="mean_dopp_vel",
    #         name="mean_dopp_vel",
    #         long_name="Mean Doppler Velocity",
    #         units=Units.METERS_PER_SECOND,
    #         scale=Scales.THOUSAND,
    #         dtype=DType.I2,
    #         flag=DType.I2.min,
    #         dimensions=(self._dimensions["time"], self._dimensions["level"]),
    #     )
    #     self._add_single_variable(dataset, value_request)

    def _add_offset(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="offset",
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

    # def _add_refl(self, dataset: DataSet) -> None:
    #     value_request: VariableRequest = VariableRequest(
    #         variable="refl",
    #         name="refl",
    #         long_name="Reflectivity",
    #         units=Units.DBZ,
    #         scale=Scales.HUNDRED,
    #         dtype=DType.I2,
    #         flag=DType.I2.min,
    #         dimensions=(self._dimensions["time"], self._dimensions["level"]),
    #     )
    #     self._add_single_variable(dataset, value_request)

    # def _add_spec_width(self, dataset: DataSet) -> None:
    #     value_request: VariableRequest = VariableRequest(
    #         variable="spec_width",
    #         name="spec_width",
    #         long_name="Spectral Width",
    #         units=Units.METERS_PER_SECOND,
    #         scale=Scales.THOUSAND,
    #         dtype=DType.I2,
    #         flag=DType.I2.min,
    #         dimensions=(self._dimensions["time"], self._dimensions["level"]),
    #     )
    #     self._add_single_variable(dataset, value_request)

    # def _add_cloud_source_flag(self, dataset: DataSet) -> None:
    #     value_request: VariableRequest = VariableRequest(
    #         variable="cloud_source_flag",
    #         name="cloud_source_flag",
    #         long_name="Cloud Source Flag",
    #         # 0 'No detection due to missing radar and micropulse lidar data'
    #         # 1 'Clear according to radar and lidar'
    #         # 2 'Cloud detected by radar and lidar'
    #         # 3 'Cloud detected by radar only'
    #         # 4 'Cloud detected by lidar only'
    #         # 5 'Cloud detected by radar but lidar data missing'
    #         # 6 'Cloud detected by lidar but radar data missing'
    #         units=Units.NONE,
    #         scale=Scales.ONE,
    #         dtype=DType.U1,
    #         flag=NINES,
    #         dimensions=(self._dimensions["time"], self._dimensions["level"]),
    #     )
    #     self._add_single_variable(dataset, value_request)

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
