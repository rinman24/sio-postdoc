"""Encapsulate windows for analysis."""

from math import ceil, floor


class GridWindow:
    """Encapsulate a 2-dimensional window."""

    def __init__(self, length: int, height: int) -> None:
        """Initialize the `GridWindow`."""
        self._length: int = length
        self._height: int = height
        _horizontal_padding: tuple[int, int] = self._get_padding(size=length)
        _vertical_padding: tuple[int, int] = self._get_padding(size=height)
        self._padding: dict[str, int] = {
            "left": _horizontal_padding[0],
            "right": _horizontal_padding[1],
            "bottom": _vertical_padding[0],
            "top": _vertical_padding[1],
        }
        self._initial: tuple[int, int] = (
            self._padding["left"],
            self._padding["bottom"],
        )

    @property
    def initial(self) -> tuple[int, int]:
        """Return the initial position of the `GridWindow`."""
        return self._initial

    @property
    def padding(self) -> dict[str, int]:
        """Return the padding for the `GridWindow`."""
        return self._padding

    @staticmethod
    def _get_padding(size: int) -> tuple[int, int]:
        left: int = ceil(size / 2) - 1
        right: int = floor(size / 2)
        return (left, right)
