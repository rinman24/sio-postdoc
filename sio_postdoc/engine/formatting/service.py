"""Formatting Engine Service."""

import netCDF4 as nc

from sio_postdoc.engine.formatting.strategies import (
    AbstractConcatStrategy,
    AbstractDateStrategy,
)


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


class ConcatenatingContext:
    """The Context defines the interface of interest to clients."""

    def __init__(self, strategy: AbstractConcatStrategy) -> None:
        """Return a Context with the defined strategy."""
        self._strategy: AbstractConcatStrategy = strategy

    @property
    def strategy(self) -> AbstractConcatStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbstractConcatStrategy) -> None:
        self._strategy = strategy

    def concat(self, datasets: tuple[nc.Dataset, ...]) -> None:
        return self.strategy.concat(datasets)
