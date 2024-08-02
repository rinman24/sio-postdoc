"""Observation Manager Module."""

import os
import pickle
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Generator

import matplotlib.pyplot as plt
import numpy as np
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
    Direction,
    InstrumentData,
    MaskCode,
    MaskRequest,
    Threshold,
    Variable,
    VerticalLayers,
    VerticalTransition,
)
from sio_postdoc.engine.transformation.service import TransformationEngine
from sio_postdoc.engine.transformation.strategies.base import (
    SECONDS_PER_DAY,
    TransformationStrategy,
)
from sio_postdoc.engine.transformation.strategies.daily.products.arscl import (
    Arscl1Cloth,
    ArsclKazr1Kollias,
)
from sio_postdoc.engine.transformation.strategies.daily.products.mplcmask import (
    MplCmask1Zwang,
    MplCmaskMl,
)
from sio_postdoc.engine.transformation.strategies.daily.products.mwr import MwrLos
from sio_postdoc.engine.transformation.strategies.daily.products.sonde import (
    InterpolatedSonde,
)
from sio_postdoc.engine.transformation.strategies.daily.sheba.dabul import (
    ShebaDabulDaily,
)
from sio_postdoc.engine.transformation.strategies.daily.sheba.mmcr import ShebaMmcrDaily
from sio_postdoc.engine.transformation.strategies.daily.utqiagvik.kazr import (
    UtqiagvikKazrDaily,
)
from sio_postdoc.engine.transformation.strategies.masks import Masks
from sio_postdoc.engine.transformation.strategies.raw.eureka.ahsrl import EurekaAhsrlRaw
from sio_postdoc.engine.transformation.strategies.raw.eureka.mmcr import EurekaMmcrRaw
from sio_postdoc.engine.transformation.strategies.raw.products.ahsrl import (
    AhsrlRaw,
    AhsrlSondeRaw,
)
from sio_postdoc.engine.transformation.strategies.raw.products.arscl import (
    Arscl1ClothRaw,
    ArsclKazr1KolliasRaw,
    MmcrMergeRaw,
)
from sio_postdoc.engine.transformation.strategies.raw.products.mplcmask import (
    MplCmask1ZwangRaw,
    MplCmaskMlRaw,
)
from sio_postdoc.engine.transformation.strategies.raw.products.mrwlos import (
    MwrLosRaw,
    MwrLosRawEureka,
)
from sio_postdoc.engine.transformation.strategies.raw.products.sonde import (
    InterpolatedSondeRaw,
)
from sio_postdoc.engine.transformation.strategies.raw.sheba.dabul import ShebaDabulRaw
from sio_postdoc.engine.transformation.strategies.raw.sheba.mmcr import ShebaMmcrRaw
from sio_postdoc.engine.transformation.strategies.raw.utqiagvik.kazr import (
    UtqiagvikKazrRaw,
)
from sio_postdoc.manager.observation.contracts import (
    DailyProductRequest,
    DailyRequest,
    Instrument,
    Observatory,
    ObservatoryRequest,
    Product,
)

OFFSETS: dict[str, int] = {"time": 15, "elevation": 45}
STEPS: dict[str, int] = {key: value * 2 for key, value in OFFSETS.items()}
MIN_ELEVATION: int = 500
MASK_TYPE: DType = DType.I1
ONE_HALF: float = 1 / 2
VERTICAL_RAIL: int = -10

RAIN: int = 6
DRIZZLE: int = 5
LIQUID: int = 4
MIXED: int = 3
ICE: int = 2
SNOW: int = 1

NEW_LIQUID: int = 5
MIXED_LIQUID: int = 4
MIXED_ICE: int = 2
NEW_ICE: int = 1

RECLASSIFIED = {"ice": {1, 2}, "liquid": {4, 5}}

MIN_BASE: int = 300
MIN_DEPTH: int = 500

MINUTES_PER_DAY: int = int(24 * 60)

SHUPE = {
    "depol": {
        "ice": 0.1,
    },
    "refl": {
        "low": -17,
        "high": 5,
    },
    "mean_dopp_vel": {
        "low": 1,
        "high": 2.5,
    },
    "spec_width": {
        "low": 0.4,
    },
    "occultation": {
        "low": 500,
        "high": 750,
        "lwp": 25,
    },
    "freezing": {
        "nominal": 0,
        "homogeneous": -40,
    },
    "window": {
        "buffer": 3,
        "clear": 14,
        "match": 7,
    },
    "persistence": {
        "thresh": 30,
    },
}

PRODUCT_SUITE_THRESH: int = 2009

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

    # NOTE: Most likely depreciated.
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
                case (Observatory.UTQIAGVIK, Instrument.KAZR):
                    strategy: TransformationStrategy = UtqiagvikKazrRaw()
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
                directory=f"{request.instrument.name.lower()}/daily_30smplcmask1zwang/{request.year}/",
            )
            # Remove the file
            os.remove(filepath)

    def create_daily_product_files(self, request: DailyProductRequest) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"{request.product.name.lower()}/raw/{request.year}/",
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
            strategy: TransformationStrategy
            prev_day: bool = False
            next_day: bool = False
            match request.product:
                case Product.AHSRL:
                    strategy = AhsrlRaw()
                case Product.AHSRLSONDE:
                    strategy = AhsrlSondeRaw()
                    # target
                    next_day_name: tuple[str, ...] = self.filter_context.apply(
                        target + timedelta(days=1),
                        blobs,
                        strategy=NamesByDate(),
                    )
                    if next_day_name:
                        next_day = True
                    prev_day_name: tuple[str, ...] = self.filter_context.apply(
                        target - timedelta(days=1),
                        blobs,
                        strategy=NamesByDate(),
                    )
                    if prev_day_name:
                        prev_day = True
                    selected = tuple(
                        list(prev_day_name) + list(selected) + list(next_day_name)
                    )
                case Product.ARSCL1CLOTH:
                    strategy = Arscl1ClothRaw()
                case Product.ARSCLKAZR1KOLLIAS:
                    strategy = ArsclKazr1KolliasRaw()
                case Product.INTERPOLATEDSONDE:
                    strategy = InterpolatedSondeRaw()
                case Product.MMCRMERGE:
                    strategy = MmcrMergeRaw()
                case Product.MPLCMASK1ZWANG:
                    strategy = MplCmask1ZwangRaw()
                case Product.MPLCMASKML:
                    strategy = MplCmaskMlRaw()
                case Product.MWRLOS:
                    strategy = (
                        MwrLosRawEureka()
                        if (request.observatory == Observatory.EUREKA)
                        else MwrLosRaw()
                    )
            # Generate a InstrumentData for each DataSet corresponding to the target date
            results: tuple[InstrumentData, ...] = tuple(
                self._generate_data(
                    selected,
                    request,
                    strategy=strategy,
                    prev_day=prev_day,
                    next_day=next_day,
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
                directory=f"{request.product.name.lower()}/daily/{request.year}/",
            )
            # Remove the file
            os.remove(filepath)

    def create_daily_resampled_merged_files(self, request: ObservatoryRequest) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # Use request.year to select the product suite
        product_suites: dict[str, tuple[Product, ...]] = {
            "a": [
                Product.ARSCLKAZR1KOLLIAS,
                Product.INTERPOLATEDSONDE,
                Product.MPLCMASKML,
            ],
            "b": [
                Product.ARSCL1CLOTH,
                Product.INTERPOLATEDSONDE,
                Product.MPLCMASK1ZWANG,
                Product.MWRLOS,
            ],
        }
        product_key = "b" if request.year <= PRODUCT_SUITE_THRESH else "a"
        products = product_suites[product_key]
        # Get a list of all the relevant blobs
        blobs: dict[str, tuple[str, ...]] = {
            product.name.lower(): self.instrument_access.list_blobs(
                container=request.observatory.name.lower(),
                name_starts_with=f"{product.name.lower()}/daily/{request.year}/",
            )
            for product in products
        }
        # Create a daily file for each day in the month
        for target in self._dates_in_month(request.year, request.month.value):
            print(target)
            selected: dict[str, tuple[str] | tuple] = {
                product.name.lower(): self.filter_context.apply(
                    target,
                    blobs[product.name.lower()],
                    strategy=NamesByDate(),
                    time=False,
                )
                for product in products
            }
            if not all(selected.values()):
                continue
            # Because you need to set the strategy, you need to go through each product
            frames = {}
            for product in products:
                # Select the Strategy
                strategy: TransformationStrategy
                match product:
                    case Product.ARSCL1CLOTH:
                        strategy = Arscl1Cloth()
                    case Product.ARSCLKAZR1KOLLIAS:
                        strategy = ArsclKazr1Kollias()
                    case Product.INTERPOLATEDSONDE:
                        strategy = InterpolatedSonde()
                    case Product.MPLCMASK1ZWANG:
                        strategy = MplCmask1Zwang()
                    case Product.MPLCMASKML:
                        strategy = MplCmaskMl()
                    case Product.MWRLOS:
                        strategy = MwrLos()
                # Generate a InstrumentData for each DataSet corresponding to the target date
                results: tuple[InstrumentData, ...] = tuple(
                    self._generate_data(
                        selected[product.name.lower()],
                        request,
                        strategy=strategy,
                    )
                )
                if not results:
                    continue
                # There is only one per day
                data: InstrumentData = results[0]
                # Now that you have the instrument data, you want to construct the dataframes
                # NOTE: You can move these match statements to methods that take the product and return the frames object.
                match product:
                    case Product.ARSCL1CLOTH:
                        frames["radar_mask"] = pd.DataFrame(
                            data.variables["radar_mask"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                        frames["refl"] = pd.DataFrame(
                            data.variables["refl"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                        frames["mean_dopp_vel"] = pd.DataFrame(
                            data.variables["mean_dopp_vel"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                        frames["spec_width"] = pd.DataFrame(
                            data.variables["spec_width"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                        frames["spec_width"] = pd.DataFrame(
                            data.variables["spec_width"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                    case Product.ARSCLKAZR1KOLLIAS:
                        frames["radar_mask"] = pd.DataFrame(
                            data.variables["radar_mask"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                        frames["refl"] = pd.DataFrame(
                            data.variables["refl"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                        frames["mean_dopp_vel"] = pd.DataFrame(
                            data.variables["mean_dopp_vel"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                        frames["spec_width"] = pd.DataFrame(
                            data.variables["spec_width"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                        frames["mwr_lwp"] = pd.DataFrame(
                            data.variables["mwr_lwp"].values,
                            index=data.variables["offset"].values,
                            columns=["mwr_lwp"],
                        )
                    case Product.INTERPOLATEDSONDE:
                        frames["temp"] = pd.DataFrame(
                            data.variables["temp"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                        frames["rh"] = pd.DataFrame(
                            data.variables["rh"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                    case Product.MPLCMASK1ZWANG | Product.MPLCMASKML:
                        frames["lidar_mask"] = pd.DataFrame(
                            data.variables["lidar_mask"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                        frames["depol"] = pd.DataFrame(
                            data.variables["depol"].values,
                            index=data.variables["offset"].values,
                            columns=data.variables["range"].values,
                        )
                    case Product.MWRLOS:
                        frames["mwr_lwp"] = pd.DataFrame(
                            data.variables["mwr_lwp"].values,
                            index=data.variables["offset"].values,
                            columns=["mwr_lwp"],
                        )
                # Now we have all of the dataframes
                match product:
                    case Product.ARSCL1CLOTH:
                        # Radar Mask
                        flag_ = data.variables["radar_mask"].dtype.min
                        scale = data.variables["radar_mask"].scale.value
                        frames["radar_mask"].replace(flag_, 0, inplace=True)
                        frames["radar_mask"] = frames["radar_mask"] / scale
                        frames["radar_mask"].replace(2, 1, inplace=True)
                        frames["radar_mask"] = self._reformat(
                            frames["radar_mask"], method="mode"
                        )
                        # Reflectivity
                        flag_ = data.variables["refl"].dtype.min
                        scale = data.variables["refl"].scale.value
                        frames["refl"].replace(flag_, np.nan, inplace=True)
                        frames["refl"] = frames["refl"] / scale
                        frames["refl"] = self._reformat(
                            frames["refl"],
                            method="mean",
                        )
                        frames["refl"][frames["radar_mask"] == 0] = np.nan
                        # Mean Doppler Velocity
                        flag_ = data.variables["mean_dopp_vel"].dtype.min
                        scale = data.variables["mean_dopp_vel"].scale.value
                        frames["mean_dopp_vel"].replace(flag_, np.nan, inplace=True)
                        frames["mean_dopp_vel"] = frames["mean_dopp_vel"] / scale
                        frames["mean_dopp_vel"] = self._reformat(
                            frames["mean_dopp_vel"],
                            method="mean",
                        )
                        frames["mean_dopp_vel"][frames["radar_mask"] == 0] = np.nan
                        # Spectral Width
                        flag_ = data.variables["spec_width"].dtype.min
                        scale = data.variables["spec_width"].scale.value
                        frames["spec_width"].replace(flag_, np.nan, inplace=True)
                        frames["spec_width"] = frames["spec_width"] / scale
                        frames["spec_width"] = self._reformat(
                            frames["spec_width"],
                            method="mean",
                        )
                        frames["spec_width"][frames["radar_mask"] == 0] = np.nan
                    case Product.ARSCLKAZR1KOLLIAS:
                        # Radar Mask
                        flag_ = data.variables["radar_mask"].dtype.min
                        scale = data.variables["radar_mask"].scale.value
                        frames["radar_mask"].replace(flag_, 0, inplace=True)
                        frames["radar_mask"] = frames["radar_mask"] / scale
                        frames["radar_mask"].replace(2, 1, inplace=True)
                        frames["radar_mask"] = self._reformat(
                            frames["radar_mask"], method="mode"
                        )
                        # Reflectivity
                        flag_ = data.variables["refl"].dtype.min
                        scale = data.variables["refl"].scale.value
                        frames["refl"].replace(flag_, np.nan, inplace=True)
                        frames["refl"] = frames["refl"] / scale
                        frames["refl"] = self._reformat(
                            frames["refl"],
                            method="mean",
                        )
                        frames["refl"][frames["radar_mask"] == 0] = np.nan
                        # Mean Doppler Velocity
                        flag_ = data.variables["mean_dopp_vel"].dtype.min
                        scale = data.variables["mean_dopp_vel"].scale.value
                        frames["mean_dopp_vel"].replace(flag_, np.nan, inplace=True)
                        frames["mean_dopp_vel"] = frames["mean_dopp_vel"] / scale
                        frames["mean_dopp_vel"] = self._reformat(
                            frames["mean_dopp_vel"],
                            method="mean",
                        )
                        frames["mean_dopp_vel"][frames["radar_mask"] == 0] = np.nan
                        # Spectral Width
                        flag_ = data.variables["spec_width"].dtype.min
                        scale = data.variables["spec_width"].scale.value
                        frames["spec_width"].replace(flag_, np.nan, inplace=True)
                        frames["spec_width"] = frames["spec_width"] / scale
                        frames["spec_width"] = self._reformat(
                            frames["spec_width"],
                            method="mean",
                        )
                        frames["spec_width"][frames["radar_mask"] == 0] = np.nan
                        # MWR LWP
                        flag_ = data.variables["mwr_lwp"].dtype.min
                        scale = data.variables["mwr_lwp"].scale.value
                        frames["mwr_lwp"].replace(flag_, np.nan, inplace=True)
                        frames["mwr_lwp"] = frames["mwr_lwp"] / scale
                        frames["mwr_lwp"] = self._reformat_1D(
                            frames["mwr_lwp"],
                            method="mean",
                        )
                    case Product.INTERPOLATEDSONDE:
                        # Temperature
                        flag_ = data.variables["temp"].dtype.min
                        scale = data.variables["temp"].scale.value
                        frames["temp"].replace(flag_, np.nan, inplace=True)
                        frames["temp"] = frames["temp"] / scale
                        frames["temp"] = self._reformat(
                            frames["temp"],
                            method="mean",
                        )
                        # Relative Humidity
                        flag_ = data.variables["rh"].dtype.min
                        scale = data.variables["rh"].scale.value
                        frames["rh"].replace(flag_, np.nan, inplace=True)
                        frames["rh"] = frames["rh"] / scale
                        frames["rh"] = self._reformat(
                            frames["rh"],
                            method="mean",
                        )
                    case Product.MPLCMASK1ZWANG | Product.MPLCMASKML:
                        # Lidar Mask
                        flag_ = data.variables["lidar_mask"].dtype.min
                        scale = data.variables["lidar_mask"].scale.value
                        frames["lidar_mask"].replace(flag_, 0, inplace=True)
                        frames["lidar_mask"] = frames["lidar_mask"] / scale
                        frames["lidar_mask"] = self._reformat(
                            frames["lidar_mask"], method="mode"
                        )
                        # Depolarization Ratio
                        flag_ = data.variables["depol"].dtype.min
                        scale = data.variables["depol"].scale.value
                        frames["depol"].replace(flag_, np.nan, inplace=True)
                        frames["depol"] = frames["depol"] / scale
                        frames["depol"] = self._reformat(
                            frames["depol"],
                            method="mean",
                        )
                        frames["depol"][frames["lidar_mask"] == 0] = np.nan
                    case Product.MWRLOS:
                        # MWR LWP
                        flag_ = data.variables["mwr_lwp"].dtype.min
                        scale = data.variables["mwr_lwp"].scale.value
                        frames["mwr_lwp"].replace(flag_, np.nan, inplace=True)
                        frames["mwr_lwp"] = frames["mwr_lwp"] / scale
                        frames["mwr_lwp"] = self._reformat_1D(
                            frames["mwr_lwp"],
                            method="mean",
                        )
            # Now we should have all of the reformatted data that we want to seralize
            # pickle the frames.
            filepath: Path = Path.cwd() / (
                f"D{target.year}"
                f"-{str(target.month).zfill(2)}"
                f"-{str(target.day).zfill(2)}"
                f"-{request.observatory.name.lower()}"
                "-resampled_frames"
                ".pkl"
            )
            with open(filepath, "wb") as file:
                pickle.dump(frames, file)
            # Add to blob storage
            self.instrument_access.add_blob(
                name=request.observatory.name.lower(),
                path=filepath,
                directory=f"resampled_frames/daily/{request.year}/",
            )
            # Remove the file
            os.remove(filepath)

    def create_daily_layers_and_phases(self, request: ObservatoryRequest) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"resampled_frames/daily/{request.year}/",
        )
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
            # Now that I have the blob (pkl) I need to download it
            # There is only one in each selected
            name: str = selected[0]
            filename = self.instrument_access.download_blob(
                container=request.observatory.name.lower(),
                name=name,
            )
            # Rather than yield the instrument data, you just want to unpickle the dataframes
            filepath: Path = Path.cwd() / filename
            with open(filepath, "rb") as file:
                frames = pickle.load(file)
            os.remove(filepath)
            # Now we should have the combined frames
            steps: dict[str, pd.DataFrame] = {}
            # Step 1 ------------------------------------------------------------------------
            steps["1"] = frames["depol"].copy(deep=True)
            steps["1"][frames["depol"] < SHUPE["depol"]["ice"]] = LIQUID
            steps["1"][SHUPE["depol"]["ice"] <= frames["depol"]] = ICE
            # Step 2 ------------------------------------------------------------------------
            # Make a copy
            steps["2"] = steps["1"].copy(deep=True)
            # Classify mixed-phase
            steps["2"][
                (steps["1"] == LIQUID)  # Lidar detected liquid
                & (frames["temp"] < SHUPE["freezing"]["nominal"])
                & (SHUPE["refl"]["low"] <= frames["refl"])
            ] = MIXED
            steps["2"][
                (steps["1"] == LIQUID)  # Lidar detected liquid
                & (frames["temp"] < SHUPE["freezing"]["nominal"])
                & (SHUPE["mean_dopp_vel"]["low"] <= frames["mean_dopp_vel"])
            ] = MIXED
            # Classify Drizzle
            steps["2"][
                (steps["1"] == LIQUID)  # Lidar detected liquid
                & (SHUPE["freezing"]["nominal"] <= frames["temp"])
                & (SHUPE["refl"]["low"] <= frames["refl"])
            ] = DRIZZLE
            steps["2"][
                (steps["1"] == LIQUID)  # Lidar detected liquid
                & (SHUPE["freezing"]["nominal"] <= frames["temp"])
                & (SHUPE["mean_dopp_vel"]["low"] <= frames["mean_dopp_vel"])
            ] = DRIZZLE
            # Step 3 ------------------------------------------------------------------------
            # Make a copy
            steps["3"] = steps["2"].copy(deep=True)
            # Reclassify snow and rain based on reflectivity greater than 5
            steps["3"][
                (frames["temp"] < SHUPE["freezing"]["nominal"])
                & (SHUPE["refl"]["high"] <= frames["refl"])
            ] = SNOW
            steps["3"][
                (SHUPE["freezing"]["nominal"] <= frames["temp"])
                & (SHUPE["refl"]["high"] <= frames["refl"])
            ] = RAIN
            # Reclassify rain when velocity is greater than 2.5 and temperature is above freezing
            steps["3"][
                (SHUPE["freezing"]["nominal"] <= frames["temp"])
                & (SHUPE["mean_dopp_vel"]["high"] <= frames["mean_dopp_vel"])
            ] = RAIN
            # Step 4 ------------------------------------------------------------------------
            # Make a copy for step 4
            steps["4"] = steps["3"].copy(deep=True)
            # First set all of the values that are in the mask to rain
            steps["4"][
                (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (SHUPE["freezing"]["nominal"] <= frames["temp"])
                & (frames["radar_mask"] == 1)  # Pixels viewed by radar
            ] = RAIN
            # Now cut in with drizzle
            steps["4"][
                (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (SHUPE["freezing"]["nominal"] <= frames["temp"])
                & (frames["refl"] < SHUPE["refl"]["high"])
                & (frames["mean_dopp_vel"] < SHUPE["mean_dopp_vel"]["high"])
            ] = DRIZZLE
            # Finally cut in with liquid
            steps["4"][
                (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (SHUPE["freezing"]["nominal"] <= frames["temp"])
                & (frames["refl"] < SHUPE["refl"]["low"])
                & (frames["mean_dopp_vel"] < 1)  # Low velocity
            ] = LIQUID
            # Differentiate between snow and ice below freezing using reflectivity at narrow widths.
            steps["4"][
                (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (frames["temp"] < SHUPE["freezing"]["nominal"])
                & (frames["spec_width"] < SHUPE["spec_width"]["low"])
                & (frames["refl"] < SHUPE["refl"]["high"])
            ] = ICE
            steps["4"][
                (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (frames["temp"] < SHUPE["freezing"]["nominal"])
                & (frames["spec_width"] < SHUPE["spec_width"]["low"])
                & (SHUPE["refl"]["high"] <= frames["refl"])
            ] = SNOW
            # Differentiate between liquid, mixed-phase, and snow below freezing using reflectivity at elevated widths.
            # First set everything to snow
            steps["4"][
                (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (frames["temp"] < SHUPE["freezing"]["nominal"])
                & (SHUPE["spec_width"]["low"] <= frames["spec_width"])
            ] = SNOW
            # Now cut in with mixed-phase
            steps["4"][
                (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (frames["temp"] < SHUPE["freezing"]["nominal"])
                & (SHUPE["spec_width"]["low"] <= frames["spec_width"])
                & (frames["refl"] < SHUPE["refl"]["high"])
            ] = MIXED
            # Finally cut in with liquid
            steps["4"][
                (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (frames["temp"] < SHUPE["freezing"]["nominal"])
                & (SHUPE["spec_width"]["low"] <= frames["spec_width"])
                & (frames["refl"] < SHUPE["refl"]["low"])
                & (frames["mean_dopp_vel"] < SHUPE["mean_dopp_vel"]["low"])
            ] = LIQUID
            # Lidar Occulation Zone
            # Start with a dataframe of all zeros
            # NOTE: the Occulation Zone is Step -1
            steps["occulation_zone"] = steps["4"].copy(deep=True)
            for col in steps["occulation_zone"].columns:
                steps["occulation_zone"][col].values[:] = 0
            # Find the radar tops
            steps["radar_tops"] = steps["4"].copy(deep=True)
            steps["radar_tops"].iloc[:, :-1] = (
                frames["radar_mask"].iloc[:, :-1].values
                - frames["radar_mask"].iloc[:, 1:].values
            )
            steps["radar_tops"].iloc[:, -1] = 0
            # Find the lidar tops
            steps["lidar_tops"] = steps["4"].copy(deep=True)
            steps["lidar_tops"].iloc[:, :-1] = (
                frames["lidar_mask"].iloc[:, :-1].values
                - frames["lidar_mask"].iloc[:, 1:].values
            )
            steps["lidar_tops"].iloc[:, -1] = 0
            # Find Lidar Occulation Levels and Radar Tops
            lidar_occulation_levels = steps["lidar_tops"].T.apply(
                lambda series: series[series == 1].index.max()
            )
            radar_tops_levels = steps["radar_tops"].T.apply(
                lambda series: series[series == 1].index.tolist()
            )
            for i, t in enumerate(steps["lidar_tops"].index):
                for radar_top in radar_tops_levels[t]:
                    base = lidar_occulation_levels[t]
                    if 0 <= radar_top - base <= SHUPE["occultation"]["high"]:
                        # then set the values in the given location between these values to 1
                        steps["occulation_zone"].loc[t, base:radar_top] = 1
            # Use occulation zone to Differentiate between liquid, mixed-phase, and snow below freezing using reflectivity regardless of spectral width.
            # First set everything to snow
            steps["4"][
                (steps["occulation_zone"] == 1)  # In occulation zone
                & (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (frames["temp"] < SHUPE["freezing"]["nominal"])
            ] = SNOW
            # Now cut in with mixed-phase
            steps["4"][
                (steps["occulation_zone"] == 1)  # In occulation zone
                & (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (frames["temp"] < SHUPE["freezing"]["nominal"])
                & (frames["refl"] < SHUPE["refl"]["high"])
            ] = MIXED
            # Finally cut in with liquid
            steps["4"][
                (steps["occulation_zone"] == 1)  # In occulation zone
                & (frames["lidar_mask"] == 0)  # Pixels not viewed by lidar
                & (frames["temp"] < SHUPE["freezing"]["nominal"])
                & (frames["refl"] < SHUPE["refl"]["low"])
                & (frames["mean_dopp_vel"] < SHUPE["mean_dopp_vel"]["low"])
            ] = LIQUID
            # Step 5 ------------------------------------------------------------------------
            # Absolute Temperature Rules
            # TODO: You are here
            # Make a copy for step 5
            steps["5"] = steps["4"].copy(deep=True)
            # Find all the locations where step 4 is in both of the masks is below -40
            # Below - 40 you can only have ice or snow and you can differentiate show using reflectivity > 5
            steps["5"][
                (frames["temp"] < SHUPE["freezing"]["homogeneous"])
                & (steps["5"] == RAIN)
            ] = SNOW
            steps["5"][
                (frames["temp"] < SHUPE["freezing"]["homogeneous"])
                & (steps["5"] == LIQUID)
            ] = ICE
            steps["5"][
                (frames["temp"] < SHUPE["freezing"]["homogeneous"])
                & (steps["5"] == MIXED)
            ] = ICE
            # Above zero you can only have rain, drizzle, or liquid.
            # You can differentiate these with doppler velocity and reflectivity.
            steps["5"][
                (SHUPE["freezing"]["nominal"] <= frames["temp"])
                & (steps["5"] == MIXED)  # Mixed-Phase
            ] = LIQUID
            steps["5"][
                (SHUPE["freezing"]["nominal"] <= frames["temp"]) & (steps["5"] == ICE)
            ] = LIQUID
            steps["5"][
                (SHUPE["freezing"]["nominal"] <= frames["temp"]) & (steps["5"] == SNOW)
            ] = RAIN
            # Step 6 ------------------------------------------------------------------------
            # Make a copy for step 6
            steps["6"] = steps["5"].copy(deep=True)
            # Identify layers and phases
            layers_and_phases = steps["6"].T.apply(self._identify_layers_and_phases)
            # Add liquid if the lwp is greater than 25 but no liquid in the column
            for row in frames["mwr_lwp"].index:
                lwp = frames["mwr_lwp"].loc[row, "mwr_lwp"]
                if SHUPE["occultation"]["lwp"] <= lwp:
                    this_column = layers_and_phases[row]
                    if all(
                        phase["phase"] <= ICE
                        for layer in this_column
                        for phase in layer
                    ):
                        # No liquid was detected
                        lidar_tops = steps["lidar_tops"].loc[row, :]
                        base = lidar_tops[lidar_tops == -1].index.min() - 45
                        if np.isnan(base):
                            # Then use the radar base
                            radar_tops = steps["radar_tops"].loc[row, :]
                            base = radar_tops[radar_tops == -1].index.min() - 45
                            if np.isnan(base):
                                continue
                        # Now we have a base
                        # Is there a top within 500 m
                        # Now we want to find the first top that is within 500 m of the base
                        tops = []
                        for layer in this_column:
                            if layer:
                                tops.append(layer[-1]["top"])
                        top = None
                        for this_top in tops:
                            if 0 < this_top - base <= SHUPE["occultation"]["low"]:
                                top = this_top
                                break
                        if not top:
                            # We need to calculate the thickness
                            thickness = lwp / 0.2
                            top = base + thickness
                        # Now that we have a base and a top
                        # We want to classify everything above the base and below the top as liquid
                        steps["6"].loc[
                            row,
                            (base < steps["6"].columns) & (steps["6"].columns < top),
                        ] = LIQUID
                elif lwp < 0:
                    # Then all liquid containing elements below freezing are set to ice
                    steps["6"].loc[
                        row,
                        (frames["temp"].loc[row, :] < SHUPE["freezing"]["nominal"])
                        & (MIXED <= steps["6"].loc[row, :]),
                    ] = ICE
            # Step 7 ------------------------------------------------------------------------
            # Make a copy for step 7
            steps["7"] = steps["6"].copy(deep=True)
            # Start with all NaN
            for col in steps["7"].columns:
                steps["7"][col].values[:] = np.nan
            times = len(steps["7"].index)
            elevations = len(steps["7"].columns)
            for i, index in enumerate(steps["7"].index):
                if i % 250 == 0:
                    print(f"\t{round(i / times * 100)}%")
                if (i < SHUPE["window"]["buffer"]) or (
                    times - SHUPE["window"]["buffer"] - 1 < i
                ):
                    steps["7"].loc[index, :] = steps["6"].loc[index, :].values
                    # Or you can just pass
                    continue
                for j, column in enumerate(steps["7"].columns):
                    if (j < SHUPE["window"]["buffer"]) or (
                        elevations - SHUPE["window"]["buffer"] - 1 < j
                    ):
                        steps["7"].loc[:, column] = steps["6"].loc[:, column].values
                        continue
                    # If we haven't continued, then we know that we can grab all the values
                    values = steps["6"].iloc[
                        i
                        - SHUPE["window"]["buffer"] : i
                        + SHUPE["window"]["buffer"]
                        + 1,
                        j
                        - SHUPE["window"]["buffer"] : j
                        + SHUPE["window"]["buffer"]
                        + 1,
                    ]
                    if values.count().sum() < SHUPE["window"]["clear"]:
                        # Then we want to classify the central one as clear
                        # But step 7 is already all nan
                        # so we just continue
                        continue
                    else:
                        # The center value currently is
                        center = steps["6"].loc[index, column]
                        try:
                            match_center_count = (
                                values.apply(pd.Series.value_counts)
                                .fillna(0)
                                .loc[center, :]
                                .sum()
                            )
                        except KeyError:
                            match_center_count = 0
                        if SHUPE["window"]["match"] < match_center_count:
                            steps["7"].loc[index, column] = center
                        else:
                            # Use the mode
                            mode = values.mode().T.mode().iloc[0, 0]
                            steps["7"].loc[index, column] = mode
            # Step 8 ------------------------------------------------------------------------
            # Make a copy for step 8
            steps["8"] = steps["7"].copy(deep=True)
            # Reidentify phases and layers
            layers_and_phases = steps["8"].T.apply(self._identify_layers_and_phases)
            # Now check the reclassification
            for time in steps["8"].index:
                for layer in layers_and_phases[time]:
                    if 2 <= len(layer):
                        for i in range(len(layer)):
                            above = None
                            below = None
                            if i == 0:
                                # Then you can only look above
                                above = layer[i + 1]["phase"]
                            elif i == len(layer) - 1:
                                # You can only look below
                                below = layer[i - 1]["phase"]
                            else:
                                # You look above and below
                                above = layer[i + 1]["phase"]
                                below = layer[i - 1]["phase"]
                            phase = layer[i]["phase"]
                            depth = layer[i]["depth"]
                            new_phase = None
                            if (phase == ICE) and (depth < 200) and (below == MIXED):
                                new_phase = MIXED
                            elif (phase == ICE) and (depth < 200) and (below == LIQUID):
                                new_phase = LIQUID
                            elif (phase == LIQUID) and (above == DRIZZLE):
                                new_phase = DRIZZLE
                            elif (phase == DRIZZLE) and (above == ICE):
                                new_phase = ICE
                            elif (phase == DRIZZLE) and (below == ICE):
                                new_phase = ICE
                            elif (phase == DRIZZLE) and (above == MIXED):
                                new_phase = MIXED
                            elif (phase == DRIZZLE) and (below == MIXED):
                                new_phase = MIXED
                            # Set new phase if required
                            if new_phase:
                                base = layer[i]["base"]
                                top = layer[i]["top"]
                                steps["8"].loc[
                                    time,
                                    (base < steps["8"].columns)
                                    & (steps["8"].columns < top),
                                ] = new_phase
            filepath: Path = Path.cwd() / (
                f"D{target.year}"
                f"-{str(target.month).zfill(2)}"
                f"-{str(target.day).zfill(2)}"
                f"-{request.observatory.name.lower()}"
                "-mask_steps"
                ".pkl"
            )
            with open(filepath, "wb") as file:
                pickle.dump(steps, file)
            # Add to blob storage
            self.instrument_access.add_blob(
                name=request.observatory.name.lower(),
                path=filepath,
                directory=f"mask_steps/daily/{request.year}/",
            )
            # Remove the file
            os.remove(filepath)

    def reclassify_mixed_columns(self, request: ObservatoryRequest) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"mask_steps/daily/{request.year}/",
        )
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
            # Now that I have the blob (pkl) I need to download it
            # There is only one in each selected
            name: str = selected[0]
            filename = self.instrument_access.download_blob(
                container=request.observatory.name.lower(),
                name=name,
            )
            # Unpickle the dataframes [steps]
            filepath: Path = Path.cwd() / filename
            with open(filepath, "rb") as file:
                steps = pickle.load(file)
            os.remove(filepath)
            reference = steps["8"]
            # Start with a copy
            phase_map = steps["8"].copy(deep=True)
            # Reclassify phases and layers
            phase_map[reference == ICE] = NEW_ICE
            phase_map[reference == SNOW] = NEW_ICE
            phase_map[reference == LIQUID] = NEW_LIQUID
            phase_map[reference == DRIZZLE] = NEW_LIQUID
            phase_map[reference == RAIN] = NEW_LIQUID
            layers_and_phases = phase_map.T.apply(self._identify_layers_and_phases)
            # Now check the reclassification
            for time in phase_map.index:
                for layer in layers_and_phases[time]:
                    if 2 <= len(layer):
                        # First find mixed-ice (under liquid or mixed-phase)
                        new_phase = None
                        for i in range(len(layer)):
                            above = None
                            if i == 0:
                                # Then you can only look above
                                above = layer[i + 1]["phase"]
                            elif i == len(layer) - 1:
                                # We don't look below
                                continue
                            else:
                                # You look above and below
                                above = layer[i + 1]["phase"]
                            phase = layer[i]["phase"]
                            # Look for mixed Ice
                            if (phase == NEW_ICE) and (above == MIXED):
                                new_phase = MIXED_ICE
                            elif (phase == NEW_ICE) and (above == NEW_LIQUID):
                                new_phase = MIXED_ICE
                            # Set new phase if required
                            if new_phase:
                                base = layer[i]["base"]
                                top = layer[i]["top"]
                                phase_map.loc[
                                    time,
                                    (base < phase_map.columns)
                                    & (phase_map.columns < top),
                                ] = new_phase
                        # Now find the mixed liquid in the same layer
                        if new_phase:
                            # Then all of the liquid goes to mixed liquid
                            for i in range(len(layer)):
                                if layer[i]["phase"] == NEW_LIQUID:
                                    base = layer[i]["base"]
                                    top = layer[i]["top"]
                                    phase_map.loc[
                                        time,
                                        (base < phase_map.columns)
                                        & (phase_map.columns < top),
                                    ] = MIXED_LIQUID
            # Now save the results
            filepath: Path = Path.cwd() / (
                f"D{target.year}"
                f"-{str(target.month).zfill(2)}"
                f"-{str(target.day).zfill(2)}"
                f"-{request.observatory.name.lower()}"
                "-reclassified_phases"
                ".pkl"
            )
            with open(filepath, "wb") as file:
                pickle.dump(phase_map, file)
            # Add to blob storage
            self.instrument_access.add_blob(
                name=request.observatory.name.lower(),
                path=filepath,
                directory=f"reclassified_phases/daily/{request.year}/",
            )
            # Remove the file
            os.remove(filepath)

    def create_monthly_phase_summary(self, request: ObservatoryRequest) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # The first step is to make all of the zeros
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"reclassified_phases/daily/{request.year}/",
        )
        # The issue that we're having is that we don't know what the indexes are until we get to the
        # first day
        # So, for now, we just need to make the series
        for target in self._dates_in_month(request.year, request.month.value):
            selected: tuple[str, ...] = self.filter_context.apply(
                target,
                blobs,
                strategy=NamesByDate(),
                time=False,
            )
            if not selected:
                continue
            # Now that I have the blob (pkl) I need to download it
            # There is only one in each selected
            name: str = selected[0]
            filename = self.instrument_access.download_blob(
                container=request.observatory.name.lower(),
                name=name,
            )
            # Unpickle the dataframes [steps]
            filepath: Path = Path.cwd() / filename
            with open(filepath, "rb") as file:
                phase_map = pickle.load(file)
            os.remove(filepath)
            # Now we should have the combined steps
            # Create a dict of dataframes to hold the results
            index: list[datetime.date] = list(
                self._dates_in_month(request.year, request.month.value)
            )
            columns: list[int] = phase_map.columns.to_list()
            phases: dict[str, pd.DataFrame] = {
                key: pd.DataFrame(np.nan, index=index, columns=columns)
                for key in [
                    "ice",
                    "mixed_ice",
                    "mixed",
                    "mixed_liquid",
                    "liquid",
                    "all_mixed",
                    "total",
                    "clear",
                ]
            }
            break
        # Now that you have the series with the correct index
        # You can produce the summary counts
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
            # Now that I have the blob (pkl) I need to download it
            # There is only one in each selected
            name: str = selected[0]
            filename = self.instrument_access.download_blob(
                container=request.observatory.name.lower(),
                name=name,
            )
            # Unpickle the dataframes [steps]
            filepath: Path = Path.cwd() / filename
            with open(filepath, "rb") as file:
                phase_map = pickle.load(file)
            os.remove(filepath)
            # Now we are going to go through each day and compile
            # Set zero for all the phases in this day
            for phase in phases:
                phases[phase].loc[target, :] = 0
            for time in phase_map.index:
                this_slice = phase_map.loc[time, :]
                if all(np.isnan(this_slice)):
                    continue
                phases["ice"].loc[target, this_slice == NEW_ICE] += 1
                phases["mixed_ice"].loc[target, this_slice == MIXED_ICE] += 1
                phases["mixed"].loc[target, this_slice == MIXED] += 1
                phases["mixed_liquid"].loc[target, this_slice == MIXED_LIQUID] += 1
                phases["liquid"].loc[target, this_slice == NEW_LIQUID] += 1
                phases["all_mixed"].loc[
                    target, (1 < this_slice) & (this_slice < 5)
                ] += 1
                phases["total"].loc[target, 0 < this_slice] += 1
                phases["clear"].loc[target, this_slice == 0] += 1
            # Now we are done with all of the days in a month
            # Now save the daily results
        filepath: Path = Path.cwd() / (
            f"D{target.year}"
            f"-{str(target.month).zfill(2)}"
            f"-{request.observatory.name.lower()}"
            "-daily_phase_counts"
            ".pkl"
        )
        with open(filepath, "wb") as file:
            pickle.dump(phases, file)
        # Add to blob storage
        self.instrument_access.add_blob(
            name=request.observatory.name.lower(),
            path=filepath,
            directory=f"phase_counts/monthly/{request.year}/",
        )
        # Remove the file
        os.remove(filepath)

    def create_annual_phase_summary(self, request: ObservatoryRequest) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # The first step is to make all of the zeros
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"reclassified_phases/daily/{request.year}/",
        )
        # The issue that we're having is that we don't know what the indexes are until we get to the
        # first day
        # So, for now, we just need to make the series
        for target in self._dates_in_month(request.year, 1):
            selected: tuple[str, ...] = self.filter_context.apply(
                target,
                blobs,
                strategy=NamesByDate(),
                time=False,
            )
            if not selected:
                continue
            # Now that I have the blob (pkl) I need to download it
            # There is only one in each selected
            name: str = selected[0]
            filename = self.instrument_access.download_blob(
                container=request.observatory.name.lower(),
                name=name,
            )
            # Unpickle the dataframes [steps]
            filepath: Path = Path.cwd() / filename
            with open(filepath, "rb") as file:
                phase_map = pickle.load(file)
            os.remove(filepath)
            # Now we should have the combined steps
            # Create a dict of dataframes to hold the results
            # The index is a group of five days at a time.
            index: list[int] = list(range(1, int(365 / 5) + 1))
            columns: list[int] = phase_map.columns.to_list()
            phases: dict[str, pd.DataFrame] = {
                key: pd.DataFrame(0, index=index, columns=columns)
                for key in [
                    "ice",
                    "mixed_ice",
                    "mixed",
                    "mixed_liquid",
                    "liquid",
                    "all_mixed",
                    "total",
                    "clear",
                ]
            }
            break
        # Now that you have the series with the correct index
        # You can produce the summary counts
        for month in range(1, 13):
            for target in self._dates_in_month(request.year, month):
                day_of_year: int = target.timetuple().tm_yday
                week_group: int = round((day_of_year + 2) / 5)
                if int(365 / 5) < week_group:
                    continue
                print(target, day_of_year, week_group)
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # Now that I have the blob (pkl) I need to download it
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                with open(filepath, "rb") as file:
                    phase_map = pickle.load(file)
                os.remove(filepath)
                # Now we are going to go through each day and compile
                for time in phase_map.index:
                    this_slice = phase_map.loc[time, :]
                    if all(np.isnan(this_slice)):
                        continue
                    phases["ice"].loc[week_group, this_slice == NEW_ICE] += 1
                    phases["mixed_ice"].loc[week_group, this_slice == MIXED_ICE] += 1
                    phases["mixed"].loc[week_group, this_slice == MIXED] += 1
                    phases["mixed_liquid"].loc[
                        week_group, this_slice == MIXED_LIQUID
                    ] += 1
                    phases["liquid"].loc[week_group, this_slice == NEW_LIQUID] += 1
                    phases["all_mixed"].loc[
                        week_group, (1 < this_slice) & (this_slice < 5)
                    ] += 1
                    phases["total"].loc[week_group, 0 < this_slice] += 1
                    phases["clear"].loc[week_group, this_slice == 0] += 1
        # Now we are done with all of the days in a month
        # Now save the daily results
        filepath: Path = Path.cwd() / (
            f"{target.year}"
            f"-{request.observatory.name.lower()}"
            "-week_group_phase_counts"
            ".pkl"
        )
        with open(filepath, "wb") as file:
            pickle.dump(phases, file)
        # Add to blob storage
        self.instrument_access.add_blob(
            name=request.observatory.name.lower(),
            path=filepath,
            directory="phase_counts/annual/",
        )
        # Remove the file
        os.remove(filepath)

    def create_annual_phase_summary_by_temp(self, request: ObservatoryRequest) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # The first step is to make all of the zeros
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"reclassified_phases/daily/{request.year}/",
        )
        temperature_blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"resampled_frames/daily/{request.year}/",
        )
        # The issue that we're having is that we don't know what the indexes are until we get to the
        # first day
        # So, for now, we just need to make the series
        for target in self._dates_in_month(request.year, 1):
            selected: tuple[str, ...] = self.filter_context.apply(
                target,
                blobs,
                strategy=NamesByDate(),
                time=False,
            )
            if not selected:
                continue
            # Now that I have the blob (pkl) I need to download it
            # There is only one in each selected
            name: str = selected[0]
            filename = self.instrument_access.download_blob(
                container=request.observatory.name.lower(),
                name=name,
            )
            # Unpickle the dataframes [steps]
            filepath: Path = Path.cwd() / filename
            with open(filepath, "rb") as file:
                phase_map = pickle.load(file)
            os.remove(filepath)
            # Now we should have the combined steps
            # Create a dict of dataframes to hold the results
            # The index is a group of five days at a time.
            index: list[int] = list(range(1, 12 + 1))
            columns: list[int] = phase_map.columns.to_list()
            phases: dict[str, dict[str, pd.DataFrame]] = {
                phase: {
                    temp: pd.DataFrame(0, index=index, columns=columns)
                    for temp in range(-40, 5 + 1, 5)
                }
                for phase in [
                    "ice",
                    "mixed_ice",
                    "mixed",
                    "mixed_liquid",
                    "liquid",
                    "all_mixed",
                    "total",
                    "clear",
                ]
            }
            counts: pd.Series = pd.Series(0, index=index)
            break
        # Now that you have the series with the correct index
        # You can produce the summary counts
        for month in range(1, 13):
            for target in self._dates_in_month(request.year, month):
                print(target)
                # Download the phase map ---------------------------------
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                with open(filepath, "rb") as file:
                    phase_map = pickle.load(file)
                os.remove(filepath)
                # Download the frame with the temperatures ----------------
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    temperature_blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # Now that I have the blob (pkl) I need to download it
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                with open(filepath, "rb") as file:
                    frames = pickle.load(file)
                os.remove(filepath)

                # Now we are going to go through each day and compile
                for time in phase_map.index:
                    counts[month] += 1
                    this_slice = phase_map.loc[time, :]
                    if all(np.isnan(this_slice)):
                        continue
                    for temp in range(-40, 5 + 1, 5):
                        upper = temp
                        lower = temp - 5
                        if temp == -40:
                            lower = -273
                        elif temp == 5:
                            upper = 100
                        # Here is where we also need the temps to filter by
                        temp_slice = frames["temp"].loc[time, :]
                        phases["ice"][temp].loc[
                            month,
                            (this_slice == NEW_ICE)
                            & (lower < temp_slice)
                            & (temp_slice <= upper),
                        ] += 1
                        phases["mixed_ice"][temp].loc[
                            month,
                            (this_slice == MIXED_ICE)
                            & (lower < temp_slice)
                            & (temp_slice <= upper),
                        ] += 1
                        phases["mixed"][temp].loc[
                            month,
                            (this_slice == MIXED)
                            & (lower < temp_slice)
                            & (temp_slice <= upper),
                        ] += 1
                        phases["mixed_liquid"][temp].loc[
                            month,
                            (this_slice == MIXED_LIQUID)
                            & (lower < temp_slice)
                            & (temp_slice <= upper),
                        ] += 1
                        phases["liquid"][temp].loc[
                            month,
                            (this_slice == NEW_LIQUID)
                            & (lower < temp_slice)
                            & (temp_slice <= upper),
                        ] += 1
                        phases["all_mixed"][temp].loc[
                            month,
                            (1 < this_slice)
                            & (this_slice < 5)
                            & (lower < temp_slice)
                            & (temp_slice <= upper),
                        ] += 1
                        phases["total"][temp].loc[
                            month,
                            (0 < this_slice)
                            & (lower < temp_slice)
                            & (temp_slice <= upper),
                        ] += 1
        # Now we are done with all of the days in a month
        # Now save the daily results
        filepath: Path = Path.cwd() / (
            f"{target.year}"
            f"-{request.observatory.name.lower()}"
            "-monthly_phase_counts_by_temp"
            ".pkl"
        )
        result = {
            "phases": phases,
            "counts": counts,
        }
        with open(filepath, "wb") as file:
            pickle.dump(result, file)
        # Add to blob storage
        self.instrument_access.add_blob(
            name=request.observatory.name.lower(),
            path=filepath,
            directory="phase_counts_by_temp/annual/",
        )
        # Remove the file
        os.remove(filepath)

    def create_annual_phase_summary_for_report(
        self, request: ObservatoryRequest
    ) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # The first step is to make all of the zeros
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"reclassified_phases/daily/{request.year}/",
        )
        temperature_blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"resampled_frames/daily/{request.year}/",
        )
        index: list[int] = list(range(1, 12 + 1))
        counts: pd.Series = pd.Series(0, index=index)
        year_data = []
        month_data = []
        temp_data = []
        phase_data = []
        base_data = []
        top_data = []
        depth_data = []
        # Now start building results
        for month in range(1, 13):
            for target in self._dates_in_month(request.year, month):
                print(target)
                # Download the phase map ---------------------------------
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                with open(filepath, "rb") as file:
                    phase_map = pickle.load(file)
                os.remove(filepath)
                # Download the frame with the temperatures ----------------
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    temperature_blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # Now that I have the blob (pkl) I need to download it
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                try:
                    with open(filepath, "rb") as file:
                        frames = pickle.load(file)
                    os.remove(filepath)
                except FileNotFoundError:
                    print("Skipping the file that was not found")
                    continue

                layers_and_phases = phase_map.T.apply(self._identify_layers_and_phases)
                # Now we are going to go through each day and compile
                for time in layers_and_phases.index:
                    counts[month] += 1
                    this_temp_slice = frames["temp"].loc[time, :]
                    for layer in layers_and_phases[time]:
                        for phase_layer in layer:
                            base = phase_layer["base"]
                            top = phase_layer["top"]
                            depth = phase_layer["depth"]
                            # Now append the data
                            year_data.append(request.year)
                            month_data.append(month)
                            base_data.append(base)
                            top_data.append(top)
                            depth_data.append(depth)
                            match phase_layer["phase"]:
                                case 1 | 2:
                                    phase_data.append("ice")
                                case 3:
                                    phase_data.append("mixed")
                                case 4 | 5:
                                    phase_data.append("liquid")
                            # You also need to get the average temp
                            avg_temp = this_temp_slice.loc[
                                (base < this_temp_slice.index)
                                & (this_temp_slice.index < top)
                            ].mean()
                            temp_data.append(avg_temp)
        # Now we are done with all of the days in a month
        # Now save the daily results
        filepath: Path = Path.cwd() / (
            f"{target.year}"
            f"-{request.observatory.name.lower()}"
            "-report_fig_01"
            ".pkl"
        )
        result = pd.DataFrame(
            {
                "year": year_data,
                "month": month_data,
                "base": base_data,
                "top": top_data,
                "depth": depth_data,
                "temp": temp_data,
                "phase": phase_data,
            }
        )
        with open(filepath, "wb") as file:
            pickle.dump(result, file)
        # Add to blob storage
        self.instrument_access.add_blob(
            name=request.observatory.name.lower(),
            path=filepath,
            directory="report_fig/01/annual/",
        )
        # Remove the file
        os.remove(filepath)

    def create_annual_phase_summary_for_report_2(
        self, request: ObservatoryRequest
    ) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # The first step is to make all of the zeros
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"reclassified_phases/daily/{request.year}/",
        )
        index: list[int] = list(range(1, 12 + 1))
        counts: pd.Series = pd.Series(0, index=index)
        # Now that you have the series with the correct index
        # You can produce the summary counts
        year_data = []
        month_data = []
        phase_data = []
        fraction_data = []
        # Things to interate over
        # Now start building results
        for month in range(1, 13):
            ice = 0
            mixed = 0
            liquid = 0
            for target in self._dates_in_month(request.year, month):
                print(target)
                # Download the phase map ---------------------------------
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                with open(filepath, "rb") as file:
                    phase_map = pickle.load(file)
                os.remove(filepath)

                # Now we are going to go through each day and compile
                for time in phase_map.index:
                    counts[month] += 1
                    this_slice = phase_map.loc[time, :]
                    if any(this_slice.isin([1, 2])):
                        ice += 1
                    if any(this_slice.isin([3])):
                        mixed += 1
                    if any(this_slice.isin([4, 5])):
                        liquid += 1
            # ice
            phase_data.append("ice")
            fraction_data.append(ice / counts[month])
            year_data.append(request.year)
            month_data.append(month)
            # mixed
            phase_data.append("mixed")
            fraction_data.append(mixed / counts[month])
            year_data.append(request.year)
            month_data.append(month)
            # liquid
            phase_data.append("liquid")
            fraction_data.append(liquid / counts[month])
            year_data.append(request.year)
            month_data.append(month)
        # Now we are done with all of the days in a month
        # Now save the daily results
        filepath: Path = Path.cwd() / (
            f"{target.year}"
            f"-{request.observatory.name.lower()}"
            "-report_fig_02"
            ".pkl"
        )
        result = pd.DataFrame(
            {
                "year": year_data,
                "month": month_data,
                "phase": phase_data,
                "fraction": fraction_data,
            }
        )
        with open(filepath, "wb") as file:
            pickle.dump(result, file)
        # Add to blob storage
        self.instrument_access.add_blob(
            name=request.observatory.name.lower(),
            path=filepath,
            directory="report_fig/02/annual/",
        )
        # Remove the file
        os.remove(filepath)

    def create_annual_phase_duration_for_report(
        self, request: ObservatoryRequest
    ) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # The first step is to make all of the zeros
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"reclassified_phases/daily/{request.year}/",
        )
        index: list[int] = list(range(1, 12 + 1))
        counts: pd.Series = pd.Series(0, index=index)
        # Now that you have the series with the correct index
        # You can produce the summary counts
        year_data = []
        month_data = []
        phase_data = []
        duration_data = []
        phase_ids = {"ice": [1, 2], "mixed": [3], "liquid": [4, 5]}
        # Things to interate over
        # Now start building results
        for month in range(1, 13):
            # Initial state
            count = {"ice": 0, "mixed": 0, "liquid": 0}
            in_cloud = {"ice": False, "mixed": False, "liquid": False}
            persistence = {"ice": 0, "mixed": 0, "liquid": 0}
            gap = {"ice": 0, "mixed": 0, "liquid": 0}
            in_gap = {"ice": False, "mixed": False, "liquid": False}

            # For each month in the year
            for target in self._dates_in_month(request.year, month):
                print(target)
                # Download the phase map ---------------------------------
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                with open(filepath, "rb") as file:
                    phase_map = pickle.load(file)
                os.remove(filepath)

                # Now we are going to go through each day and compile
                for time in phase_map.index:
                    counts[month] += 1
                    this_slice = phase_map.loc[time, :]
                    for phase in count.keys():
                        if any(this_slice.isin(phase_ids[phase])):
                            if in_cloud[phase]:
                                if in_gap[phase]:
                                    # I think this line is the issue,
                                    persistence[phase] += gap[phase]
                                    in_gap[phase] = False
                                    gap[phase] = 0
                                persistence[phase] += 1
                            else:  # Not in cloud
                                count[phase] += 1
                                if count[phase] == SHUPE["persistence"]["thresh"]:
                                    in_cloud[phase] = True
                                    persistence[phase] = count[phase]
                        elif in_gap[phase]:
                            gap[phase] += 1
                            if gap[phase] > SHUPE["persistence"]["thresh"]:
                                year_data.append(request.year)
                                month_data.append(month)
                                phase_data.append(phase)
                                duration_data.append(persistence[phase])
                                # Reset everything
                                count[phase] = 0
                                in_cloud[phase] = False
                                gap[phase] = 0
                                in_gap[phase] = False
                                persistence[phase] = 0
                        elif in_cloud[phase]:
                            in_gap[phase] = True
                            gap[phase] = 1
                        else:  # No gap and no cloud
                            count[phase] = 0
            for phase in count.keys():
                if in_cloud[phase]:
                    year_data.append(request.year)
                    month_data.append(month)
                    phase_data.append(phase)
                    duration_data.append(persistence[phase])
        # Now we are done with all of the days in a month
        # Now save the daily results
        filepath: Path = Path.cwd() / (
            f"{target.year}"
            f"-{request.observatory.name.lower()}"
            "-report_fig_03"
            ".pkl"
        )
        result = pd.DataFrame(
            {
                "year": year_data,
                "month": month_data,
                "phase": phase_data,
                "duration": duration_data,
            }
        )
        with open(filepath, "wb") as file:
            pickle.dump(result, file)
        # Add to blob storage
        self.instrument_access.add_blob(
            name=request.observatory.name.lower(),
            path=filepath,
            directory="report_fig/03/annual/",
        )
        # Remove the file
        os.remove(filepath)

    def create_annual_correlation_timeseries(self, request: ObservatoryRequest) -> None:
        """TODO: Docstring."""
        # The first step is to make all of the zeros
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"reclassified_phases/daily/{request.year}/",
        )
        temperature_blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"resampled_frames/daily/{request.year}/",
        )
        index: list[int] = list(range(1, 12 + 1))
        # counts: pd.Series = pd.Series(0, index=index)
        year_data = []
        month_data = []
        temp_data = []
        phase_data = []
        base_data = []
        top_data = []
        depth_data = []
        datetime_data = []
        # Now start building results
        for month in range(1, 13):
            for target in self._dates_in_month(request.year, month):
                print(target)
                # Download the phase map ---------------------------------
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                with open(filepath, "rb") as file:
                    phase_map = pickle.load(file)
                os.remove(filepath)
                # Download the frame with the temperatures ----------------
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    temperature_blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # Now that I have the blob (pkl) I need to download it
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                try:
                    with open(filepath, "rb") as file:
                        frames = pickle.load(file)
                    os.remove(filepath)
                except FileNotFoundError:
                    print("Skipping the file that was not found")
                    continue

                layers_and_phases = phase_map.T.apply(self._identify_layers_and_phases)
                # Now we are going to go through each day and compile
                for time in layers_and_phases.index:
                    # counts[month] += 1
                    # NOTE: IT SEEMS LIKE WE HAVE THE FIRST TIMESTAMP REPEATED IN THESE THINGS!!!
                    # TODO: You might need to remove the last timestamp from each of these
                    time_stamp: datetime = datetime(
                        target.year, target.month, target.day, tzinfo=timezone.utc
                    ) + timedelta(seconds=time)
                    if time_stamp.date() != target:
                        continue
                    this_temp_slice = frames["temp"].loc[time, :]
                    if len(layers_and_phases[time]) == 0:
                        year_data.append(request.year)
                        month_data.append(month)
                        base_data.append(np.nan)
                        top_data.append(np.nan)
                        depth_data.append(np.nan)
                        phase_data.append(np.nan)
                        temp_data.append(np.nan)
                        datetime_data.append(time_stamp)
                        continue
                    layer = layers_and_phases[time][0][0]
                    base = layer["base"]
                    top = layer["top"]
                    depth = layer["depth"]
                    # Now append the data
                    year_data.append(request.year)
                    month_data.append(month)
                    base_data.append(base)
                    top_data.append(top)
                    depth_data.append(depth)
                    match layer["phase"]:
                        case 1 | 2:
                            phase_data.append("ice")
                        case 3:
                            phase_data.append("mixed")
                        case 4 | 5:
                            phase_data.append("liquid")
                    # You also need to get the average temp
                    avg_temp = this_temp_slice.loc[
                        (base < this_temp_slice.index) & (this_temp_slice.index < top)
                    ].mean()
                    temp_data.append(avg_temp)
                    # Finally add the time_stamp
                    datetime_data.append(time_stamp)
        # Now we are done with all of the days in a month
        # Now save the daily results
        filepath: Path = Path.cwd() / (
            f"{target.year}"
            f"-{request.observatory.name.lower()}"
            "-first_layer_timeseries"
            ".pkl"
        )
        result = pd.DataFrame(
            {
                "year": year_data,
                "month": month_data,
                "base": base_data,
                "top": top_data,
                "depth": depth_data,
                "temp": temp_data,
                "phase": phase_data,
                "datetime": datetime_data,
            }
        )
        with open(filepath, "wb") as file:
            pickle.dump(result, file)
        # Add to blob storage
        self.instrument_access.add_blob(
            name=request.observatory.name.lower(),
            path=filepath,
            directory="results/correlation_timeseries/annual/",
        )
        # Remove the file
        os.remove(filepath)

    def create_annual_structure_summary(self, request: ObservatoryRequest) -> None:
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"reclassified_phases/daily/{request.year}/",
        )
        monthly_counts = pd.DataFrame(
            {"year": [request.year] * 12, "total": [0] * 12}, index=range(1, 13)
        )
        years = []
        months = []
        structures = []
        phase_layers = []
        cloud_layers = []
        bases = []
        tops = []
        depths = []
        for month in range(1, 13):
            for target in self._dates_in_month(request.year, month):
                print(target)
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # Now that I have the blob (pkl) I need to download it
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                with open(filepath, "rb") as file:
                    phase_map = pickle.load(file)
                os.remove(filepath)
                # Now we are going to go through each day and compile
                layers_and_phases = phase_map.T.apply(self._identify_layers_and_phases)
                # extract structure
                for seconds in layers_and_phases.index:
                    monthly_counts.loc[month, "total"] += 1
                    cloud_layer = 0
                    for layer in layers_and_phases[seconds]:
                        structure = ""
                        if layer:
                            base = layer[0]["base"]
                            top = layer[-1]["top"]
                            depth = top - base
                            if (base < MIN_BASE) and (depth < MIN_DEPTH):
                                continue
                            cloud_layer += 1
                        for phase in layer:
                            if phase["phase"] in RECLASSIFIED["ice"]:
                                structure += "I"
                            elif phase["phase"] in RECLASSIFIED["liquid"]:
                                structure += "L"
                            elif phase["phase"] == MIXED:
                                structure += "M"
                        # Now you're done with the structure
                        structures.append(structure)
                        phase_layers.append(len(structure))
                        cloud_layers.append(cloud_layer)
                        years.append(request.year)
                        months.append(month)
                        bases.append(base)
                        tops.append(top)
                        depths.append(depth)
        # Now make the dataframe
        results = pd.DataFrame(
            {
                "year": years,
                "month": months,
                "base": bases,
                "top": tops,
                "depth": depths,
                "structure": structures,
                "phase_layer": phase_layers,
                "cloud_layer": cloud_layers,
            }
        )
        filepath: Path = Path.cwd() / (
            f"D{target.year}"
            f"-{request.observatory.name.lower()}"
            "-phase_structure"
            ".pkl"
        )
        results.to_pickle(filepath)
        # Add to blob storage
        self.instrument_access.add_blob(
            name=request.observatory.name.lower(),
            path=filepath,
            directory="results/structure/annual/",
        )
        # Remove the file
        os.remove(filepath)
        # Do the same with the monthly counts
        filepath: Path = Path.cwd() / (
            f"D{target.year}"
            f"-{request.observatory.name.lower()}"
            "-monthly_counts"
            ".pkl"
        )
        monthly_counts.to_pickle(filepath)
        # Add to blob storage
        self.instrument_access.add_blob(
            name=request.observatory.name.lower(),
            path=filepath,
            directory="results/monthly_counts/annual/",
        )
        # Remove the file
        os.remove(filepath)

    def create_annual_lwp_ts(self, request: ObservatoryRequest) -> None:
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"resampled_frames/daily/{request.year}/",
        )
        years = []
        months = []
        timestamps = []
        values = []
        for month in range(1, 13):
            for target in self._dates_in_month(request.year, month):
                initial_datetime = datetime(
                    year=target.year,
                    month=target.month,
                    day=target.day,
                    tzinfo=timezone.utc,
                )
                print(target)
                selected: tuple[str, ...] = self.filter_context.apply(
                    target,
                    blobs,
                    strategy=NamesByDate(),
                    time=False,
                )
                if not selected:
                    continue
                # Now that I have the blob (pkl) I need to download it
                # There is only one in each selected
                name: str = selected[0]
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                # Unpickle the dataframes [steps]
                filepath: Path = Path.cwd() / filename
                with open(filepath, "rb") as file:
                    data = pickle.load(file)
                os.remove(filepath)
                lwp = data["mwr_lwp"]
                # Now we are going to go through each day and compile
                timestamps += [
                    initial_datetime + timedelta(seconds=i) for i in lwp.index
                ]
                values += [i[0] for i in lwp.values]
                months += [month] * len(lwp.index)
                years += [request.year] * len(lwp.index)
        results = pd.DataFrame(
            {
                "year": years,
                "month": months,
                "lwp": values,
                "timestamps": timestamps,
            }
        )
        filepath: Path = Path.cwd() / (
            f"D{target.year}-{request.observatory.name.lower()}-mwr_lwp.pkl"
        )
        results.to_pickle(filepath)
        # Add to blob storage
        self.instrument_access.add_blob(
            name=request.observatory.name.lower(),
            path=filepath,
            directory="results/lwp/annual/",
        )
        # Remove the file
        os.remove(filepath)

    def _persistence(self, data) -> int:
        """NOTE: This is just an example of what the algorithm should look like."""
        # Initialize the parameters ---------------------------------------------
        count = 0
        in_cloud: bool = False
        persistence = 0
        gap = 0
        in_gap = False
        result = []
        # Iterate through each data point ---------------------------------------
        for d in data:
            if d == 1:
                if in_cloud:
                    if in_gap:
                        persistence += gap
                        in_gap = False
                        gap = 0
                    persistence += 1
                else:  # Not in cloud
                    count += 1
                    if count == SHUPE["persistence"]["thresh"]:
                        # We found 30 mins of a cloud and can start logging
                        in_cloud = True
                        persistence = count
            elif in_gap:
                gap += 1
                if gap > SHUPE["persistence"]["thresh"]:
                    # Now we know we were in a gap that got longer than 30
                    # This is the end of a duration of a cloud
                    result.append(persistence)
                    # Reset everything
                    count = 0
                    in_cloud = False
                    gap = 0
                    in_gap = False
            elif in_cloud:
                in_gap = True
                gap = 1
            else:  # No gap and no cloud
                count = 0
        if in_cloud:
            result.append(persistence)
        return result

    # NOTE: Most likely depreciated
    def create_monthly_elevation_by_phase(self, request: ObservatoryRequest) -> None:
        """TODO: Docstring."""
        # Get a list of all the relevant blobs
        blobs: dict[str, tuple[str, ...]] = {}
        blobs["steps"] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"mask_steps/daily/{request.year}/",
        )
        blobs["frames"] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"resampled_frames/daily/{request.year}/",
        )
        for target in self._dates_in_month(request.year, request.month.value):
            print(target)
            selected: dict[str, tuple[str, ...]] = {}
            selected["steps"] = self.filter_context.apply(
                target,
                blobs["steps"],
                strategy=NamesByDate(),
                time=False,
            )
            selected["frames"] = self.filter_context.apply(
                target,
                blobs["frames"],
                strategy=NamesByDate(),
                time=False,
            )
            if not all(selected.values):
                continue
            # Now that I have the blob (pkl) I need to download it
            # There is only one in each selected
            name: str = selected[0]
            filename = self.instrument_access.download_blob(
                container=request.observatory.name.lower(),
                name=name,
            )
            # Rather than yield the instrument data, you just want to unpickle the dataframes
            filepath: Path = Path.cwd() / filename
            with open(filepath, "rb") as file:
                steps = pickle.load(file)
            os.remove(filepath)
            # Now we should have the combined frames
            print("You are here")
            for t in steps["5"].index:
                slice_ = steps["5"].loc[t, :]
                if all(np.isnan(slice_)):
                    pass
            # NOTE: This is the end of it
            filepath: Path = Path.cwd() / (
                f"D{target.year}"
                f"-{str(target.month).zfill(2)}"
                f"-{str(target.day).zfill(2)}"
                f"-{request.observatory.name.lower()}"
                "-mask_steps"
                ".pkl"
            )
            with open(filepath, "wb") as file:
                pickle.dump(steps, file)
            # Add to blob storage
            self.instrument_access.add_blob(
                name=request.observatory.name.lower(),
                path=filepath,
                directory=f"mask_steps/daily/{request.year}/",
            )
            # Remove the file
            os.remove(filepath)

    # NOTE: Most likely depreciated
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
                case (Observatory.EUREKA, Instrument.MMCR):
                    # NOTE: You can use the single MmcrDaily Strategy
                    # TODO: Rename this from ShebaMmcrDaily to MmcrDaily
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
            length: int = 3
            scale: int = 100
            dtype: DType = DType.I2
            match (request.observatory, request.instrument):
                case (Observatory.EUREKA, Instrument.MMCR):
                    height: int = 2
                    long_name: str = "Radar Cloud Mask"
                    name: str = "refl"
                    threshold: Threshold = Threshold(
                        value=10, direction=Direction.LESS_THAN
                    )
                case (Observatory.SHEBA, Instrument.DABUL):
                    height: int = 3
                    long_name: str = "Lidar Cloud Mask"
                    name: str = "far_par"
                    threshold: Threshold = Threshold(
                        value=55, direction=Direction.GREATER_THAN
                    )
                case (Observatory.SHEBA, Instrument.MMCR):
                    height: int = 2
                    long_name: str = "Radar Cloud Mask"
                    name: str = "refl"
                    threshold: Threshold = Threshold(
                        value=10, direction=Direction.LESS_THAN
                    )
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
            data.variables["cloud_mask"] = Variable(
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
            # Serialize the data.
            filepath: Path = self.transformation_context.serialize(
                target, data, request
            )
            # Add to blob storage
            self.instrument_access.add_blob(
                name=request.observatory.name.lower(),
                path=filepath,
                directory=f"{request.instrument.name.lower()}/masks/{request.year}/threshold_{threshold.value}/",
            )
            # Remove the file
            os.remove(filepath)

    # NOTE: Most likely depreciated
    def merge_daily_masks(self, request: ObservatoryRequest) -> None:
        """Merge daily masks for a given observatory, month and year.

        TODO: The logic belogs in an engine (Transformation).
        """
        # Get a list of all the relevant blobs
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
                    instrument_data.variables["cloud_mask"].values,
                    index=instrument_data.variables["offset"].values,
                    columns=instrument_data.variables["range"].values,
                )
                for instrument, instrument_data in data.items()
            }
            # Set up the new merged mask
            max_elevation: int = min(df.columns.max() for df in dataframes.values())
            times: list[int] = list(range(0, SECONDS_PER_DAY + 1, STEPS["time"]))
            elevations: list[int] = list(
                range(0, max_elevation + 1, STEPS["elevation"])
            )
            mask: list[list[int]] = [[0 for _ in elevations] for _ in times]
            for i, time in enumerate(times):
                selected_times: dict[Instrument, list[bool]] = {
                    key: [
                        a and b
                        for a, b in zip(
                            time - OFFSETS["time"] <= df.index,
                            df.index < time + OFFSETS["time"],
                        )
                    ]
                    for key, df in dataframes.items()
                }
                for j, elevation in enumerate(elevations):
                    if elevation < MIN_ELEVATION:
                        continue
                    selected_elevations: dict[Instrument, list[bool]] = {}
                    values: dict[Instrument, pd.DataFrame] = {}
                    sizes: dict[Instrument, int] = {}
                    means: dict[Instrument, float] = {}
                    for inst, df in dataframes.items():
                        selected_elevations[inst] = [
                            a and b
                            for a, b in zip(
                                elevation - OFFSETS["elevation"] <= df.columns,
                                df.columns < elevation + OFFSETS["elevation"],
                            )
                        ]
                        values[inst] = df.iloc[
                            selected_times[inst], selected_elevations[inst]
                        ]
                        sizes[inst] = values[inst].size
                        means[inst] = values[inst].mean().mean()
                    # Now set the value of the flags
                    CLOUD = DType.I1.min
                    NO_CLOUD = DType.I1.min
                    if not any(sizes.values()):
                        mask[i][j] = -6  # Missing all data
                        continue
                    elif all(DType.I1.min in df.values for df in values.values()):
                        if not any(
                            ONE_HALF <= df.replace(DType.I1.min, 0).mean().mean()
                            for df in values.values()
                        ):
                            mask[i][j] = 0
                            continue
                        for instrument, df in values.items():
                            if ONE_HALF <= df.replace(DType.I1.min, 0).mean().mean():
                                match instrument:
                                    case (
                                        Instrument.AHSRL
                                        | Instrument.DABUL
                                        | Instrument.MPL
                                    ):
                                        # This is when the lidar is greater than 0.5 while the radar has flags
                                        mask[i][j] = 1
                                    case Instrument.MMCR:
                                        # This is when the radar is greater than 0.5 while the lidar has flags
                                        mask[i][j] = 2
                                break
                        continue
                    elif not all(sizes.values()):  # At least one is empty
                        for instrument, size in sizes.items():
                            if not size:
                                match instrument:
                                    case (
                                        Instrument.AHSRL
                                        | Instrument.DABUL
                                        | Instrument.MPL
                                    ):
                                        # Cloud detected by radar with EMPTY lidar signal
                                        CLOUD = 4
                                        # No cloud detected by radar with EMPTY lidar signal
                                        NO_CLOUD = -4
                                    case Instrument.MMCR:
                                        # Cloud detected by lidar with EMPTY radar signal
                                        CLOUD = 5
                                        # No cloud detected by lidar with EMPTY radar signal
                                        NO_CLOUD = -5
                                break
                    elif any(DType.I1.min in df.values for df in values.values()):
                        # The Flag is in at lease one
                        for instrument, df in values.items():
                            if DType.I1.min in df.values:
                                match instrument:
                                    case (
                                        Instrument.AHSRL
                                        | Instrument.DABUL
                                        | Instrument.MPL
                                    ):
                                        # Cloud detected by radar with both signals available
                                        CLOUD = 2
                                        # No cloud detected by radar with both signals available
                                        NO_CLOUD = -2
                                    case Instrument.MMCR:
                                        # Cloud detected by lidar with both signals available
                                        CLOUD = 1
                                        # No cloud detected by lidar with both signals available
                                        NO_CLOUD = -1
                                break
                    elif all(ONE_HALF <= i for i in means.values()):
                        # Then both of the signals say there is a cloud
                        mask[i][j] = 3
                        continue
                    elif any(ONE_HALF <= i for i in means.values()):
                        # Then only one is saying there is a value
                        for instrument, df in values.items():
                            if means[instrument] < ONE_HALF:
                                match instrument:
                                    case (
                                        Instrument.AHSRL
                                        | Instrument.DABUL
                                        | Instrument.MPL
                                    ):
                                        # Lidar less than 1/2 but not radar
                                        mask[i][j] = 2
                                    case Instrument.MMCR:
                                        # Radar less than 1/2 but not lidar
                                        mask[i][j] = 1
                                break
                        continue
                    else:  # all means are less than 0.5 (Clear by both)
                        mask[i][j] = -3
                        continue
                    mask[i][j] = (
                        CLOUD
                        if any(ONE_HALF <= v.mean().mean() for v in values.values())
                        else NO_CLOUD
                    )
            # NOTE: SPEED THINGS UP
            # with open("mask_list.pkl", "rb") as file:
            #     mask = pickle.load(file)
            mask: pd.DataFrame = pd.DataFrame(
                mask,
                index=times,
                columns=elevations,
            )
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
                    dtype=DType.I1,
                    long_name="Cloud Mask",
                    scale=Scales.ONE,
                    units=Units.NONE,
                    values=tuple(tuple(j for j in mask.loc[i][:]) for i in mask.index),
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

    def extract_daily_extents(self, request: ObservatoryRequest) -> None:
        """Extract daily cloud extent from combined masks for a given observatory, month and year.

        TODO: The logic belogs in an engine (Transformation).
        """
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"combined_masks/{request.year}/",
        )
        # Extract the data for each day
        for target in self._dates_in_month(request.year, request.month.value):
            print(target)
            selected: tuple[str, ...] = self.filter_context.apply(
                target, blobs, strategy=NamesByDate(), time=False
            )
            if not selected:
                continue
            # Generate a InstrumentData of the Mask
            results: tuple[InstrumentData, ...] = tuple(
                self._generate_data(
                    selected,
                    request,
                    strategy=Masks(),
                )
            )
            if not results:
                continue
            # There should only be one value in the result
            data: InstrumentData = results[0]
            # Convert to DataFrames for processing
            # NOTE: This could be done with a transformation strategy as well.
            # TODO: Use a transformation strategy here.
            dataframe: pd.DataFrame = pd.DataFrame(
                data.variables["cloud_mask"].values,
                index=data.variables["offset"].values,
                columns=data.variables["range"].values,
            )
            # NOTE: This looks like an internal method.
            # NOTE: Or a method that belongs in the engine.
            base_time: datetime = datetime(
                target.year, target.month, target.day, tzinfo=timezone.utc
            )
            result: list[VerticalLayers] = []
            for i, offset in enumerate(dataframe.index):
                below: int = VERTICAL_RAIL
                bases: list[VerticalTransition] = []
                tops: list[VerticalTransition] = []
                for j, elevation in enumerate(dataframe.columns[:-1]):
                    if elevation < MIN_ELEVATION:
                        continue
                    current: int = int(dataframe.iloc[i, j])
                    above: int = int(dataframe.iloc[i, j + 1])
                    if below <= 0 < current:
                        bases.append(
                            VerticalTransition(
                                elevation=elevation - OFFSETS["elevation"],
                                code=MaskCode(bottom=below, top=current),
                            )
                        )
                    if above <= 0 < current:
                        tops.append(
                            VerticalTransition(
                                elevation=elevation + OFFSETS["elevation"],
                                code=MaskCode(bottom=current, top=above),
                            )
                        )
                    # But before moving on, set below to current
                    below = int(current)
                # Now, you're one away from the top
                current = dataframe.iloc[i, j + 1]
                if 0 < current:
                    tops.append(
                        VerticalTransition(
                            elevation=elevation + OFFSETS["elevation"],
                            code=MaskCode(bottom=current, top=VERTICAL_RAIL),
                        )
                    )
                    if below <= 0:
                        bases.append(
                            VerticalTransition(
                                elevation=elevation - OFFSETS["elevation"],
                                code=MaskCode(bottom=below, top=current),
                            )
                        )
                # Now that you are done with the time slice create VerticalLayers
                result.append(
                    VerticalLayers(
                        datetime=base_time + timedelta(seconds=offset),
                        bases=tuple(bases),
                        tops=tuple(tops),
                    )
                )
            # Searalize via pkl
            filepath: Path = Path(
                f"D{request.year}"
                f"-{str(request.month.value).zfill(2)}"
                f"-{str(target.day).zfill(2)}"
                f"-cloud-stats-{request.observatory.name.lower()}.pkl"
            )
            with open(filepath, "wb") as file:
                pickle.dump(tuple(result), file)
            # Persist blob
            self.instrument_access.add_blob(
                name=request.observatory.name.lower(),
                path=filepath,
                directory=f"vertical_extent/{request.year}/",
            )
            # Remove the file
            os.remove(filepath)

    @staticmethod
    def _identify_layers_and_phases(series: pd.Series):
        # So, when you come into here, you want to make it easy for yourself
        # to summarize the layers as well as the phases
        # You may need to use this two times.
        below = np.nan
        in_layer = False
        atmospheric_column = []  # Start with a clear column (free of clouds)
        for pointer, index in enumerate(series.index[:-1]):
            center = series[index]
            above = series.iloc[pointer + 1]
            if np.isnan(below) and not np.isnan(center):
                # As soon as we come in, we create a new layer list
                layer_phase_extents = []
                base = index - 45
                in_layer = True
                phase = center
            if in_layer and phase != center:
                # Then you need to go ahead and append the phase
                top = index - 45
                depth = top - base
                layer_phase_extents.append(
                    {
                        "base": base,
                        "top": top,
                        "depth": depth,
                        "phase": int(phase),
                    }
                )
                # Then update the base and phase
                base = top
                phase = center
            if in_layer and np.isnan(above):
                top = index + 45
                depth = top - base
                # Add the layer information
                layer_phase_extents.append(
                    {
                        "base": base,
                        "top": top,
                        "depth": top - base,
                        "phase": int(phase),
                    }
                )
                # Now that you have closed this layer, you want to append layers to results
                atmospheric_column.append(layer_phase_extents)
                # Now you're out of the layer
                in_layer = False
            # Update the below before moving on
            below = center
        # Now that you've gone through all except the last one, handle the edge
        index = series.index[-1]  # Use the last index
        center = series[index]  # Center on the top
        if in_layer:
            # This means the one below was not nan and center is not nan, else it would have been a top
            # So, if we're in layer at the top then we need to say that's it
            # This is the top of the layer.
            if center != phase:
                top = index - 45
                depth = top - base
                layer_phase_extents.append(
                    {
                        "base": base,
                        "top": top,
                        "depth": depth,
                        "phase": int(phase),
                    }
                )
                # Then update the base and phase
                base = top
            top = index + 45
            phase = center
            depth = top - base
            layer_phase_extents.append(
                {
                    "base": base,
                    "top": top,
                    "depth": depth,
                    "phase": int(phase),
                }
            )
            atmospheric_column.append(layer_phase_extents)
        elif not np.isnan(center):
            top = index + 45
            phase = center
            base = index - 45
            depth = top - base
            try:
                layer_phase_extents.append(
                    {
                        "base": base,
                        "top": top,
                        "depth": depth,
                        "phase": int(phase),
                    }
                )
            except NameError:
                layer_phase_extents = []
                layer_phase_extents.append(
                    {
                        "base": base,
                        "top": top,
                        "depth": depth,
                        "phase": int(phase),
                    }
                )
        return atmospheric_column

    # def make_fig_3_bases(self, request: ObservatoryRequest) -> None:
    #     """Extract fractioin of the time that lidar detected the base."""
    #     # Get a list of all the relevant blobs
    #     blobs: tuple[str, ...] = self.instrument_access.list_blobs(
    #         container=request.observatory.name.lower(),
    #         name_starts_with=f"vertical_extent/{request.year}/",
    #     )
    #     # Extract the data for each day
    #     total: int = 0
    #     lidar: int = 0
    #     radar: int = 0
    #     both: int = 0
    #     for target in self._dates_in_month(request.year, request.month.value):
    #         print(target)
    #         selected: tuple[str, ...] = self.filter_context.apply(
    #             target, blobs, strategy=NamesByDate(), time=False
    #         )
    #         if not selected:
    #             continue
    #         # Read the pickle file
    #         layers: tuple[VerticalLayers, ...] = self._read_pickle(selected[0], request)
    #         if not layers:
    #             continue
    #         for time_slice in layers:
    #             total += 1
    #             try:
    #                 match time_slice.bases[0].code.top:
    #                     case 1:
    #                         lidar += 1
    #                     case 2:
    #                         radar += 1
    #                     case 3:
    #                         both += 1
    #             except IndexError:
    #                 continue
    #         # Now that you have gone through all of the times,
    #         # You need to save the total, lidar, radar, and both
    #         # Then you can start to make the plot
    #     return {"total": total, "both": both, "lidar": lidar, "radar": radar}
    #     # # Searalize via pkl
    #     # filepath: Path = Path(
    #     #     f"D{request.year}"
    #     #     f"-{str(request.month.value).zfill(2)}"
    #     #     f"-{str(target.day).zfill(2)}"
    #     #     f"-cloud-stats-{request.observatory.name.lower()}.pkl"
    #     # )
    #     # with open(filepath, "wb") as file:
    #     #     pickle.dump(tuple(result), file)
    #     # # Persist blob
    #     # self.instrument_access.add_blob(
    #     #     name=request.observatory.name.lower(),
    #     #     path=filepath,
    #     #     directory=f"vertical_extent/{request.year}/",
    #     # )
    #     # # Remove the file
    #     # os.remove(filepath)

    # def make_fig_3_tops(self, request: ObservatoryRequest) -> None:
    #     """Extract fractioin of the time that lidar detected the base."""
    #     # Get a list of all the relevant blobs
    #     blobs: tuple[str, ...] = self.instrument_access.list_blobs(
    #         container=request.observatory.name.lower(),
    #         name_starts_with=f"vertical_extent/{request.year}/",
    #     )
    #     # Extract the data for each day
    #     total: int = 0
    #     lidar: int = 0
    #     radar: int = 0
    #     both: int = 0
    #     for target in self._dates_in_month(request.year, request.month.value):
    #         print(target)
    #         selected: tuple[str, ...] = self.filter_context.apply(
    #             target, blobs, strategy=NamesByDate(), time=False
    #         )
    #         if not selected:
    #             continue
    #         # Read the pickle file
    #         layers: tuple[VerticalLayers, ...] = self._read_pickle(selected[0], request)
    #         if not layers:
    #             continue
    #         for time_slice in layers:
    #             total += 1
    #             try:
    #                 match time_slice.tops[0].code.bottom:
    #                     case 1:
    #                         lidar += 1
    #                     case 2:
    #                         radar += 1
    #                     case 3:
    #                         both += 1
    #             except IndexError:
    #                 continue
    #         # Now that you have gone through all of the times,
    #         # You need to save the total, lidar, radar, and both
    #         # Then you can start to make the plot
    #     return {"total": total, "both": both, "lidar": lidar, "radar": radar}

    # def make_fig_4_layers(self, request: ObservatoryRequest) -> None:
    #     """Extract fractioin of the time that lidar detected the base."""
    #     # Get a list of all the relevant blobs
    #     blobs: tuple[str, ...] = self.instrument_access.list_blobs(
    #         container=request.observatory.name.lower(),
    #         name_starts_with=f"vertical_extent/{request.year}/",
    #     )
    #     # Extract the data for each day
    #     zero = 0
    #     one = 0
    #     two = 0
    #     three = 0
    #     four = 0
    #     five = 0
    #     for target in self._dates_in_month(request.year, request.month.value):
    #         print(target)
    #         selected: tuple[str, ...] = self.filter_context.apply(
    #             target, blobs, strategy=NamesByDate(), time=False
    #         )
    #         if not selected:
    #             continue
    #         # Read the pickle file
    #         layers: tuple[VerticalLayers, ...] = self._read_pickle(selected[0], request)
    #         if not layers:
    #             continue
    #         for time_slice in layers:
    #             layers = len(time_slice.bases)
    #             match layers:
    #                 case 0:
    #                     zero += 1
    #                 case 1:
    #                     one += 1
    #                 case 2:
    #                     two += 1
    #                 case 3:
    #                     three += 1
    #                 case 4:
    #                     four += 1
    #                 case 5:
    #                     five += 1
    #                 case _:
    #                     five += 1
    #         # Now that you have gone through all of the times,
    #         # You need to save the total, lidar, radar, and both
    #         # Then you can start to make the plot
    #     return {
    #         "zero": zero,
    #         "one": one,
    #         "two": two,
    #         "three": three,
    #         "four": four,
    #         "five": five,
    #     }

    # NOTE: Most likely depreciated
    def create_daily_layer_plots(self, request: DailyRequest) -> None:
        """Create daily files for a given instrument, observatory, month and year."""
        # Get a list of all the relevant blobs
        blobs: tuple[str, ...] = self.instrument_access.list_blobs(
            container=request.observatory.name.lower(),
            name_starts_with=f"{request.instrument.name.lower()}/daily_30smplcmask1zwang/{request.year}/",
        )
        # Create a daily file for each day in the month
        monthly_datetimes: list[datetime] = []
        monthly_layers: list[list[np.nan | int]] = []
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
            # Select the Strategy
            match (request.observatory, request.instrument):
                case (Observatory.UTQIAGVIK, Instrument.KAZR):
                    strategy: TransformationStrategy = UtqiagvikKazrDaily()
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
            # There should only be one Instrument data
            data: InstrumentData = results[0]
            if not data:
                continue
            # You are just going to do this for every time
            times: list[int] = list(data.variables["offset"].values)
            elevations: list[int] = list(data.variables["range"].values)
            default_values: list[list[int]] = [
                [np.nan for _ in elevations] for _ in times
            ]
            layers: pd.DataFrame = pd.DataFrame(
                default_values, index=times, columns=elevations
            )
            for i, time in enumerate(layers.index):
                monthly_datetimes.append(
                    datetime(target.year, target.month, target.day)
                    + timedelta(seconds=time)
                )
                base_elevations = data.variables["cloud_layer_base_height"].values[i]
                top_elevations = data.variables["cloud_layer_top_height"].values[i]
                if not any(base_elevations) and not any(top_elevations):
                    monthly_layers.append(layers.iloc[i, :])
                    continue
                layer = 1
                for base, top in zip(base_elevations, top_elevations):
                    if not base and not top:
                        break
                    layers.iloc[
                        i, (base <= layers.columns) & (layers.columns <= top)
                    ] = layer
                    layer += 1
                # Now that you are done with the layers
                monthly_layers.append(layers.iloc[i, :])
        monthly_df: pd.DataFrame = pd.DataFrame(
            monthly_layers, index=monthly_datetimes, columns=list(layers.columns)
        )
        # Plot the results
        plt.matshow(
            monthly_df.T,
            aspect="auto",
            origin="lower",
            extent=[
                monthly_df.index.min(),
                monthly_df.index.max(),
                monthly_df.columns.min() / 1000,
                monthly_df.columns.max() / 1000,
            ],
        )
        plt.colorbar()
        plt.gca().xaxis.tick_bottom()
        plt.xlabel("Timestamp, [UTC]")
        plt.ylabel("Range, [km]")
        plt.title(
            f"Cloud Layers, {request.observatory.name.capitalize()} ({request.month.name.capitalize()}. {request.year})"
        )
        plt.savefig(
            f"{request.month.name.capitalize()}-{request.year}.png", bbox_inches="tight"
        )
        # Searalize via pkl
        filepath: Path = Path(
            f"D{request.year}"
            f"-{str(request.month.value).zfill(2)}"
            f"-{str(target.day).zfill(2)}"
            f"-cloud-layers-numbered-{request.observatory.name.lower()}.pkl"
        )
        monthly_df.to_pickle(filepath)

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
        prev_day: bool = False,
        next_day: bool = False,
    ) -> Generator[InstrumentData, None, None]:
        self.transformation_context.strategy = strategy
        if isinstance(strategy, AhsrlSondeRaw):
            yield self._generate_sonde_data(
                selected, request, strategy, prev_day, next_day
            )
        else:
            for name in selected:
                filename = self.instrument_access.download_blob(
                    container=request.observatory.name.lower(),
                    name=name,
                )
                filepath: Path = Path.cwd() / filename
                with DataSet(filename) as dataset:
                    yield self.transformation_context.hydrate(dataset, filepath)
                os.remove(filepath)

    def _generate_sonde_data(
        self,
        selected: tuple[str, ...],
        request: DailyRequest,
        strategy: TransformationStrategy,
        prev_day: bool,
        next_day: bool,
    ) -> Generator[InstrumentData, None, None]:
        self.transformation_context.strategy = strategy
        match (prev_day, next_day):
            case (True, True):
                prev_day_name = selected[0]
                current_day_name = selected[1]
                next_day_name = selected[2]
            case (True, False):
                prev_day_name = selected[0]
                current_day_name = selected[1]
            case (False, True):
                current_day_name = selected[0]
                next_day_name = selected[1]
            case (False, False):
                current_day_name = selected[0]
        datasets = []
        if prev_day:
            prev_filename = self.instrument_access.download_blob(
                container=request.observatory.name.lower(),
                name=prev_day_name,
            )
            prev_filepath: Path = Path.cwd() / prev_filename
            prev_dataset = DataSet(prev_filename)
            datasets.append(prev_dataset)
        # Current
        current_filename = self.instrument_access.download_blob(
            container=request.observatory.name.lower(),
            name=current_day_name,
        )
        current_filepath: Path = Path.cwd() / current_filename
        current_dataset = DataSet(current_filename)
        datasets.append(current_dataset)
        if next_day:
            next_filename = self.instrument_access.download_blob(
                container=request.observatory.name.lower(),
                name=next_day_name,
            )
            next_filepath: Path = Path.cwd() / next_filename
            next_dataset = DataSet(next_filename)
            datasets.append(next_dataset)
        timestamps = []
        temperatures = []
        for dataset in datasets:
            for i, new_cal_time in enumerate(dataset["new_cal_times"][:].data):
                if all(new_cal_time == DType.I2.min + 1):
                    continue
                this_timestamp = datetime(
                    year=new_cal_time[0],
                    month=new_cal_time[1],
                    day=new_cal_time[2],
                    hour=new_cal_time[3],
                    minute=new_cal_time[4],
                    tzinfo=timezone.utc,
                )
                timestamps.append(this_timestamp)
                temperatures.append(
                    list(dataset["temperature_profile"][i].data - 273.15)
                )
        # Now that we have the targets the datetimes
        df = pd.DataFrame(
            np.nan,
            index=pd.date_range(
                start=timestamps[0], end=timestamps[-1], freq="min", tz=timezone.utc
            ),
            columns=dataset["altitude"][:].data,
        )
        for ts, profile in zip(timestamps, temperatures):
            i_ = list(df.index == ts).index(True)
            df.iloc[i_, 0 : len(profile)] = profile
        df.interpolate(method="time", limit_direction="both", inplace=True)
        # You just need to create the instrument data
        dimensions = {}
        dimensions["time"] = Dimension(
            name=Dimensions.TIME,
            size=dataset.dimensions["time"].size,
        )
        dimensions["level"] = Dimension(
            name=Dimensions.LEVEL,
            size=dataset.dimensions["altitude"].size,
        )
        # Variables
        variables = {}
        value = DateTime(
            year=timestamps[0].year,
            month=timestamps[0].month,
            day=timestamps[0].day,
            hour=timestamps[0].hour,
            minute=timestamps[0].minute,
            second=timestamps[0].second,
        ).unix
        variables["epoch"] = Variable(
            dtype=DType.I4,
            long_name="Unix Epoch 1970 of Initial Timestamp",
            scale=Scales.ONE,
            units=Units.SECONDS,
            dimensions=(),
            values=value,
        )
        variables["offset"] = Variable(
            dtype=DType.I4,
            long_name="Seconds Since Initial Timestamp",
            scale=Scales.ONE,
            units=Units.SECONDS,
            dimensions=(dimensions["time"],),
            values=tuple(int(i * 60) for i in range(len(df.index))),
        )
        variables["range"] = Variable(
            dtype=DType.U2,
            long_name="Return Range",
            scale=Scales.ONE,
            units=Units.METERS,
            dimensions=(dimensions["level"],),
            values=tuple(map(round, df.columns)),
        )
        df.replace(np.nan, -128, inplace=True)
        variables["temp"] = Variable(
            dtype=DType.I1,
            long_name="Temperature",
            scale=Scales.ONE,
            units=Units.CELCIUS,
            dimensions=(dimensions["time"], dimensions["level"]),
            values=tuple(tuple(map(round, values)) for values in df.values),
        )
        instrument_data = InstrumentData(dimensions=dimensions, variables=variables)
        if prev_day:
            prev_dataset.close()
            os.remove(prev_filepath)
        current_dataset.close()
        os.remove(current_filepath)
        if next_day:
            next_dataset.close()
            os.remove(next_filepath)
        return instrument_data

    @staticmethod
    def _resample(df: pd.DataFrame, base: int, transpose: bool, method: str):
        if transpose:
            df = df.T
        new_df: pd.DataFrame = pd.DataFrame(
            [base * round(i / base) for i in df.index],
            columns=[
                "new_column",
            ],
            index=df.index,
        )
        df = pd.concat([df, new_df], axis=1)
        match method:
            case "mode":
                df = df.groupby("new_column").agg(lambda x: min(pd.Series.mode(x)))
            case "mean":
                df = df.groupby("new_column").mean()
            case _:
                raise ValueError("invalid method")
        if transpose:
            df = df.T
        return df

    @staticmethod
    def _reindex(df: pd.DataFrame, method: str):
        match method:
            case "time":
                df = df.reindex([i for i in range(0, 60 * 60 * 24, 60)], method="ffill")
            case "height":
                df = df.T
                df = df.reindex([i for i in range(0, 17501, 90)], method="ffill")
                df = df.T
            case _:
                raise ValueError("invalid method: try 'time' or 'height'")
        return df

    def _reformat(self, df: pd.DataFrame, method: str):
        print("resample time")
        df = self._resample(df, 60, transpose=False, method=method)
        print("resample height")
        df = self._resample(df, 90, transpose=True, method=method)

        print("reindex time")
        df = self._reindex(df, "time")
        print("reindex height")
        df = self._reindex(df, "height")
        return df

    def _reformat_1D(self, df: pd.DataFrame, method: str):
        print("resample time")
        df = self._resample(df, 60, transpose=False, method=method)

        print("reindex time")
        df = self._reindex(df, "time")

        return df

    # def _read_pickle(
    #     self, name: str, request: ObservatoryRequest
    # ) -> tuple[VerticalLayers, ...]:
    #     filename = self.instrument_access.download_blob(
    #         container=request.observatory.name.lower(),
    #         name=name,
    #     )
    #     filepath: Path = Path.cwd() / filename
    #     with open(filepath, "rb") as file:
    #         result = pickle.load(file)
    #     os.remove(filepath)
    #     return result
    #         result = pickle.load(file)
    #     os.remove(filepath)
    #     return result
