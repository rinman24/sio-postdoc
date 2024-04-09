"""Constants for raw data builders."""

from tests.helper.builder.raw.strategies import ShebaDabulRaw
from tests.helper.builder.raw.types import (
    FilenameMap,
    Instrument,
    Observatory,
    StrategyMap,
)

STRATEGIES: StrategyMap = {
    Observatory.SHEBA: {
        Instrument.DABUL: ShebaDabulRaw(),
    }
}

FILENAMES: FilenameMap = {
    Observatory.SHEBA: {
        Instrument.DABUL: "D1997-11-04T00-31-00.BHAR.sheba_dabul_test.ncdf"
    }
}
