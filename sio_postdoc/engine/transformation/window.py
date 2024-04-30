"""Encapsulate windows for analysis."""

from math import ceil, floor
from typing import Generator


class GridWindow:
    """Encapsulate a 2-dimensional window."""

    def __init__(self, length: int, height: int) -> None:
        """Initialize the `GridWindow`."""
        self._length: int = length
        self._height: int = height
        _horizontal_padding: tuple[int, int] = self._get_padding(size=length)
        _vertical_padding: tuple[int, int] = self._get_padding(size=height)
        self.padding: dict[str, int] = {
            "left": _horizontal_padding[0],
            "right": _horizontal_padding[1],
            "bottom": _vertical_padding[0],
            "top": _vertical_padding[1],
        }
        self.position: tuple[int, int] = (
            self.padding["left"],
            self.padding["bottom"],
        )

    @staticmethod
    def _get_padding(size: int) -> tuple[int, int]:
        left: int = ceil(size / 2) - 1
        right: int = floor(size / 2)
        return (left, right)

    def members(self) -> Generator[tuple[int, int], None, None]:
        """Return the member's indices."""
        x: int = self.position[0]
        y: int = self.position[1]
        for i in range(x - self.padding["left"], x + self.padding["right"] + 1):
            for j in range(y - self.padding["bottom"], y + self.padding["top"] + 1):
                yield (i, j)
