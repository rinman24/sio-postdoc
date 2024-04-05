"""Contexts for InstrumentData strategies"""

from sio_postdoc.access.instrument.contracts import InstrumentData
from sio_postdoc.access.instrument.strategies.data import InstrumentDataStrategy


class DataContext:
    """Context for delivering InstrumentData from different sources."""

    def __init__(self, strategy: InstrumentDataStrategy) -> None:
        self._strategy: InstrumentDataStrategy = strategy

    @property
    def strategy(self) -> InstrumentDataStrategy:
        """TODO: Docstring."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: InstrumentDataStrategy) -> None:
        self._strategy = strategy

    def extract(self, name: str) -> InstrumentData:
        """Extract InstrumentData from a given source."""
        name: str = name.split("/")[-1]
        return self.strategy.extract(name)
