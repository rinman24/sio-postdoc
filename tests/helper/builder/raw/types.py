"""Types for raw data builders."""

from enum import Enum, auto

from tests.helper.builder.raw.strategies import RawDataHydrationStrategy


class Observatory(Enum):
    """Observatory names."""

    SHEBA = auto()


class Instrument(Enum):
    """Instrument names."""

    DABUL = auto()
    MMCR = auto()


StrategyMap = dict[Observatory, dict[Instrument, RawDataHydrationStrategy]]
FilenameMap = dict[Observatory, dict[Instrument, str]]
