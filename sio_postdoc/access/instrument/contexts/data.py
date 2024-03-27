"""Contexts for InstrumentData strategies"""

from sio_postdoc.access.instrument.contracts import InstrumentData
from sio_postdoc.access.instrument.strategies.data import AbstractDataStrategy


class DataContext:
    """Context for delivering InstrumentData from different sources."""

    def __init__(self, strategy: AbstractDataStrategy) -> None:
        self._strategy: AbstractDataStrategy = strategy

    @property
    def strategy(self) -> AbstractDataStrategy:
        """TODO: Docstring."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbstractDataStrategy) -> None:
        self._strategy = strategy

    def extract(self, name: str) -> InstrumentData:
        """Extract InstrumentData from a given source."""
        return self.strategy.extract(name)
