"""Observation Manager Module."""

from pathlib import Path

from sio_postdoc.access.instrument.service import InstrumentAccess
from sio_postdoc.access.local.service import LocalAccess
from sio_postdoc.engine.filtering.service import FilteringEngine
from sio_postdoc.engine.formatting.service import FormattingContext
from sio_postdoc.engine.formatting.strategies import MMDDhhmm

Content = tuple[Path, ...]


class ObservationManager:
    """TODO: Docstring."""

    def __init__(self) -> None:
        self._instrument_access: InstrumentAccess = InstrumentAccess()
        self._local_access: LocalAccess = LocalAccess()
        self._filtering_engine: FilteringEngine = FilteringEngine()
        self._formatting_context: FormattingContext = FormattingContext(MMDDhhmm())

    @property
    def instrument_access(self) -> InstrumentAccess:
        """TODO: Docstring."""
        return self._instrument_access

    @property
    def local_access(self) -> LocalAccess:
        """TODO: Docstring."""
        return self._local_access

    @property
    def filtering_engine(self) -> FilteringEngine:
        """TODO: Docstring."""
        return self._filtering_engine

    @property
    def formatting_context(self) -> FormattingContext:
        """TODO: Docstring."""
        return self._formatting_context

    def format_dir(self, directory: Path, suffix: str, year: str):
        """Format the directory using the current formatting context."""
        current: Content = self.local_access.list_files(directory, suffix)
        new: Content = tuple(
            file.parent / self.formatting_context.format(file.name, year)
            for file in current
        )
        self.local_access.rename_files(current, new)
