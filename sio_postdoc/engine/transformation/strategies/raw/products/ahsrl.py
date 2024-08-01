"""Define strategy to extract raw Utqiagvik MPLCMASKML data."""

from pathlib import Path

import numpy as np
import pandas as pd

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
DELTA_THRESH: float = 0.25
BETA_THRESH_1: float = 1e-6
BETA_THRESH_2: float = 3e-5
BETA_THRESH_3: float = 1e-4

BACK_SCATTER_THRESH: float = 1e-7
OPTICAL_DEPTH_THRESH: float = 0.03
BACK_SCATTER_3_NEIGHBORS: float = 5e-7
BACK_SCATTER_1_NEIGHBOR: float = 1e-6
MOL_COUNT_SNR_THRESH: int = 5
BACK_SCATTER_SNR_THRESH: int = 10
THREE: int = 3
ONE: int = 1


class AhsrlRaw(TransformationStrategy):
    """Engine logic for raw Utqiagvik KAZR data."""

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

    def _add_variables(self, dataset: DataSet, path: Path) -> None:
        """Use a `DataSet` to set the state of `_variables`."""
        self._add_epoch(path)
        self._add_offset(dataset)
        self._add_range(dataset)
        self._add_cloud_mask(dataset)
        self._add_depolarization_ratio(dataset)

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

    def _add_cloud_mask(self, dataset: DataSet) -> None:
        n_rows: int = dataset.dimensions["time"].size
        n_columns: int = dataset.dimensions["altitude"].size
        index = dataset["time"][:].data
        columns = dataset["altitude"][:].data
        optical_depth = pd.DataFrame(
            dataset["od"][:].data,
            index=index,
            columns=columns,
        )
        back_scatter = pd.DataFrame(
            dataset["beta_a_backscat"][:].data,
            index=index,
            columns=columns,
        )
        back_scatter_noise = pd.DataFrame(
            dataset["std_beta_a_backscat"][:].data,
            index=index,
            columns=columns,
        )
        back_scatter_snr = back_scatter / back_scatter_noise
        molecular_counts = pd.DataFrame(
            dataset["molecular_counts"][:].data,
            index=index,
            columns=columns,
        )
        mol_dark_counts = pd.Series(
            dataset["mol_dark_count"][:].data,
            index=index,
        )
        mol_counts_snr = (molecular_counts.T * (1 / mol_dark_counts)).T
        # Create the mask
        mask = optical_depth.copy(deep=True)
        # Set all the values to one
        for col in mask.columns:
            mask[col].values[:] = 0
        for i in range(1, n_rows - 1):
            if i % 250 == 0:
                print(f"\t{round(i / n_rows * 100)}%")
            # The first pixel within a vertical column with a backscatter
            # greater than 10-7 / (m sr) is used to adjust the HSRL-
            # accumulated optical depth profile to zero.
            vert_col: list[float] = back_scatter.iloc[i, :].to_list()
            try:
                od_idx: int = list(
                    map(lambda i: i > BACK_SCATTER_THRESH, vert_col)
                ).index(True)
            except ValueError:
                continue
            optical_depth.iloc[i, :] -= optical_depth.iloc[i, od_idx]
            for j in range(1, n_columns - 1):
                if mol_counts_snr.iloc[i, j] > MOL_COUNT_SNR_THRESH:
                    if back_scatter_snr.iloc[i, j] > BACK_SCATTER_SNR_THRESH:
                        if back_scatter.iloc[i, j] > BACK_SCATTER_THRESH:
                            if optical_depth.iloc[i, j] > OPTICAL_DEPTH_THRESH:
                                neighbors: pd.DataFrame = back_scatter.iloc[
                                    i - 1 : i + 2, j - 1 : j + 2
                                ]
                                if (
                                    neighbors > BACK_SCATTER_3_NEIGHBORS
                                ).sum().sum() >= THREE:
                                    if (
                                        neighbors > BACK_SCATTER_1_NEIGHBOR
                                    ).sum().sum() >= ONE:
                                        mask.iloc[i, j] = ONE
        values = tuple(tuple(map(round, values)) for values in mask.values)
        # Add the variable
        self._variables["lidar_mask"] = Variable(
            dtype=DType.I1,
            long_name="Lidar Mask",
            scale=Scales.ONE,
            units=Units.NONE,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
            values=values,
        )

    def _add_depolarization_ratio(self, dataset: DataSet) -> None:
        depol = pd.DataFrame(
            dataset["depol"][:].data,
            index=dataset["time"][:].data,
            columns=dataset["altitude"][:].data,
        )
        mask = pd.DataFrame(
            self._variables["lidar_mask"].values,
            index=dataset["time"][:].data,
            columns=dataset["altitude"][:].data,
        )
        depol.replace(np.float32("nan"), DType.I2.min, inplace=True)
        depol[depol != DType.I2.min] *= Scales.THOUSAND.value
        depol[mask == 0] = DType.I2.min
        values = tuple(tuple(map(round, values)) for values in depol.values)
        # Add the variable
        self._variables["depol"] = Variable(
            dtype=DType.I2,
            long_name="Circular Depolarization Ratio",
            scale=Scales.THOUSAND,
            units=Units.NONE,
            dimensions=(self._dimensions["time"], self._dimensions["level"]),
            values=values,
        )
