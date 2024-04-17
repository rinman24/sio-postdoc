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


class UtqiagvikMplRaw(RawDataHydrationStrategy):
    """Utqiagvik Mpl Raw Data Strategy."""

    time: int = 6
    height: int = 3
    layer: int = 10
    num_deadtime_corr: int = 16

    def _add_attributes(self, filename: str) -> None:
        self.dataset.command_line = (
            "mplcmask -s nsa -f C1 -D 2 -b 20080924 -e 20080925 -R"
        )
        self.dataset.process_version = "vap-mplcmask-0.4-0.el6"
        self.dataset.dod_version = "30smplcmask1zwang-c1-1.0"
        self.dataset.input_datastreams = "nsamplpolavgC1.c1 : 1.14 : 20080924.000030\nnsasondewnpnC1.b1 : 8.1 : 20080924.052600-20080924.165800"
        self.dataset.site_id = "nsa"
        self.dataset.platform_id = "30smplcmask1zwang"
        self.dataset.facility_id = "C1"
        self.dataset.location_description = (
            "North Slope of Alaska (NSA), Barrow, Alaska"
        )
        self.dataset.datastream = "nsa30smplcmask1zwangC1.c1"
        self.dataset.serial_number = "105"
        self.dataset.height_uncertainty = "N/A"
        self.dataset.min_cloud_detection_height = "0.500 km AGL"
        self.dataset.max_cloud_detection_height = "20.000 km AGL"
        self.dataset.deadtime_correction = (
            "Applied deadtime correction factor from the configuration file"
        )
        self.dataset.overlap_correction = "Applied overlap correction from the configuration file to the height of the MPL"
        self.dataset.afterpulse_correction = "No afterpulse corrections are applied"
        self.dataset.nasa_gsfc_mpl_help = "N/A"
        self.dataset.missing_value = "-9999.0"
        self.dataset.applied_corrections = (
            "Applied overlap, energy and deadtime correction"
        )
        self.dataset.backscatter_data_quality_comment = (
            "Data quality ok for both cloud and aerosol analysis"
        )
        self.dataset.data_level = "c1"
        self.dataset.comment = "VAP that applies Zhien's cloud boundary algorithm"
        self.dataset.history = "created by user sri on machine amber at 2014-07-12 00:18:36, using vap-mplcmask-0.4-0.el6"

    def _add_dimensions(self, filename: str) -> None:
        self.dataset.createDimension("time", self.time)
        self.dataset.createDimension("height", self.height)
        self.dataset.createDimension("layer", self.layer)
        self.dataset.createDimension("num_deadtime_corr", self.num_deadtime_corr)

    def _add_variables(self) -> None:
        self._add_base_time()
        self._add_time_offset()
        self._add_time()
        self._add_height()
        self._add_cloud_base()
        self._add_cloud_top()
        self._add_num_cloud_layers()
        self._add_linear_depol_ratio()
        self._add_qc_linear_depol_ratio()
        self._add_linear_depol_snr()
        self._add_qc_linear_depol_snr()
        self._add_cloud_mask()
        self._add_qc_cloud_mask()
        self._add_cloud_base_layer()
        self._add_cloud_top_layer()
        self._add_backscatter()
        self._add_qc_backscatter()
        self._add_backscatter_snr()
        self._add_qc_backscatter_snr()
        self._add_background_signal()
        self._add_cloud_top_attenuation_flag()
        self._add_shots_summed()
        self._add_deadtime_correction_counts()
        self._add_deadtime_correction()
        self._add_afterpulse_correction()
        self._add_overlap_correction()
        self._add_lat()
        self._add_lon()
        self._add_alt()

    def _add_base_time(self) -> None:
        base_time = self.dataset.createVariable("base_time", "i4")
        base_time.string = "2008-09-24 00:00:00 0:00"
        base_time.long_name = "Base time in Epoch"
        base_time.units = "seconds since 1970-1-1 0:00:00 0:00"
        base_time.ancillary_variables = "time_offset"
        base_time[:] = 1222214400

    def _add_time_offset(self) -> None:
        time_offset = self.dataset.createVariable("time_offset", "f8", ("time",))
        time_offset.long_name = "Time offset from base_time"
        time_offset.units = "seconds since 2008-09-24 00:00:00 0:00"
        time_offset.ancillary_variables = "base_time"
        time_offset[:] = [30.0, 60.0, 90.0, 120.0, 150.0, 180.0]

    def _add_time(self) -> None:
        time = self.dataset.createVariable("time", "f8", ("time",))
        time.long_name = "Time offset from midnight"
        time.units = "seconds since 2008-09-24 00:00:00 0:00"
        time[:] = [30.0, 60.0, 90.0, 120.0, 150.0, 180.0]

    def _add_height(self) -> None:
        height = self.dataset.createVariable("height", "f4", ("height",))
        height.long_name = "Vertical height above ground level (AGL) corresponding to the bottom of height bin"
        height.units = "km"
        height[:] = [0.02249481, 0.05247406, 0.0824533]

    def _add_cloud_base(self) -> None:
        cloud_base = self.dataset.createVariable("cloud_base", "f4", ("time",))
        cloud_base.long_name = "Lowest cloud base height above ground level (AGL)"
        cloud_base.units = "km"
        cloud_base.comment = "A value of -1 means no cloud is detected"
        cloud_base.missing_value = -9999.0
        cloud_base[:] = [0.682038, -1.0, -1.0, -1.0, -1.0, -1.0]

    def _add_cloud_top(self) -> None:
        cloud_top = self.dataset.createVariable("cloud_top", "f4", ("time",))
        cloud_top.long_name = "Highest cloud top height above ground level (AGL)"
        cloud_top.units = "km"
        cloud_top.comment = "A value of -1 means no cloud is detected"
        cloud_top.missing_value = -9999.0
        cloud_top[:] = [1.7912695, -1.0, -1.0, -1.0, -1.0, -1.0]

    def _add_num_cloud_layers(self) -> None:
        num_cloud_layers = self.dataset.createVariable(
            "num_cloud_layers", "i4", ("time",)
        )
        num_cloud_layers.long_name = "Number of cloud layers"
        num_cloud_layers.units = "unitless"
        num_cloud_layers.missing_value = -9999
        num_cloud_layers[:] = [1, 0, 0, 0, 0, 0]

    def _add_linear_depol_ratio(self) -> None:
        linear_depol_ratio = self.dataset.createVariable(
            "linear_depol_ratio", "f4", ("time", "height")
        )
        linear_depol_ratio.long_name = "Linear depolarization ratio"
        linear_depol_ratio.units = "unitless"
        linear_depol_ratio.missing_value = -9999.0
        linear_depol_ratio.ancillary_variables = "qc_linear_depol_ratio"
        linear_depol_ratio[:] = [
            [-0.28459275, 0.977915, 0.38756308],
            [-0.35307893, 0.9776862, 0.39125702],
            [-0.4996107, 0.9772247, 0.3911428],
            [0.4311789, 0.9775953, 0.38763753],
            [0.16858189, 0.9769985, 0.38921818],
            [1.5727872, 0.97737384, 0.38858318],
        ]

    def _add_qc_linear_depol_ratio(self) -> None:
        qc_linear_depol_ratio = self.dataset.createVariable(
            "qc_linear_depol_ratio", "i4", ("time", "height")
        )
        qc_linear_depol_ratio.long_name = (
            "Quality check results on field: Linear depolarization ratio"
        )
        qc_linear_depol_ratio.units = "unitless"
        qc_linear_depol_ratio.comment = "This field contains bit packed integer values, where each bit represents a QC test on the data. Non-zero bits indicate the QC condition given in the description for those bits; a value of 0 (no bits set) indicates the data has not failed any QC tests."
        qc_linear_depol_ratio.flag_method = "bit"
        qc_linear_depol_ratio.bit_1_description = "The value of signal is zero in the denominator causing the value of depolarization ratio to be NaN, data value set to missing_value in output file."
        qc_linear_depol_ratio.bit_1_assessment = "Bad"
        qc_linear_depol_ratio.bit_2_description = "Data value not available in input file, data value set to missing_value in output file."
        qc_linear_depol_ratio.bit_2_assessment = "Bad"
        qc_linear_depol_ratio[:] = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    def _add_linear_depol_snr(self) -> None:
        linear_depol_snr = self.dataset.createVariable(
            "linear_depol_snr", "f4", ("time", "height")
        )
        linear_depol_snr.long_name = (
            "Signal to noise ratio for the linear depolarization ratio"
        )
        linear_depol_snr.units = "unitless"
        linear_depol_snr.missing_value = -9999.0
        linear_depol_snr.ancillary_variables = "qc_linear_depol_snr"
        linear_depol_snr[:] = [
            [-9999.0, 268.67264, 126.09152],
            [-9999.0, 268.61926, 126.32019],
            [-9999.0, 268.60895, 126.207695],
            [4.3232746, 268.49026, 125.94582],
            [3.128249, 268.46893, 126.202],
            [3.5918827, 268.5175, 125.94176],
        ]

    def _add_qc_linear_depol_snr(self) -> None:
        qc_linear_depol_snr = self.dataset.createVariable(
            "qc_linear_depol_snr", "i4", ("time", "height")
        )
        qc_linear_depol_snr.long_name = "Quality check results on field: Signal to noise ratio for the linear depolarization ratio"
        qc_linear_depol_snr.units = "unitless"
        qc_linear_depol_snr.description = "This field contains bit packed integer values, where each bit represents a QC test on the data. Non-zero bits indicate the QC condition given in the description for those bits; a value of 0 (no bits set) indicates the data has not failed any QC tests."
        qc_linear_depol_snr.flag_method = "bit"
        qc_linear_depol_snr.bit_1_description = "The value of signal is zero in the denominator causing the value of snr to be NaN, data value set to missing_value in output file."
        qc_linear_depol_snr.bit_1_assessment = "Bad"
        qc_linear_depol_snr.bit_2_description = "Data value not available in input file, data value set to missing_value in output file."
        qc_linear_depol_snr.bit_2_assessment = "Bad"
        qc_linear_depol_snr[:] = [
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    def _add_cloud_mask(self) -> None:
        cloud_mask = self.dataset.createVariable("cloud_mask", "i4", ("time", "height"))
        cloud_mask.long_name = "Cloud mask"
        cloud_mask.units = "unitless"
        cloud_mask.comment = "Cloud mask indeterminate below 500 m"
        cloud_mask.flag_values = [0, 1]
        cloud_mask.flag_meanings = "clear cloudy"
        cloud_mask.flag_0_description = "Clear"
        cloud_mask.flag_1_description = "Cloudy"
        cloud_mask.missing_value = -9999
        cloud_mask.ancillary_variables = "qc_cloud_mask"
        cloud_mask[:] = [
            [-9999, 0, 1],
            [-9999, 0, 1],
            [-9999, 0, 1],
            [-9999, 0, 1],
            [-9999, 0, 1],
            [-9999, 0, 1],
        ]

    def _add_qc_cloud_mask(self) -> None:
        qc_cloud_mask = self.dataset.createVariable(
            "qc_cloud_mask", "i4", ("time", "height")
        )
        qc_cloud_mask.long_name = "Quality check results on field: Cloud mask"
        qc_cloud_mask.units = "unitless"
        qc_cloud_mask.description = "This field contains bit packed integer values, where each bit represents a QC test on the data. Non-zero bits indicate the QC condition given in the description for those bits; a value of 0 (no bits set) indicates the data has not failed any QC tests."
        qc_cloud_mask.flag_method = "bit"
        qc_cloud_mask.bit_1_description = "Unable to determine the cloud mask, data value set to missing_value in output file."
        qc_cloud_mask.bit_1_assessment = "Bad"
        qc_cloud_mask.bit_2_description = "backscatter is unusable due to instrument malfunction, data value set to missing_value in output file."
        qc_cloud_mask.bit_2_assessment = "Bad"
        qc_cloud_mask[:] = [
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
        ]

    def _add_cloud_base_layer(self) -> None:
        cloud_base_layer = self.dataset.createVariable(
            "cloud_base_layer", "f4", ("time", "layer")
        )
        cloud_base_layer.long_name = "Cloud base for each layer"
        cloud_base_layer.units = "km"
        cloud_base_layer.missing_value = -9999.0
        cloud_base_layer.comment = (
            "Positive values indicate the height of the cloud base"
        )
        cloud_base_layer[:] = [
            [0.682038, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
        ]

    def _add_cloud_top_layer(self) -> None:
        cloud_top_layer = self.dataset.createVariable(
            "cloud_top_layer", "f4", ("time", "layer")
        )
        cloud_top_layer.long_name = "Cloud top for each layer above ground level (AGL)"
        cloud_top_layer.units = "km"
        cloud_top_layer.missing_value = -9999.0
        cloud_top_layer.comment = "Positive values indicate the height of the cloud top"
        cloud_top_layer[:] = [
            [1.7912695, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
        ]

    def _add_backscatter(self) -> None:
        backscatter = self.dataset.createVariable(
            "backscatter", "f4", ("time", "height")
        )
        backscatter.long_name = "Total attenuated backscatter"
        backscatter.units = "counts/microsecond"
        backscatter.missing_value = -9999.0
        backscatter.comment = (
            "background subtracted, overlap, energy and dead-time corrected"
        )
        backscatter.calculation = "((copol+(2*crosspol))*overlap)/energy"
        backscatter.data_quality_comment = (
            "Data quality ok for both cloud and aerosol analysis"
        )
        backscatter.normalization_factor = "N/A"
        backscatter.backscatter_data_quality_comment = (
            "Data quality ok for both cloud and aerosol analysis"
        )
        backscatter.ancillary_variables = "qc_backscatter"
        backscatter[:] = [
            [6.0800654e-01, 2.4693540e03, 3.1821454e02],
            [2.6602274e-01, 2.4681104e03, 3.1809964e02],
            [1.3450946e-04, 2.4683525e03, 3.1760068e02],
            [1.8580000e00, 2.4659375e03, 3.1742856e02],
            [1.5707090e00, 2.4655125e03, 3.1815848e02],
            [9.6904886e-01, 2.4663083e03, 3.1706573e02],
        ]

    def _add_qc_backscatter(self) -> None:
        qc_backscatter = self.dataset.createVariable(
            "qc_backscatter", "i4", ("time", "height")
        )
        qc_backscatter.long_name = (
            "Quality check results on field: Total attenuated backscatter"
        )
        qc_backscatter.units = "unitless"
        qc_backscatter.description = "This field contains bit packed integer values, where each bit represents a QC test on the data. Non-zero bits indicate the QC condition given in the description for those bits; a value of 0 (no bits set) indicates the data has not failed any QC tests."
        qc_backscatter.flag_method = "bit"
        qc_backscatter.bit_1_description = "The value of backscatter is not finite, data value set to missing_value in output file."
        qc_backscatter.bit_1_assessment = "Bad"
        qc_backscatter[:] = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    def _add_backscatter_snr(self) -> None:
        backscatter_snr = self.dataset.createVariable(
            "backscatter_snr", "f4", ("time", "height")
        )
        backscatter_snr.long_name = "Signal to noise ratio of backscatter"
        backscatter_snr.units = "unitless"
        backscatter_snr.missing_value = -9999.0
        backscatter_snr.ancillary_variables = "qc_backscatter_snr"
        backscatter_snr[:] = [
            [0.3529468, 0.3529468, 0.3529468],
            [0.35290167, 0.35290167, 0.35290167],
            [0.35320997, 0.35320997, 0.35320997],
            [0.35394973, 0.35394973, 0.35394973],
            [0.35389477, 0.35389477, 0.35389477],
            [0.35366353, 0.35366353, 0.35366353],
        ]

    def _add_qc_backscatter_snr(self) -> None:
        qc_backscatter_snr = self.dataset.createVariable(
            "qc_backscatter_snr", "i4", ("time", "height")
        )
        qc_backscatter_snr.long_name = (
            "Quality check results on field: Signal to noise ratio of backscatter"
        )
        qc_backscatter_snr.units = "unitless"
        qc_backscatter_snr.description = "This field contains bit packed integer values, where each bit represents a QC test on the data. Non-zero bits indicate the QC condition given in the description for those bits; a value of 0 (no bits set) indicates the data has not failed any QC tests."
        qc_backscatter_snr.flag_method = "bit"
        qc_backscatter_snr.bit_1_description = "The value of Signal to noise ratio of backscatter is not finite, data value set to missing_value in output file."
        qc_backscatter_snr.bit_1_assessment = "Bad"
        qc_backscatter_snr[:] = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    def _add_background_signal(self) -> None:
        background_signal = self.dataset.createVariable(
            "background_signal", "f4", ("time",)
        )
        background_signal.long_name = "Background signal"
        background_signal.units = "counts/microsecond"
        background_signal.missing_value = -9999.0
        background_signal.comment = (
            "sum of co-polarized and cross polarized signals from input source"
        )
        background_signal[:] = [
            0.3424501,
            0.34605426,
            0.33168215,
            0.3724103,
            0.3804245,
            0.37163568,
        ]

    def _add_cloud_top_attenuation_flag(self) -> None:
        cloud_top_attenuation_flag = self.dataset.createVariable(
            "cloud_top_attenuation_flag", "i4", ("time",)
        )
        cloud_top_attenuation_flag.long_name = (
            "Flag indicating whether the beam was extinguished at indicated cloud top"
        )
        cloud_top_attenuation_flag.units = "unitless"
        cloud_top_attenuation_flag.missing_value = -9999
        cloud_top_attenuation_flag.flag_values = [0, 1]
        cloud_top_attenuation_flag.flag_meanings = (
            "beam_not_extinguished_by_layer beam_extinguished_by_layer"
        )
        cloud_top_attenuation_flag.flag_0_description = (
            "Indicates that the beam was not extinguished by the layer"
        )
        cloud_top_attenuation_flag.flag_1_description = (
            "Indicates that the beam was totally extinguished by the layer"
        )
        cloud_top_attenuation_flag[:] = [1, 0, 0, 0, 0, 0]

    def _add_shots_summed(self) -> None:
        shots_summed = self.dataset.createVariable("shots_summed", "f4", ("time",))
        shots_summed.long_name = "Number of lidar pulses summed"
        shots_summed.units = "unitless"
        shots_summed[:] = [37500.0, 37500.0, 37500.0, 37500.0, 37500.0, 37500.0]

    def _add_deadtime_correction_counts(self) -> None:
        deadtime_correction_counts = self.dataset.createVariable(
            "deadtime_correction_counts", "f4", ("num_deadtime_corr",)
        )
        deadtime_correction_counts.long_name = "Laboratory measured counts used to calculate the deadtime correction samples"
        deadtime_correction_counts.units = "counts/microsecond"
        deadtime_correction_counts[:] = [
            0.0174,
            0.0427,
            0.1072,
            0.2658,
            0.64790004,
            1.5681,
            2.3818998,
            3.5411,
            5.1162996,
            7.1609,
            9.4056,
            10.3771,
            11.3029,
            12.1121,
            13.8199005,
            13.422299,
        ]

    def _add_deadtime_correction(self) -> None:
        deadtime_correction = self.dataset.createVariable(
            "deadtime_correction", "f4", ("num_deadtime_corr",)
        )
        deadtime_correction.long_name = "Deadtime correction factor"
        deadtime_correction.units = "unitless"
        deadtime_correction[:] = (
            [
                1.0,
                1.02,
                1.02,
                1.04,
                1.07,
                1.11,
                1.16,
                1.23,
                1.35,
                1.54,
                1.85,
                2.11,
                2.44,
                2.86,
                3.4,
                4.09,
            ],
        )

    def _add_afterpulse_correction(self) -> None:
        afterpulse_correction = self.dataset.createVariable(
            "afterpulse_correction", "f4", ("height",)
        )
        afterpulse_correction.long_name = "Detector afterpulse from laser flash"
        afterpulse_correction.units = "counts/microsecond"
        afterpulse_correction.comment = "No afterpulse corrections are applied"
        afterpulse_correction[:] = [1.0, 1.0, 1.0]

    def _add_overlap_correction(self) -> None:
        overlap_correction = self.dataset.createVariable(
            "overlap_correction", "f4", ("height",)
        )
        overlap_correction.long_name = "Overlap correction"
        overlap_correction.units = "unitless"
        overlap_correction[:] = [
            547.11566,
            211.03833,
            101.589676,
        ]

    def _add_lat(self) -> None:
        lat = self.dataset.createVariable("lat", "f4")
        lat.long_name = "North latitude"
        lat.units = "degree_N"
        lat.standard_name = "latitude"
        lat.valid_min = -90.0
        lat.valid_max = 90.0
        lat[:] = 71.323

    def _add_lon(self) -> None:
        lon = self.dataset.createVariable("lon", "f4")
        lon.long_name = "East longitude"
        lon.units = "degree_E"
        lon.standard_name = "longitude"
        lon.valid_min = -180.0
        lon.valid_max = 180.0
        lon[:] = -156.609

    def _add_alt(self) -> None:
        alt = self.dataset.createVariable("alt", "f4")
        alt.long_name = "Altitude above mean sea level"
        alt.units = "m"
        alt.standard_name = "altitude"
        alt[:] = 8.0


class UtqiagvikMmcrRaw(RawDataHydrationStrategy):
    """Utqiagvik Mpl Raw Data Strategy."""

    time: int = 6
    nheights: int = 3
    numlayers: int = 10

    def _add_attributes(self, filename: str) -> None:
        self.dataset.Date = "Wed Jun 10 21:07:04 GMT 2009"
        self.dataset.Version = "$State: Release_4_0 $"
        self.dataset.Number_Input_Platforms = 4
        self.dataset.Input_Platforms = (
            "nsamplpolavgxxC1.c1,vap-mplpolavg-1.9-0,nsavceil25kC1.b1,nsammcrmomC1.b1"
        )
        self.dataset.Input_Platforms_Versions = "$State:,$,8.2,1.16"
        self.dataset.zeb_platform = "nsaarscl1clothC1.c1"
        self.dataset.Command_Line = (
            "arsc1/arscl2 -s YYYYMMDD -e YYYYMMDD SITE FACILITY QCFILE ZIPPING"
        )
        self.dataset.contact = ""
        self.dataset.commenta = "At each height and time, the MMCR reflectivity, velocity, width and signal-to-noise ratio always come from the same mode.  The mode is indicated by ModeId."
        self.dataset.commentb = "MeanDopplerVelocity, ModeId, qc_RadarArtifacts, qc_ReflectivityClutterFlag, SpectralWidth, and SignaltoNoiseRatio data are reported at all range gates for which there is a significant detection, including from clutter."
        self.dataset.commentc = "The value of qc_ReflectivityClutterFlag indicates whether or not the signal is from clutter."
        self.dataset.commentd = "Use the appropriate reflectivity fields (e.g., with clutter, with clutter removed, or best estimate) to filter the variables discussed in commentb."
        self.dataset.commente = "Missing (i.e., does not exist) data for a particular time period are indicated by a value of 10 for the ModeId, qc_RadarArtifacts, and qc_ReflectivityClutterFlag variables.  The geophysical variables should contain a value of -32768 at these times."
        self.dataset.commentf = "Note that -32768 is also used for the geophysical variables when there are no significant detections, in which case ModeId, qc_RadarArtifacts, and qc_ReflectivityClutterFlag are 0."

    def _add_dimensions(self, filename: str) -> None:
        self.dataset.createDimension("time", self.time)
        self.dataset.createDimension("nheights", self.nheights)
        self.dataset.createDimension("numlayers", self.numlayers)

    def _add_variables(self) -> None:
        self._add_base_time()
        self._add_time_offset()
        self._add_Heights()
        self._add_Reflectivity()
        self._add_ReflectivityNoClutter()
        self._add_ReflectivityBestEstimate()
        self._add_MeanDopplerVelocity()
        self._add_SpectralWidth()
        self._add_RadarFirstTop()
        self._add_ModeId()
        self._add_SignaltoNoiseRatio()
        self._add_CloudBasePrecipitation()
        self._add_CloudBaseCeilometerStd()
        self._add_CloudBaseCeilometerCloth()
        self._add_CloudBaseMplScott()
        self._add_CloudBaseMplCamp()
        self._add_CloudBaseMplCloth()
        self._add_CloudBaseBestEstimate()
        self._add_CloudMaskMplCamp()
        self._add_CloudMaskMplCloth()
        self._add_CloudLayerBottomHeightMplCamp()
        self._add_CloudLayerBottomHeightMplCloth()
        self._add_CloudLayerTopHeightMplCamp()
        self._add_CloudLayerTopHeightMplCloth()
        self._add_qc_RadarArtifacts()
        self._add_qc_ReflectivityClutterFlag()
        self._add_qc_CloudLayerTopHeightMplCamp()
        self._add_qc_CloudLayerTopHeightMplCloth()
        self._add_qc_BeamAttenuationMplCamp()
        self._add_qc_BeamAttenuationMplCloth()

    def _add_base_time(self) -> None:
        base_time = self.dataset.createVariable("base_time", "i4")
        base_time.long_name = "Beginning Time of File"
        base_time.units = "seconds since 1970-01-01 00:00:00 00:00"
        base_time.calendar_date = "Year 2008 Month 09 Day 24 00:00:00"
        base_time[:] = 1222214400

    def _add_time_offset(self) -> None:
        time_offset = self.dataset.createVariable("time_offset", "f8", ("time",))
        time_offset.long_name = "Time Offset from base_time"
        time_offset.units = "seconds"
        time_offset.comment = "none"
        time_offset[:] = [0.0, 10.0, 20.0, 30.0, 40.0, 50.0]

    def _add_Heights(self) -> None:
        Heights = self.dataset.createVariable("Heights", "f4", ("nheights",))
        Heights.long_name = "Height of Measured Value"
        Heights.units = "m AGL"
        Heights.comment = "none"
        Heights[:] = [75.67602, 119.383286, 163.09055]

    def _add_Reflectivity(self) -> None:
        Reflectivity = self.dataset.createVariable(
            "Reflectivity", "i2", ("time", "nheights")
        )
        Reflectivity.long_name = "MMCR Reflectivity"
        Reflectivity.units = "dBZ (X100)"
        Reflectivity.comment = "Divide Reflectivity by 100 to get dBZ"
        Reflectivity[:] = [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-6216, -5650, -6338],
            [-32768, -32768, -32768],
            [-6428, -6320, -7052],
            [-6162, -5892, -6603],
        ]

    def _add_ReflectivityNoClutter(self) -> None:
        ReflectivityNoClutter = self.dataset.createVariable(
            "ReflectivityNoClutter", "i2", ("time", "nheights")
        )
        ReflectivityNoClutter.long_name = "MMCR Reflectivity with Clutter Removed"
        ReflectivityNoClutter.units = "dBZ (X100)"
        ReflectivityNoClutter.comment = "Divide ReflectivityNoClutter by 100 to get dBZ"
        ReflectivityNoClutter[:] = [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
        ]

    def _add_ReflectivityBestEstimate(self) -> None:
        ReflectivityBestEstimate = self.dataset.createVariable(
            "ReflectivityBestEstimate", "i2", ("time", "nheights")
        )
        ReflectivityBestEstimate.long_name = (
            "MMCR Best Estimate of Hydrometeor Reflectivity"
        )
        ReflectivityBestEstimate.units = "dBZ (X100)"
        ReflectivityBestEstimate.comment = (
            "Divide ReflectivityBestEstimate by 100 to get dBZ"
        )
        ReflectivityBestEstimate[:] = [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
        ]

    def _add_MeanDopplerVelocity(self) -> None:
        MeanDopplerVelocity = self.dataset.createVariable(
            "MeanDopplerVelocity", "i2", ("time", "nheights")
        )
        MeanDopplerVelocity.long_name = "MMCR Mean Doppler Velocity"
        MeanDopplerVelocity.units = "m/s (X1000)"
        MeanDopplerVelocity.comment = "Divide MeanDopplerVelocity by 1000 to get m/s"
        MeanDopplerVelocity[:] = [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-3600, -3719, -3745],
            [-32768, -32768, -32768],
            [319, 3102, 3701],
            [-3843, 461, 1387],
        ]

    def _add_SpectralWidth(self) -> None:
        SpectralWidth = self.dataset.createVariable(
            "SpectralWidth", "i2", ("time", "nheights")
        )
        SpectralWidth.long_name = "MMCR Spectral Width"
        SpectralWidth.units = "m/s (X1000)"
        SpectralWidth.comment = "Divide SpectralWidth by 1000 to get m/s"
        SpectralWidth[:] = [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [41, 52, 54],
            [-32768, -32768, -32768],
            [41, 41, 41],
            [41, 41, 41],
        ]

    def _add_RadarFirstTop(self) -> None:
        RadarFirstTop = self.dataset.createVariable("RadarFirstTop", "f4", ("time",))
        RadarFirstTop.long_name = (
            "MMCR Top Height of Lowest Detected Layer before Clutter Removal"
        )
        RadarFirstTop.units = "m AGL"
        RadarFirstTop.comment = "-3. Data do not exist, 0. No significant detection in column, > 0. Top Height of Lowest Cloud/Clutter Layer"
        RadarFirstTop[:] = [-3.0, -3.0, 184.94418, 0.0, 184.94418, 184.94418]

    def _add_ModeId(self) -> None:
        ModeId = self.dataset.createVariable("ModeId", "S1", ("time", "nheights"))
        ModeId.long_name = "MMCR Mode I.D."
        ModeId.units = "unitless"
        ModeId.comment = (
            "0 No significant power return, 1-5 Valid modes, 10 Data do not exist"
        )
        ModeId[:] = [
            [b"\n", b"\n", b"\n"],
            [b"\n", b"\n", b"\n"],
            [b"\x01", b"\x01", b"\x01"],
            [b"", b"", b""],
            [b"\x01", b"\x01", b"\x01"],
            [b"\x01", b"\x01", b"\x01"],
        ]

    def _add_SignaltoNoiseRatio(self) -> None:
        SignaltoNoiseRatio = self.dataset.createVariable(
            "SignaltoNoiseRatio", "i2", ("time", "nheights")
        )
        SignaltoNoiseRatio.long_name = "MMCR Signal-to-Noise Ratio"
        SignaltoNoiseRatio.units = "dB (X100)"
        SignaltoNoiseRatio.comment = "Divide SignaltoNoiseRatio by 100 to get dB"
        SignaltoNoiseRatio[:] = [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-2142, -1819, -2524],
            [-32768, -32768, -32768],
            [-2236, -2175, -2915],
            [-2143, -1977, -2700],
        ]

    def _add_CloudBasePrecipitation(self) -> None:
        CloudBasePrecipitation = self.dataset.createVariable(
            "CloudBasePrecipitation", "f4", ("time",)
        )
        CloudBasePrecipitation.long_name = (
            "Microwave Radiometer Wet Window/Optical Rain Gauge Cloud Base Height"
        )
        CloudBasePrecipitation.units = "m AGL"
        CloudBasePrecipitation.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
        CloudBasePrecipitation[:] = [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0]

    def _add_CloudBaseCeilometerStd(self) -> None:
        CloudBaseCeilometerStd = self.dataset.createVariable(
            "CloudBaseCeilometerStd", "f4", ("time",)
        )
        CloudBaseCeilometerStd.long_name = (
            "BLC/VCEIL Standard Algorithm Cloud Base Height"
        )
        CloudBaseCeilometerStd.units = "m AGL"
        CloudBaseCeilometerStd.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
        CloudBaseCeilometerStd[:] = [716.28, 716.28, 716.28, 716.28, 716.28, 1371.6]

    def _add_CloudBaseCeilometerCloth(self) -> None:
        CloudBaseCeilometerCloth = self.dataset.createVariable(
            "CloudBaseCeilometerCloth", "f4", ("time",)
        )
        CloudBaseCeilometerCloth.long_name = (
            "BLC/VCEIL Clothiaux et al. Algorithm Cloud Base Height"
        )
        CloudBaseCeilometerCloth.units = "m AGL"
        CloudBaseCeilometerCloth.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
        CloudBaseCeilometerCloth[:] = [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0]

    def _add_CloudBaseMplScott(self) -> None:
        CloudBaseMplScott = self.dataset.createVariable(
            "CloudBaseMplScott", "f4", ("time",)
        )
        CloudBaseMplScott.long_name = "MPL Scott Algorithm Cloud Base Height"
        CloudBaseMplScott.units = "m AGL"
        CloudBaseMplScott.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
        CloudBaseMplScott[:] = [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0]

    def _add_CloudBaseMplCamp(self) -> None:
        CloudBaseMplCamp = self.dataset.createVariable(
            "CloudBaseMplCamp", "f4", ("time",)
        )
        CloudBaseMplCamp.long_name = "MPL Campbell et al. Algorithm Cloud Base Height"
        CloudBaseMplCamp.units = "m AGL"
        CloudBaseMplCamp.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
        CloudBaseMplCamp[:] = [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0]

    def _add_CloudBaseMplCloth(self) -> None:
        CloudBaseMplCloth = self.dataset.createVariable(
            "CloudBaseMplCloth", "f4", ("time",)
        )
        CloudBaseMplCloth.long_name = "MPL Clothiaux et al. Algorithm Cloud Base Height"
        CloudBaseMplCloth.units = "m AGL"
        CloudBaseMplCloth.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
        CloudBaseMplCloth[:] = [-3.0, -3.0, -3.0, 719.0529, 719.0529, 719.0529]

    def _add_CloudBaseBestEstimate(self) -> None:
        CloudBaseBestEstimate = self.dataset.createVariable(
            "CloudBaseBestEstimate", "f4", ("time",)
        )
        CloudBaseBestEstimate.long_name = "LASER Cloud Base Height Best Estimate"
        CloudBaseBestEstimate.units = "m AGL"
        CloudBaseBestEstimate.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
        CloudBaseBestEstimate[:] = [716.28, 716.28, 716.28, 716.28, 716.28, 1371.6]

    def _add_CloudMaskMplCamp(self) -> None:
        CloudMaskMplCamp = self.dataset.createVariable(
            "CloudMaskMplCamp", "i2", ("time", "nheights")
        )
        CloudMaskMplCamp.long_name = (
            "MPL Campbell et al. Algorithm Cloud Mask Occurrence"
        )
        CloudMaskMplCamp.units = "Percent(x100)"
        CloudMaskMplCamp.comment = "-30000 Data do not exist, -20000 Beam blocked, -10000 Beam attenuated, 0 No cloud (clear), > 0 Valid cloud"
        CloudMaskMplCamp[:] = [
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
        ]

    def _add_CloudMaskMplCloth(self) -> None:
        CloudMaskMplCloth = self.dataset.createVariable(
            "CloudMaskMplCloth", "i2", ("time", "nheights")
        )
        CloudMaskMplCloth.long_name = (
            "MPL Clothiaux et al. Algorithm Cloud Mask Occurrence"
        )
        CloudMaskMplCloth.units = "Percent(x100)"
        CloudMaskMplCloth.comment = "-30000 Data do not exist, -20000 Beam blocked, -10000 Beam attenuated, 0 No cloud (clear), > 0 Valid cloud"
        CloudMaskMplCloth[:] = [
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

    def _add_CloudLayerBottomHeightMplCamp(self) -> None:
        CloudLayerBottomHeightMplCamp = self.dataset.createVariable(
            "CloudLayerBottomHeightMplCamp", "f4", ("time", "numlayers")
        )
        CloudLayerBottomHeightMplCamp.long_name = "Bottom Height of Hydrometeor Layer from Composite (MMCR/Campbell et al. MPL) Algorithms"
        CloudLayerBottomHeightMplCamp.units = "m AGL"
        CloudLayerBottomHeightMplCamp.comment = "none"
        CloudLayerBottomHeightMplCamp[:] = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]

    def _add_CloudLayerBottomHeightMplCloth(self) -> None:
        CloudLayerBottomHeightMplCloth = self.dataset.createVariable(
            "CloudLayerBottomHeightMplCloth", "f4", ("time", "numlayers")
        )
        CloudLayerBottomHeightMplCloth.long_name = "Bottom Height of Hydrometeor Layer from Composite (MMCR/Clothiaux et al. MPL) Algorithms"
        CloudLayerBottomHeightMplCloth.units = "m AGL"
        CloudLayerBottomHeightMplCloth.comment = "none"
        CloudLayerBottomHeightMplCloth[:] = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1299.4795, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1299.4795, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1299.4795, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]

    def _add_CloudLayerTopHeightMplCamp(self) -> None:
        CloudLayerTopHeightMplCamp = self.dataset.createVariable(
            "CloudLayerTopHeightMplCamp", "f4", ("time", "numlayers")
        )
        CloudLayerTopHeightMplCamp.long_name = "Top Height of Hydrometeor Layer from Composite (MMCR/Campbell et al. MPL) Algorithms"
        CloudLayerTopHeightMplCamp.units = "m AGL"
        CloudLayerTopHeightMplCamp.comment = "none"
        CloudLayerTopHeightMplCamp[:] = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]

    def _add_CloudLayerTopHeightMplCloth(self) -> None:
        CloudLayerTopHeightMplCloth = self.dataset.createVariable(
            "CloudLayerTopHeightMplCloth", "f4", ("time", "numlayers")
        )
        CloudLayerTopHeightMplCloth.long_name = "Top Height of Hydrometeor Layer from Composite (MMCR/Clothiaux et al. MPL) Algorithms"
        CloudLayerTopHeightMplCloth.units = "m AGL"
        CloudLayerTopHeightMplCloth.comment = "none"
        CloudLayerTopHeightMplCloth[:] = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1430.6013, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1430.6013, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1430.6013, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]

    def _add_qc_RadarArtifacts(self) -> None:
        qc_RadarArtifacts = self.dataset.createVariable(
            "qc_RadarArtifacts", "S1", ("time", "nheights")
        )
        qc_RadarArtifacts.long_name = "MMCR Mode Quality Control Flags"
        qc_RadarArtifacts.units = "unitless"
        qc_RadarArtifacts.comment = "0 No significant power return, 1 Significant, problem free data, 2 Second trip echo problems, 3 Coherent integration problems, 4 Second trip echo and coherent integration problems, 5 Pulse coding problems, 10 Data do not exist"
        qc_RadarArtifacts[:] = [
            [b"\n", b"\n", b"\n"],
            [b"\n", b"\n", b"\n"],
            [b"\x01", b"\x01", b"\x01"],
            [b"", b"", b""],
            [b"\x01", b"\x01", b"\x01"],
            [b"\x01", b"\x01", b"\x01"],
        ]

    def _add_qc_ReflectivityClutterFlag(self) -> None:
        qc_ReflectivityClutterFlag = self.dataset.createVariable(
            "qc_ReflectivityClutterFlag", "S1", ("time", "nheights")
        )
        qc_ReflectivityClutterFlag.long_name = "MMCR Reflectivity Clutter Flags"
        qc_ReflectivityClutterFlag.units = "unitless"
        qc_ReflectivityClutterFlag.comment = "0 No significant power return, 1 Significant, problem free data, 2 Clutter and cloud contribution, 3 Clutter only contribution, 10 Data do not exist"
        qc_ReflectivityClutterFlag[:] = [
            [b"\n", b"\n", b"\n"],
            [b"\n", b"\n", b"\n"],
            [b"\x03", b"\x03", b"\x03"],
            [b"", b"", b""],
            [b"\x03", b"\x03", b"\x03"],
            [b"\x03", b"\x03", b"\x03"],
        ]

    def _add_qc_CloudLayerTopHeightMplCamp(self) -> None:
        qc_CloudLayerTopHeightMplCamp = self.dataset.createVariable(
            "qc_CloudLayerTopHeightMplCamp", "f4", ("time", "numlayers")
        )
        qc_CloudLayerTopHeightMplCamp.long_name = "Value Indicating the Reliability of the Layer Top Height Using the Campbell et al. MPL Algorithm"
        qc_CloudLayerTopHeightMplCamp.units = "unitless"
        qc_CloudLayerTopHeightMplCamp.comment = "none"
        qc_CloudLayerTopHeightMplCamp[:] = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]

    def _add_qc_CloudLayerTopHeightMplCloth(self) -> None:
        qc_CloudLayerTopHeightMplCloth = self.dataset.createVariable(
            "qc_CloudLayerTopHeightMplCloth", "f4", ("time", "numlayers")
        )
        qc_CloudLayerTopHeightMplCloth.long_name = "Value Indicating the Reliability of the Layer Top Height Using the Clothiaux et al. MPL Algorithm"
        qc_CloudLayerTopHeightMplCloth.units = "unitless"
        qc_CloudLayerTopHeightMplCloth.comment = "none"
        qc_CloudLayerTopHeightMplCloth[:] = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]

    def _add_qc_BeamAttenuationMplCamp(self) -> None:
        qc_BeamAttenuationMplCamp = self.dataset.createVariable(
            "qc_BeamAttenuationMplCamp", "f4", ("time",)
        )
        qc_BeamAttenuationMplCamp.long_name = (
            "MPL Campbell et al. Algorithm Beam Attenuation Assessment"
        )
        qc_BeamAttenuationMplCamp.units = "unitless"
        qc_BeamAttenuationMplCamp.comment = "-9. Data do not exist, -2. Beam blocked, -1. Beam attenuated, 0. No cloud (clear), 1. Beam penetrated atmosphere"
        qc_BeamAttenuationMplCamp[:] = [-9.0, -9.0, -9.0, -9.0, -9.0, -9.0]

    def _add_qc_BeamAttenuationMplCloth(self) -> None:
        qc_BeamAttenuationMplCloth = self.dataset.createVariable(
            "qc_BeamAttenuationMplCloth", "f4", ("time",)
        )
        qc_BeamAttenuationMplCloth.long_name = (
            "MPL Cloth et al. Algorithm Beam Attenuation Assessment"
        )
        qc_BeamAttenuationMplCloth.units = "unitless"
        qc_BeamAttenuationMplCloth.comment = "-9. Data do not exist, Log10(Signal Power above Cloud/Estimated Clearsky Power above Cloud)"
        qc_BeamAttenuationMplCloth[:] = [
            -9.0,
            -9.0,
            -9.0,
            -1.2243652,
            -1.2243652,
            -1.2243652,
        ]
