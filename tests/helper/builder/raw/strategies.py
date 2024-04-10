"""Define strategies for raw data creatioin."""

from abc import ABC, abstractmethod

from sio_postdoc.access.instrument.types import Dataset, Variable


class RawDataHydrationStrategy(ABC):
    """Declare operations common to raw data creation."""

    def __init__(self) -> None:
        """Create a new Dataset when you instantiate the object."""
        self._dataset: Dataset

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


class ShebaMmcrRaw(RawDataHydrationStrategy):
    """Sheba Mmcr Raw Data Strategy."""

    _time: int = 6
    _nheights: int = 3

    def _add_attributes(self, filename: str) -> None:
        self.dataset.contact = "Eugene E. Clothiaux, Gerald. G. Mace, Thomas A. Ackerman, 503 Walker Building, University Park, PA, 16802; Phone: , FAX: , E-mail: cloth,mace,ackerman@essc.psu.edu"
        self.dataset.comment = "Divide Reflectivity by 100 to get dBZ, SignaltoNoiseRatio by 100 to get dB and MeanDopplerVelocity and SpectralWidth by 1000 to get m/s!"
        self.dataset.commenta = "For each merged range gate reflectivity, velocity and width always come from the same mode."
        self.dataset.commentb = "Quality Control Flags: 0 - No Data, 1 - Good Data, 2 - Second Trip Echo Problems, 3 - Coherent Integration Problems, 4 - Second Trip Echo and Coherent Integration Problems"

    def _add_dimensions(self, filename: str) -> None:
        self.dataset.createDimension("time", self._time)
        self.dataset.createDimension("nheights", self._nheights)

    def _add_variables(self) -> None:
        self._add_base_time()
        self._add_time_offset()
        self._add_Heights()
        self._add_Qc()
        self._add_Reflectivity()
        self._add_MeanDopplerVelocity()
        self._add_SpectralWidth()
        self._add_ModeId()
        self._add_SignaltoNoiseRatio()

    def _add_base_time(self) -> None:
        base_time = self.dataset.createVariable("base_time", "i4")
        base_time.long_name = "Beginning Time of File"
        base_time.units = "seconds since 1970-01-01 00:00:00 00:00"
        base_time.calendar_date = "Year 1997 Month 11 Day 20 00:00:50"
        base_time[:] = 879984050

    def _add_time_offset(self) -> None:
        time_offset = self.dataset.createVariable("time_offset", "f8", ("time",))
        time_offset.long_name = "Time Offset from base_time"
        time_offset.units = "seconds"
        time_offset.comment = "none"
        time_offset[:] = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0]

    def _add_Heights(self) -> None:
        Heights = self.dataset.createVariable("Heights", "f4", ("nheights",))
        Heights.long_name = "Height of Measured Value; agl"
        Heights.units = "m"
        Heights[:] = [105.0, 150.0, 195.0]

    def _add_Qc(self) -> None:
        Qc = self.dataset.createVariable(
            "Qc",
            "S1",
            ("time", "nheights"),
        )
        Qc.long_name = "Quality Control Flags"
        Qc.units = "unitless"
        Qc[:] = [
            [b"\x01", b"\x01", b""],
            [b"\x01", b"\x01", b""],
            [b"\x01", b"\x01", b""],
            [b"\x01", b"\x01", b""],
            [b"\x01", b"\x01", b""],
            [b"\x01", b"\x01", b""],
        ]

    def _add_Reflectivity(self) -> None:
        Reflectivity = self.dataset.createVariable(
            "Reflectivity",
            "i2",
            ("time", "nheights"),
        )
        Reflectivity.long_name = "Reflectivity"
        Reflectivity.units = "dBZ (X100)"
        Reflectivity[:] = [
            [-4713, -3745, -32768],
            [-4713, -3745, -32768],
            [-4713, -3745, -32768],
            [-4725, -3727, -32768],
            [-4738, -3709, -32768],
            [-4751, -3692, -32768],
        ]

    def _add_MeanDopplerVelocity(self) -> None:
        MeanDopplerVelocity = self.dataset.createVariable(
            "MeanDopplerVelocity",
            "i2",
            ("time", "nheights"),
        )
        MeanDopplerVelocity.long_name = "Mean Doppler Velocity"
        MeanDopplerVelocity.units = "m/s (X1000)"
        MeanDopplerVelocity[:] = [
            [-826, -299, -32768],
            [-826, -299, -32768],
            [-826, -299, -32768],
            [-821, -303, -32768],
            [-816, -308, -32768],
            [-810, -313, -32768],
        ]

    def _add_SpectralWidth(self) -> None:
        SpectralWidth = self.dataset.createVariable(
            "SpectralWidth",
            "i2",
            ("time", "nheights"),
        )
        SpectralWidth.long_name = "Spectral Width"
        SpectralWidth.units = "m/s (X1000)"
        SpectralWidth[:] = [
            [101, 116, -32768],
            [101, 116, -32768],
            [101, 116, -32768],
            [173, 180, -32768],
            [244, 244, -32768],
            [316, 308, -32768],
        ]

    def _add_ModeId(self) -> None:
        ModeId = self.dataset.createVariable(
            "ModeId",
            "S1",
            ("time", "nheights"),
        )
        ModeId.long_name = "Mode I.D. for Merged Time-Height Moments Data"
        ModeId.units = "unitless"
        ModeId[:] = [
            [b"\x03", b"\x03", b""],
            [b"\x03", b"\x03", b""],
            [b"\x03", b"\x03", b""],
            [b"\x03", b"\x03", b""],
            [b"\x03", b"\x03", b""],
            [b"\x03", b"\x03", b""],
        ]

    def _add_SignaltoNoiseRatio(self) -> None:
        SignaltoNoiseRatio = self.dataset.createVariable(
            "SignaltoNoiseRatio",
            "i2",
            ("time", "nheights"),
        )
        SignaltoNoiseRatio.long_name = "Signal-to-Noise Ratio"
        SignaltoNoiseRatio.units = "dB (X100)"
        SignaltoNoiseRatio[:] = [
            [1376, 1219, -32768],
            [1376, 1219, -32768],
            [1376, 1219, -32768],
            [1356, 1212, -32768],
            [1336, 1205, -32768],
            [1314, 1197, -32768],
        ]
