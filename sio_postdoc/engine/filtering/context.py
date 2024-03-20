"""from sio_postdoc.engine.filtering.contracts import """

from datetime import date
from typing import Any

from sio_postdoc.engine.filtering.strategies import AbstractDateStrategy


class DateContext:
    """TODO: docstring."""

    def __init__(self, strategy: AbstractDateStrategy) -> None:
        self._strategy: AbstractDateStrategy = strategy

    @property
    def strategy(self) -> AbstractDateStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbstractDateStrategy) -> None:
        self._strategy = strategy

    # TODO: Content is either tuple of str or InstrumentData
    def apply(self, target: date, content: Any) -> AbstractDateStrategy:
        return self.strategy.apply(target=target, content=content)
