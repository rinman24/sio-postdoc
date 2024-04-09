"""Define the raw data context."""

from dataclasses import dataclass

from tests.helper.builder.raw.constants import FILENAMES, STRATEGIES
from tests.helper.builder.raw.strategies import RawDataHydrationStrategy
from tests.helper.builder.raw.types import Instrument, Observatory


@dataclass
class RawDataContext:
    """Represenation of raw data for testing."""

    observatory: Observatory
    instrument: Instrument

    @property
    def strategy(self) -> RawDataHydrationStrategy:
        """Return the `RawDataHydrationStrategy` for the given observatory and instrument."""
        return STRATEGIES[self.observatory][self.instrument]

    @property
    def filename(self) -> str:
        """Return the name of the raw data netCDF file."""
        return FILENAMES[self.observatory][self.instrument]

    def hydrate(self) -> None:
        """Hydrate the raw data file using the specified strategy."""
        self.strategy.hydrate(self.filename)
