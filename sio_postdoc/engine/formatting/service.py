"""Formatting Engine Service."""

from sio_postdoc.engine.formatting.strategies import AbstractDateStrategy


class FormattingContext:
    """The Context defines the interface of interest to clients."""

    def __init__(self) -> None:
        """Return a Context with the defined strategy."""
        self._strategy: AbstractDateStrategy | None = None

    @property
    def strategy(self) -> AbstractDateStrategy:
        """Retrun the private strategy."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbstractDateStrategy) -> None:
        """Update the strategy at runtime."""
        self._strategy = strategy

    def format(self, raw: str, year: str, strategy: AbstractDateStrategy) -> str:
        """Concrete implementation of `format_filename`."""
        self.strategy = strategy
        return self.strategy.format(raw, year)
