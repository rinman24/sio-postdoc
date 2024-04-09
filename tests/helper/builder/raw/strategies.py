"""Define strategies for raw data creatioin."""

from abc import ABC, abstractmethod

from sio_postdoc.access.instrument.types import Dataset, Variable


class RawDataHydrationStrategy(ABC):
    """Declare operations common to raw data creation."""

    @property
    def dataset(self) -> Dataset:
        """Return the dataset property."""
        return self._dataset

    @dataset.setter
    def dataset(self, dataset: Dataset) -> None:
        self._dataset = dataset

    @abstractmethod
    def _add_attributes(self, filename: str) -> None:
        """Add attributes to netCDF Dataset."""

    @abstractmethod
    def _add_dimensions(self, filename: str) -> None:
        """Add dimensions to netCDF Dataset."""

    @abstractmethod
    def _add_variables(self) -> None:
        """Add variables to netCDF Dataset."""

    def hydrate(self, filename: str) -> None:
        """Hydrate SHEBA DABUL netCDF Dataset."""
        self.dataset = Dataset(filename, "w", format="NETCDF4")
        self._add_attributes(filename)
        self._add_dimensions(filename)
        self._add_variables()
        self.dataset.close()


class ShebaDabulRaw(RawDataHydrationStrategy):
    """Sheba Dabul Raw Data Strategy."""

    _records: int = 6
    _levels: int = 3

    def __init__(self) -> None:
        """Create a new Dataset when you iinstantiate the object."""
        self._dataset: Dataset

    def _add_attributes(self, filename: str) -> None:
        self.dataset.instrument_name = "dabul"
        self.dataset.experiment_name = "sheba"
        self.dataset.site_name = "arctic"
        self.dataset.netcdf_filename = filename
        self.dataset.netcdf_file_creation = "012201"

    def _add_dimensions(self, filename: str) -> None:
        self.dataset.createDimension("record", self._records)
        self.dataset.createDimension("level", self._levels)
        self.dataset.createDimension("filename_size", len(filename))

    def _add_variables(self) -> None:
        self._add_range()
        self._add_time()
        self._add_latitude()
        self._add_longitude()
        self._add_altitude()
        self._add_elevation()
        self._add_azimuth()
        self._add_scanmode()
        self._add_depolarization()
        self._add_far_parallel()

    def _add_range(self) -> None:
        range_: Variable = self.dataset.createVariable("range", "f4", ("level",))
        range_.long_name = "range"
        range_.units = "meter"
        range_[:] = [0, 30, 60]

    def _add_time(self) -> None:
        time: Variable = self.dataset.createVariable("time", "f4", ("record",))
        time.long_name = "time"
        time.units = "seconds since 1970-01-01 00:00 UTC"
        time[:] = [
            0.41666666,
            0.41944444,
            0.42222223,
            0.42499998,
            0.42777777,
            0.43055555,
        ]

    def _add_latitude(self) -> None:
        latitude: Variable = self.dataset.createVariable("latitude", "f4", ("record",))
        latitude.long_name = "platform latitude"
        latitude.units = "degrees_north"
        latitude[:] = [
            76.03717,
            76.03717,
            76.03718,
            76.03718,
            76.037186,
            76.037186,
        ]

    def _add_longitude(self) -> None:
        longitude: Variable = self.dataset.createVariable(
            "longitude", "f4", ("record",)
        )
        longitude.long_name = "platform longitude"
        longitude.units = "degrees_east"
        longitude[:] = [
            -165.25378,
            -165.25378,
            -165.25377,
            -165.25375,
            -165.25374,
            -165.25372,
        ]

    def _add_altitude(self) -> None:
        altitude: Variable = self.dataset.createVariable("altitude", "f4", ("record",))
        altitude.long_name = "platform altitude"
        altitude.units = "meter"
        altitude[:] = [10.0] * 6

    def _add_elevation(self) -> None:
        elevation: Variable = self.dataset.createVariable(
            "elevation", "f4", ("record",)
        )
        elevation.long_name = "beam elevation angle"
        elevation.units = "degrees"
        elevation[:] = [
            95.043205,
            95.167625,
            94.96686,
            94.948654,
            95.03751,
            95.015335,
        ]

    def _add_azimuth(self) -> None:
        azimuth: Variable = self.dataset.createVariable("azimuth", "f4", ("record",))
        azimuth.long_name = "beam azimuth angle"
        azimuth.units = "degrees"
        azimuth[:] = [
            194.38048,
            194.38042,
            194.38037,
            194.38025,
            194.38014,
            194.38008,
        ]

    def _add_scanmode(self) -> None:
        scanmode: Variable = self.dataset.createVariable("scanmode", "i2", ("record",))
        scanmode.long_name = "scan mode"
        scanmode[:] = [-999] * 6

    def _add_depolarization(self) -> None:
        depolarization: Variable = self.dataset.createVariable(
            "depolarization",
            "f4",
            ("record", "level"),
        )
        depolarization.long_name = "far parallel channel"
        depolarization[:] = [
            [1.5441344, 1.3981241, 0.3610639],
            [1.3873776, 1.6597508, 0.40076607],
            [1.477456, 1.3367455, 0.42651573],
            [1.4093928, 1.1275327, 0.39695445],
            [1.3849448, 1.1230909, 0.2626472],
            [1.5751007, 1.0160526, 0.29984418],
        ]

    def _add_far_parallel(self) -> None:
        far_parallel: Variable = self.dataset.createVariable(
            "far_parallel",
            "f4",
            ("record", "level"),
        )
        far_parallel[:] = [
            [-999.0, -999.0, 59.016533],
            [-999.0, -999.0, 62.122227],
            [-999.0, -999.0, 60.314087],
            [-999.0, -999.0, 60.391975],
            [-999.0, -999.0, 58.352943],
            [-999.0, -999.0, 59.214672],
        ]
