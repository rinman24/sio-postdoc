"""Transformation Context Service."""

from pathlib import Path

from sio_postdoc.access import DataSet
from sio_postdoc.engine.transformation.strategies.base import TransformationStrategy


class TransformationContext:
    """Encapsulate the interface of interest for transformations."""

    def __init__(self) -> None:
        """Initialize the `TransformationContext`."""
        self.strategy: None | TransformationStrategy = None

    def instrument_data(self, dataset: DataSet, path: Path) -> None:
        """Use the strategy to hydrate an instance of `InstrumentData`."""
        return self.strategy.hydrate(dataset, path)
