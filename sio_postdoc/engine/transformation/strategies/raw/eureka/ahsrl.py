"""Define strategy to extract raw SHEBA DABUL data."""

from pathlib import Path

from numpy import nan

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

NAN: float = nan
NEG_ONE: int = -1
NINES: int = -999


class EurekaAhsrlRaw(TransformationStrategy):
    """Engine logic for raw SHEBA DABUL data."""

    def _add_dimensions(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_dimensions`."""
        self._dimensions["time"] = Dimension(
            name=Dimensions.TIME,
            size=dataset.dimensions["time"].size,
        )
        self._dimensions["level"] = Dimension(
            name=Dimensions.LEVEL,
            size=dataset.dimensions["altitude"].size,
        )
        # self._dimensions["angle"] = Dimension(
        #     name=Dimensions.ANGLE,
        #     size=4,
        # )

    def _add_variables(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_variables`."""
        self._add_counts_lo(dataset)
        self._add_counts_hi(dataset)
        self._add_cross_counts(dataset)
        self._add_depol(dataset)
        self._add_epoch(path)
        # self._add_latitude(dataset)
        # self._add_longitude(dataset)
        self._add_molecular_counts(dataset)
        self._add_offset(dataset)
        self._add_range(dataset)

    def _add_counts_lo(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="combined_counts_lo",
            name="counts_lo",
            long_name="Low Gain Combined Photon Counts",
            units=Units.NONE,
            scale=Scales.ONE,
            dtype=DType.I4,
            flag=NEG_ONE,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_counts_hi(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="combined_counts_hi",
            name="counts_hi",
            long_name="High Gain Combined Photon Counts",
            units=Units.NONE,
            scale=Scales.ONE,
            dtype=DType.I4,
            flag=NEG_ONE,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_cross_counts(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="cross_counts",
            name="cross_counts",
            long_name="Cross Polarized Photon Counts",
            units=Units.NONE,
            scale=Scales.ONE,
            dtype=DType.I4,
            flag=NEG_ONE,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_depol(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="depol",
            name="depol",
            long_name="Circular depolarization ratio for particulate",
            units=Units.NONE,
            scale=Scales.THOUSAND,
            conversion_scale=Scales.THOUSAND,
            dtype=DType.I2,
            flag=NAN,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_epoch(self, path: Path) -> None:
        # Change this to base: it should not be epoch
        extracted: DateTime = utility.extract_datetime(path.name)
        value: int = DateTime(
            year=extracted.year,
            month=extracted.month,
            day=extracted.day,
            hour=extracted.hour,
            minute=extracted.minute,
            second=extracted.second,
        ).unix
        self._variables["epoch"] = Variable(
            dtype=DType.I4,
            long_name="Unix Epoch 1970 of Initial Timestamp",
            scale=Scales.ONE,
            units=Units.SECONDS,
            dimensions=(),
            values=value,
        )

    # def _add_latitude(self, dataset: DataSet) -> None:
    #     value_request: VariableRequest = VariableRequest(
    #         variable="latitude",
    #         name="latitude",
    #         long_name="Platform Latitude [North]",
    #         units=Units.DEGREES,
    #         scale=Scales.ONE,
    #         dtype=DType.U1,
    #         flag=NINES,
    #         dimensions=(),
    #     )
    #     self._add_single_variable(dataset, value_request)

    # def _add_longitude(self, dataset: DataSet) -> None:
    #     value_request: VariableRequest = VariableRequest(
    #         variable="longitude",
    #         name="longitude",
    #         long_name="Platform Longitude [East]",
    #         units=Units.DEGREES,
    #         scale=Scales.ONE,
    #         dtype=DType.U1,
    #         flag=NINES,
    #         dimensions=(),
    #     )
    #     self._add_single_variable(dataset, value_request)

    def _add_molecular_counts(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="molecular_counts",
            name="molecular_counts",
            long_name="Molecular Photon Counts",
            units=Units.NONE,
            scale=Scales.ONE,
            dtype=DType.I4,
            flag=NEG_ONE,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
        )
        self._add_single_variable(dataset, value_request)

    def _add_offset(self, dataset: DataSet) -> None:
        value_request: VariableRequest = VariableRequest(
            variable="time_offset",
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
            variable="altitude",
            name="range",
            long_name="Return Range",
            units=Units.METERS,
            scale=Scales.ONE,
            dtype=DType.U2,
            flag=NINES,
            dimensions=(self._dimensions["level"],),
        )
        self._add_single_variable(dataset, value_request)
