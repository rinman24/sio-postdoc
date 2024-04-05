"""Strategies to construct netCDF4.Datasets instrument data from InstrumentData"""

from abc import ABC, abstractmethod

import netCDF4 as nc

from sio_postdoc.access.instrument.contracts import InstrumentData


class AbstractHardwareStrategy(ABC):
    """TODO: Docstring."""

    @abstractmethod
    def write_data(  # pylint: disable=no-member, missing-function-docstring
        self,
        data: InstrumentData,
        rootgrp: nc.Dataset,
    ) -> nc.Dataset: ...


class DabulHardware(AbstractHardwareStrategy):
    """TODO: Docstring."""

    def write_data(  # pylint: disable=no-member
        self,
        data: InstrumentData,
        rootgrp: nc.Dataset,
    ) -> nc.Dataset:
        # One and two dimensions
        dimension: tuple[str] = ("record",)
        dimensions: tuple[str, str] = ("record", "level")
        dtype: str
        # Vectors
        for vector in data.vectors.values():
            match vector.name:
                case "elevation":
                    dtype = vector.dtype
                    elevation = rootgrp.createVariable("elevation", dtype, dimension)
                    elevation[:] = list(vector.values)
                    elevation.units = vector.units
                    elevation.name_ = vector.name
                    elevation.scale_ = vector.scale
                    elevation.flag = vector.flag
                case "azimuth":
                    dtype = vector.dtype
                    azimuth = rootgrp.createVariable("azimuth", dtype, dimension)
                    azimuth[:] = list(vector.values)
                    azimuth.units = vector.units
                    azimuth.name_ = vector.name
                    azimuth.scale_ = vector.scale
                    azimuth.flag = vector.flag
                case "scanmode":
                    dtype = vector.dtype
                    scanmode = rootgrp.createVariable("scanmode", dtype, dimension)
                    scanmode[:] = list(vector.values)
                    scanmode.units = vector.units
                    scanmode.name_ = vector.name
                    scanmode.scale_ = vector.scale
                    scanmode.flag = vector.flag
        # Matrices
        for matrix in data.matrices.values():
            match matrix.name:
                case "depolarization":
                    dtype = matrix.dtype
                    depolarization = rootgrp.createVariable("depolarization", dtype, dimensions)
                    depolarization[:] = matrix.values
                    depolarization.units = matrix.units
                    depolarization.name_ = matrix.name
                    depolarization.scale_ = matrix.scale
                    depolarization.flag = matrix.flag
                case "far_parallel":
                    dtype = matrix.dtype
                    far_parallel = rootgrp.createVariable("far_parallel", dtype, dimensions)
                    far_parallel[:] = matrix.values
                    far_parallel.units = matrix.units
                    far_parallel.name_ = matrix.name
                    far_parallel.scale_ = matrix.scale
                    far_parallel.flag = matrix.flag

        return rootgrp


class MmcrHardware(AbstractHardwareStrategy):
    """TODO: Docstring."""

    def write_data(  # pylint: disable=no-member
        self,
        data: InstrumentData,
        rootgrp: nc.Dataset,
    ) -> nc.Dataset:
        """TODO: Implement"""
