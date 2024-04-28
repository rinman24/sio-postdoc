"""Observation Manager Module."""

import os
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Generator

from sio_postdoc.access import DataSet
from sio_postdoc.access.instrument.service import InstrumentAccess
from sio_postdoc.access.local.service import LocalAccess
from sio_postdoc.engine.filtering.context import FilterContext
from sio_postdoc.engine.filtering.strategies import IndicesByDate, NamesByDate
from sio_postdoc.engine.formatting.service import FormattingContext
from sio_postdoc.engine.formatting.strategies import YYYYMMDDdothhmmss
from sio_postdoc.engine.transformation.context.service import TransformationContext
from sio_postdoc.engine.transformation.contracts import InstrumentData
from sio_postdoc.engine.transformation.strategies.base import TransformationStrategy
from sio_postdoc.engine.transformation.strategies.raw.sheba.dabul import ShebaDabulRaw
from sio_postdoc.manager.observation.contracts import DailyRequest

Content = tuple[Path, ...]


class ObservationManager:
    """TODO: Docstring."""

    def __init__(self) -> None:
        """Initialize the `ObservationManager`."""
        self._instrument_access: InstrumentAccess = InstrumentAccess()
        self._filter_context: FilterContext = FilterContext()
        self._transformation_context: TransformationContext = TransformationContext()
        self._formatting_context: FormattingContext = FormattingContext()
        self._local_access: LocalAccess = LocalAccess()

    @property
    def instrument_access(self) -> InstrumentAccess:
        """Return the private instrument access."""
        return self._instrument_access

    @property
    def filter_context(self) -> FilterContext:
        """Return the private filter context."""
        return self._filter_context

    @property
    def transformation_context(self) -> TransformationContext:
        """Return the private transformation context."""
        return self._transformation_context

    @property
    def formatting_context(self) -> TransformationContext:
        """Return the private formatting context."""
        return self._formatting_context

    @property
    def local_access(self) -> TransformationContext:
        """Return the private local access."""
        return self._local_access

    def format_dir(self, directory: Path, suffix: str, year: str):
        """Format the directory using the current formatting context."""
        current: Content = self.local_access.list_files(directory, suffix)
        new: Content = tuple(
            file.parent
            / self.formatting_context.format(
                file.name,
                year,
                strategy=YYYYMMDDdothhmmss(),
            )
            for file in current
        )
        self.local_access.rename_files(current, new)

    def create_daily_files(self, request: DailyRequest) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"{request.instrument.name.lower()}/raw/{request.year}/",
        )
        # Create a daily file for each day in the month
        for target in self._dates_in_month(request.year, request.month.value):
            selected: tuple[str, ...] = self.filter_context.apply(
                target,
                blobs,
                strategy=NamesByDate(),
            )
            if not selected:
                continue
            # Generate a InstrumentData for each DataSet corresponding to the target date
            results: tuple[InstrumentData, ...] = tuple(
                self._generate_data(
                    selected,
                    request,
                    strategy=ShebaDabulRaw(),
                )
            )
            if not results:  # check if the instrument data is empty
                continue
            # Filter so only the target date exists in a single instance of `InstrumentData`
            data: InstrumentData | None = self.filter_context.apply(
                target,
                results,
                strategy=IndicesByDate(),
            )
            if not data:
                continue
            # Serialize the data.
            filepath: Path = self.transformation_context.serialize(
                target, data, request
            )
            # Add to blob storage
            self.instrument_access.add_blob(
                name=request.observatory.name.lower(),
                path=filepath,
                directory=f"{request.instrument.name.lower()}/test_daily/{request.year}/",
            )
            # Remove the file
            os.remove(filepath)

    @staticmethod
    def _dates_in_month(year: int, month: int) -> Generator[date, None, None]:
        current = datetime(year, month, 1)
        while current.month == month:
            yield date(year, month, current.day)
            current = current + timedelta(days=1)

    def _generate_data(
        self,
        selected: tuple[str, ...],
        request: DailyRequest,
        strategy: TransformationStrategy,
    ) -> Generator[InstrumentData, None, None]:
        cwd: Path = Path.cwd()
        self.transformation_context.strategy = strategy
        for name in selected:
            filename = self.instrument_access.download_blob(
                container=request.observatory.name.lower(),
                name=name,
            )
            filepath: Path = cwd / filename
            with DataSet(filename) as dataset:
                yield self.transformation_context.hydrate(dataset, filepath)
            os.remove(filepath)
