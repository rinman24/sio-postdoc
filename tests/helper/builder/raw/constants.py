"""Constants for raw data builders."""

from tests.helper.builder.raw.strategies import (
    EurekaAhsrlRaw,
    ShebaDabulRaw,
    ShebaMmcrRaw,
)
from tests.helper.builder.raw.types import (
    FilenameMap,
    Instrument,
    Observatory,
    StrategyMap,
)

STRATEGIES: StrategyMap = {
    Observatory.SHEBA: {
        Instrument.DABUL: ShebaDabulRaw(),
        Instrument.MMCR: ShebaMmcrRaw(),
    },
    Observatory.EUREKA: {
        Instrument.AHSRL: EurekaAhsrlRaw(),
    },
}

FILENAMES: FilenameMap = {
    Observatory.SHEBA: {
        Instrument.DABUL: "D1998-05-06T00-25-00.BARO.sheba_dabul_test.ncdf",
        Instrument.MMCR: "D1997-11-20T00-00-00.mrg.corrected.sheba_mmcr_test.nc",
    },
    Observatory.EUREKA: {
        Instrument.AHSRL: "ahsrl_D2008-09-21T00-00-00_30s_30m.eureka_ahsrl_test.nc",
    },
}
