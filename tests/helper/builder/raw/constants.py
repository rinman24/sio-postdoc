"""Constants for raw data builders."""

from tests.helper.builder.raw.strategies import (
    EurekaAhsrlRaw,
    EurekaMmcrRaw,
    ShebaDabulRaw,
    ShebaMmcrRaw,
    UtqiagvikMmcrRaw,
    UtqiagvikMplRaw,
)
from tests.helper.builder.raw.types import (
    FilenameMap,
    Instrument,
    Observatory,
    StrategyMap,
)

STRATEGIES: StrategyMap = {
    Observatory.EUREKA: {
        Instrument.AHSRL: EurekaAhsrlRaw(),
        Instrument.MMCR: EurekaMmcrRaw(),
    },
    Observatory.SHEBA: {
        Instrument.DABUL: ShebaDabulRaw(),
        Instrument.MMCR: ShebaMmcrRaw(),
    },
    Observatory.UTQIAGVIK: {
        Instrument.MPL: UtqiagvikMplRaw(),
        Instrument.MMCR: UtqiagvikMmcrRaw(),
    },
}

FILENAMES: FilenameMap = {
    Observatory.EUREKA: {
        Instrument.AHSRL: "ahsrl_D2008-09-21T00-00-00_30s_30m.eureka_ahsrl_test.nc",
        Instrument.MMCR: "eurmmcrmerge.C1.c1.D2008-09-21T00-00-00.eureka_mmcr_test.nc",
    },
    Observatory.SHEBA: {
        Instrument.DABUL: "D1998-05-06T00-25-00.BARO.sheba_dabul_test.ncdf",
        Instrument.MMCR: "D1997-11-20T00-00-00.mrg.corrected.sheba_mmcr_test.nc",
    },
    Observatory.UTQIAGVIK: {
        Instrument.MPL: "nsa30smplcmask1zwangC1.c1.20080924.000030.utqiagvik_mpl_test.cdf",
        Instrument.MMCR: "nsaarscl1clothC1.c1.D2008-09-24T00-00-00.utqiagvik_mmcr_test.cdf",
    },
}
