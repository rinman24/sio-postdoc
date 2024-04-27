"""Encapsulate configuration of transformaion engine."""

from enum import Enum, auto


class DType(Enum):
    """Define data Types."""

    U1 = auto()
    U2 = auto()
    U4 = auto()
    U8 = auto()
    I1 = auto()
    I2 = auto()
    I4 = auto()
    I8 = auto()

    @property
    def _bytes(self) -> int:
        """Return the number of bytes."""
        return int(self.name[-1])

    @property
    def _bits(self) -> int:
        """Return the number of bits."""
        return int(self._bytes * 8)

    @property
    def _sign(self) -> int:
        """Return zero for unsigned or negative one for signed."""
        if self.name.lower().startswith("i"):
            return -1
        return 0  # self.name.lower() starts with "u"

    @property
    def _denominator(self) -> int:
        """Returns two for signed and one for unsigned."""
        if self._sign == -1:
            return 2
        return 1  # self._sign is zero

    @property
    def min(self) -> int:
        """Return the minimum value."""
        return int(self._sign * 2**self._bits / self._denominator)

    @property
    def max(self) -> int:
        """Return the maximum value."""
        return int(2**self._bits / self._denominator - 1)

    @property
    def limits(self) -> tuple[int, int]:
        """Return the limits of the given `DType`."""
        return (self.min, self.max)


class Units(Enum):
    """Define physical units."""

    DBZ = auto()
    DEGREES = auto()
    METERS = auto()
    METERS_PER_SECOND = auto()
    NONE = auto()
    SECONDS = auto()
    UNSPECIFIED = auto()


class Dimensions(Enum):
    """Define physical dimensions."""

    ANGLE = auto()
    LEVEL = auto()
    TIME = auto()


class Scales(Enum):
    """Define scales."""

    ONE = 1
    TEN = 10
    HUNDRED = 100
    THOUSAND = 1000
    SECONDS_PER_HOUR = 3600
