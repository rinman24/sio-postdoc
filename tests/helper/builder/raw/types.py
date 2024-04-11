"""Types for raw data builders."""

from enum import Enum, auto

from tests.helper.builder.raw.strategies import RawDataHydrationStrategy


class Observatory(Enum):
    """Observatory names."""

    EUREKA = auto()
    SHEBA = auto()


class Instrument(Enum):
    """Instrument names."""

    AHSRL = auto()
    DABUL = auto()
    MMCR = auto()


StrategyMap = dict[Observatory, dict[Instrument, RawDataHydrationStrategy]]
FilenameMap = dict[Observatory, dict[Instrument, str]]
