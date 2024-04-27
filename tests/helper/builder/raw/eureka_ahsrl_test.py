"""Test the creation of netCDF files."""

import os
from math import isclose
from typing import Generator

import pytest
from numpy import allclose, infty, isinf, isnan, nan

from sio_postdoc.access import DataSet
from tests.helper.builder.raw.context import RawDataContext
from tests.helper.builder.raw.strategies import EurekaAhsrlRaw
from tests.helper.builder.raw.types import Instrument, Observatory


@pytest.fixture(scope="module")
def dataset() -> Generator[DataSet, None, None]:
    # Arrange
    data = RawDataContext(Observatory.EUREKA, Instrument.AHSRL)
    data.hydrate()
    dataset = DataSet(data.filename)
    # Test
    yield dataset
    # Cleanup
    dataset.close()
    os.remove(data.filename)


def test_attributes(dataset):
    assert (
        dataset.code_version
        == "$Id: processed_netcdf.m,v 1.96 2008/10/29 15:32:21 jpgarcia Exp $"
    )
    assert (
        dataset.load_calibration_version
        == "$Id: load_calibration.m,v 1.25 2008/10/30 15:04:39 eloranta Exp $"
    )
    assert (
        dataset.get_internal_cal_vals_version
        == "$Id: get_internal_cal_vals.m,v 1.109 2008/09/12 21:20:05 eloranta Exp $"
    )
    assert (
        dataset.calvals
        == "$Id: calvals_ahsrl.m,v 1.108 2008/10/31 17:19:06 eloranta Exp $"
    )
    assert (
        dataset.find_new_cal_times_version
        == "$Id: find_new_cal_times.m,v 1.21 2008/02/25 19:33:32 jpgarcia Exp $"
    )
    assert (
        dataset.radiosonde_profile_version
        == "$Id: radiosonde_profile.m,v 1.30 2008/04/09 17:04:51 jpgarcia Exp $"
    )
    assert (
        dataset.fetch_cal_version
        == "$Id: fetch_cal.m,v 1.19 2008/09/04 21:06:16 eloranta Exp $"
    )
    assert (
        dataset.quick_cal_version
        == "$Id: quick_cal.m,v 1.58 2008/10/30 15:03:20 eloranta Exp $"
    )
    assert (
        dataset.processed_netcdf_version
        == "$Id: processed_netcdf.m,v 1.96 2008/10/29 15:32:21 jpgarcia Exp $"
    )
    assert (
        dataset.process_data_version
        == "$Id: process_data.m,v 1.202 2008/10/30 15:04:39 eloranta Exp $"
    )
    assert (
        dataset.timefill_sum_version
        == "$Id: time_block.cc,v 1.54 2008/04/16 21:33:02 jpgarcia Exp $"
    )
    assert (
        dataset.timefill_average_version
        == "$Id: time_block.cc,v 1.54 2008/04/16 21:33:02 jpgarcia Exp $"
    )
    assert dataset.file_version == 20050323
    assert dataset.time_zone == "UTC"
    assert dataset.file_created == "2008-11-05 01:44:26"
    assert dataset.Conventions == "COARDS"
    assert dataset.time_axis_average_mode == "time"
    assert dataset.time_axis_average_parameter == 30.0
    assert dataset.range_axis_average_parameter == 30.0
    assert dataset.featureset == 8175
    assert dataset.featureset_version == "$Revision: 1.13 $"
    assert dataset.processing_parameters__qc_params__min_radar_backscat == 1e-15
    assert dataset.processing_parameters__qc_params__mol_lost == 1.0
    assert dataset.processing_parameters__qc_params__lock_level == 0.6
    assert dataset.processing_parameters__qc_params__min_radar_dBz == -66.1
    assert dataset.processing_parameters__qc_params__backscat_snr == 1.0
    assert dataset.processing_parameters__particlesettings__alpha_water == 2.0
    assert dataset.processing_parameters__particlesettings__g_water == 1.0
    assert dataset.processing_parameters__particlesettings__alpha_ice == 1.0
    assert dataset.processing_parameters__particlesettings__g_ice == 1.0
    assert (
        dataset.processing_parameters__particlesettings__type
        == "Bullet Rosettes (Mitchell 1996)"
    )
    assert dataset.processing_parameters__particlesettings__Dr == 60.0
    assert dataset.processing_parameters__particlesettings__sigma_a == 1.0
    assert dataset.processing_parameters__particlesettings__sigma_v == 0.26
    assert dataset.processing_parameters__particlesettings__delta_a1 == 2.0
    assert dataset.processing_parameters__particlesettings__delta_v1 == 3.0
    assert dataset.processing_parameters__particlesettings__delta_a2 == 1.57
    assert dataset.processing_parameters__particlesettings__delta_v2 == 2.26
    assert dataset.processing_parameters__particlesettings__h20_depol_threshold == 0.05
    assert dataset.processing_parameters__particlesettings__p180_ice == 0.035


def test_dimensions(dataset):
    assert dataset.dimensions["time"].size == EurekaAhsrlRaw._time
    assert dataset.dimensions["altitude"].size == EurekaAhsrlRaw._altitude
    assert dataset.dimensions["time_vector"].size == 8
    assert dataset.dimensions["calibration"].size == 3
    assert dataset.dimensions["sondenamelength"].size == 6
    assert dataset.dimensions["i2header"].size == 9
    assert dataset.dimensions["geoheader"].size == 2
    assert dataset.dimensions["apheader"].size == 3


def test_base_time(dataset):
    assert str(dataset["base_time"].dtype) == "int32"
    assert dataset["base_time"].string == "2008-09-21 00:00:00 UTC"
    assert dataset["base_time"].long_name == "Base seconds since Unix Epoch"
    assert dataset["base_time"].units == "seconds since 1970-01-01 00:00:00 UTC"
    assert int(dataset["base_time"][:].data) == 1221955200


def test_first_time(dataset):
    assert str(dataset["first_time"].dtype) == "int16"
    assert dataset["first_time"].long_name == "First Time in file"
    assert list(dataset["first_time"][:].data) == [2008, 9, 21, 0, 0, 0, 0, 0]


def test_last_time(dataset):
    assert str(dataset["last_time"].dtype) == "int16"
    assert dataset["last_time"].long_name == "Last Time in file"
    assert list(dataset["last_time"][:].data) == [2008, 9, 21, 23, 59, 58, 88, 24]


def test_time(dataset):
    assert str(dataset["time"].dtype) == "float64"
    assert dataset["time"].long_name == "Time"
    assert dataset["time"].units == "seconds since 2008-09-21 00:00:00 UTC"
    assert allclose(
        dataset["time"][:].data,
        [
            -1.335016,
            29.401152,
            59.137664,
            87.875208,
            121.05104,
            150.789744,
        ],
    )


def test_time_offset(dataset):
    assert str(dataset["time_offset"].dtype) == "float64"
    assert dataset["time_offset"].long_name == "Time offset from base_time"
    assert dataset["time_offset"].description == 'same times as "First time in record"'
    assert dataset["time_offset"].units == "seconds since 2008-09-21 00:00:00 UTC"
    assert allclose(
        dataset["time_offset"][:].data,
        [
            -1.335016,
            29.401152,
            59.137664,
            87.875208,
            121.05104,
            150.789744,
        ],
    )


def test_start_time(dataset):
    assert str(dataset["start_time"].dtype) == "int16"
    assert dataset["start_time"].long_name == "First Time in record"
    assert (
        dataset["start_time"].description
        == "time of first laser shot in averaging interval"
    )
    assert allclose(
        dataset["start_time"][:].data,
        [
            [2008, 9, 20, 23, 59, 58, 664, 984],
            [2008, 9, 21, 0, 0, 29, 401, 152],
            [2008, 9, 21, 0, 0, 59, 137, 664],
            [2008, 9, 21, 0, 1, 27, 875, 208],
            [2008, 9, 21, 0, 2, 1, 51, 40],
            [2008, 9, 21, 0, 2, 30, 789, 744],
        ],
    )


def test_mean_time(dataset):
    assert str(dataset["mean_time"].dtype) == "int16"
    assert dataset["mean_time"].long_name == "mean time of record"
    assert (
        dataset["mean_time"].description
        == "mean time of laser shots collected in averaging interval"
    )
    assert allclose(
        dataset["mean_time"][:].data,
        [
            [2008, 9, 21, 0, 0, 13, 694, 104],
            [2008, 9, 21, 0, 0, 43, 430, 184],
            [2008, 9, 21, 0, 1, 13, 167, 368],
            [2008, 9, 21, 0, 1, 44, 142, 360],
            [2008, 9, 21, 0, 2, 15, 81, 160],
            [2008, 9, 21, 0, 2, 43, 820, 576],
        ],
    )


def test_end_time(dataset):
    assert str(dataset["end_time"].dtype) == "int16"
    assert dataset["end_time"].long_name == "Last Time in record"
    assert (
        dataset["end_time"].description
        == "time of last laser shot in averaging interval"
    )
    assert allclose(
        dataset["end_time"][:].data,
        [
            [2008, 9, 21, 0, 0, 29, 305, 528],
            [2008, 9, 21, 0, 0, 59, 42, 64],
            [2008, 9, 21, 0, 1, 27, 779, 584],
            [2008, 9, 21, 0, 2, 0, 975, 424],
            [2008, 9, 21, 0, 2, 30, 694, 112],
            [2008, 9, 21, 0, 3, 0, 434, 496],
        ],
    )


def test_latitude(dataset):
    assert str(dataset["latitude"].dtype) == "float32"
    assert dataset["latitude"].long_name == "latitude of lidar"
    assert dataset["latitude"].units == "degree_N"
    assert isclose(dataset["latitude"][:].data, 79.9903, abs_tol=1e-5)


def test_longitude(dataset):
    assert str(dataset["longitude"].dtype) == "float32"
    assert dataset["longitude"].long_name == "longitude of lidar"
    assert dataset["longitude"].units == "degree_W"
    assert isclose(dataset["longitude"][:].data, 85.9389, abs_tol=1e-5)


def test_range_resolution(dataset):
    assert str(dataset["range_resolution"].dtype) == "float32"
    assert dataset["range_resolution"].long_name == "Range resolution"
    assert (
        dataset["range_resolution"].description
        == "vertical distance between data points after averaging"
    )
    assert dataset["range_resolution"].units == "meters"
    assert float(dataset["range_resolution"][:].data) == 30.0


def test_time_average(dataset):
    assert str(dataset["time_average"].dtype) == "float32"
    assert dataset["time_average"].long_name == "Time Averaging Width"
    assert (
        dataset["time_average"].description
        == "Time between data points after averaging"
    )
    assert dataset["time_average"].units == "seconds"
    assert float(dataset["time_average"][:].data) == 30.0


def test_new_cal_times(dataset):
    assert str(dataset["new_cal_times"].dtype) == "int16"
    assert dataset["new_cal_times"].long_name == "Time of Calibration Change"
    assert (
        dataset["new_cal_times"].description
        == "New raob or system calibration data triggered recalibration"
    )
    assert allclose(
        dataset["new_cal_times"][:].data,
        [
            [2008, 9, 21, 0, 0, 0, 0, 0],
            [2008, 9, 21, 6, 0, 0, 0, 0],
            [2008, 9, 21, 18, 0, 0, 0, 0],
        ],
    )


def test_altitude(dataset):
    assert str(dataset["altitude"].dtype) == "float32"
    assert dataset["altitude"].long_name == "Height above lidar"
    assert dataset["altitude"].units == "meters"
    assert allclose(dataset["altitude"][:].data, [11.25, 41.25, 71.25])


def test_new_cal_trigger(dataset):
    assert str(dataset["new_cal_trigger"].dtype) == "int8"
    assert dataset["new_cal_trigger"].long_name == "Trigger of Calibration Change"
    assert dataset["new_cal_trigger"].description == "reason for recalibration"
    assert dataset["new_cal_trigger"].bit_0 == "radiosonde profile"
    assert dataset["new_cal_trigger"].bit_1 == "i2 scan"
    assert dataset["new_cal_trigger"].bit_2 == "geometry"
    assert allclose(dataset["new_cal_trigger"][:].data, [2, 2, 2])


def test_new_cal_offset(dataset):
    assert str(dataset["new_cal_offset"].dtype) == "int16"
    assert dataset["new_cal_offset"].long_name == "Record Dimension equivalent Offset"
    assert dataset["new_cal_offset"].min_value == 0
    assert allclose(dataset["new_cal_offset"][:].data, [0, 719, 2159])


def test_temperature_profile(dataset):
    assert str(dataset["temperature_profile"].dtype) == "float32"
    assert dataset["temperature_profile"].long_name == "Raob Temperature Profile"
    assert (
        dataset["temperature_profile"].description
        == "Temperature interpolated to requested altitude resolution"
    )
    assert dataset["temperature_profile"].units == "degrees Kelvin"
    assert allclose(
        dataset["temperature_profile"][:].data,
        [
            [nan, 270.145, 270.68594],
            [nan, 269.72464, 270.04163],
            [nan, 268.13953, 267.86047],
        ],
        equal_nan=True,
    )


def test_pressure_profile(dataset):
    assert str(dataset["pressure_profile"].dtype) == "float32"
    assert dataset["pressure_profile"].long_name == "Raob pressure Profile"
    assert (
        dataset["pressure_profile"].description
        == "Pressure interpolated to requested altitude resolution"
    )
    assert dataset["pressure_profile"].units == "hectopascals"
    assert allclose(
        dataset["pressure_profile"][:].data,
        [
            [nan, 1001.35, 997.65625],
            [nan, 1004.2226, 1000.5187],
            [nan, 1006.0436, 1002.2064],
        ],
        equal_nan=True,
    )


def test_dewpoint_profile(dataset):
    assert str(dataset["dewpoint_profile"].dtype) == "float32"
    assert dataset["dewpoint_profile"].long_name == "Raob Dewpoint Temperature Profile"
    assert (
        dataset["dewpoint_profile"].description
        == "Dewpoint interpolated to requested altitude resolution"
    )
    assert dataset["dewpoint_profile"].units == "degrees Kelvin"
    assert isnan(dataset["dewpoint_profile"].missing_value)
    assert allclose(
        dataset["dewpoint_profile"][:].data,
        [
            [nan, 268.09, 268.17578],
            [nan, 267.13458, 266.94662],
            [nan, 266.43954, 266.16046],
        ],
        equal_nan=True,
    )


def test_windspeed_profile(dataset):
    assert str(dataset["windspeed_profile"].dtype) == "float32"
    assert dataset["windspeed_profile"].long_name == "Raob Wind Speed Profile"
    assert (
        dataset["windspeed_profile"].description
        == "Speeds interpolated to requested altitude resolution"
    )
    assert dataset["windspeed_profile"].units == "m/s"
    assert isnan(dataset["windspeed_profile"].missing_value)
    assert allclose(
        dataset["windspeed_profile"][:].data,
        [
            [nan, 7.8125, 7.6393204],
            [nan, 10.472945, 9.496701],
            [nan, 9.322093, 10.577908],
        ],
        equal_nan=True,
    )


def test_winddir_profile(dataset):
    assert str(dataset["winddir_profile"].dtype) == "float32"
    assert dataset["winddir_profile"].long_name == "Raob Wind Direction Profile"
    assert (
        dataset["winddir_profile"].description
        == "Directions interpolated to requested altitude resolution"
    )
    assert dataset["winddir_profile"].units == "degrees"
    assert isnan(dataset["winddir_profile"].missing_value)
    assert allclose(
        dataset["winddir_profile"][:].data,
        [
            [nan, 283.875, 276.95996],
            [nan, 290.0, 289.32037],
            [nan, 287.7471, 286.0029],
        ],
        equal_nan=True,
    )


def test_raob_station(dataset):
    assert str(dataset["raob_station"].dtype) == "|S1"
    assert dataset["raob_station"].long_name == "Radiosonde Station ID"
    for row in dataset["raob_station"][:].data:
        assert list(row) == [b"Y", b"E", b"U", b" ", b" ", b" "]


def test_i2_txt_header(dataset):
    assert str(dataset["i2_txt_header"].dtype) == "|S1"
    assert dataset["i2_txt_header"].long_name == "i2_scan_file_text_info"
    assert (
        dataset["i2_txt_header"].description
        == "Contains name of file used to compute calibration"
    )
    for row in dataset["i2_txt_header"][:].data:
        assert list(row) == [b"", b"", b"", b"", b"", b"", b"", b"", b""]


def test_geo_txt_header(dataset):
    assert str(dataset["geo_txt_header"].dtype) == "|S1"
    assert (
        dataset["geo_txt_header"].long_name == "geometric_correction_file_txt_header."
    )
    for row in dataset["geo_txt_header"][:].data:
        assert list(row) == [b"", b""]


def test_ap_txt_header(dataset):
    assert str(dataset["ap_txt_header"].dtype) == "|S1"
    assert (
        dataset["ap_txt_header"].long_name == "afterpulse_correction_file_txt_header."
    )
    for row in dataset["ap_txt_header"][:].data:
        assert list(row) == [b"", b"", b""]


def test_raob_time_offset(dataset):
    assert str(dataset["raob_time_offset"].dtype) == "float64"
    assert dataset["raob_time_offset"].units == "seconds"
    assert dataset["raob_time_offset"].long_name == "Radiosonde Launch time offset"
    assert dataset["raob_time_offset"].description == "Time after base time in seconds"
    assert list(dataset["raob_time_offset"][:].data) == [0.0, 43200.0, 86400.0]


def test_raob_time_vector(dataset):
    assert str(dataset["raob_time_vector"].dtype) == "int16"
    assert dataset["raob_time_vector"].long_name == "Radiosonde Launch time vector"
    assert (
        dataset["raob_time_vector"].description
        == "Time in [year month day hour min sec ms us] format"
    )
    assert allclose(
        dataset["raob_time_vector"][:].data,
        [
            [2008, 9, 21, 0, 0, 0, 0, 0],
            [2008, 9, 21, 12, 0, 0, 0, 0],
            [2008, 9, 22, 0, 0, 0, 0, 0],
        ],
    )


def test_Cmc(dataset):
    assert str(dataset["Cmc"].dtype) == "float32"
    assert dataset["Cmc"].long_name == "Molecular in Combined Calibration"
    assert allclose(
        dataset["Cmc"][:].data,
        [
            [nan, 0.94958466, 0.94958436],
            [nan, 0.94975173, 0.9497569],
            [nan, 0.94991046, 0.9499172],
        ],
        equal_nan=True,
    )


def test_Cmm(dataset):
    assert str(dataset["Cmm"].dtype) == "float32"
    assert dataset["Cmm"].long_name == "Molecular in Molecular Calibration"
    assert allclose(
        dataset["Cmm"][:].data,
        [
            [nan, 1.6482617, 1.6479046],
            [nan, 1.6463878, 1.6459568],
            [nan, 1.6445122, 1.6440556],
        ],
        equal_nan=True,
    )


def test_Cam(dataset):
    assert str(dataset["Cam"].dtype) == "float32"
    assert dataset["Cam"].long_name == "Aerosol in Molecular Calibration"
    assert allclose(
        dataset["Cam"][:].data,
        [
            [0.001, 0.001, 0.001],
            [0.001, 0.001, 0.001],
            [0.001, 0.001, 0.001],
        ],
    )


def test_beta_m(dataset):
    assert str(dataset["beta_m"].dtype) == "float32"
    assert (
        dataset["beta_m"].long_name
        == "Raob molecular scattering cross section per unit volume"
    )
    assert dataset["beta_m"].units == "1/meter"
    assert dataset["beta_m"].plot_scale == "logarithmic"
    assert allclose(
        dataset["beta_m"][:].data,
        [
            [1.40424545e-05, 1.39996182e-05, 1.39039485e-05],
            [1.4113830e-05, 1.4043256e-05, 1.3976750e-05],
            [1.4194106e-05, 1.4155382e-05, 1.4115825e-05],
        ],
    )


def test_transmitted_energy(dataset):
    assert str(dataset["transmitted_energy"].dtype) == "float32"
    assert dataset["transmitted_energy"].long_name == "Transmitted Energy"
    assert dataset["transmitted_energy"].units == "Joules"
    assert isnan(dataset["transmitted_energy"].missing_value)
    assert allclose(
        dataset["transmitted_energy"][:].data,
        [12438.077, 12471.298, 12438.722, 13498.255, 12504.95, 12527.273],
    )


def test_piezovoltage(dataset):
    assert str(dataset["piezovoltage"].dtype) == "float32"
    assert dataset["piezovoltage"].long_name == "piezovoltage"
    assert dataset["piezovoltage"].units == "Volts"
    assert isnan(dataset["piezovoltage"].missing_value)
    assert allclose(
        dataset["piezovoltage"][:].data,
        [22.264818, 21.840616, 21.988153, 23.283442, 22.362902, 23.3313],
    )


def test_num_seeded_shots(dataset):
    assert str(dataset["num_seeded_shots"].dtype) == "int32"
    assert dataset["num_seeded_shots"].long_name == "Number of Seeded Shots"
    assert dataset["num_seeded_shots"].missing_value == -1
    assert list(dataset["num_seeded_shots"][:].data) == [
        119998,
        119996,
        120000,
        129998,
        119999,
        120000,
    ]


def test_c_pol_dark_count(dataset):
    assert str(dataset["c_pol_dark_count"].dtype) == "float32"
    assert dataset["c_pol_dark_count"].long_name == "Cross Polarization Dark Count"
    assert (
        dataset["c_pol_dark_count"].description
        == "total counts per averaging interval(eg. one altitude, one time)"
    )
    assert isnan(dataset["c_pol_dark_count"].missing_value)
    assert allclose(
        dataset["c_pol_dark_count"][:].data,
        [17.142857, 16.571428, 20.0, 13.714286, 14.857142, 10.857142],
    )


def test_mol_dark_count(dataset):
    assert str(dataset["mol_dark_count"].dtype) == "float32"
    assert dataset["mol_dark_count"].long_name == "Molecular Dark Count"
    assert (
        dataset["mol_dark_count"].description
        == "total counts per averaging interval(eg. one altitude, one time)"
    )
    assert dataset["mol_dark_count"].units == "counts"
    assert isnan(dataset["mol_dark_count"].missing_value)
    assert allclose(
        dataset["mol_dark_count"][:].data,
        [12.571428, 10.285714, 10.857142, 13.714286, 9.714286, 7.428571],
    )


def test_combined_dark_count_lo(dataset):
    assert str(dataset["combined_dark_count_lo"].dtype) == "float32"
    assert dataset["combined_dark_count_lo"].long_name == "Low Gain Combined Dark Count"
    assert (
        dataset["combined_dark_count_lo"].description
        == "total counts per averaging interval(eg. one altitude, one time)"
    )
    assert dataset["combined_dark_count_lo"].units == "counts"
    assert isnan(dataset["combined_dark_count_lo"].missing_value)
    assert allclose(
        dataset["combined_dark_count_lo"][:].data,
        [17.142857, 13.714286, 10.285714, 16.0, 16.571428, 9.142858],
    )


def test_combined_dark_count_hi(dataset):
    assert str(dataset["combined_dark_count_hi"].dtype) == "float32"
    assert (
        dataset["combined_dark_count_hi"].long_name == "High Gain Combined Dark Count"
    )
    assert (
        dataset["combined_dark_count_hi"].description
        == "total counts per averaging interval(eg. one altitude, one time)"
    )
    assert dataset["combined_dark_count_hi"].units == "counts"
    assert isnan(dataset["combined_dark_count_hi"].missing_value)
    assert allclose(
        dataset["combined_dark_count_hi"][:].data,
        [18.857143, 9.714286, 12.0, 22.857143, 13.142858, 13.714286],
    )


def test_combined_gain(dataset):
    assert str(dataset["combined_gain"].dtype) == "float32"
    assert dataset["combined_gain"].long_name == "Combined Gain Factor"
    assert (
        dataset["combined_gain"].description
        == "Low Gain level * Factor ~ High Gain level"
    )
    assert allclose(
        dataset["combined_gain"][:].data,
        [16.0, 16.0, 16.0],
    )


def test_combined_merge_threshhold(dataset):
    assert str(dataset["combined_merge_threshhold"].dtype) == "float32"
    assert dataset["combined_merge_threshhold"].long_name == "Combined Merge Threshhold"
    assert allclose(
        dataset["combined_merge_threshhold"][:].data,
        [0.05, 0.05, 0.05],
    )


def test_geo_cor(dataset):
    assert str(dataset["geo_cor"].dtype) == "float32"
    assert dataset["geo_cor"].long_name == "Overlap correction"
    assert (
        dataset["geo_cor"].description
        == "Geometric overlap correction averaged to requested altitude resolution"
    )
    assert dataset["geo_cor"].units == ""
    assert isnan(dataset["geo_cor"].missing_value)
    assert dataset["geo_cor"].plot_scale == "logarithmic"
    assert allclose(
        dataset["geo_cor"][:].data,
        [
            [nan, -47064.75, 1247.525],
            [nan, -47064.75, 1247.525],
            [nan, -47064.75, 1247.525],
        ],
        equal_nan=True,
    )


def test_od(dataset):
    assert str(dataset["od"].dtype) == "float32"
    assert dataset["od"].long_name == "Optical depth of particulate"
    assert dataset["od"].units == ""
    assert isnan(dataset["od"].missing_value)
    assert isinf(dataset["od"].insufficient_data)
    assert dataset["od"].plot_scale == "logarithmic"
    assert allclose(
        dataset["od"][:].data,
        [
            [4.8634334, -0.37113133, 0.0068785],
            [4.8634334, -0.37626463, infty],
            [4.8634334, -0.36846352, 0.00587574],
            [4.8634334e00, -3.7711456e-01, -3.0243865e-04],
            [4.8634334, -0.3702242, nan],
            [4.8634334, -0.35479563, 0.01458123],
        ],
        equal_nan=True,
    )


def test_profile_od(dataset):
    assert str(dataset["profile_od"].dtype) == "float32"
    assert dataset["profile_od"].long_name == "Optical depth of particulate Profile"
    assert dataset["profile_od"].units == ""
    assert isnan(dataset["profile_od"].missing_value)
    assert isinf(dataset["profile_od"].insufficient_data)
    assert dataset["profile_od"].plot_scale == "logarithmic"
    assert allclose(
        dataset["profile_od"][:].data,
        [4.8688040e00, nan, -infty],
        equal_nan=True,
    )


def test_beta_a(dataset):
    assert str(dataset["beta_a"].dtype) == "float32"
    assert (
        dataset["beta_a"].long_name
        == "Particulate extinction cross section per unit volume"
    )
    assert dataset["beta_a"].units == "1/m"
    assert isnan(dataset["beta_a"].missing_value)
    assert dataset["beta_a"].plot_scale == "logarithmic"
    assert allclose(
        dataset["beta_a"][:].data,
        [
            [nan, -0.08094258, 0.00615082],
            [nan, -0.08091412, 0.00629274],
            [nan, -0.08095929, 0.00619717],
            [nan, -0.08106226, 0.00622874],
            [nan, -0.08092479, 0.00616121],
            [nan, -0.0808142, 0.00602002],
        ],
        equal_nan=True,
    )


def test_atten_beta_r_backscat(dataset):
    assert str(dataset["atten_beta_r_backscat"].dtype) == "float32"
    assert dataset["atten_beta_r_backscat"].long_name == "Attenuated Molecular return"
    assert dataset["atten_beta_r_backscat"].units == "1/(m sr)"
    assert isnan(dataset["atten_beta_r_backscat"].missing_value)
    assert dataset["atten_beta_r_backscat"].plot_scale == "logarithmic"
    assert allclose(
        dataset["atten_beta_r_backscat"][:].data,
        [
            [nan, 3.5104126e-06, 1.6369860e-06],
            [nan, 3.5466383e-06, 1.6314056e-06],
            [nan, 3.4917323e-06, 1.6402723e-06],
            [nan, 3.5526723e-06, 1.6606658e-06],
            [nan, 3.5040496e-06, 1.6334950e-06],
            [nan, 3.3975759e-06, 1.6119608e-06],
        ],
        equal_nan=True,
    )


def test_profile_atten_beta_r_backscat(dataset):
    assert str(dataset["profile_atten_beta_r_backscat"].dtype) == "float32"
    assert (
        dataset["profile_atten_beta_r_backscat"].long_name
        == "Attenuated Molecular Profile"
    )
    assert dataset["profile_atten_beta_r_backscat"].units == "1/(m sr)"
    assert isnan(dataset["profile_atten_beta_r_backscat"].missing_value)
    assert dataset["profile_atten_beta_r_backscat"].plot_scale == "logarithmic"
    assert allclose(
        dataset["profile_atten_beta_r_backscat"][:].data,
        [nan, 3.5764958e-06, 1.6776088e-06],
        equal_nan=True,
    )


def test_depol(dataset):
    assert str(dataset["depol"].dtype) == "float32"
    assert dataset["depol"].long_name == "Circular depolarization ratio for particulate"
    assert (
        dataset["depol"].description
        == "left circular return divided by right circular return"
    )
    assert dataset["depol"].units == ""
    assert isnan(dataset["depol"].missing_value)
    assert dataset["depol"].plot_scale == "logarithmic"
    assert allclose(
        dataset["depol"][:].data,
        [
            [nan, 0.8910097, -0.01050728],
            [nan, 0.87681854, -0.0091269],
            [nan, 0.87386703, -0.0107031],
            [nan, 0.8854666, -0.01125472],
            [nan, 0.87619394, -0.01357443],
            [nan, 0.88363147, -0.00955483],
        ],
        equal_nan=True,
    )


def test_molecular_counts(dataset):
    assert str(dataset["molecular_counts"].dtype) == "int32"
    assert dataset["molecular_counts"].long_name == "Molecular Photon Counts"
    assert (
        dataset["molecular_counts"].description
        == "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
    )
    assert dataset["molecular_counts"].units == "counts"
    assert dataset["molecular_counts"].missing_value == -1
    assert dataset["molecular_counts"].plot_scale == "logarithmic"
    assert allclose(
        dataset["molecular_counts"][:].data,
        [
            [941193, 17500, 31942],
            [940739, 17726, 31574],
            [941563, 17342, 32121],
            [1016112, 18831, 34467],
            [938971, 17644, 32128],
            [943866, 17841, 32346],
        ],
    )


def test_combined_counts_lo(dataset):
    assert str(dataset["combined_counts_lo"].dtype) == "int32"
    assert dataset["combined_counts_lo"].long_name == "Low Gain Combined Photon Counts"
    assert (
        dataset["combined_counts_lo"].description
        == "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
    )
    assert dataset["combined_counts_lo"].units == "counts"
    assert dataset["combined_counts_lo"].missing_value == -1
    assert dataset["combined_counts_lo"].plot_scale == "logarithmic"
    assert allclose(
        dataset["combined_counts_lo"][:].data,
        [
            [557654, 56641, 1980],
            [557940, 57206, 2093],
            [558454, 57456, 1992],
            [604798, 61537, 2027],
            [558429, 57499, 1769],
            [558247, 57274, 2026],
        ],
    )


def test_combined_counts_hi(dataset):
    assert str(dataset["combined_counts_hi"].dtype) == "int32"
    assert dataset["combined_counts_hi"].long_name == "High Gain Combined Photon Counts"
    assert (
        dataset["combined_counts_hi"].description
        == "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
    )
    assert dataset["combined_counts_hi"].units == "counts"
    assert dataset["combined_counts_hi"].missing_value == -1
    assert dataset["combined_counts_hi"].plot_scale == "logarithmic"
    assert allclose(
        dataset["combined_counts_hi"][:].data,
        [
            [793186, 225421, 36897],
            [793750, 224982, 37594],
            [794103, 225480, 36914],
            [860080, 242103, 36056],
            [793712, 222074, 30974],
            [794443, 227433, 38366],
        ],
    )


def test_cross_counts(dataset):
    assert str(dataset["cross_counts"].dtype) == "int32"
    assert dataset["cross_counts"].long_name == "Cross Polarized Photon Counts"
    assert (
        dataset["cross_counts"].description
        == "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
    )
    assert dataset["cross_counts"].units == "counts"
    assert dataset["cross_counts"].missing_value == -1
    assert dataset["cross_counts"].plot_scale == "logarithmic"
    assert allclose(
        dataset["cross_counts"][:].data,
        [
            [3259673, 765202, 0],
            [3257464, 761927, 0],
            [3256298, 765139, 0],
            [3528099, 828282, 0],
            [3255033, 767666, 0],
            [3253180, 769465, 0],
        ],
    )


def test_beta_a_backscat(dataset):
    assert str(dataset["beta_a_backscat"].dtype) == "float32"
    assert (
        dataset["beta_a_backscat"].long_name
        == "Particulate backscatter cross section per unit volume"
    )
    assert dataset["beta_a_backscat"].units == "1/(m sr)"
    assert isnan(dataset["beta_a_backscat"].missing_value)
    assert dataset["beta_a_backscat"].plot_scale == "logarithmic"
    assert allclose(
        dataset["beta_a_backscat"][:].data,
        [
            [nan, 3.7125070e-04, 1.1108813e-06],
            [nan, 3.6797742e-04, 1.3044502e-06],
            [nan, 3.7921261e-04, 1.1211707e-06],
            [nan, 3.750138e-04, 9.747085e-07],
            [nan, 3.7294455e-04, 8.0712221e-07],
            [nan, 3.6752902e-04, 1.1509022e-06],
        ],
        equal_nan=True,
    )


def test_profile_beta_a_backscat(dataset):
    assert str(dataset["profile_beta_a_backscat"].dtype) == "float32"
    assert (
        dataset["profile_beta_a_backscat"].long_name
        == "Particulate backscatter cross section profile"
    )
    assert dataset["profile_beta_a_backscat"].units == "1/(m sr)"
    assert isnan(dataset["profile_beta_a_backscat"].missing_value)
    assert dataset["profile_beta_a_backscat"].plot_scale == "logarithmic"
    assert allclose(
        dataset["profile_beta_a_backscat"][:].data,
        [nan, 3.672536e-04, 7.564736e-07],
        equal_nan=True,
    )


def test_profile_beta_m(dataset):
    assert str(dataset["profile_beta_m"].dtype) == "float32"
    assert (
        dataset["profile_beta_m"].long_name
        == "Raob molecular scattering cross section profile"
    )
    assert dataset["profile_beta_m"].units == "1/meter"
    assert dataset["profile_beta_m"].plot_scale == "logarithmic"
    assert allclose(
        dataset["profile_beta_m"][:].data,
        [1.4194106e-05, 1.4155382e-05, 1.4115825e-05],
    )


def test_qc_mask(dataset):
    assert str(dataset["qc_mask"].dtype) == "int32"
    assert dataset["qc_mask"].long_name == "Quality Mask"
    assert (
        dataset["qc_mask"].description
        == "Quality mask,bits:1=&(2:8),2=lock,3=seed,4=m_count,5=beta_err,6=m_lost,7=min_lid,8=min_rad"
    )
    assert dataset["qc_mask"].units == ""
    assert dataset["qc_mask"].missing_value == -1
    assert dataset["qc_mask"].bit_0 == "AND"
    assert dataset["qc_mask"].bit_1 == "lock"
    assert dataset["qc_mask"].bit_2 == "seed"
    assert dataset["qc_mask"].bit_3 == "m_count"
    assert dataset["qc_mask"].bit_4 == "beta_err"
    assert dataset["qc_mask"].bit_5 == "m_lost"
    assert dataset["qc_mask"].bit_6 == "min_lid"
    assert dataset["qc_mask"].bit_7 == "min_rad"
    assert dataset["qc_mask"].plot_scale == "linear"
    assert allclose(
        dataset["qc_mask"][:].data,
        [
            [65502, 65502, 65502],
            [65502, 65502, 65502],
            [65502, 65502, 65502],
            [65502, 65502, 65502],
            [65502, 65502, 65502],
            [65502, 65502, 65502],
        ],
    )


def test_std_beta_a_backscat(dataset):
    assert str(dataset["std_beta_a_backscat"].dtype) == "float32"
    assert (
        dataset["std_beta_a_backscat"].long_name
        == "Std dev of backscat cross section (photon counting)"
    )
    assert dataset["std_beta_a_backscat"].units == "1/(m sr)"
    assert isnan(dataset["std_beta_a_backscat"].missing_value)
    assert dataset["std_beta_a_backscat"].plot_scale == "logarithmic"
    assert allclose(
        dataset["std_beta_a_backscat"][:].data,
        [
            [nan, 3.0208066e-06, 1.8732067e-08],
            [nan, 2.9744365e-06, 1.9653946e-08],
            [nan, 3.1054185e-06, 1.8700767e-08],
            [nan, 2.9440828e-06, 1.7485702e-08],
            [nan, 3.0241167e-06, 1.7450182e-08],
            [nan, 2.9597777e-06, 1.8751841e-08],
        ],
        equal_nan=True,
    )
