"""Strategies to construct netCDF4.Datasets location data from InstrumentData"""

from abc import ABC, abstractmethod

import netCDF4 as nc

from sio_postdoc.access.instrument.contracts import InstrumentData


class AbstractLocationStrategy(ABC):
    """This class is responsible for handling the location specifics."""

    @abstractmethod
    def write_data(  # pylint: disable=no-member, missing-function-docstring
        self,
        data: InstrumentData,
        rootgrp: nc.Dataset,
    ) -> nc.Dataset: ...


class MobileLocationStrategy(AbstractLocationStrategy):
    """TODO: Docstring."""

    def write_data(  # pylint: disable=no-member, missing-function-docstring
        self,
        data: InstrumentData,
        rootgrp: nc.Dataset,
    ) -> nc.Dataset:
        dimension: tuple[str] = ("record",)
        latitude = rootgrp.createVariable("latitude", "f4", dimension)
        longitude = rootgrp.createVariable("longitude", "f4", dimension)
        altitude = rootgrp.createVariable("altitude", "f4", dimension)
        for vector in data.vectors:
            match vector.name:
                case "latitude":
                    latitude[:] = list(vector.values)
                    latitude.units = vector.units
                    latitude.name_ = vector.name
                    latitude.scale_ = vector.scale
                    latitude.flag = vector.flag
                case "longitude":
                    longitude[:] = list(vector.values)
                    longitude.units = vector.units
                    longitude.name_ = vector.name
                    longitude.scale_ = vector.scale
                    longitude.flag = vector.flag
                case "altitude":
                    altitude[:] = list(vector.values)
                    altitude.units = vector.units
                    altitude.name_ = vector.name
                    altitude.scale_ = vector.scale
                    altitude.flag = vector.flag
        return rootgrp


class StationaryLocationStrategy(AbstractLocationStrategy):
    """TODO: Docstring."""

    @abstractmethod
    def write_data(  # pylint: disable=no-member
        self,
        data: InstrumentData,
        rootgrp: nc.Dataset,
    ) -> nc.Dataset: ...
