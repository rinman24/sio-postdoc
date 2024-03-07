"""TODO: Module level docstring."""

from typing import Optional

from sio_postdoc.engine.formatting.strategies import AbstractDateStrategy


class FormattingContext:
    """The Context defines the interface of interest to clients."""

    def __init__(self, strategy: AbstractDateStrategy) -> None:
        """Return a Context with the defined strategy."""
        self._strategy: AbstractDateStrategy = strategy

    @property
    def strategy(self) -> AbstractDateStrategy:
        """Retrun the private strategy."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbstractDateStrategy) -> None:
        """Update the strategy at runtime."""
        self._strategy = strategy

    def format(self, raw: str, year: str) -> str:
        """Concrete implementation of `format_filename`."""
        return self.strategy.format(raw, year)
