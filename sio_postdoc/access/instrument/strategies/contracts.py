"""Contracts for Instrument Access Strategies."""

from dataclasses import dataclass
from typing import Callable


@dataclass
class ValidRange:
    """Encapsulate the valid range of physical values."""

    min: int
    max: int


@dataclass
class RawDataParams:
    """Encapsulate parameters of `PhysicalMatrix`."""

    units: str
    name: str
    long_name: str
    scale: int
    dtype: str
    valid_range: ValidRange
    flag: int
    strategy: Callable
