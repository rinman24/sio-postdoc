"""Encapsulate Manager Configuration."""

from enum import Enum, auto


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

    ARSCLKAZR1KOLLIAS = auto()
    MPLCMASKML = auto()
    INTERPOLATEDSONDE = auto()


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
