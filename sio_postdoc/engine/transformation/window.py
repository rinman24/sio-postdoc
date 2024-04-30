"""Encapsulate windows for analysis."""

from math import ceil, floor

from pydantic import BaseModel


class GridWindow(BaseModel):
    """Encapsulate a 2-dimensional window."""

    @staticmethod
    def _get_padding(size: int) -> tuple[int, int]:
        left: int = ceil(size / 2) - 1
        right: int = floor(size / 2)
        return (left, right)
