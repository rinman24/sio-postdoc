"""Test the creation of netCDF files."""

import os
from typing import Generator

import pytest
from numpy import allclose

from sio_postdoc.access import DataSet
from tests.helper.builder.raw.context import RawDataContext
from tests.helper.builder.raw.strategies import UtqiagvikMplRaw
from tests.helper.builder.raw.types import Instrument, Observatory


@pytest.fixture(scope="module")
def dataset() -> Generator[DataSet, None, None]:
    # Arrange
    data = RawDataContext(Observatory.UTQIAGVIK, Instrument.MPL)
    data.hydrate()
    dataset = DataSet(data.filename)
    # Test
    yield dataset
    # Cleanup
    dataset.close()
    os.remove(data.filename)


def test_attributes(dataset):
    assert (
        dataset.command_line == "mplcmask -s nsa -f C1 -D 2 -b 20080924 -e 20080925 -R"
    )
    assert dataset.process_version == "vap-mplcmask-0.4-0.el6"
    assert dataset.dod_version == "30smplcmask1zwang-c1-1.0"
    assert (
        dataset.input_datastreams
        == "nsamplpolavgC1.c1 : 1.14 : 20080924.000030\nnsasondewnpnC1.b1 : 8.1 : 20080924.052600-20080924.165800"
    )
    assert dataset.site_id == "nsa"
    assert dataset.platform_id == "30smplcmask1zwang"
    assert dataset.facility_id == "C1"
    assert dataset.location_description == "North Slope of Alaska (NSA), Barrow, Alaska"
    assert dataset.datastream == "nsa30smplcmask1zwangC1.c1"
    assert dataset.serial_number == "105"
    assert dataset.height_uncertainty == "N/A"
    assert dataset.min_cloud_detection_height == "0.500 km AGL"
    assert dataset.max_cloud_detection_height == "20.000 km AGL"
    assert (
        dataset.deadtime_correction
        == "Applied deadtime correction factor from the configuration file"
    )
    assert (
        dataset.overlap_correction
        == "Applied overlap correction from the configuration file to the height of the MPL"
    )
    assert dataset.afterpulse_correction == "No afterpulse corrections are applied"
    assert dataset.nasa_gsfc_mpl_help == "N/A"
    assert dataset.missing_value == "-9999.0"
    assert (
        dataset.applied_corrections == "Applied overlap, energy and deadtime correction"
    )
    assert (
        dataset.backscatter_data_quality_comment
        == "Data quality ok for both cloud and aerosol analysis"
    )
    assert dataset.data_level == "c1"
    assert dataset.comment == "VAP that applies Zhien's cloud boundary algorithm"
    assert (
        dataset.history
        == "created by user sri on machine amber at 2014-07-12 00:18:36, using vap-mplcmask-0.4-0.el6"
    )


def test_dimensions(dataset):
    assert dataset.dimensions["time"].size == UtqiagvikMplRaw.time
    assert dataset.dimensions["height"].size == UtqiagvikMplRaw.height
    assert dataset.dimensions["layer"].size == UtqiagvikMplRaw.layer
    assert (
        dataset.dimensions["num_deadtime_corr"].size
        == UtqiagvikMplRaw.num_deadtime_corr
    )


def test_base_time(dataset):
    variable: str = dataset["base_time"]
    assert str(variable.dtype) == "int32"
    assert variable.string == "2008-09-24 00:00:00 0:00"
    assert variable.long_name == "Base time in Epoch"
    assert variable.units == "seconds since 1970-1-1 0:00:00 0:00"
    assert variable.ancillary_variables == "time_offset"
    assert variable[:].data == 1222214400


def test_time_offset(dataset):
    variable: str = dataset["time_offset"]
    assert str(variable.dtype) == "float64"
    assert variable.long_name == "Time offset from base_time"
    assert variable.units == "seconds since 2008-09-24 00:00:00 0:00"
    assert variable.ancillary_variables == "base_time"
    assert allclose(
        variable[:].data,
        [30.0, 60.0, 90.0, 120.0, 150.0, 180.0],
    )


def test_time(dataset):
    variable: str = dataset["time"]
    assert str(variable.dtype) == "float64"
    assert variable.long_name == "Time offset from midnight"
    assert variable.units == "seconds since 2008-09-24 00:00:00 0:00"
    assert allclose(
        variable[:].data,
        [30.0, 60.0, 90.0, 120.0, 150.0, 180.0],
    )


def test_height(dataset):
    variable: str = dataset["height"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "Vertical height above ground level (AGL) corresponding to the bottom of height bin"
    )
    assert variable.units == "km"
    assert allclose(
        variable[:].data,
        [0.02249481, 0.05247406, 0.0824533],
    )


def test_cloud_base(dataset):
    variable: str = dataset["cloud_base"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Lowest cloud base height above ground level (AGL)"
    assert variable.units == "km"
    assert variable.comment == "A value of -1 means no cloud is detected"
    assert variable.missing_value == -9999.0
    assert allclose(
        variable[:].data,
        [0.682038, -1.0, -1.0, -1.0, -1.0, -1.0],
    )


def test_cloud_top(dataset):
    variable: str = dataset["cloud_top"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Highest cloud top height above ground level (AGL)"
    assert variable.units == "km"
    assert variable.comment == "A value of -1 means no cloud is detected"
    assert variable.missing_value == -9999.0
    assert allclose(
        variable[:].data,
        [1.7912695, -1.0, -1.0, -1.0, -1.0, -1.0],
    )


def test_num_cloud_layers(dataset):
    variable: str = dataset["num_cloud_layers"]
    assert str(variable.dtype) == "int32"
    assert variable.long_name == "Number of cloud layers"
    assert variable.units == "unitless"
    assert variable.missing_value == -9999
    assert allclose(
        variable[:].data,
        [1, 0, 0, 0, 0, 0],
    )


def test_linear_depol_ratio(dataset):
    variable: str = dataset["linear_depol_ratio"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Linear depolarization ratio"
    assert variable.units == "unitless"
    assert variable.missing_value == -9999.0
    assert variable.ancillary_variables == "qc_linear_depol_ratio"
    assert allclose(
        variable[:].data,
        [
            [-0.28459275, 0.977915, 0.38756308],
            [-0.35307893, 0.9776862, 0.39125702],
            [-0.4996107, 0.9772247, 0.3911428],
            [0.4311789, 0.9775953, 0.38763753],
            [0.16858189, 0.9769985, 0.38921818],
            [1.5727872, 0.97737384, 0.38858318],
        ],
    )


def test_qc_linear_depol_ratio(dataset):
    variable: str = dataset["qc_linear_depol_ratio"]
    assert str(variable.dtype) == "int32"
    assert (
        variable.long_name
        == "Quality check results on field: Linear depolarization ratio"
    )
    assert variable.units == "unitless"
    assert (
        variable.comment
        == "This field contains bit packed integer values, where each bit represents a QC test on the data. Non-zero bits indicate the QC condition given in the description for those bits; a value of 0 (no bits set) indicates the data has not failed any QC tests."
    )
    assert variable.flag_method == "bit"
    assert (
        variable.bit_1_description
        == "The value of signal is zero in the denominator causing the value of depolarization ratio to be NaN, data value set to missing_value in output file."
    )
    assert variable.bit_1_assessment == "Bad"
    assert (
        variable.bit_2_description
        == "Data value not available in input file, data value set to missing_value in output file."
    )
    assert variable.bit_2_assessment == "Bad"
    assert allclose(
        variable[:].data,
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
    )


def test_linear_depol_snr(dataset):
    variable: str = dataset["linear_depol_snr"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "Signal to noise ratio for the linear depolarization ratio"
    )
    assert variable.units == "unitless"
    assert variable.missing_value == -9999.0
    assert variable.ancillary_variables == "qc_linear_depol_snr"
    assert allclose(
        variable[:].data,
        [
            [-9999.0, 268.67264, 126.09152],
            [-9999.0, 268.61926, 126.32019],
            [-9999.0, 268.60895, 126.207695],
            [4.3232746, 268.49026, 125.94582],
            [3.128249, 268.46893, 126.202],
            [3.5918827, 268.5175, 125.94176],
        ],
    )


def test_qc_linear_depol_snr(dataset):
    variable: str = dataset["qc_linear_depol_snr"]
    assert str(variable.dtype) == "int32"
    assert (
        variable.long_name
        == "Quality check results on field: Signal to noise ratio for the linear depolarization ratio"
    )
    assert variable.units == "unitless"
    assert (
        variable.description
        == "This field contains bit packed integer values, where each bit represents a QC test on the data. Non-zero bits indicate the QC condition given in the description for those bits; a value of 0 (no bits set) indicates the data has not failed any QC tests."
    )
    assert variable.flag_method == "bit"
    assert (
        variable.bit_1_description
        == "The value of signal is zero in the denominator causing the value of snr to be NaN, data value set to missing_value in output file."
    )
    assert variable.bit_1_assessment == "Bad"
    assert (
        variable.bit_2_description
        == "Data value not available in input file, data value set to missing_value in output file."
    )
    assert variable.bit_2_assessment == "Bad"
    assert allclose(
        variable[:].data,
        [
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
    )


def test_cloud_mask(dataset):
    variable: str = dataset["cloud_mask"]
    assert str(variable.dtype) == "int32"
    assert variable.long_name == "Cloud mask"
    assert variable.units == "unitless"
    assert variable.comment == "Cloud mask indeterminate below 500 m"
    assert list(variable.flag_values) == [0, 1]
    assert variable.flag_meanings == "clear cloudy"
    assert variable.flag_0_description == "Clear"
    assert variable.flag_1_description == "Cloudy"
    assert variable.missing_value == -9999
    assert variable.ancillary_variables == "qc_cloud_mask"
    assert allclose(
        variable[:].data,
        [
            [-9999, 0, 1],
            [-9999, 0, 1],
            [-9999, 0, 1],
            [-9999, 0, 1],
            [-9999, 0, 1],
            [-9999, 0, 1],
        ],
    )


def test_qc_cloud_mask(dataset):
    variable: str = dataset["qc_cloud_mask"]
    assert str(variable.dtype) == "int32"
    assert variable.long_name == "Quality check results on field: Cloud mask"
    assert variable.units == "unitless"
    assert (
        variable.description
        == "This field contains bit packed integer values, where each bit represents a QC test on the data. Non-zero bits indicate the QC condition given in the description for those bits; a value of 0 (no bits set) indicates the data has not failed any QC tests."
    )
    assert variable.flag_method == "bit"
    assert (
        variable.bit_1_description
        == "Unable to determine the cloud mask, data value set to missing_value in output file."
    )
    assert variable.bit_1_assessment == "Bad"
    assert (
        variable.bit_2_description
        == "backscatter is unusable due to instrument malfunction, data value set to missing_value in output file."
    )
    assert variable.bit_2_assessment == "Bad"
    assert allclose(
        variable[:].data,
        [
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
        ],
    )


def test_cloud_base_layer(dataset):
    variable: str = dataset["cloud_base_layer"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Cloud base for each layer"
    assert variable.units == "km"
    assert variable.missing_value == -9999.0
    assert variable.comment == "Positive values indicate the height of the cloud base"
    assert allclose(
        variable[:].data,
        [
            [0.682038, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
        ],
    )


def test_cloud_top_layer(dataset):
    variable: str = dataset["cloud_top_layer"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Cloud top for each layer above ground level (AGL)"
    assert variable.units == "km"
    assert variable.missing_value == -9999.0
    assert variable.comment == "Positive values indicate the height of the cloud top"
    assert allclose(
        variable[:].data,
        [
            [1.7912695, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
        ],
    )


def test_backscatter(dataset):
    variable: str = dataset["backscatter"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Total attenuated backscatter"
    assert variable.units == "counts/microsecond"
    assert variable.missing_value == -9999.0
    assert (
        variable.comment
        == "background subtracted, overlap, energy and dead-time corrected"
    )
    assert variable.calculation == "((copol+(2*crosspol))*overlap)/energy"
    assert (
        variable.data_quality_comment
        == "Data quality ok for both cloud and aerosol analysis"
    )
    assert variable.normalization_factor == "N/A"
    assert (
        variable.backscatter_data_quality_comment
        == "Data quality ok for both cloud and aerosol analysis"
    )
    assert variable.ancillary_variables == "qc_backscatter"
    assert allclose(
        variable[:].data,
        [
            [6.0800654e-01, 2.4693540e03, 3.1821454e02],
            [2.6602274e-01, 2.4681104e03, 3.1809964e02],
            [1.3450946e-04, 2.4683525e03, 3.1760068e02],
            [1.8580000e00, 2.4659375e03, 3.1742856e02],
            [1.5707090e00, 2.4655125e03, 3.1815848e02],
            [9.6904886e-01, 2.4663083e03, 3.1706573e02],
        ],
    )


def test_qc_backscatter(dataset):
    variable: str = dataset["qc_backscatter"]
    assert str(variable.dtype) == "int32"
    assert (
        variable.long_name
        == "Quality check results on field: Total attenuated backscatter"
    )
    assert variable.units == "unitless"
    assert (
        variable.description
        == "This field contains bit packed integer values, where each bit represents a QC test on the data. Non-zero bits indicate the QC condition given in the description for those bits; a value of 0 (no bits set) indicates the data has not failed any QC tests."
    )
    assert variable.flag_method == "bit"
    assert (
        variable.bit_1_description
        == "The value of backscatter is not finite, data value set to missing_value in output file."
    )
    assert variable.bit_1_assessment == "Bad"
    assert allclose(
        variable[:].data,
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
    )


def test_backscatter_snr(dataset):
    variable: str = dataset["backscatter_snr"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Signal to noise ratio of backscatter"
    assert variable.units == "unitless"
    assert variable.missing_value == -9999.0
    assert variable.ancillary_variables == "qc_backscatter_snr"
    assert allclose(
        variable[:].data,
        [
            [0.3529468, 0.3529468, 0.3529468],
            [0.35290167, 0.35290167, 0.35290167],
            [0.35320997, 0.35320997, 0.35320997],
            [0.35394973, 0.35394973, 0.35394973],
            [0.35389477, 0.35389477, 0.35389477],
            [0.35366353, 0.35366353, 0.35366353],
        ],
    )


def test_qc_backscatter_snr(dataset):
    variable: str = dataset["qc_backscatter_snr"]
    assert str(variable.dtype) == "int32"
    assert (
        variable.long_name
        == "Quality check results on field: Signal to noise ratio of backscatter"
    )
    assert variable.units == "unitless"
    assert (
        variable.description
        == "This field contains bit packed integer values, where each bit represents a QC test on the data. Non-zero bits indicate the QC condition given in the description for those bits; a value of 0 (no bits set) indicates the data has not failed any QC tests."
    )
    assert variable.flag_method == "bit"
    assert (
        variable.bit_1_description
        == "The value of Signal to noise ratio of backscatter is not finite, data value set to missing_value in output file."
    )
    assert variable.bit_1_assessment == "Bad"
    assert allclose(
        variable[:].data,
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
    )


def test_background_signal(dataset):
    variable: str = dataset["background_signal"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Background signal"
    assert variable.units == "counts/microsecond"
    assert variable.missing_value == -9999.0
    assert (
        variable.comment
        == "sum of co-polarized and cross polarized signals from input source"
    )
    assert allclose(
        variable[:].data,
        [0.3424501, 0.34605426, 0.33168215, 0.3724103, 0.3804245, 0.37163568],
    )


def test_cloud_top_attenuation_flag(dataset):
    variable: str = dataset["cloud_top_attenuation_flag"]
    assert str(variable.dtype) == "int32"
    assert (
        variable.long_name
        == "Flag indicating whether the beam was extinguished at indicated cloud top"
    )
    assert variable.units == "unitless"
    assert variable.missing_value == -9999
    assert list(variable.flag_values) == [0, 1]
    assert (
        variable.flag_meanings
        == "beam_not_extinguished_by_layer beam_extinguished_by_layer"
    )
    assert (
        variable.flag_0_description
        == "Indicates that the beam was not extinguished by the layer"
    )
    assert (
        variable.flag_1_description
        == "Indicates that the beam was totally extinguished by the layer"
    )
    assert allclose(
        variable[:].data,
        [1, 0, 0, 0, 0, 0],
    )


def test_shots_summed(dataset):
    variable: str = dataset["shots_summed"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Number of lidar pulses summed"
    assert variable.units == "unitless"
    assert allclose(
        variable[:].data,
        [37500.0, 37500.0, 37500.0, 37500.0, 37500.0, 37500.0],
    )


def test_deadtime_correction_counts(dataset):
    variable: str = dataset["deadtime_correction_counts"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "Laboratory measured counts used to calculate the deadtime correction samples"
    )
    assert variable.units == "counts/microsecond"
    assert allclose(
        variable[:].data,
        [
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
        ],
    )


def test_deadtime_correction(dataset):
    variable: str = dataset["deadtime_correction"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Deadtime correction factor"
    assert variable.units == "unitless"
    assert allclose(
        variable[:].data,
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


def test_afterpulse_correction(dataset):
    variable: str = dataset["afterpulse_correction"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Detector afterpulse from laser flash"
    assert variable.units == "counts/microsecond"
    assert variable.comment == "No afterpulse corrections are applied"
    assert allclose(
        variable[:].data,
        [
            1.0,
            1.0,
            1.0,
        ],
    )


def test_overlap_correction(dataset):
    variable: str = dataset["overlap_correction"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Overlap correction"
    assert variable.units == "unitless"
    assert allclose(
        variable[:].data,
        [
            547.11566,
            211.03833,
            101.589676,
        ],
    )


def test_lat(dataset):
    variable: str = dataset["lat"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "North latitude"
    assert variable.units == "degree_N"
    assert variable.standard_name == "latitude"
    assert variable.valid_min == -90.0
    assert variable.valid_max == 90.0
    assert allclose(
        variable[:].data,
        71.323,
    )


def test_lon(dataset):
    variable: str = dataset["lon"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "East longitude"
    assert variable.units == "degree_E"
    assert variable.standard_name == "longitude"
    assert variable.valid_min == -180.0
    assert variable.valid_max == 180.0
    assert allclose(
        variable[:].data,
        -156.609,
    )


def test_alt(dataset):
    variable: str = dataset["alt"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Altitude above mean sea level"
    assert variable.units == "m"
    assert variable.standard_name == "altitude"
    assert allclose(
        variable[:].data,
        8.0,
    )
