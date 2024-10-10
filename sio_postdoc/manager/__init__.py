"""Encapsulate Manager Configuration."""

from enum import Enum, auto

from sio_postdoc.engine.transformation.wavelet import TopHat


class InstrumentType(Enum):
    """Instrument types."""

    RADAR = auto()
    LIDAR = auto()
    SONDE = auto()
    MWR = auto()
    IRP = auto()


class Instrument(Enum):
    """Instrument names."""

    AHSRL = auto()
    DABUL = auto()
    KAZR = auto()
    MMCR = auto()
    MPL = auto()


class Observatory(Enum):
    """Observatory names."""

    EUREKA = auto()
    SHEBA = auto()
    UTQIAGVIK = auto()
    OLIKTOK = auto()


class Product(Enum):
    """Data Products names."""

    AHSRL = auto()
    AHSRLSONDE = auto()
    ARSCL1CLOTH = auto()
    ARSCLKAZR1KOLLIAS = auto()
    INTERPOLATEDSONDE = auto()
    MMCRMERGE = auto()
    MPLCMASK1ZWANG = auto()
    MPLCMASKML = auto()
    MWRRET1LILJCLOU = auto()
    QCRAD1LONG = auto()


class Month(Enum):
    """Instrument names."""

    JAN = auto()
    FEB = auto()
    MAR = auto()
    APR = auto()
    MAY = auto()
    JUN = auto()
    JUL = auto()
    AUG = auto()
    SEP = auto()
    OCT = auto()
    NOV = auto()
    DEC = auto()


class FileType(Enum):
    """Types of processing for files."""

    RAW = auto()
    DAILY = auto()
    MONTHLY = auto()


class Process(Enum):
    """Types of processing workflows."""

    PHASES = auto()
    RECLASSIFY = auto()
    RESAMPLE = auto()
    TIMESERIES = auto()
    ISOLATE = auto()
    ISOLATED_PHASES = auto()
    NORMALIZE_PHASES = auto()
    MONTHLY_TIMESERIES = auto()
    MONTHLY_WAVELET = auto()


class ResampleMethod(Enum):
    """Types of methods to resample."""

    MEAN = auto()
    MODE = auto()


class PlotPane(Enum):
    """Types of plot panes."""

    DEPOL = auto()
    DLR = auto()
    LWP = auto()
    MEAN_DOPP_VEL = auto()
    PHASES = auto()
    RECLASS_PHASES = auto()
    REFL = auto()
    SPEC_WIDTH = auto()
    STEP_1 = auto()
    STEP_2 = auto()
    STEP_3 = auto()
    STEP_4A = auto()
    STEP_RADAR_EDGES = auto()
    STEP_LIDAR_EDGES = auto()
    STEP_OCCULTATION_ZONE = auto()
    STEP_4B = auto()
    STEP_5 = auto()
    STEP_6 = auto()
    STEP_7 = auto()
    STEP_8 = auto()
    TEMP = auto()
    REFERENCE = auto()
    RENUMBERED = auto()
    MODIFIED_MIXED = auto()


class Phase2007(Enum):
    """Thermodynamic Phase Classifications from Shupe 2007."""

    SNOW = auto()
    ICE = auto()
    MIXED = auto()
    LIQUID = auto()
    DRIZZLE = auto()
    RAIN = auto()


class Phase2011(Enum):
    """Thermodynamic Phase Classifications from Shupe 2011."""

    ICE = auto()
    MIXED_ICE = auto()
    MIXED = auto()
    MIXED_LIQUID = auto()
    LIQUID = auto()
    RAIN = auto()


class PhaseAggregate(Enum):
    """Aggregate Thermodynamic Phase Classifications from Shupe 2007."""

    ICE = auto()
    MIXED = auto()
    LIQUID = auto()


class PhaseClass(Enum):
    """Types of Phase Classifications."""

    SHUPE_2007 = tuple(i for i in Phase2007)
    SHUPE_2011 = tuple(i for i in Phase2011)
    AGGREGATED = tuple(i for i in PhaseAggregate)


class Wavelet(Enum):
    """Wavelet shapes."""

    TOP_HAT = TopHat


class WaveletOrder(Enum):
    """Valid wavelet orders."""

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
