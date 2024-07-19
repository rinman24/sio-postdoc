"""Define strategy to extract raw Utqiagvik KAZR data."""

from pathlib import Path

from sio_postdoc.access import DataSet
from sio_postdoc.engine import Dimensions
from sio_postdoc.engine.transformation.contracts import Dimension
from sio_postdoc.engine.transformation.strategies.base import TransformationStrategy

NINES: int = -9999


class MwrLos(TransformationStrategy):
    """Engine logic for raw MicroWave Radiometer data."""

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
