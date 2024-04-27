"""Encapsulate the context used to filer."""

from datetime import date
from typing import Any

from sio_postdoc.engine.filtering.strategies import AbstractDateStrategy


class FilterContext:
    """TODO: docstring."""

    def __init__(self) -> None:
        """Initialize the `FilterContext`."""
        self._strategy: AbstractDateStrategy | None = None

    @property
    def strategy(self) -> AbstractDateStrategy:
        """TODO: Docstring."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbstractDateStrategy) -> None:
        self._strategy = strategy

    def apply(self, target: date, content: Any, strategy: AbstractDateStrategy) -> Any:
        """TODO: Docstring."""
        # TODO: You should address the signature of this method.
        self.strategy = strategy
        return self.strategy.apply(target=target, content=content)
