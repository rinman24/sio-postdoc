"""Create test files."""

import sys

from netCDF4 import Dataset


def main(observatory, instrument):  # noqa: PLR0915
    """Create test netCDF files."""
    print("Creating NCDF file...")

    if observatory not in ["sheba", "eureka", "utqiagvik"]:
        print("invalid observatory...")
        return False
    if instrument not in ["dabul", "mmcr", "ahsrl"]:
        print("invalid instrument...")
        return False

    filename: str
    if observatory == "sheba" and instrument == "dabul":
        filename = "D1997-11-04T00-31-00.BHAR.ncdf"
    elif observatory == "sheba" and instrument == "mmcr":
        filename = "D1997-10-30T12-00-00.mrg.corrected.nc"
    elif observatory == "eureka" and instrument == "mmcr":
        filename = "eurmmcrmerge.C1.c1.D2005-08-10T00-00-00.nc"
    elif observatory == "eureka" and instrument == "ahsrl":
        filename = "ahsrl_D2005-08-12T00-00-00_30s_30m.cdf"
    elif observatory == "utqiagvik" and instrument == "mmcr":
        filename = "nsaarscl1clothC1.c1.D1999-03-20T00-00-00.cdf"

    with Dataset(filename, "w", format="NETCDF4") as rootgrp:
        if observatory == "sheba" and instrument == "dabul":
            pass
        elif observatory == "eureka" and instrument == "mmcr":
            pass
        elif observatory == "eureka" and instrument == "ahsrl":
            pass
        elif observatory == "utqiagvik" and instrument == "mmcr":
            # Attributes
            print("Creating attributes...")
            rootgrp.Date = "Fri Mar 09 12:41:12 GMT 2001"
            rootgrp.Version = "Release_2_8"
            rootgrp.Number_Input_Platforms = 5
            rootgrp.Input_Platforms = "nsamplC1.a1,nsaorgC1.a1,nsavceil25kC1.a1,nsammcrcalC1.a1,nsammcrmomentsC1.a1"
            rootgrp.Input_Platforms_Versions = "3.0.10,1.4,1.4,Release_1_4,1.1"
            rootgrp.zeb_platform = "nsaarscl1clothC1.c1"
            rootgrp.Command_Line = (
                "arsc1/arscl2 -s YYYYMMDD -e YYYYMMDD SITE FACILITY QCFILE ZIPPING"
            )
            rootgrp.contact = ""
            rootgrp.commenta = "At each height and time, the MMCR reflectivity, velocity, width and signal-to-noise ratio always come from the same mode.  The mode is indicated by ModeId."
            rootgrp.commentb = "MeanDopplerVelocity, ModeId, qc_RadarArtifacts, qc_ReflectivityClutterFlag, SpectralWidth, and SignaltoNoiseRatio data are reported at all range gates for which there is a significant detection, including from clutter."
            rootgrp.commentc = "The value of qc_ReflectivityClutterFlag indicates whether or not the signal is from clutter."
            rootgrp.commentd = "Use the appropriate reflectivity fields (e.g., with clutter, with clutter removed, or best estimate) to filter the variables discussed in commentb."
            rootgrp.commente = "Missing (i.e., does not exist) data for a particular time period are indicated by a value of 10 for the ModeId, qc_RadarArtifacts, and qc_ReflectivityClutterFlag variables.  The geophysical variables should contain a value of -32768 at these times."
            rootgrp.commentf = "Note that -32768 is also used for the geophysical variables when there are no significant detections, in which case ModeId, qc_RadarArtifacts, and qc_ReflectivityClutterFlag are 0."

            # Dimensions
            print("Creating dimensions...")
            rootgrp.createDimension("time", 3)
            rootgrp.createDimension("nheights", 2)  # noqa: F841
            rootgrp.createDimension("numlayers", 10)  # noqa: F841

            # Variables
            print("Creating variables...")

            # base_time
            base_time = rootgrp.createVariable("base_time", "i4")
            base_time.long_name = "Beginning Time of File"
            base_time.units = "seconds since 1970-01-01 00:00:00 00:00"
            base_time.calendar_date = "Year 1999 Month 03 Day 20 00:00:00"
            base_time[:] = int(921888000)

            # time_offset
            time_offset = rootgrp.createVariable("time_offset", "f8", ("time",))
            time_offset.long_name = "Time Offset from base_time"
            time_offset.units = "seconds"
            time_offset.comment = "none"
            time_offset[:] = [0.0, 10.0, 20.0]

            # Heights
            Heights = rootgrp.createVariable("Heights", "f4", ("nheights",))
            Heights.long_name = "Height of Measured Value"
            Heights.units = "m AGL"
            Heights.comment = "none"
            Heights[:] = [104.0, 149.0]

            # Reflectivity
            Reflectivity = rootgrp.createVariable(
                "Reflectivity", "i2", ("time", "nheights")
            )
            Reflectivity.long_name = "MMCR Reflectivity"
            Reflectivity.units = "dBZ (X100)"
            Reflectivity.comment = "Divide Reflectivity by 100 to get dBZ"
            Reflectivity[:] = [
                [-32768, -32768],
                [-32768, -32768],
                [-32768, -32768],
            ]

            # ReflectivityNoClutter
            ReflectivityNoClutter = rootgrp.createVariable(
                "ReflectivityNoClutter", "i2", ("time", "nheights")
            )
            ReflectivityNoClutter.long_name = "MMCR Reflectivity with Clutter Removed"
            ReflectivityNoClutter.units = "dBZ (X100)"
            ReflectivityNoClutter.comment = (
                "Divide ReflectivityNoClutter by 100 to get dBZ"
            )
            ReflectivityNoClutter[:] = [
                [-32768, -32768],
                [-32768, -32768],
                [-32768, -32768],
            ]

            # ReflectivityBestEstimate
            ReflectivityBestEstimate = rootgrp.createVariable(
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
                [-32768, -32768],
                [-32768, -32768],
                [-32768, -32768],
            ]

            # MeanDopplerVelocity
            MeanDopplerVelocity = rootgrp.createVariable(
                "MeanDopplerVelocity", "i2", ("time", "nheights")
            )
            MeanDopplerVelocity.long_name = "MMCR Mean Doppler Velocity"
            MeanDopplerVelocity.units = "m/s (X1000)"
            MeanDopplerVelocity.comment = (
                "Divide MeanDopplerVelocity by 1000 to get m/s"
            )
            MeanDopplerVelocity[:] = [
                [-32768, -32768],
                [-32768, -32768],
                [-32768, -32768],
            ]

            # SpectralWidth
            SpectralWidth = rootgrp.createVariable(
                "SpectralWidth", "i2", ("time", "nheights")
            )
            SpectralWidth.long_name = "MMCR Spectral Width"
            SpectralWidth.units = "m/s (X1000)"
            SpectralWidth.comment = "Divide SpectralWidth by 1000 to get m/s"
            SpectralWidth[:] = [
                [-32768, -32768],
                [-32768, -32768],
                [-32768, -32768],
            ]

            # RadarFirstTop
            RadarFirstTop = rootgrp.createVariable("RadarFirstTop", "f4", ("time",))
            RadarFirstTop.long_name = (
                "MMCR Top Height of Lowest Detected Layer before Clutter Removal"
            )
            RadarFirstTop.units = "m AGL"
            RadarFirstTop.comment = "-3. Data do not exist, 0. No significant detection in column, > 0. Top Height of Lowest Cloud/Clutter Layer"
            RadarFirstTop[:] = [-3.0, -3.0, -3.0]

            # ModeId
            ModeId = rootgrp.createVariable("ModeId", "S1", ("time", "nheights"))
            ModeId.long_name = "MMCR Mode I.D."
            ModeId.units = "unitless"
            ModeId.comment = (
                "0 No significant power return, 1-5 Valid modes, 10 Data do not exist"
            )
            ModeId[:] = [
                [b"\n", b"\n"],
                [b"\n", b"\n"],
                [b"\n", b"\n"],
            ]

            # SignaltoNoiseRatio
            SignaltoNoiseRatio = rootgrp.createVariable(
                "SignaltoNoiseRatio", "i2", ("time", "nheights")
            )
            SignaltoNoiseRatio.long_name = "MMCR Signal-to-Noise Ratio"
            SignaltoNoiseRatio.units = "dB (X100)"
            SignaltoNoiseRatio.comment = "Divide SignaltoNoiseRatio by 100 to get dB"
            SignaltoNoiseRatio[:] = [
                [-32768, -32768],
                [-32768, -32768],
                [-32768, -32768],
            ]

            # CloudBasePrecipitation
            CloudBasePrecipitation = rootgrp.createVariable(
                "CloudBasePrecipitation", "f4", ("time",)
            )
            CloudBasePrecipitation.long_name = (
                "Microwave Radiometer Wet Window/Optical Rain Gauge Cloud Base Height"
            )
            CloudBasePrecipitation.units = "m AGL"
            CloudBasePrecipitation.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
            CloudBasePrecipitation[:] = [-1.0, -1.0, -1.0]

            # CloudBaseCeilometerStd
            CloudBaseCeilometerStd = rootgrp.createVariable(
                "CloudBaseCeilometerStd", "f4", ("time",)
            )
            CloudBaseCeilometerStd.long_name = (
                "BLC/VCEIL Standard Algorithm Cloud Base Height"
            )
            CloudBaseCeilometerStd.units = "m AGL"
            CloudBaseCeilometerStd.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
            CloudBaseCeilometerStd[:] = [270.0, 270.0, 270.0]

            # CloudBaseCeilometerCloth
            CloudBaseCeilometerCloth = rootgrp.createVariable(
                "CloudBaseCeilometerCloth", "f4", ("time",)
            )
            CloudBaseCeilometerCloth.long_name = (
                "BLC/VCEIL Clothiaux et al. Algorithm Cloud Base Height"
            )
            CloudBaseCeilometerCloth.units = "m AGL"
            CloudBaseCeilometerCloth.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
            CloudBaseCeilometerCloth[:] = [-3.0, -3.0, -3.0]

            # CloudBaseMplScott
            CloudBaseMplScott = rootgrp.createVariable(
                "CloudBaseMplScott", "f4", ("time",)
            )
            CloudBaseMplScott.long_name = "MPL Scott Algorithm Cloud Base Height"
            CloudBaseMplScott.units = "m AGL"
            CloudBaseMplScott.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
            CloudBaseMplScott[:] = [-3.0, -3.0, -3.0]

            # CloudBaseMplCamp
            CloudBaseMplCamp = rootgrp.createVariable(
                "CloudBaseMplCamp", "f4", ("time",)
            )
            CloudBaseMplCamp.long_name = (
                "MPL Campbell et al. Algorithm Cloud Base Height"
            )
            CloudBaseMplCamp.units = "m AGL"
            CloudBaseMplCamp.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
            CloudBaseMplCamp[:] = [-3.0, -3.0, -3.0]

            # CloudBaseMplCloth
            CloudBaseMplCloth = rootgrp.createVariable(
                "CloudBaseMplCloth", "f4", ("time",)
            )
            CloudBaseMplCloth.long_name = (
                "MPL Clothiaux et al. Algorithm Cloud Base Height"
            )
            CloudBaseMplCloth.units = "m AGL"
            CloudBaseMplCloth.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
            CloudBaseMplCloth[:] = [210.00002, 240.00002, 240.00002]

            # CloudBaseBestEstimate
            CloudBaseBestEstimate = rootgrp.createVariable(
                "CloudBaseBestEstimate", "f4", ("time",)
            )
            CloudBaseBestEstimate.long_name = "LASER Cloud Base Height Best Estimate"
            CloudBaseBestEstimate.units = "m AGL"
            CloudBaseBestEstimate.comment = "-3. Data do not exist, -2. Data exist but no retrieval, -1. Clear sky, >= 0. Valid cloud base height"
            CloudBaseBestEstimate[:] = [270.0, 270.0, 270.0]

            # CloudMaskMplCamp
            CloudMaskMplCamp = rootgrp.createVariable(
                "CloudMaskMplCamp", "i2", ("time", "nheights")
            )
            CloudMaskMplCamp.long_name = (
                "MPL Campbell et al. Algorithm Cloud Mask Occurrence"
            )
            CloudMaskMplCamp.units = "Percent(x100)"
            CloudMaskMplCamp.comment = "-30000 Data do not exist, -20000 Beam blocked, -10000 Beam attenuated, 0 No cloud (clear), > 0 Valid cloud percent occurrence (x 100) during time interval."
            CloudMaskMplCamp[:] = [
                [-30000, -30000],
                [-30000, -30000],
                [-30000, -30000],
            ]

            # CloudMaskMplCloth
            CloudMaskMplCloth = rootgrp.createVariable(
                "CloudMaskMplCloth", "i2", ("time", "nheights")
            )
            CloudMaskMplCloth.long_name = (
                "MPL Clothiaux et al. Algorithm Cloud Mask Occurrence"
            )
            CloudMaskMplCloth.units = "Percent(x100)"
            CloudMaskMplCloth.comment = "-30000 Data do not exist, -20000 Beam blocked, -10000 Beam attenuated, 0 No cloud (clear), > 0 Valid cloud percent occurrence (x 100) during time interval."
            CloudMaskMplCloth[:] = [
                [0, 0],
                [0, 0],
                [0, 0],
            ]

            # CloudLayerBottomHeightMplCamp
            CloudLayerBottomHeightMplCamp = rootgrp.createVariable(
                "CloudLayerBottomHeightMplCamp", "f4", ("time", "numlayers")
            )
            CloudLayerBottomHeightMplCamp.long_name = "Bottom Height of Hydrometeor Layer from Composite (MMCR/Campbell et al. MPL) Algorithms"
            CloudLayerBottomHeightMplCamp.units = "m AGL"
            CloudLayerBottomHeightMplCamp.comment = "none"
            CloudLayerBottomHeightMplCamp[:] = [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]

            # CloudLayerBottomHeightMplCloth
            CloudLayerBottomHeightMplCloth = rootgrp.createVariable(
                "CloudLayerBottomHeightMplCloth", "f4", ("time", "numlayers")
            )
            CloudLayerBottomHeightMplCloth.long_name = "Bottom Height of Hydrometeor Layer from Composite (MMCR/Clothiaux et al. MPL) Algorithms"
            CloudLayerBottomHeightMplCloth.units = "m AGL"
            CloudLayerBottomHeightMplCloth.comment = "none"
            CloudLayerBottomHeightMplCloth[:] = [
                [194.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [239.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [239.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]

            # CloudLayerTopHeightMplCamp
            CloudLayerTopHeightMplCamp = rootgrp.createVariable(
                "CloudLayerTopHeightMplCamp", "f4", ("time", "numlayers")
            )
            CloudLayerTopHeightMplCamp.long_name = "Top Height of Hydrometeor Layer from Composite (MMCR/Campbell et al. MPL) Algorithms"
            CloudLayerTopHeightMplCamp.units = "m AGL"
            CloudLayerTopHeightMplCamp.comment = "none"
            CloudLayerTopHeightMplCamp[:] = [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]

            # CloudLayerTopHeightMplCloth
            CloudLayerTopHeightMplCloth = rootgrp.createVariable(
                "CloudLayerTopHeightMplCloth", "f4", ("time", "numlayers")
            )
            CloudLayerTopHeightMplCloth.long_name = "Top Height of Hydrometeor Layer from Composite (MMCR/Clothiaux et al. MPL) Algorithms"
            CloudLayerTopHeightMplCloth.units = "m AGL"
            CloudLayerTopHeightMplCloth.comment = "none"
            CloudLayerTopHeightMplCloth[:] = [
                [374.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [419.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [419.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]

            # qc_RadarArtifacts
            qc_RadarArtifacts = rootgrp.createVariable(
                "qc_RadarArtifacts", "S1", ("time", "nheights")
            )
            qc_RadarArtifacts.long_name = "MMCR Mode Quality Control Flags"
            qc_RadarArtifacts.units = "unitless"
            qc_RadarArtifacts.comment = "0 No significant power return, 1 Significant, problem free data, 2 Second trip echo problems, 3 Coherent integration problems, 4 Second trip echo and coherent integration problems, 5 Pulse coding problems, 10 Data do not exist"
            qc_RadarArtifacts[:] = [
                [b"\n", b"\n"],
                [b"\n", b"\n"],
                [b"\n", b"\n"],
            ]

            # qc_ReflectivityClutterFlag
            qc_ReflectivityClutterFlag = rootgrp.createVariable(
                "qc_ReflectivityClutterFlag", "S1", ("time", "nheights")
            )
            qc_ReflectivityClutterFlag.long_name = "MMCR Reflectivity Clutter Flags"
            qc_ReflectivityClutterFlag.units = "unitless"
            qc_ReflectivityClutterFlag.comment = "0 No significant power return, 1 Significant, problem free data, 2 Clutter and cloud contribution, 3 Clutter only contribution, 10 Data do not exist"
            qc_ReflectivityClutterFlag[:] = [
                [b"\n", b"\n"],
                [b"\n", b"\n"],
                [b"\n", b"\n"],
            ]

            # qc_CloudLayerTopHeightMplCamp
            qc_CloudLayerTopHeightMplCamp = rootgrp.createVariable(
                "qc_CloudLayerTopHeightMplCamp", "f4", ("time", "numlayers")
            )
            qc_CloudLayerTopHeightMplCamp.long_name = "Value Indicating the Reliability of the Layer Top Height Using the Campbell et al. MPL Algorithm"
            qc_CloudLayerTopHeightMplCamp.units = "unitless"
            qc_CloudLayerTopHeightMplCamp.comment = "none"
            qc_CloudLayerTopHeightMplCamp[:] = [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]

            # qc_CloudLayerTopHeightMplCloth
            qc_CloudLayerTopHeightMplCloth = rootgrp.createVariable(
                "qc_CloudLayerTopHeightMplCloth", "f4", ("time", "numlayers")
            )
            qc_CloudLayerTopHeightMplCloth.long_name = "Value Indicating the Reliability of the Layer Top Height Using the Clothiaux et al. MPL Algorithm"
            qc_CloudLayerTopHeightMplCloth.units = "unitless"
            qc_CloudLayerTopHeightMplCloth.comment = "none"
            qc_CloudLayerTopHeightMplCloth[:] = [
                [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]

            # qc_BeamAttenuationMplCamp
            qc_BeamAttenuationMplCamp = rootgrp.createVariable(
                "qc_BeamAttenuationMplCamp", "f4", ("time",)
            )
            qc_BeamAttenuationMplCamp.long_name = (
                "MPL Campbell et al. Algorithm Beam Attenuation Assessment"
            )
            qc_BeamAttenuationMplCamp.units = "unitless"
            qc_BeamAttenuationMplCamp.comment = "-9. Data do not exist, -2. Beam blocked, -1. Beam attenuated, 0. No cloud (clear), 1. Beam penetrated atmosphere"
            qc_BeamAttenuationMplCamp[:] = [-9.0, -9.0, -9.0]

            # qc_BeamAttenuationMplCloth
            qc_BeamAttenuationMplCloth = rootgrp.createVariable(
                "qc_BeamAttenuationMplCloth", "f4", ("time",)
            )
            qc_BeamAttenuationMplCloth.long_name = (
                "MPL Cloth et al. Algorithm Beam Attenuation Assessment"
            )
            qc_BeamAttenuationMplCloth.units = "unitless"
            qc_BeamAttenuationMplCloth.comment = "-9. Data do not exist, Log10(Signal Power above Cloud/Estimated Clearsky Power above Cloud)"
            qc_BeamAttenuationMplCloth[:] = [-0.8169538, -0.83418494, -0.83418494]

    print("Closing file...")


if __name__ == "__main__":
    print("Running main...")
    observatory = sys.argv[1]
    instrument = sys.argv[2]
    print(f"Observatory: {observatory} and Instrument: {instrument}")
    main(observatory, instrument)
    print("Done.")
