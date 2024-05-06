"""Observation Manager Module."""

import os
import pickle
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Generator

import pandas as pd

from sio_postdoc.access import DataSet
from sio_postdoc.access.instrument.service import InstrumentAccess
from sio_postdoc.access.local.service import LocalAccess
from sio_postdoc.engine import Dimensions, DType, Scales, Units
from sio_postdoc.engine.filtering import Content
from sio_postdoc.engine.filtering.context import FilterContext
from sio_postdoc.engine.filtering.strategies import IndicesByDate, NamesByDate
from sio_postdoc.engine.formatting.service import FormattingContext
from sio_postdoc.engine.formatting.strategies import YYYYMMDDdothhmmss
from sio_postdoc.engine.transformation.context.service import TransformationContext
from sio_postdoc.engine.transformation.contracts import (
    DateTime,
    Dimension,
    InstrumentData,
    MaskRequest,
    Variable,
)
from sio_postdoc.engine.transformation.service import TransformationEngine
from sio_postdoc.engine.transformation.strategies.base import (
    SECONDS_PER_DAY,
    TransformationStrategy,
)
from sio_postdoc.engine.transformation.strategies.daily.sheba.dabul import (
    ShebaDabulDaily,
)
from sio_postdoc.engine.transformation.strategies.daily.sheba.mmcr import ShebaMmcrDaily
from sio_postdoc.engine.transformation.strategies.masks import Masks
from sio_postdoc.engine.transformation.strategies.raw.eureka.ahsrl import EurekaAhsrlRaw
from sio_postdoc.engine.transformation.strategies.raw.eureka.mmcr import EurekaMmcrRaw
from sio_postdoc.engine.transformation.strategies.raw.sheba.dabul import ShebaDabulRaw
from sio_postdoc.engine.transformation.strategies.raw.sheba.mmcr import ShebaMmcrRaw
from sio_postdoc.manager.observation.contracts import (
    DailyRequest,
    Instrument,
    Observatory,
    ObservatoryRequest,
)

OFFSETS: dict[str, int] = {"time": 15, "elevation": 45}
STEPS: dict[str, int] = {key: value * 2 for key, value in OFFSETS.items()}
MIN_ELEVATION: int = 500
MASK_TYPE: DType = DType.I1

Mask = tuple[tuple[int, ...], ...]


class ObservationManager:
    """TODO: Docstring."""

    def __init__(self) -> None:
        """Initialize the `ObservationManager`."""
        self._instrument_access: InstrumentAccess = InstrumentAccess()
        self._filter_context: FilterContext = FilterContext()
        self._transformation_context: TransformationContext = TransformationContext()
        self._formatting_context: FormattingContext = FormattingContext()
        self._transformation_engine: TransformationEngine = TransformationEngine()
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
    def transformation_engine(self) -> TransformationEngine:
        """Return the private transformation engine."""
        return self._transformation_engine

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
            print(target)
            selected: tuple[str, ...] = self.filter_context.apply(
                target,
                blobs,
                strategy=NamesByDate(),
            )
            if not selected:
                continue
            # Select the Strategy
            match (request.observatory, request.instrument):
                case (Observatory.EUREKA, Instrument.AHSRL):
                    strategy: TransformationStrategy = EurekaAhsrlRaw()
                case (Observatory.EUREKA, Instrument.MMCR):
                    strategy: TransformationStrategy = EurekaMmcrRaw()
                case (Observatory.SHEBA, Instrument.DABUL):
                    strategy: TransformationStrategy = ShebaDabulRaw()
                case (Observatory.SHEBA, Instrument.MMCR):
                    strategy: TransformationStrategy = ShebaMmcrRaw()
            # Generate a InstrumentData for each DataSet corresponding to the target date
            results: tuple[InstrumentData, ...] = tuple(
                self._generate_data(
                    selected,
                    request,
                    strategy=strategy,
                )
            )
            if not results:
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
                directory=f"{request.instrument.name.lower()}/daily/{request.year}/",
            )
            # Remove the file
            os.remove(filepath)

    def create_daily_masks(self, request: DailyRequest) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"{request.instrument.name.lower()}/daily/{request.year}/",
        )
        # Create a daily file for each day in the month
        for target in self._dates_in_month(request.year, request.month.value):
            print(target)
            selected: tuple[str, ...] = self.filter_context.apply(
                target,
                blobs,
                strategy=NamesByDate(),
                time=False,
            )
            if not selected:
                continue
            # Set the strategy
            strategy: TransformationStrategy
            match (request.observatory, request.instrument):
                case (Observatory.SHEBA, Instrument.DABUL):
                    strategy = ShebaDabulDaily()
                case (Observatory.SHEBA, Instrument.MMCR):
                    strategy = ShebaMmcrDaily()
            # Generate a InstrumentData for each DataSet corresponding to the target date
            results: tuple[InstrumentData, ...] = tuple(
                self._generate_data(
                    selected,
                    request,
                    strategy=strategy,
                )
            )
            if not results:
                continue
            # Filter so only the target date exists in a single instance of `InstrumentData`
            data: InstrumentData = results[0]
            if not data:
                continue
            # Set the Window and threshold
            strategy: TransformationStrategy
            length: int = 3
            scale: int = 100
            dtype: DType = DType.I2
            match (request.observatory, request.instrument):
                case (Observatory.SHEBA, Instrument.DABUL):
                    height: int = 3
                    long_name: str = "Lidar Cloud Mask"
                    name: str = "far_par"
                    threshold: int = 55
                case (Observatory.SHEBA, Instrument.MMCR):
                    height: int = 2
                    long_name: str = "Radar Cloud Mask"
                    name: str = "refl"
                    threshold: int = -5
            # Now you want to apply the mask.
            mask_request: MaskRequest = MaskRequest(
                values=data.variables[name].values,
                length=length,
                height=height,
                threshold=threshold,
                scale=scale,
                dtype=dtype,
            )
            mask: Mask = self.transformation_engine.get_mask(mask_request)
            this_var = Variable(
                dtype=MASK_TYPE,
                long_name=long_name,
                scale=Scales.ONE,
                units=Units.NONE,
                dimensions=(
                    Dimension(
                        name=Dimensions.TIME, size=len(data.variables[name].values)
                    ),
                    Dimension(
                        name=Dimensions.LEVEL, size=len(data.variables[name].values[0])
                    ),
                ),
                values=mask,
            )
            data.variables["cloud_mask"] = this_var
            # Serialize the data.
            filepath: Path = self.transformation_context.serialize(
                target, data, request
            )
            # Add to blob storage
            self.instrument_access.add_blob(
                name=request.observatory.name.lower(),
                path=filepath,
                directory=f"{request.instrument.name.lower()}/masks/{request.year}/threshold_{threshold}/",
            )
            # Remove the file
            os.remove(filepath)

    def merge_daily_masks(self, request: ObservatoryRequest) -> None:
        """Merge daily masks for a given observatory, month and year."""
        # Get a list of all the relevant blobs
        # We know that we need to get two different instrument maps
        instruments: dict[str, Instrument] = {}
        match request.observatory:
            case Observatory.SHEBA:
                instruments["lidar"] = Instrument.DABUL
                instruments["radar"] = Instrument.MMCR
        blobs: dict[Instrument, tuple[str, ...]] = {
            instrument: self.instrument_access.list_blobs(
                container=request.observatory.name.lower(),
                name_starts_with=f"{instrument.name.lower()}/masks/{request.year}/",
            )
            for instrument in instruments.values()
        }
        # Merge the masks for each day in the month
        for target in self._dates_in_month(request.year, request.month.value):
            print(target)
            selected: dict[Instrument, tuple[str, ...]] = {
                instrument: self.filter_context.apply(
                    target,
                    blobs[instrument],
                    strategy=NamesByDate(),
                    time=False,
                )
                for instrument in instruments.values()
            }
            if not all(selected.values()):
                continue
            strategy: TransformationStrategy = Masks()
            # Generate a InstrumentData for each DataSet corresponding to the target date
            results: dict[Instrument, tuple[InstrumentData, ...]] = {
                instrument: tuple(
                    self._generate_data(
                        selected[instrument],
                        request,
                        strategy=strategy,
                    )
                )
                for instrument in instruments.values()
            }
            # NOTE: You can quickly skip to here by using the following.
            # with open("results.pkl", "rb") as file:
            #     results = pickle.load(file)
            if not all(results.values()):
                continue
            # There should only be one value in each result
            data: dict[Instrument, InstrumentData] = {
                instrument: results[instrument][0]
                for instrument in instruments.values()
            }
            # Convert to DataFrames for processing
            # NOTE: This could be done with a transformation strategy as well.
            # TODO: Use a transformation strategy here.
            dataframes: dict[Instrument, pd.DataFrame] = {
                instrument: pd.DataFrame(
                    data[instrument].variables["cloud_mask"].values,
                    index=data[instrument].variables["offset"].values,
                    columns=data[instrument].variables["range"].values,
                )
                for instrument in instruments.values()
            }
            # Set up the new merged mask
            max_elevation: int = min(df.columns.max() for df in dataframes.values())
            times: list[int] = list(range(0, SECONDS_PER_DAY + 1, STEPS["time"]))
            elevations: list[int] = list(
                range(0, max_elevation + 1, STEPS["elevation"])
            )
            mask: list[list[bool]] = [[False for _ in elevations] for _ in times]
            for i, time in enumerate(times):
                for j, elevation in enumerate(elevations):
                    selected_times: dict[Instrument, list[bool]] = {
                        key: [
                            a and b
                            for a, b in zip(
                                time - OFFSETS["time"] <= value.index,
                                value.index < time + OFFSETS["time"],
                            )
                        ]
                        for key, value in dataframes.items()
                    }
                    selected_elevations: dict[Instrument, list[bool]] = {
                        key: [
                            a and b
                            for a, b in zip(
                                elevation - OFFSETS["elevation"] <= value.columns,
                                value.columns < elevation + OFFSETS["elevation"],
                            )
                        ]
                        for key, value in dataframes.items()
                    }
                    # Now you have the values to slice by
                    values: dict[Instrument, pd.DataFrame] = {
                        key: value.iloc[selected_times[key], selected_elevations[key]]
                        for key, value in dataframes.items()
                    }
                    # Now that you have the values, you want to take the the mean of them
                    mask[i][j] = (
                        True
                        if any(v.mean().mean() >= 1 / 2 for v in values.values())
                        else False
                    )
            # Now, assume that you have a bunch of values for the combined cloud map
            # The next thing you need to do is make this into a dataframe
            # with open("mask_list.pkl", "rb") as file:
            #     mask = pickle.load(file)
            mask: pd.DataFrame = pd.DataFrame(
                mask,
                index=times,
                columns=elevations,
            )
            # Now that you have the mask, go through each time and find out how many clouds there
            # are and the the elevations are.
            previous: bool
            current: bool
            current_time: datetime
            cloud_extent = {}
            for i, time in enumerate(times):
                previous = False
                current_time = datetime(
                    year=target.year,
                    month=target.month,
                    day=target.day,
                    tzinfo=timezone.utc,
                ) + timedelta(seconds=time)
                bases: list[int] = []
                tops: list[int] = []
                for j, elevation in enumerate(elevations[:-1]):
                    if elevation <= MIN_ELEVATION:
                        continue
                    current = True if mask.loc[time, elevation] else False
                    next_ = True if mask.iloc[i, j + 1] else False
                    if not previous and current:
                        bases.append(elevation - OFFSETS["elevation"])
                    if current and not next_:
                        tops.append(elevation + OFFSETS["elevation"])
                    # Set previous to current
                    previous = True if current else False
                # Now, you're one away from the top, so go to the top and
                current = True if mask.iloc[i, j + 1] else False
                if not previous and current:
                    bases.append(elevation - OFFSETS["elevation"])
                if current:
                    tops.append(elevation + OFFSETS["elevation"])
                # Now that we're ready to go to the next time, we should append the results
                cloud_extent[current_time] = {"bases": bases, "tops": tops}
            # Now construct the instrument data that you can persist as a blob
            dimensions: dict[str, Dimension] = {
                "time": Dimension(name=Dimensions.TIME, size=len(times)),
                "level": Dimension(name=Dimensions.LEVEL, size=len(elevations)),
            }
            variables: dict[str, Variable] = {
                "epoch": Variable(
                    dimensions=(),
                    dtype=DType.I4,
                    long_name="Unix Epoch 1970 of Initial Timestamp",
                    scale=Scales.ONE,
                    units=Units.SECONDS,
                    values=DateTime(
                        year=target.year,
                        month=target.month,
                        day=target.day,
                        hour=0,
                        minute=0,
                        second=0,
                    ).unix,
                ),
                "offset": Variable(
                    dimensions=(dimensions["time"],),
                    dtype=DType.I4,
                    long_name="Seconds Since Initial Timestamp",
                    scale=Scales.ONE,
                    units=Units.SECONDS,
                    values=tuple(times),
                ),
                "range": Variable(
                    dimensions=(dimensions["level"],),
                    dtype=DType.U2,
                    long_name="Return Range",
                    scale=Scales.ONE,
                    units=Units.METERS,
                    values=tuple(elevations),
                ),
                "cloud_mask": Variable(
                    dimensions=(dimensions["time"], dimensions["level"]),
                    dtype=DType.I4,
                    long_name="Cloud Mask",
                    scale=Scales.ONE,
                    units=Units.NONE,
                    values=tuple(
                        tuple(1 if j else 0 for j in mask.loc[i][:]) for i in mask.index
                    ),
                ),
            }
            instrument_data: InstrumentData = InstrumentData(
                dimensions=dimensions, variables=variables
            )
            # Serialize the data.
            filepath: Path = self.transformation_context.serialize_mask(
                target,
                instrument_data,
                request,
            )
            # Add to blob storage
            self.instrument_access.add_blob(
                name=request.observatory.name.lower(),
                path=filepath,
                directory=f"combined_masks/{request.year}/",
            )
            # Remove the file
            os.remove(filepath)
        # Now you're done with all the times as well.
        # Make sure you save the cloud_extent data
        pickle_name: str = (
            f"cloud-stats-{request.observatory.name.lower()}-{request.year}-{str(request.month.value).zfill(2)}.pkl"
        )
        with open(pickle_name, "wb") as file:
            pickle.dump(cloud_extent, file)

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
