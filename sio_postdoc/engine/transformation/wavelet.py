"""Encapsulate windows for analysis."""

from abc import ABC, abstractmethod


class Wavelet(ABC):
    """Define protocol for wavelets."""

    def __init__(self, j: int) -> None:
        """Initialize the wavelet."""
        self._j: int = j
        self._len: int = 2 ** (j + 1)
        self._values: tuple[float, ...] = self._get_values()

    @abstractmethod
    def _get_values(self) -> tuple[float, ...]:
        pass

    @property
    def order(self) -> int:
        """Return the order of the wavelet."""
        return self._j

    @property
    def length(self) -> int:
        """Return the length of the wavelet."""
        return self._len

    @property
    def values(self) -> tuple[int, ...]:
        """Return the values of the wavelet."""
        return self._values


class TopHat(Wavelet):
    """Encapsulate a top hat wavelet transform."""

    def _get_values(self) -> tuple[float, ...]:
        ends: tuple[int, ...] = (-1,) * int(self.length / 4)
        middle: tuple[int, ...] = (1,) * int(self.length / 2)
        return ends + middle + ends
