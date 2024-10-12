"""Define custom types used by all access components."""

from pathlib import Path

import netCDF4

Contents = tuple[Path, ...]
DataSet = netCDF4.Dataset
Variable = netCDF4.Variable
