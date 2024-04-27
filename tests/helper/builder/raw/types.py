"""Types for raw data builders."""

from sio_postdoc.manager import Instrument, Observatory
from tests.helper.builder.raw.strategies import RawDataHydrationStrategy

StrategyMap = dict[Observatory, dict[Instrument, RawDataHydrationStrategy]]
FilenameMap = dict[Observatory, dict[Instrument, str]]
