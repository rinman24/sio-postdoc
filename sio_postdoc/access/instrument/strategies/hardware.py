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
        # Vectors
        elevation = rootgrp.createVariable("elevation", "f4", dimension)
        azimuth = rootgrp.createVariable("azimuth", "f4", dimension)
        scanmode = rootgrp.createVariable("scanmode", "i2", dimension)
        for vector in data.vectors:
            match vector.name:
                case "elevation":
                    elevation[:] = list(vector.values)
                    elevation.units = vector.units
                    elevation.name_ = vector.name
                    elevation.scale_ = vector.scale
                    elevation.flag = vector.flag
                case "azimuth":
                    azimuth[:] = list(vector.values)
                    azimuth.units = vector.units
                    azimuth.name_ = vector.name
                    azimuth.scale_ = vector.scale
                    azimuth.flag = vector.flag
                case "scanmode":
                    scanmode[:] = list(vector.values)
                    scanmode.units = vector.units
                    scanmode.name_ = vector.name
                    scanmode.scale_ = vector.scale
                    scanmode.flag = vector.flag
        # Matrices
        depolarization = rootgrp.createVariable("depolarization", "f4", dimensions)
        far_parallel = rootgrp.createVariable("far_parallel", "f4", dimensions)
        for matrix in data.matrices:
            match matrix.name:
                case "depolarization":
                    depolarization[:] = matrix.values
                    depolarization.units = matrix.units
                    depolarization.name_ = matrix.name
                    depolarization.scale_ = matrix.scale
                    depolarization.flag = matrix.flag
                case "far_parallel":
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
