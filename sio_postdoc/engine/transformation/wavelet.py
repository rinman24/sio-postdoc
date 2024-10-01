"""Encapsulate windows for analysis."""

from math import ceil, floor, sqrt
from typing import Protocol


class Wavelet(Protocol):
    """Define protocol for wavelets."""

    def norm(self) -> float: ...
    def len(self) -> int: ...
    def values(self) -> tuple[int, ...]: ...


class TopHat(Wavelet):
    """Encapsulate a top hat wavelet transform."""

    def __init__(self, j: int) -> None:
        """Initialize the `TopHat` wavelet."""
        self._j: int = j
        self._norm: float = 1 / sqrt(2 ** (self._j + 1))
        self._len: int = 2**j
        self._values: tuple[float, ...] = self._get_values()

    def _get_values(self) -> tuple[float, ...]:
        # For the tophat the shape is
        ends: tuple[int, ...] = (-self.norm,) * int(self.len / 4)
        middle: tuple[int, ...] = (self.norm,) * int(self.len / 2)
        return ends + middle + ends

    @property
    def norm(self) -> float:
        """Return the normalization factor of the wavelet."""
        return self._norm

    @property
    def len(self) -> int:
        """Return the length of the wavelet."""
        return self._len

    @property
    def values(self) -> tuple[int, ...]:
        """Return the values of the wavelet."""
        return self._values
