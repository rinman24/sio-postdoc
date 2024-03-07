"""Observation Manager Module."""

from pathlib import Path

from sio_postdoc.access._local.service import LocalAccess
from sio_postdoc.access.instrument.service import InstrumentAccess
from sio_postdoc.engine.formatting.service import FormattingContext
from sio_postdoc.engine.formatting.strategies import AbstractDateStrategy, MMDDhhmm

Content = tuple[Path, ...]


class ObservationManager:

    def __init__(self) -> None:
        self._instrument_access: InstrumentAccess = InstrumentAccess()
        self._local_access: LocalAccess = LocalAccess()
        self._strategy: AbstractDateStrategy = MMDDhhmm()
        self._formatting_context: FormattingContext = FormattingContext(self._strategy)

    @property
    def instrument_access(self) -> InstrumentAccess:
        return self._instrument_access

    @property
    def local_access(self) -> LocalAccess:
        return self._local_access

    @property
    def formatting_context(self) -> FormattingContext:
        return self._formatting_context

    def format_dir(self, directory: Path, suffix: str, year: str):
        """Format the directory using the current formatting context."""
        current: Content = self.local_access.list_files(directory, suffix)
        new: Content = tuple(
            file.parent / self.formatting_context.format(file.name, year)
            for file in current
        )
        self.local_access.rename_files(current, new)
