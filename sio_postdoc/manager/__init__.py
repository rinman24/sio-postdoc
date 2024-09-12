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
    MWRLOS = auto()
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

    RESAMPLE = auto()


class ResampleMethod(Enum):
    """Types of methods to resample."""

    MEAN = auto()
    MODE = auto()
