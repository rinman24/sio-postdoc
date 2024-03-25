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
        """TODO: Docstring."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbstractDateStrategy) -> None:
        self._strategy = strategy

    def apply(self, target: date, content: Any) -> AbstractDateStrategy:
        """TODO: Docstring."""
        return self.strategy.apply(target=target, content=content)
