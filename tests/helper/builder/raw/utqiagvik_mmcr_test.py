"""Test the creation of netCDF files."""

import os
from typing import Generator

import pytest
from numpy import allclose

from sio_postdoc.access.instrument.types import Dataset
from tests.helper.builder.raw.context import RawDataContext
from tests.helper.builder.raw.strategies import UtqiagvikMmcrRaw
from tests.helper.builder.raw.types import Instrument, Observatory


@pytest.fixture(scope="module")
def dataset() -> Generator[Dataset, None, None]:
    # Arrange
    data = RawDataContext(Observatory.UTQIAGVIK, Instrument.MMCR)
    data.hydrate()
    dataset = Dataset(data.filename)
    # Test
    yield dataset
    # Cleanup
    dataset.close()
    os.remove(data.filename)


def test_attributes(dataset):
    assert dataset.Date == "Wed Jun 10 21:07:04 GMT 2009"
    assert dataset.Version == "$State: Release_4_0 $"
    assert dataset.Number_Input_Platforms == 4
    assert (
        dataset.Input_Platforms
        == "nsamplpolavgxxC1.c1,vap-mplpolavg-1.9-0,nsavceil25kC1.b1,nsammcrmomC1.b1"
    )
    assert dataset.Input_Platforms_Versions == "$State:,$,8.2,1.16"
    assert dataset.zeb_platform == "nsaarscl1clothC1.c1"
    assert (
        dataset.Command_Line
        == "arsc1/arscl2 -s YYYYMMDD -e YYYYMMDD SITE FACILITY QCFILE ZIPPING"
    )
    assert dataset.contact == ""
    assert (
        dataset.commenta
        == "At each height and time, the MMCR reflectivity, velocity, width and signal-to-noise ratio always come from the same mode.  The mode is indicated by ModeId."
    )
    assert (
        dataset.commentb
        == "MeanDopplerVelocity, ModeId, qc_RadarArtifacts, qc_ReflectivityClutterFlag, SpectralWidth, and SignaltoNoiseRatio data are reported at all range gates for which there is a significant detection, including from clutter."
    )
    assert (
        dataset.commentc
        == "The value of qc_ReflectivityClutterFlag indicates whether or not the signal is from clutter."
    )
    assert (
        dataset.commentd
        == "Use the appropriate reflectivity fields (e.g., with clutter, with clutter removed, or best estimate) to filter the variables discussed in commentb."
    )
    assert (
        dataset.commente
        == "Missing (i.e., does not exist) data for a particular time period are indicated by a value of 10 for the ModeId, qc_RadarArtifacts, and qc_ReflectivityClutterFlag variables.  The geophysical variables should contain a value of -32768 at these times."
    )
    assert (
        dataset.commentf
        == "Note that -32768 is also used for the geophysical variables when there are no significant detections, in which case ModeId, qc_RadarArtifacts, and qc_ReflectivityClutterFlag are 0."
    )


def test_dimensions(dataset):
    assert dataset.dimensions["time"].size == UtqiagvikMmcrRaw.time
    assert dataset.dimensions["nheights"].size == UtqiagvikMmcrRaw.nheights
    assert dataset.dimensions["numlayers"].size == UtqiagvikMmcrRaw.numlayers


def test_base_time(dataset):
    variable: str = dataset["base_time"]
    assert str(variable.dtype) == "int32"
    assert variable.long_name == "Beginning Time of File"
    assert variable.units == "seconds since 1970-01-01 00:00:00 00:00"
    assert variable.calendar_date == "Year 2008 Month 09 Day 24 00:00:00"
    assert int(variable[:].data) == 1222214400


def test_time_offset(dataset):
    variable: str = dataset["time_offset"]
    assert str(variable.dtype) == "float64"
    assert variable.long_name == "Time Offset from base_time"
    assert variable.units == "seconds"
    assert variable.comment == "none"
    assert allclose(
        variable[:].data,
        [0.0, 10.0, 20.0, 30.0, 40.0, 50.0],
    )


def test_Heights(dataset):
    variable: str = dataset["Heights"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "Height of Measured Value"
    assert variable.units == "m AGL"
    assert variable.comment == "none"
    assert allclose(
        variable[:].data,
        [75.67602, 119.383286, 163.09055],
    )


def test_Reflectivity(dataset):
    variable: str = dataset["Reflectivity"]
    assert str(variable.dtype) == "int16"
    assert variable.long_name == "MMCR Reflectivity"
    assert variable.units == "dBZ (X100)"
    assert variable.comment == "Divide Reflectivity by 100 to get dBZ"
    assert allclose(
        variable[:].data,
        [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-6216, -5650, -6338],
            [-32768, -32768, -32768],
            [-6428, -6320, -7052],
            [-6162, -5892, -6603],
        ],
    )


def test_ReflectivityNoClutter(dataset):
    variable: str = dataset["ReflectivityNoClutter"]
    assert str(variable.dtype) == "int16"
    assert variable.long_name == "MMCR Reflectivity with Clutter Removed"
    assert variable.units == "dBZ (X100)"
    assert variable.comment == "Divide ReflectivityNoClutter by 100 to get dBZ"
    assert allclose(
        variable[:].data,
        [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
        ],
    )


def test_ReflectivityBestEstimate(dataset):
    variable: str = dataset["ReflectivityBestEstimate"]
    assert str(variable.dtype) == "int16"
    assert variable.long_name == "MMCR Best Estimate of Hydrometeor Reflectivity"
    assert variable.units == "dBZ (X100)"
    assert variable.comment == "Divide ReflectivityBestEstimate by 100 to get dBZ"
    assert allclose(
        variable[:].data,
        [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
        ],
    )


def test_MeanDopplerVelocity(dataset):
    variable: str = dataset["MeanDopplerVelocity"]
    assert str(variable.dtype) == "int16"
    assert variable.long_name == "MMCR Mean Doppler Velocity"
    assert variable.units == "m/s (X1000)"
    assert variable.comment == "Divide MeanDopplerVelocity by 1000 to get m/s"
    assert allclose(
        variable[:].data,
        [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-3600, -3719, -3745],
            [-32768, -32768, -32768],
            [319, 3102, 3701],
            [-3843, 461, 1387],
        ],
    )


def test_SpectralWidth(dataset):
    variable: str = dataset["SpectralWidth"]
    assert str(variable.dtype) == "int16"
    assert variable.long_name == "MMCR Spectral Width"
    assert variable.units == "m/s (X1000)"
    assert variable.comment == "Divide SpectralWidth by 1000 to get m/s"
    assert allclose(
        variable[:].data,
        [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [41, 52, 54],
            [-32768, -32768, -32768],
            [41, 41, 41],
            [41, 41, 41],
        ],
    )


def test_RadarFirstTop(dataset):
    variable: str = dataset["RadarFirstTop"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "MMCR Top Height of Lowest Detected Layer before Clutter Removal"
    )
    assert variable.units == "m AGL"
    assert (
        variable.comment
        == "-3. Data do not exist, 0. No significant detection in column, > 0. Top Height of Lowest Cloud/Clutter Layer"
    )
    assert allclose(
        variable[:].data,
        [-3.0, -3.0, 184.94418, 0.0, 184.94418, 184.94418],
    )


def test_ModeId(dataset):
    variable: str = dataset["ModeId"]
    assert str(variable.dtype) == "|S1"
    assert variable.long_name == "MMCR Mode I.D."
    assert variable.units == "unitless"
    assert (
        variable.comment
        == "0 No significant power return, 1-5 Valid modes, 10 Data do not exist"
    )
    expected: list[list[bytes]] = [
        [b"\n", b"\n", b"\n"],
        [b"\n", b"\n", b"\n"],
        [b"\x01", b"\x01", b"\x01"],
        [b"", b"", b""],
        [b"\x01", b"\x01", b"\x01"],
        [b"\x01", b"\x01", b"\x01"],
    ]
    for row, truth in zip(variable[:].data, expected):
        assert all(row == truth)


def test_SignaltoNoiseRatio(dataset):
    variable: str = dataset["SignaltoNoiseRatio"]
    assert str(variable.dtype) == "int16"
    assert variable.long_name == "MMCR Signal-to-Noise Ratio"
    assert variable.units == "dB (X100)"
    assert variable.comment == "Divide SignaltoNoiseRatio by 100 to get dB"
    assert allclose(
        variable[:].data,
        [
            [-32768, -32768, -32768],
            [-32768, -32768, -32768],
            [-2142, -1819, -2524],
            [-32768, -32768, -32768],
            [-2236, -2175, -2915],
            [-2143, -1977, -2700],
        ],
    )


def test_CloudBasePrecipitation(dataset):
    variable: str = dataset["CloudBasePrecipitation"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "Microwave Radiometer Wet Window/Optical Rain Gauge Cloud Base Height"
    )
    assert variable.units == "m AGL"
    assert (
        variable.comment
        == "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
    )
    assert allclose(variable[:].data, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0])


def test_CloudBaseCeilometerStd(dataset):
    variable: str = dataset["CloudBaseCeilometerStd"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "BLC/VCEIL Standard Algorithm Cloud Base Height"
    assert variable.units == "m AGL"
    assert (
        variable.comment
        == "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
    )
    assert allclose(variable[:].data, [716.28, 716.28, 716.28, 716.28, 716.28, 1371.6])


def test_CloudBaseCeilometerCloth(dataset):
    variable: str = dataset["CloudBaseCeilometerCloth"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name == "BLC/VCEIL Clothiaux et al. Algorithm Cloud Base Height"
    )
    assert variable.units == "m AGL"
    assert (
        variable.comment
        == "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
    )
    assert allclose(variable[:].data, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0])


def test_CloudBaseMplScott(dataset):
    variable: str = dataset["CloudBaseMplScott"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "MPL Scott Algorithm Cloud Base Height"
    assert variable.units == "m AGL"
    assert (
        variable.comment
        == "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
    )
    assert allclose(variable[:].data, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0])


def test_CloudBaseMplCamp(dataset):
    variable: str = dataset["CloudBaseMplCamp"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "MPL Campbell et al. Algorithm Cloud Base Height"
    assert variable.units == "m AGL"
    assert (
        variable.comment
        == "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
    )
    assert allclose(variable[:].data, [-3.0, -3.0, -3.0, -3.0, -3.0, -3.0])


def test_CloudBaseMplCloth(dataset):
    variable: str = dataset["CloudBaseMplCloth"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "MPL Clothiaux et al. Algorithm Cloud Base Height"
    assert variable.units == "m AGL"
    assert (
        variable.comment
        == "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
    )
    assert allclose(variable[:].data, [-3.0, -3.0, -3.0, 719.0529, 719.0529, 719.0529])


def test_CloudBaseBestEstimate(dataset):
    variable: str = dataset["CloudBaseBestEstimate"]
    assert str(variable.dtype) == "float32"
    assert variable.long_name == "LASER Cloud Base Height Best Estimate"
    assert variable.units == "m AGL"
    assert (
        variable.comment
        == "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
    )
    assert allclose(variable[:].data, [716.28, 716.28, 716.28, 716.28, 716.28, 1371.6])


def test_CloudMaskMplCamp(dataset):
    variable: str = dataset["CloudMaskMplCamp"]
    assert str(variable.dtype) == "int16"
    assert variable.long_name == "MPL Campbell et al. Algorithm Cloud Mask Occurrence"
    assert variable.units == "Percent(x100)"
    assert (
        variable.comment
        == "-30000 Data do not exist, -20000 Beam blocked, -10000 Beam attenuated, 0 No cloud (clear), > 0 Valid cloud"
    )
    assert allclose(
        variable[:].data,
        [
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
        ],
    )


def test_CloudMaskMplCloth(dataset):
    variable: str = dataset["CloudMaskMplCloth"]
    assert str(variable.dtype) == "int16"
    assert variable.long_name == "MPL Clothiaux et al. Algorithm Cloud Mask Occurrence"
    assert variable.units == "Percent(x100)"
    assert (
        variable.comment
        == "-30000 Data do not exist, -20000 Beam blocked, -10000 Beam attenuated, 0 No cloud (clear), > 0 Valid cloud"
    )
    assert allclose(
        variable[:].data,
        [
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [-30000, -30000, -30000],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
    )


def test_CloudLayerBottomHeightMplCamp(dataset):
    variable: str = dataset["CloudLayerBottomHeightMplCamp"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "Bottom Height of Hydrometeor Layer from Composite (MMCR/Campbell et al. MPL) Algorithms"
    )
    assert variable.units == "m AGL"
    assert variable.comment == "none"
    assert allclose(
        variable[:].data,
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
    )


def test_CloudLayerBottomHeightMplCloth(dataset):
    variable: str = dataset["CloudLayerBottomHeightMplCloth"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "Bottom Height of Hydrometeor Layer from Composite (MMCR/Clothiaux et al. MPL) Algorithms"
    )
    assert variable.units == "m AGL"
    assert variable.comment == "none"
    assert allclose(
        variable[:].data,
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1299.4795, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1299.4795, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1299.4795, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
    )


def test_CloudLayerTopHeightMplCamp(dataset):
    variable: str = dataset["CloudLayerTopHeightMplCamp"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "Top Height of Hydrometeor Layer from Composite (MMCR/Campbell et al. MPL) Algorithms"
    )
    assert variable.units == "m AGL"
    assert variable.comment == "none"
    assert allclose(
        variable[:].data,
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
    )


def test_CloudLayerTopHeightMplCloth(dataset):
    variable: str = dataset["CloudLayerTopHeightMplCloth"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "Top Height of Hydrometeor Layer from Composite (MMCR/Clothiaux et al. MPL) Algorithms"
    )
    assert variable.units == "m AGL"
    assert variable.comment == "none"
    assert allclose(
        variable[:].data,
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1430.6013, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1430.6013, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [731.28503, 1430.6013, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
    )


def test_qc_RadarArtifacts(dataset):
    variable: str = dataset["qc_RadarArtifacts"]
    assert str(variable.dtype) == "|S1"
    assert variable.long_name == "MMCR Mode Quality Control Flags"
    assert variable.units == "unitless"
    assert (
        variable.comment
        == "0 No significant power return, 1 Significant, problem free data, 2 Second trip echo problems, 3 Coherent integration problems, 4 Second trip echo and coherent integration problems, 5 Pulse coding problems, 10 Data do not exist"
    )
    expected: list[list[bytes]] = [
        [b"\n", b"\n", b"\n"],
        [b"\n", b"\n", b"\n"],
        [b"\x01", b"\x01", b"\x01"],
        [b"", b"", b""],
        [b"\x01", b"\x01", b"\x01"],
        [b"\x01", b"\x01", b"\x01"],
    ]
    for row, truth in zip(variable[:].data, expected):
        assert all(row == truth)


def test_qc_ReflectivityClutterFlag(dataset):
    variable: str = dataset["qc_ReflectivityClutterFlag"]
    assert str(variable.dtype) == "|S1"
    assert variable.long_name == "MMCR Reflectivity Clutter Flags"
    assert variable.units == "unitless"
    assert (
        variable.comment
        == "0 No significant power return, 1 Significant, problem free data, 2 Clutter and cloud contribution, 3 Clutter only contribution, 10 Data do not exist"
    )
    expected: list[list[bytes]] = [
        [b"\n", b"\n", b"\n"],
        [b"\n", b"\n", b"\n"],
        [b"\x03", b"\x03", b"\x03"],
        [b"", b"", b""],
        [b"\x03", b"\x03", b"\x03"],
        [b"\x03", b"\x03", b"\x03"],
    ]
    for row, truth in zip(variable[:].data, expected):
        assert all(row == truth)


def test_qc_CloudLayerTopHeightMplCamp(dataset):
    variable: str = dataset["qc_CloudLayerTopHeightMplCamp"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "Value Indicating the Reliability of the Layer Top Height Using the Campbell et al. MPL Algorithm"
    )
    assert variable.units == "unitless"
    assert variable.comment == "none"
    assert allclose(
        variable[:].data,
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
    )


def test_qc_CloudLayerTopHeightMplCloth(dataset):
    variable: str = dataset["qc_CloudLayerTopHeightMplCloth"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "Value Indicating the Reliability of the Layer Top Height Using the Clothiaux et al. MPL Algorithm"
    )
    assert variable.units == "unitless"
    assert variable.comment == "none"
    assert allclose(
        variable[:].data,
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
    )


def test_qc_BeamAttenuationMplCamp(dataset):
    variable: str = dataset["qc_BeamAttenuationMplCamp"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name
        == "MPL Campbell et al. Algorithm Beam Attenuation Assessment"
    )
    assert variable.units == "unitless"
    assert (
        variable.comment
        == "-9. Data do not exist, -2. Beam blocked, -1. Beam attenuated, 0. No cloud (clear), 1. Beam penetrated atmosphere"
    )
    assert allclose(variable[:].data, [-9.0, -9.0, -9.0, -9.0, -9.0, -9.0])


def test_qc_BeamAttenuationMplCloth(dataset):
    variable: str = dataset["qc_BeamAttenuationMplCloth"]
    assert str(variable.dtype) == "float32"
    assert (
        variable.long_name == "MPL Cloth et al. Algorithm Beam Attenuation Assessment"
    )
    assert variable.units == "unitless"
    assert (
        variable.comment
        == "-9. Data do not exist, Log10(Signal Power above Cloud/Estimated Clearsky Power above Cloud)"
    )
    assert allclose(
        variable[:].data, [-9.0, -9.0, -9.0, -1.2243652, -1.2243652, -1.2243652]
    )
