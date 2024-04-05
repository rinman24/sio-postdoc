"""TODO: Docstring."""

from datetime import datetime

import netCDF4 as nc

import sio_postdoc.utility.service as utility
from sio_postdoc.access.instrument.contracts import InstrumentData
from sio_postdoc.access.instrument.strategies.hardware import AbstractHardwareStrategy
from sio_postdoc.access.instrument.strategies.location import AbstractLocationStrategy


class NcdfContext:
    """TODO: Docstring."""

    def __init__(
        self,
        location: AbstractLocationStrategy,
        instrument: AbstractHardwareStrategy,
    ) -> None:
        self._location: AbstractLocationStrategy = location
        self._instrument: AbstractHardwareStrategy = instrument

    @property
    def location(self) -> AbstractLocationStrategy:
        """TODO: Docstring."""
        return self._location

    @location.setter
    def location(self, location: AbstractLocationStrategy) -> None:
        self._location = location

    @property
    def instrument(self) -> AbstractHardwareStrategy:
        """TODO: Docstring."""
        return self._instrument

    @instrument.setter
    def instrument(self, instrument: AbstractHardwareStrategy) -> None:
        self._instrument = instrument

    def create_file(self, data: InstrumentData) -> str:
        """TODO: Docstring."""
        # First create the file
        filename: str = utility.get_filename(data)
        # Then delegate portions to the strategies
        with nc.Dataset(  # pylint: disable=no-member
            filename,
            "w",
            format="NETCDF4",
        ) as rootgrp:
            rootgrp.instrument = data.name
            rootgrp.observatory = data.observatory
            rootgrp.filename = filename
            rootgrp.created = str(datetime.now())
            # Dimensions
            records: int = len(data.time.offsets)
            record = rootgrp.createDimension(  # pylint: disable=unused-variable
                "record",
                records,
            )
            if data.axis:
                levels: int = len(data.axis.values)
                level = rootgrp.createDimension(  # pylint: disable=unused-variable
                    "level",
                    levels,
                )
            # Variables
            offsets = rootgrp.createVariable(
                "offsets",
                "i4",
                ("record",),
            )
            offsets[:] = list(data.time.offsets)
            offsets.units = "seconds"
            offsets.name_ = "offsets"
            offsets.scale_ = 1
            offsets.flag = -999
            if data.axis:
                range = rootgrp.createVariable(  # pylint: disable=redefined-builtin
                    "range",
                    "u2",
                    ("level",),
                )
                range[:] = list(data.axis.values)
                range.units = "meters"
                range.name_ = "range"
                range.scale_ = 1
                range.flag = int(2**16 - 1)
            rootgrp = self.location.write_data(
                data,
                rootgrp,
            )
            rootgrp = self.instrument.write_data(
                data,
                rootgrp,
            )
        return filename
