"""Define strategy to extract raw Utqiagvik MPLCMASKML data."""

from pathlib import Path

from sio_postdoc.access import DataSet
from sio_postdoc.engine import Dimensions
from sio_postdoc.engine.transformation.contracts import Dimension
from sio_postdoc.engine.transformation.strategies.base import TransformationStrategy

NINES: int = -9999


class MplCmask1Zwang(TransformationStrategy):
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
        self._add_offset(dataset)
        self._add_range(dataset)
        self._add_lidar_mask(dataset)
        self._add_linear_depolarization_ratio(dataset)


class MplCmaskMl(TransformationStrategy):
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
        self._add_offset(dataset)
        self._add_range(dataset)
        self._add_lidar_mask(dataset)
        self._add_linear_depolarization_ratio(dataset)
