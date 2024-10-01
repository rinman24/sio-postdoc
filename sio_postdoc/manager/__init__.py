"""Encapsulate Manager Configuration."""

from enum import Enum, auto


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


class Process(Enum):
    """Types of processing workflows."""

    PHASES = auto()
    RECLASSIFY = auto()
    RESAMPLE = auto()
    TIMESERIES = auto()
    ISOLATE = auto()
    MONTHLY = auto()
    ISOLATED_PHASES = auto()


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
    STEP_RADAR_TOPS = auto()
    STEP_LIDAR_TOPS = auto()
    STEP_OCCULTATION_ZONE = auto()
    STEP_4B = auto()
    STEP_5 = auto()
    STEP_6 = auto()
    STEP_7 = auto()
    STEP_8 = auto()
    TEMP = auto()


class Phase(Enum):
    """Types of phases from Shupe 2011."""

    ICE: int = 1  # NEW_ICE
    MIXED_ICE: int = 2
    MIXED: int = 3
    MIXED_LIQUID: int = 4
    LIQUID: int = 5  # NEW_LIQUID
    RAIN: int = 6
