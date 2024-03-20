from datetime import datetime

import netCDF4 as nc

import sio_postdoc.utility.service as utility
from sio_postdoc.access.instrument.contracts import InstrumentData
from sio_postdoc.access.instrument.strategies import (
    AbstractDataStrategy,
    AbstractInstrumentStrategy,
    AbstractLocationStrategy,
)


class DataContext:
    """TODO: docstring."""

    def __init__(self, strategy: AbstractDataStrategy) -> None:
        self._strategy: AbstractDataStrategy = strategy

    @property
    def strategy(self) -> AbstractDataStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: AbstractDataStrategy) -> None:
        self._strategy = strategy

    def extract(self, name: str) -> InstrumentData:
        return self.strategy.extract(name)


class NcdfContext:

    def __init__(
        self,
        location: AbstractLocationStrategy,
        instrument: AbstractInstrumentStrategy,
    ) -> None:
        self._location: AbstractLocationStrategy = location
        self._instrument: AbstractInstrumentStrategy = instrument

    @property
    def location(self) -> AbstractLocationStrategy:
        return self._location

    @location.setter
    def location(self, location: AbstractLocationStrategy) -> None:
        self._location = location

    @property
    def instrument(self) -> AbstractInstrumentStrategy:
        return self._instrument

    @instrument.setter
    def instrument(self, instrument: AbstractInstrumentStrategy) -> None:
        self._instrument = instrument

    def create_file(self, data: InstrumentData) -> str:
        # First create the file
        filename: str = utility.get_filename(data)
        # Then delegate portions to the strategies
        with nc.Dataset(filename, "w", format="NETCDF4") as rootgrp:
            rootgrp.instrument = data.name
            rootgrp.observatory = data.observatory
            rootgrp.filename = filename
            rootgrp.created = str(datetime.now())
            # Dimensions
            records: int = len(data.time.offsets)
            record = rootgrp.createDimension("record", records)
            if data.axis:
                levels: int = len(data.axis[0].values)
                level = rootgrp.createDimension("level", levels)
            # Variables
            offsets = rootgrp.createVariable("offsets", "f4", ("record",))
            offsets[:] = list(data.time.offsets)
            if data.axis:
                range_ = rootgrp.createVariable("range_", "f4", ("level",))
                range_[:] = list(data.axis[0].values)
            rootgrp = self.location.write_data(data, rootgrp)
            rootgrp = self.instrument.write_data(data, rootgrp)
        return filename
