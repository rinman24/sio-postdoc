"""Define strategies for raw data creatioin."""

from abc import ABC, abstractmethod

from numpy import infty, nan

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


class EurekaAhsrlRaw(RawDataHydrationStrategy):
    """Eureka Ahsrl Raw Data Strategy."""

    _time: int = 6
    _altitude: int = 3

    def _add_attributes(self, filename: str) -> None:
        self.dataset.code_version = (
            "$Id: processed_netcdf.m,v 1.96 2008/10/29 15:32:21 jpgarcia Exp $"
        )
        self.dataset.load_calibration_version = (
            "$Id: load_calibration.m,v 1.25 2008/10/30 15:04:39 eloranta Exp $"
        )
        self.dataset.get_internal_cal_vals_version = (
            "$Id: get_internal_cal_vals.m,v 1.109 2008/09/12 21:20:05 eloranta Exp $"
        )
        self.dataset.calvals = (
            "$Id: calvals_ahsrl.m,v 1.108 2008/10/31 17:19:06 eloranta Exp $"
        )
        self.dataset.find_new_cal_times_version = (
            "$Id: find_new_cal_times.m,v 1.21 2008/02/25 19:33:32 jpgarcia Exp $"
        )
        self.dataset.radiosonde_profile_version = (
            "$Id: radiosonde_profile.m,v 1.30 2008/04/09 17:04:51 jpgarcia Exp $"
        )
        self.dataset.fetch_cal_version = (
            "$Id: fetch_cal.m,v 1.19 2008/09/04 21:06:16 eloranta Exp $"
        )
        self.dataset.quick_cal_version = (
            "$Id: quick_cal.m,v 1.58 2008/10/30 15:03:20 eloranta Exp $"
        )
        self.dataset.processed_netcdf_version = (
            "$Id: processed_netcdf.m,v 1.96 2008/10/29 15:32:21 jpgarcia Exp $"
        )
        self.dataset.process_data_version = (
            "$Id: process_data.m,v 1.202 2008/10/30 15:04:39 eloranta Exp $"
        )
        self.dataset.timefill_sum_version = (
            "$Id: time_block.cc,v 1.54 2008/04/16 21:33:02 jpgarcia Exp $"
        )
        self.dataset.timefill_average_version = (
            "$Id: time_block.cc,v 1.54 2008/04/16 21:33:02 jpgarcia Exp $"
        )
        self.dataset.file_version = 20050323
        self.dataset.time_zone = "UTC"
        self.dataset.file_created = "2008-11-05 01:44:26"
        self.dataset.Conventions = "COARDS"
        self.dataset.time_axis_average_mode = "time"
        self.dataset.time_axis_average_parameter = 30.0
        self.dataset.range_axis_average_parameter = 30.0
        self.dataset.featureset = 8175
        self.dataset.featureset_version = "$Revision: 1.13 $"
        self.dataset.processing_parameters__qc_params__min_radar_backscat = 1e-15
        self.dataset.processing_parameters__qc_params__mol_lost = 1.0
        self.dataset.processing_parameters__qc_params__lock_level = 0.6
        self.dataset.processing_parameters__qc_params__min_radar_dBz = -66.1
        self.dataset.processing_parameters__qc_params__backscat_snr = 1.0
        self.dataset.processing_parameters__particlesettings__alpha_water = 2.0
        self.dataset.processing_parameters__particlesettings__g_water = 1.0
        self.dataset.processing_parameters__particlesettings__alpha_ice = 1.0
        self.dataset.processing_parameters__particlesettings__g_ice = 1.0
        self.dataset.processing_parameters__particlesettings__type = (
            "Bullet Rosettes (Mitchell 1996)"
        )
        self.dataset.processing_parameters__particlesettings__Dr = 60.0
        self.dataset.processing_parameters__particlesettings__sigma_a = 1.0
        self.dataset.processing_parameters__particlesettings__sigma_v = 0.26
        self.dataset.processing_parameters__particlesettings__delta_a1 = 2.0
        self.dataset.processing_parameters__particlesettings__delta_v1 = 3.0
        self.dataset.processing_parameters__particlesettings__delta_a2 = 1.57
        self.dataset.processing_parameters__particlesettings__delta_v2 = 2.26
        self.dataset.processing_parameters__particlesettings__h20_depol_threshold = 0.05
        self.dataset.processing_parameters__particlesettings__p180_ice = 0.035

    def _add_dimensions(self, filename: str) -> None:
        self.dataset.createDimension("time", self._time)
        self.dataset.createDimension("altitude", self._altitude)
        self.dataset.createDimension("time_vector", 8)
        self.dataset.createDimension("calibration", 3)
        self.dataset.createDimension("sondenamelength", 6)
        self.dataset.createDimension("i2header", 9)
        self.dataset.createDimension("geoheader", 2)
        self.dataset.createDimension("apheader", 3)

    def _add_variables(self) -> None:  # noqa: PLR0915
        self._add_base_time()
        self._add_first_time()
        self._add_last_time()
        self._add_time()
        self._add_time_offset()
        self._add_start_time()
        self._add_mean_time()
        self._add_end_time()
        self._add_latitude()
        self._add_longitude()
        self._add_range_resolution()
        self._add_time_average()
        self._add_new_cal_times()
        self._add_altitude()
        self._add_new_cal_trigger()
        self._add_new_cal_offset()
        self._add_temperature_profile()
        self._add_pressure_profile()
        self._add_dewpoint_profile()
        self._add_windspeed_profile()
        self._add_winddir_profile()
        self._add_raob_station()
        self._add_i2_txt_header()
        self._add_geo_txt_header()
        self._add_ap_txt_header()
        self._add_raob_time_offset()
        self._add_raob_time_vector()
        self._add_Cmc()
        self._add_Cmm()
        self._add_Cam()
        self._add_beta_m()
        self._add_transmitted_energy()
        self._add_piezovoltage()
        self._add_num_seeded_shots()
        self._add_c_pol_dark_count()
        self._add_mol_dark_count()
        self._add_combined_dark_count_lo()
        self._add_combined_dark_count_hi()
        self._add_combined_gain()
        self._add_combined_merge_threshhold()
        self._add_geo_cor()
        self._add_od()
        self._add_profile_od()
        self._add_beta_a()
        self._add_atten_beta_r_backscat()
        self._add_profile_atten_beta_r_backscat()
        self._add_depol()
        self._add_molecular_counts()
        self._add_combined_counts_lo()
        self._add_combined_counts_hi()
        self._add_cross_counts()
        self._add_beta_a_backscat()
        self._add_profile_beta_a_backscat()
        self._add_profile_beta_m()
        self._add_qc_mask()
        self._add_std_beta_a_backscat()

    def _add_base_time(self) -> None:
        base_time = self.dataset.createVariable("base_time", "i4")
        base_time.string = "2008-09-21 00:00:00 UTC"
        base_time.long_name = "Base seconds since Unix Epoch"
        base_time.units = "seconds since 1970-01-01 00:00:00 UTC"
        base_time[:] = 1221955200

    def _add_first_time(self) -> None:
        first_time = self.dataset.createVariable("first_time", "i2", ("time_vector",))
        first_time.long_name = "First Time in file"
        first_time[:] = [2008, 9, 21, 0, 0, 0, 0, 0]

    def _add_last_time(self) -> None:
        last_time = self.dataset.createVariable("last_time", "i2", ("time_vector",))
        last_time.long_name = "Last Time in file"
        last_time[:] = [2008, 9, 21, 23, 59, 58, 88, 24]

    def _add_time(self) -> None:
        time = self.dataset.createVariable("time", "f8", ("time",))
        time.long_name = "Time"
        time.units = "seconds since 2008-09-21 00:00:00 UTC"
        time[:] = [
            -1.335016,
            29.401152,
            59.137664,
            87.875208,
            121.05104,
            150.789744,
        ]

    def _add_time_offset(self) -> None:
        time_offset = self.dataset.createVariable("time_offset", "f8", ("time",))
        time_offset.long_name = "Time offset from base_time"
        time_offset.description = 'same times as "First time in record"'
        time_offset.units = "seconds since 2008-09-21 00:00:00 UTC"
        time_offset[:] = [
            -1.335016,
            29.401152,
            59.137664,
            87.875208,
            121.05104,
            150.789744,
        ]

    def _add_start_time(self) -> None:
        start_time = self.dataset.createVariable(
            "start_time",
            "i2",
            ("time", "time_vector"),
        )
        start_time.long_name = "First Time in record"
        start_time.description = "time of first laser shot in averaging interval"
        start_time[:] = [
            [2008, 9, 20, 23, 59, 58, 664, 984],
            [2008, 9, 21, 0, 0, 29, 401, 152],
            [2008, 9, 21, 0, 0, 59, 137, 664],
            [2008, 9, 21, 0, 1, 27, 875, 208],
            [2008, 9, 21, 0, 2, 1, 51, 40],
            [2008, 9, 21, 0, 2, 30, 789, 744],
        ]

    def _add_mean_time(self) -> None:
        mean_time = self.dataset.createVariable(
            "mean_time",
            "i2",
            ("time", "time_vector"),
        )
        mean_time.long_name = "mean time of record"
        mean_time.description = (
            "mean time of laser shots collected in averaging interval"
        )
        mean_time[:] = [
            [2008, 9, 21, 0, 0, 13, 694, 104],
            [2008, 9, 21, 0, 0, 43, 430, 184],
            [2008, 9, 21, 0, 1, 13, 167, 368],
            [2008, 9, 21, 0, 1, 44, 142, 360],
            [2008, 9, 21, 0, 2, 15, 81, 160],
            [2008, 9, 21, 0, 2, 43, 820, 576],
        ]

    def _add_end_time(self) -> None:
        end_time = self.dataset.createVariable(
            "end_time",
            "i2",
            ("time", "time_vector"),
        )
        end_time.long_name = "Last Time in record"
        end_time.description = "time of last laser shot in averaging interval"
        end_time[:] = [
            [2008, 9, 21, 0, 0, 29, 305, 528],
            [2008, 9, 21, 0, 0, 59, 42, 64],
            [2008, 9, 21, 0, 1, 27, 779, 584],
            [2008, 9, 21, 0, 2, 0, 975, 424],
            [2008, 9, 21, 0, 2, 30, 694, 112],
            [2008, 9, 21, 0, 3, 0, 434, 496],
        ]

    def _add_latitude(self) -> None:
        latitude = self.dataset.createVariable("latitude", "f4")
        latitude.long_name = "latitude of lidar"
        latitude.units = "degree_N"
        latitude[:] = 79.9903

    def _add_longitude(self) -> None:
        longitude = self.dataset.createVariable("longitude", "f4")
        longitude.long_name = "longitude of lidar"
        longitude.units = "degree_W"
        longitude[:] = 85.9389

    def _add_range_resolution(self) -> None:
        range_resolution = self.dataset.createVariable("range_resolution", "f4")
        range_resolution.long_name = "Range resolution"
        range_resolution.description = (
            "vertical distance between data points after averaging"
        )
        range_resolution.units = "meters"
        range_resolution[:] = 30.0

    def _add_time_average(self) -> None:
        time_average = self.dataset.createVariable("time_average", "f4")
        time_average.long_name = "Time Averaging Width"
        time_average.description = "Time between data points after averaging"
        time_average.units = "seconds"
        time_average[:] = 30.0

    def _add_new_cal_times(self) -> None:
        new_cal_times = self.dataset.createVariable(
            "new_cal_times", "i2", ("calibration", "time_vector")
        )
        new_cal_times.long_name = "Time of Calibration Change"
        new_cal_times.description = (
            "New raob or system calibration data triggered recalibration"
        )
        new_cal_times[:] = [
            [2008, 9, 21, 0, 0, 0, 0, 0],
            [2008, 9, 21, 6, 0, 0, 0, 0],
            [2008, 9, 21, 18, 0, 0, 0, 0],
        ]

    def _add_altitude(self) -> None:
        altitude = self.dataset.createVariable("altitude", "f4", ("altitude",))
        altitude.long_name = "Height above lidar"
        altitude.units = "meters"
        altitude[:] = [11.25, 41.25, 71.25]

    def _add_new_cal_trigger(self) -> None:
        new_cal_trigger = self.dataset.createVariable(
            "new_cal_trigger", "i1", ("calibration",)
        )
        new_cal_trigger.long_name = "Trigger of Calibration Change"
        new_cal_trigger.description = "reason for recalibration"
        new_cal_trigger.bit_0 = "radiosonde profile"
        new_cal_trigger.bit_1 = "i2 scan"
        new_cal_trigger.bit_2 = "geometry"
        new_cal_trigger[:] = [2, 2, 2]

    def _add_new_cal_offset(self) -> None:
        new_cal_offset = self.dataset.createVariable(
            "new_cal_offset", "i2", ("calibration",)
        )
        new_cal_offset.long_name = "Record Dimension equivalent Offset"
        new_cal_offset.min_value = 0
        new_cal_offset[:] = [0, 719, 2159]

    def _add_temperature_profile(self) -> None:
        temperature_profile = self.dataset.createVariable(
            "temperature_profile", "f4", ("calibration", "altitude")
        )
        temperature_profile.long_name = "Raob Temperature Profile"
        temperature_profile.description = (
            "Temperature interpolated to requested altitude resolution"
        )
        temperature_profile.units = "degrees Kelvin"
        temperature_profile[:] = [
            [nan, 270.145, 270.68594],
            [nan, 269.72464, 270.04163],
            [nan, 268.13953, 267.86047],
        ]

    def _add_pressure_profile(self) -> None:
        pressure_profile = self.dataset.createVariable(
            "pressure_profile", "f4", ("calibration", "altitude")
        )
        pressure_profile.long_name = "Raob pressure Profile"
        pressure_profile.description = (
            "Pressure interpolated to requested altitude resolution"
        )
        pressure_profile.units = "hectopascals"
        pressure_profile[:] = [
            [nan, 1001.35, 997.65625],
            [nan, 1004.2226, 1000.5187],
            [nan, 1006.0436, 1002.2064],
        ]

    def _add_dewpoint_profile(self) -> None:
        dewpoint_profile = self.dataset.createVariable(
            "dewpoint_profile", "f4", ("calibration", "altitude")
        )
        dewpoint_profile.long_name = "Raob Dewpoint Temperature Profile"
        dewpoint_profile.description = (
            "Dewpoint interpolated to requested altitude resolution"
        )
        dewpoint_profile.units = "degrees Kelvin"
        dewpoint_profile.missing_value = nan
        dewpoint_profile[:] = [
            [nan, 268.09, 268.17578],
            [nan, 267.13458, 266.94662],
            [nan, 266.43954, 266.16046],
        ]

    def _add_windspeed_profile(self) -> None:
        windspeed_profile = self.dataset.createVariable(
            "windspeed_profile", "f4", ("calibration", "altitude")
        )
        windspeed_profile.long_name = "Raob Wind Speed Profile"
        windspeed_profile.description = (
            "Speeds interpolated to requested altitude resolution"
        )
        windspeed_profile.units = "m/s"
        windspeed_profile.missing_value = nan
        windspeed_profile[:] = [
            [nan, 7.8125, 7.6393204],
            [nan, 10.472945, 9.496701],
            [nan, 9.322093, 10.577908],
        ]

    def _add_winddir_profile(self) -> None:
        winddir_profile = self.dataset.createVariable(
            "winddir_profile", "f4", ("calibration", "altitude")
        )
        winddir_profile.long_name = "Raob Wind Direction Profile"
        winddir_profile.description = (
            "Directions interpolated to requested altitude resolution"
        )
        winddir_profile.units = "degrees"
        winddir_profile.missing_value = nan
        winddir_profile[:] = [
            [nan, 283.875, 276.95996],
            [nan, 290.0, 289.32037],
            [nan, 287.7471, 286.0029],
        ]

    def _add_raob_station(self) -> None:
        raob_station = self.dataset.createVariable(
            "raob_station", "S1", ("calibration", "sondenamelength")
        )
        raob_station.long_name = "Radiosonde Station ID"
        raob_station[:] = [
            [b"Y", b"E", b"U", b" ", b" ", b" "],
            [b"Y", b"E", b"U", b" ", b" ", b" "],
            [b"Y", b"E", b"U", b" ", b" ", b" "],
        ]

    def _add_i2_txt_header(self) -> None:
        i2_txt_header = self.dataset.createVariable(
            "i2_txt_header", "S1", ("calibration", "i2header")
        )
        i2_txt_header.long_name = "i2_scan_file_text_info"
        i2_txt_header.description = "Contains name of file used to compute calibration"
        i2_txt_header[:] = [
            [b"", b"", b"", b"", b"", b"", b"", b"", b""],
            [b"", b"", b"", b"", b"", b"", b"", b"", b""],
            [b"", b"", b"", b"", b"", b"", b"", b"", b""],
        ]

    def _add_geo_txt_header(self) -> None:
        geo_txt_header = self.dataset.createVariable(
            "geo_txt_header", "S1", ("calibration", "geoheader")
        )
        geo_txt_header.long_name = "geometric_correction_file_txt_header."
        geo_txt_header[:] = [
            [b"", b""],
            [b"", b""],
            [b"", b""],
        ]

    def _add_ap_txt_header(self) -> None:
        ap_txt_header = self.dataset.createVariable(
            "ap_txt_header", "S1", ("calibration", "apheader")
        )
        ap_txt_header.long_name = "afterpulse_correction_file_txt_header."
        ap_txt_header[:] = [
            [b"", b"", b""],
            [b"", b"", b""],
            [b"", b"", b""],
        ]

    def _add_raob_time_offset(self) -> None:
        raob_time_offset = self.dataset.createVariable(
            "raob_time_offset", "f8", ("calibration",)
        )
        raob_time_offset.units = "seconds"
        raob_time_offset.long_name = "Radiosonde Launch time offset"
        raob_time_offset.description = "Time after base time in seconds"
        raob_time_offset[:] = [0.0, 43200.0, 86400.0]

    def _add_raob_time_vector(self) -> None:
        raob_time_vector = self.dataset.createVariable(
            "raob_time_vector", "i2", ("calibration", "time_vector")
        )
        raob_time_vector.long_name = "Radiosonde Launch time vector"
        raob_time_vector.description = (
            "Time in [year month day hour min sec ms us] format"
        )
        raob_time_vector[:] = [
            [2008, 9, 21, 0, 0, 0, 0, 0],
            [2008, 9, 21, 12, 0, 0, 0, 0],
            [2008, 9, 22, 0, 0, 0, 0, 0],
        ]

    def _add_Cmc(self) -> None:
        Cmc = self.dataset.createVariable("Cmc", "f4", ("calibration", "altitude"))
        Cmc.long_name = "Molecular in Combined Calibration"
        Cmc[:] = [
            [nan, 0.94958466, 0.94958436],
            [nan, 0.94975173, 0.9497569],
            [nan, 0.94991046, 0.9499172],
        ]

    def _add_Cmm(self) -> None:
        Cmm = self.dataset.createVariable("Cmm", "f4", ("calibration", "altitude"))
        Cmm.long_name = "Molecular in Molecular Calibration"
        Cmm[:] = [
            [nan, 1.6482617, 1.6479046],
            [nan, 1.6463878, 1.6459568],
            [nan, 1.6445122, 1.6440556],
        ]

    def _add_Cam(self) -> None:
        Cam = self.dataset.createVariable("Cam", "f4", ("calibration", "altitude"))
        Cam.long_name = "Aerosol in Molecular Calibration"
        Cam[:] = [
            [0.001, 0.001, 0.001],
            [0.001, 0.001, 0.001],
            [0.001, 0.001, 0.001],
        ]

    def _add_beta_m(self) -> None:
        beta_m = self.dataset.createVariable(
            "beta_m", "f4", ("calibration", "altitude")
        )
        beta_m.long_name = "Raob molecular scattering cross section per unit volume"
        beta_m.units = "1/meter"
        beta_m.plot_scale = "logarithmic"
        beta_m[:] = [
            [1.40424545e-05, 1.39996182e-05, 1.39039485e-05],
            [1.4113830e-05, 1.4043256e-05, 1.3976750e-05],
            [1.4194106e-05, 1.4155382e-05, 1.4115825e-05],
        ]

    def _add_transmitted_energy(self) -> None:
        transmitted_energy = self.dataset.createVariable(
            "transmitted_energy", "f4", ("time",)
        )
        transmitted_energy.long_name = "Transmitted Energy"
        transmitted_energy.units = "Joules"
        transmitted_energy.missing_value = nan
        transmitted_energy[:] = [
            12438.077,
            12471.298,
            12438.722,
            13498.255,
            12504.95,
            12527.273,
        ]

    def _add_piezovoltage(self) -> None:
        piezovoltage = self.dataset.createVariable("piezovoltage", "f4", ("time",))
        piezovoltage.long_name = "piezovoltage"
        piezovoltage.units = "Volts"
        piezovoltage.missing_value = nan
        piezovoltage[:] = [
            22.264818,
            21.840616,
            21.988153,
            23.283442,
            22.362902,
            23.3313,
        ]

    def _add_num_seeded_shots(self) -> None:
        num_seeded_shots = self.dataset.createVariable(
            "num_seeded_shots", "i4", ("time",)
        )
        num_seeded_shots.long_name = "Number of Seeded Shots"
        num_seeded_shots.missing_value = -1
        num_seeded_shots[:] = [119998, 119996, 120000, 129998, 119999, 120000]

    def _add_c_pol_dark_count(self) -> None:
        c_pol_dark_count = self.dataset.createVariable(
            "c_pol_dark_count", "f4", ("time",)
        )
        c_pol_dark_count.long_name = "Cross Polarization Dark Count"
        c_pol_dark_count.description = (
            "total counts per averaging interval(eg. one altitude, one time)"
        )
        c_pol_dark_count.units = "counts"
        c_pol_dark_count.missing_value = nan
        c_pol_dark_count[:] = [
            17.142857,
            16.571428,
            20.0,
            13.714286,
            14.857142,
            10.857142,
        ]

    def _add_mol_dark_count(self) -> None:
        mol_dark_count = self.dataset.createVariable("mol_dark_count", "f4", ("time",))
        mol_dark_count.long_name = "Molecular Dark Count"
        mol_dark_count.description = (
            "total counts per averaging interval(eg. one altitude, one time)"
        )
        mol_dark_count.units = "counts"
        mol_dark_count.missing_value = nan
        mol_dark_count[:] = [
            12.571428,
            10.285714,
            10.857142,
            13.714286,
            9.714286,
            7.428571,
        ]

    def _add_combined_dark_count_lo(self) -> None:
        combined_dark_count_lo = self.dataset.createVariable(
            "combined_dark_count_lo", "f4", ("time",)
        )
        combined_dark_count_lo.long_name = "Low Gain Combined Dark Count"
        combined_dark_count_lo.description = (
            "total counts per averaging interval(eg. one altitude, one time)"
        )
        combined_dark_count_lo.units = "counts"
        combined_dark_count_lo.missing_value = nan
        combined_dark_count_lo[:] = [
            17.142857,
            13.714286,
            10.285714,
            16.0,
            16.571428,
            9.142858,
        ]

    def _add_combined_dark_count_hi(self) -> None:
        combined_dark_count_hi = self.dataset.createVariable(
            "combined_dark_count_hi", "f4", ("time",)
        )
        combined_dark_count_hi.long_name = "High Gain Combined Dark Count"
        combined_dark_count_hi.description = (
            "total counts per averaging interval(eg. one altitude, one time)"
        )
        combined_dark_count_hi.units = "counts"
        combined_dark_count_hi.missing_value = nan
        combined_dark_count_hi[:] = [
            18.857143,
            9.714286,
            12.0,
            22.857143,
            13.142858,
            13.714286,
        ]

    def _add_combined_gain(self) -> None:
        combined_gain = self.dataset.createVariable(
            "combined_gain", "f4", ("calibration",)
        )
        combined_gain.long_name = "Combined Gain Factor"
        combined_gain.description = "Low Gain level * Factor ~ High Gain level"
        combined_gain[:] = [16.0, 16.0, 16.0]

    def _add_combined_merge_threshhold(self) -> None:
        combined_merge_threshhold = self.dataset.createVariable(
            "combined_merge_threshhold", "f4", ("calibration",)
        )
        combined_merge_threshhold.long_name = "Combined Merge Threshhold"
        combined_merge_threshhold[:] = [0.05, 0.05, 0.05]

    def _add_geo_cor(self) -> None:
        geo_cor = self.dataset.createVariable(
            "geo_cor", "f4", ("calibration", "altitude")
        )
        geo_cor.long_name = "Overlap correction"
        geo_cor.description = (
            "Geometric overlap correction averaged to requested altitude resolution"
        )
        geo_cor.units = ""
        geo_cor.missing_value = nan
        geo_cor.plot_scale = "logarithmic"
        geo_cor[:] = [
            [nan, -47064.75, 1247.525],
            [nan, -47064.75, 1247.525],
            [nan, -47064.75, 1247.525],
        ]

    def _add_od(self) -> None:
        od = self.dataset.createVariable("od", "f4", ("time", "altitude"))
        od.long_name = "Optical depth of particulate"
        od.units = ""
        od.missing_value = nan
        od.insufficient_data = infty
        od.plot_scale = "logarithmic"
        od[:] = [
            [4.8634334, -0.37113133, 0.0068785],
            [4.8634334, -0.37626463, infty],
            [4.8634334, -0.36846352, 0.00587574],
            [4.8634334e00, -3.7711456e-01, -3.0243865e-04],
            [4.8634334, -0.3702242, nan],
            [4.8634334, -0.35479563, 0.01458123],
        ]

    def _add_profile_od(self) -> None:
        profile_od = self.dataset.createVariable("profile_od", "f4", ("altitude",))
        profile_od.long_name = "Optical depth of particulate Profile"
        profile_od.units = ""
        profile_od.missing_value = nan
        profile_od.insufficient_data = infty
        profile_od.plot_scale = "logarithmic"
        profile_od[:] = [4.8688040e00, nan, -infty]

    def _add_beta_a(self) -> None:
        beta_a = self.dataset.createVariable("beta_a", "f4", ("time", "altitude"))
        beta_a.long_name = "Particulate extinction cross section per unit volume"
        beta_a.units = "1/m"
        beta_a.missing_value = nan
        beta_a.plot_scale = "logarithmic"
        beta_a[:] = [
            [nan, -0.08094258, 0.00615082],
            [nan, -0.08091412, 0.00629274],
            [nan, -0.08095929, 0.00619717],
            [nan, -0.08106226, 0.00622874],
            [nan, -0.08092479, 0.00616121],
            [nan, -0.0808142, 0.00602002],
        ]

    def _add_atten_beta_r_backscat(self) -> None:
        atten_beta_r_backscat = self.dataset.createVariable(
            "atten_beta_r_backscat", "f4", ("time", "altitude")
        )
        atten_beta_r_backscat.long_name = "Attenuated Molecular return"
        atten_beta_r_backscat.units = "1/(m sr)"
        atten_beta_r_backscat.missing_value = nan
        atten_beta_r_backscat.plot_scale = "logarithmic"
        atten_beta_r_backscat[:] = [
            [nan, 3.5104126e-06, 1.6369860e-06],
            [nan, 3.5466383e-06, 1.6314056e-06],
            [nan, 3.4917323e-06, 1.6402723e-06],
            [nan, 3.5526723e-06, 1.6606658e-06],
            [nan, 3.5040496e-06, 1.6334950e-06],
            [nan, 3.3975759e-06, 1.6119608e-06],
        ]

    def _add_profile_atten_beta_r_backscat(self) -> None:
        profile_atten_beta_r_backscat = self.dataset.createVariable(
            "profile_atten_beta_r_backscat", "f4", ("altitude",)
        )
        profile_atten_beta_r_backscat.long_name = "Attenuated Molecular Profile"
        profile_atten_beta_r_backscat.units = "1/(m sr)"
        profile_atten_beta_r_backscat.missing_value = nan
        profile_atten_beta_r_backscat.plot_scale = "logarithmic"
        profile_atten_beta_r_backscat[:] = [nan, 3.5764958e-06, 1.6776088e-06]

    def _add_depol(self) -> None:
        depol = self.dataset.createVariable("depol", "f4", ("time", "altitude"))
        depol.long_name = "Circular depolarization ratio for particulate"
        depol.description = "left circular return divided by right circular return"
        depol.units = ""
        depol.missing_value = nan
        depol.plot_scale = "logarithmic"
        depol[:] = [
            [nan, 0.8910097, -0.01050728],
            [nan, 0.87681854, -0.0091269],
            [nan, 0.87386703, -0.0107031],
            [nan, 0.8854666, -0.01125472],
            [nan, 0.87619394, -0.01357443],
            [nan, 0.88363147, -0.00955483],
        ]

    def _add_molecular_counts(self) -> None:
        molecular_counts = self.dataset.createVariable(
            "molecular_counts", "i4", ("time", "altitude")
        )
        molecular_counts.long_name = "Molecular Photon Counts"
        molecular_counts.description = "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
        molecular_counts.units = "counts"
        molecular_counts.missing_value = -1
        molecular_counts.plot_scale = "logarithmic"
        molecular_counts[:] = [
            [941193, 17500, 31942],
            [940739, 17726, 31574],
            [941563, 17342, 32121],
            [1016112, 18831, 34467],
            [938971, 17644, 32128],
            [943866, 17841, 32346],
        ]

    def _add_combined_counts_lo(self) -> None:
        combined_counts_lo = self.dataset.createVariable(
            "combined_counts_lo", "i4", ("time", "altitude")
        )
        combined_counts_lo.long_name = "Low Gain Combined Photon Counts"
        combined_counts_lo.description = "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
        combined_counts_lo.units = "counts"
        combined_counts_lo.missing_value = -1
        combined_counts_lo.plot_scale = "logarithmic"
        combined_counts_lo[:] = [
            [557654, 56641, 1980],
            [557940, 57206, 2093],
            [558454, 57456, 1992],
            [604798, 61537, 2027],
            [558429, 57499, 1769],
            [558247, 57274, 2026],
        ]

    def _add_combined_counts_hi(self) -> None:
        combined_counts_hi = self.dataset.createVariable(
            "combined_counts_hi", "i4", ("time", "altitude")
        )
        combined_counts_hi.long_name = "High Gain Combined Photon Counts"
        combined_counts_hi.description = "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
        combined_counts_hi.units = "counts"
        combined_counts_hi.missing_value = -1
        combined_counts_hi.plot_scale = "logarithmic"
        combined_counts_hi[:] = [
            [793186, 225421, 36897],
            [793750, 224982, 37594],
            [794103, 225480, 36914],
            [860080, 242103, 36056],
            [793712, 222074, 30974],
            [794443, 227433, 38366],
        ]

    def _add_cross_counts(self) -> None:
        cross_counts = self.dataset.createVariable(
            "cross_counts", "i4", ("time", "altitude")
        )
        cross_counts.long_name = "Cross Polarized Photon Counts"
        cross_counts.description = "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
        cross_counts.units = "counts"
        cross_counts.missing_value = -1
        cross_counts.plot_scale = "logarithmic"
        cross_counts[:] = [
            [3259673, 765202, 0],
            [3257464, 761927, 0],
            [3256298, 765139, 0],
            [3528099, 828282, 0],
            [3255033, 767666, 0],
            [3253180, 769465, 0],
        ]

    def _add_beta_a_backscat(self) -> None:
        beta_a_backscat = self.dataset.createVariable(
            "beta_a_backscat", "f4", ("time", "altitude")
        )
        beta_a_backscat.long_name = (
            "Particulate backscatter cross section per unit volume"
        )
        beta_a_backscat.units = "1/(m sr)"
        beta_a_backscat.missing_value = nan
        beta_a_backscat.plot_scale = "logarithmic"
        beta_a_backscat[:] = [
            [nan, 3.7125070e-04, 1.1108813e-06],
            [nan, 3.6797742e-04, 1.3044502e-06],
            [nan, 3.7921261e-04, 1.1211707e-06],
            [nan, 3.750138e-04, 9.747085e-07],
            [nan, 3.7294455e-04, 8.0712221e-07],
            [nan, 3.6752902e-04, 1.1509022e-06],
        ]

    def _add_profile_beta_a_backscat(self) -> None:
        profile_beta_a_backscat = self.dataset.createVariable(
            "profile_beta_a_backscat", "f4", ("altitude",)
        )
        profile_beta_a_backscat.long_name = (
            "Particulate backscatter cross section profile"
        )
        profile_beta_a_backscat.units = "1/(m sr)"
        profile_beta_a_backscat.missing_value = nan
        profile_beta_a_backscat.plot_scale = "logarithmic"
        profile_beta_a_backscat[:] = [nan, 3.672536e-04, 7.564736e-07]

    def _add_profile_beta_m(self) -> None:
        profile_beta_m = self.dataset.createVariable(
            "profile_beta_m", "f4", ("altitude",)
        )
        profile_beta_m.long_name = "Raob molecular scattering cross section profile"
        profile_beta_m.units = "1/meter"
        profile_beta_m.plot_scale = "logarithmic"
        profile_beta_m[:] = [1.4194106e-05, 1.4155382e-05, 1.4115825e-05]

    def _add_qc_mask(self) -> None:
        qc_mask = self.dataset.createVariable("qc_mask", "i4", ("time", "altitude"))
        qc_mask.long_name = "Quality Mask"
        qc_mask.description = "Quality mask,bits:1=&(2:8),2=lock,3=seed,4=m_count,5=beta_err,6=m_lost,7=min_lid,8=min_rad"
        qc_mask.units = ""
        qc_mask.missing_value = -1
        qc_mask.bit_0 = "AND"
        qc_mask.bit_1 = "lock"
        qc_mask.bit_2 = "seed"
        qc_mask.bit_3 = "m_count"
        qc_mask.bit_4 = "beta_err"
        qc_mask.bit_5 = "m_lost"
        qc_mask.bit_6 = "min_lid"
        qc_mask.bit_7 = "min_rad"
        qc_mask.plot_scale = "linear"
        qc_mask[:] = [
            [65502, 65502, 65502],
            [65502, 65502, 65502],
            [65502, 65502, 65502],
            [65502, 65502, 65502],
            [65502, 65502, 65502],
            [65502, 65502, 65502],
        ]

    def _add_std_beta_a_backscat(self) -> None:
        std_beta_a_backscat = self.dataset.createVariable(
            "std_beta_a_backscat", "f4", ("time", "altitude")
        )
        std_beta_a_backscat.long_name = (
            "Std dev of backscat cross section (photon counting)"
        )
        std_beta_a_backscat.units = "1/(m sr)"
        std_beta_a_backscat.missing_value = nan
        std_beta_a_backscat.plot_scale = "logarithmic"
        std_beta_a_backscat[:] = [
            [nan, 3.0208066e-06, 1.8732067e-08],
            [nan, 2.9744365e-06, 1.9653946e-08],
            [nan, 3.1054185e-06, 1.8700767e-08],
            [nan, 2.9440828e-06, 1.7485702e-08],
            [nan, 3.0241167e-06, 1.7450182e-08],
            [nan, 2.9597777e-06, 1.8751841e-08],
        ]


class EurekaMmcrRaw(RawDataHydrationStrategy):
    """Eureka Mmcr Raw Data Strategy."""

    time: int = 6
    nheights: int = 3
    numlayers: int = 10

    def _add_attributes(self, filename: str) -> None:
        self.dataset.Source = "20080921.000000"
        self.dataset.Version = "***1.0***"
        self.dataset.Input_Platforms = ""
        self.dataset.Contact = "***ETL***"
        self.dataset.commenta = "At each height and time, the MMCR reflectivity, velocity, spectral width and signal-to-noise ratio always come from the same mode. The mode in indicated by ModeId."
        self.dataset.commentb = "Missing (i.e., does not exist) data for a particular time period are indicated by a value of 10 for the ModeId. The geophysical variables should contain a value of -32768 at these times."
        self.dataset.commentc = "Nore that -32768 is also used for the geophysical variables when there are no significant detections, in which case ModeId is 0."

    def _add_dimensions(self, filename: str) -> None:
        self.dataset.createDimension("time", self.time)
        self.dataset.createDimension("nheights", self.nheights)  # noqa: F841
        self.dataset.createDimension("numlayers", self.numlayers)  # noqa: F841

    def _add_variables(self) -> None:
        self._add_base_time()
        self._add_time_offset()
        self._add_heights()
        self._add_Reflectivity()
        self._add_MeanDopplerVelocity()
        self._add_SpectralWidth()
        self._add_SignalToNoiseRatio()
        self._add_ModeId()
        self._add_CloudLayerBottomHeight()
        self._add_CloudLayerTopHeight()

    def _add_base_time(self) -> None:
        base_time = self.dataset.createVariable("base_time", "f8")
        base_time.long_name = "Beginning Time of File"
        base_time.units = "seconds since 1970-01-01 00:00 UTC"
        base_time.calendar_date = "20080921_00:00:09"
        base_time[:] = 1221955209.0

    def _add_time_offset(self) -> None:
        time_offset = self.dataset.createVariable("time_offset", "f8", ("time",))
        time_offset.long_name = "Time Offset from base_time"
        time_offset.units = "seconds"
        time_offset.comment = "none"
        time_offset[:] = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0]

    def _add_heights(self) -> None:
        heights = self.dataset.createVariable("heights", "f4", ("nheights",))
        heights.long_name = "Height of Measured Value"
        heights.units = "m AGL"
        heights.comment = "none"
        heights[:] = [54.0, 97.0, 140.0]

    def _add_Reflectivity(self) -> None:
        Reflectivity = self.dataset.createVariable(
            "Reflectivity", "i2", ("time", "nheights")
        )
        Reflectivity.long_name = "MMCR Reflectivity"
        Reflectivity.units = "dBZ(x100)"
        Reflectivity.comment = "Divide Reflectivity by 100 to get dBZ"
        Reflectivity[:] = [
            [-32768, -32768, -32768],
            [-3438, -3730, -5072],
            [-4511, -4802, -6151],
            [-4540, -4831, -6183],
            [-4303, -4595, -5946],
            [-4400, -4688, -5924],
        ]

    def _add_MeanDopplerVelocity(self) -> None:
        MeanDopplerVelocity = self.dataset.createVariable(
            "MeanDopplerVelocity", "i2", ("time", "nheights")
        )
        MeanDopplerVelocity.long_name = "MMCR MeanDopplerVelocity"
        MeanDopplerVelocity.units = "m/s(x1000)"
        MeanDopplerVelocity.comment = "Divide MeanDopplerVelocity by 1000 to get m/s"
        MeanDopplerVelocity[:] = [
            [-32768, -32768, -32768],
            [77, 69, 61],
            [-4057, -1847, 363],
            [-4111, -2629, -1148],
            [-4460, -1692, 1076],
            [-4284, -1676, 931],
        ]

    def _add_SpectralWidth(self) -> None:
        SpectralWidth = self.dataset.createVariable(
            "SpectralWidth", "i2", ("time", "nheights")
        )
        SpectralWidth.long_name = "MMCR SpectralWidth"
        SpectralWidth.units = "m/s(x1000)"
        SpectralWidth.comment = "Divide SpectralWidth by 1000 to get m/s"
        SpectralWidth[:] = [
            [-32768, -32768, -32768],
            [470, 300, 130],
            [593, 353, 113],
            [513, 296, 80],
            [1013, 552, 91],
            [727, 466, 205],
        ]

    def _add_SignalToNoiseRatio(self) -> None:
        SignalToNoiseRatio = self.dataset.createVariable(
            "SignalToNoiseRatio", "i2", ("time", "nheights")
        )
        SignalToNoiseRatio.long_name = "MMCR Signal-To-Noise Ratio"
        SignalToNoiseRatio.units = "dB(x100)"
        SignalToNoiseRatio.comment = "Divide SignalToNoiseRatio by 100 to get dB"
        SignalToNoiseRatio[:] = [
            [-32768, -32768, -32768],
            [2044, 1753, 405],
            [602, 312, -1002],
            [588, 297, -1035],
            [768, 477, -859],
            [712, 424, -793],
        ]

    def _add_ModeId(self) -> None:
        ModeId = self.dataset.createVariable("ModeId", "i2", ("time", "nheights"))
        ModeId.long_name = "MMCR ModeId"
        ModeId.units = "unitless"
        ModeId.comment = (
            "0 No significant power return, 1-5 Valid modes, 10 Data do not exist"
        )
        ModeId[:] = [
            [0, 0, 0],
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2],
        ]

    def _add_CloudLayerBottomHeight(self) -> None:
        CloudLayerBottomHeight = self.dataset.createVariable(
            "CloudLayerBottomHeight", "f4", ("time", "numlayers")
        )
        CloudLayerBottomHeight.long_name = "Bottom Height of Echo Layer"
        CloudLayerBottomHeight.units = "m AGL"
        CloudLayerBottomHeight.comment = "none"
        CloudLayerBottomHeight[:] = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [54.0, 1731.0, 4268.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [54.0, 1645.0, 4268.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [54.0, 1645.0, 4268.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [54.0, 1645.0, 4268.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [54.0, 1645.0, 4354.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]

    def _add_CloudLayerTopHeight(self) -> None:
        CloudLayerTopHeight = self.dataset.createVariable(
            "CloudLayerTopHeight", "f4", ("time", "numlayers")
        )
        CloudLayerTopHeight[:] = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [226.0, 1860.0, 6246.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [226.0, 1860.0, 6246.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [226.0, 1860.0, 6246.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [226.0, 1860.0, 6160.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [226.0, 1860.0, 6160.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]
        CloudLayerTopHeight.long_name = "Top Height of Echo Layer"
        CloudLayerTopHeight.units = "m AGL"
        CloudLayerTopHeight.comment = "none"
