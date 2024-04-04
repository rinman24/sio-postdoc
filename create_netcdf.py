"""Create test files."""

import sys

import numpy as np
from netCDF4 import Dataset


def main(observatory, instrument):  # noqa: PLR0915
    """Create test netCDF files."""
    print("Creating NCDF file...")

    if observatory not in ["sheba", "eureka"]:
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

    with Dataset(filename, "w", format="NETCDF4") as rootgrp:
        if observatory == "sheba" and instrument == "dabul":
            # Attributes
            print("Creating attributes...")
            rootgrp.instrument_name = "dabul"
            rootgrp.experiment_name = "sheba"
            rootgrp.site_name = "arctic"
            rootgrp.netcdf_filename = filename
            rootgrp.netcdf_file_creation = "030824"
            # Dimensions
            print("Creating dimensions...")
            record = rootgrp.createDimension("record", 6)  # noqa: F841
            level = rootgrp.createDimension("level", 3)  # noqa: F841
            filename_size = rootgrp.createDimension(  # noqa: F841
                "filename_size", len(filename)
            )  # noqa: F841
            # Variables
            print("Creating variables...")
            range = rootgrp.createVariable("range", "f4", ("level",))
            range[:] = [0, 30, 60]

            time = rootgrp.createVariable("time", "f4", ("record",))
            hours: list[int] = [0, 1, 2, 3, 4, 5]
            time[:] = [i / 24 for i in hours]

            latitude = rootgrp.createVariable("latitude", "f4", ("record",))
            latitude[:] = [75.1362] * 6

            longitude = rootgrp.createVariable("longitude", "f4", ("record",))
            longitude[:] = [-159.5352] * 6

            altitude = rootgrp.createVariable("altitude", "f4", ("record",))
            altitude[:] = [10] * 6

            elevation = rootgrp.createVariable("elevation", "f4", ("record",))
            elevation[:] = [95.32979, 95.31653, 95.31126, 95.33647, 95.35614, 95.33156]

            azimuth = rootgrp.createVariable("azimuth", "f4", ("record",))
            azimuth[:] = [80] * 6

            scanmode = rootgrp.createVariable("scanmode", "i2", ("record",))
            scanmode[:] = [-999] * 6

            depolarization = rootgrp.createVariable(
                "depolarization", "f4", ("record", "level")
            )
            depolarization[:] = [
                [-1.0809815, 0.14680599, 1.5720826],
                [-1.5588512, 0.12633708, 1.381299],
                [-1.802245, 0.17213729, 1.6474841],
                [-1.7750552, 0.13646123, 1.8563595],
                [-1.6844584, 0.12883691, 2.23747],
                [-1.3537484, 0.13436721, 1.6837305],
            ]

            far_parallel = rootgrp.createVariable(
                "far_parallel", "f4", ("record", "level")
            )
            far_parallel[:] = [
                [-999, 61.718746, -999],
                [-999, 61.790615, -999],
                [-999, 61.599712, -999],
                [-999, 61.9116, -999],
                [-999, 61.465282, -999],
                [-999, 61.77173, -999],
            ]
        elif observatory == "sheba" and instrument == "mmcr":
            # Attributes
            print("Creating attributes...")
            rootgrp.contact = "Eugene E. Clothiaux, Gerald. G. Mace, Thomas A. Ackerman, 503 Walker Building, University Park, PA, 16802; Phone: , FAX: , E-mail: cloth,mace,ackerman@essc.psu.edu"
            rootgrp.comment = "Divide Reflectivity by 100 to get dBZ, SignaltoNoiseRatio by 100 to get dB and MeanDopplerVelocity and SpectralWidth by 1000 to get m/s!"
            rootgrp.commenta = "For each merged range gate reflectivity, velocity and width always come from the same mode."
            rootgrp.commentb = "Quality Control Flags: 0 - No Data, 1 - Good Data, 2 - Second Trip Echo Problems, 3 - Coherent Integration Problems, 4 - Second Trip Echo and Coherent Integration Problems"
            # Dimensions
            print("Creating dimensions...")
            time = rootgrp.createDimension("time", 6)
            nheights = rootgrp.createDimension("nheights", 3)
            # Variables
            print("Creating variables...")
            base_time = rootgrp.createVariable("base_time", "i4")
            base_time[:] = 883828870
            base_time.long_name = "Beginning Time of File"
            base_time.units = "seconds since 1770-01-01 00:00:00 00;00"
            base_time.calendar_date = "Year 1998 Month 01 Day 03 12:01:10"

            time_offset = rootgrp.createVariable("time_offset", "f8", ("time",))
            time_offset[:] = [0, 10, 20, 30, 40, 50]
            time_offset.long_name = "Time Offset from base_time"
            time_offset.units = "seconds"
            time_offset.comment = "none"

            Heights = rootgrp.createVariable("Heights", "f4", ("nheights",))
            Heights[:] = [105, 150, 195]
            Heights.long_name = "Height of Measured Value; agl"
            Heights.units = "m"

            Qc = rootgrp.createVariable("Qc", "S1", ("time", "nheights"))
            Qc[:] = [
                [b"\x01", b"\x01", b"\x01"],
                [b"\x01", b"\x01", b"\x01"],
                [b"\x01", b"\x01", b"\x01"],
                [b"\x01", b"\x01", b"\x01"],
                [b"\x01", b"\x01", b"\x01"],
                [b"\x01", b"\x01", b"\x01"],
            ]
            Qc.long_name = "Quality Control Flags"
            Qc.units = "unitless"

            Reflectivity = rootgrp.createVariable(
                "Reflectivity", "i2", ("time", "nheights")
            )
            Reflectivity[:] = [
                [-6408, -2450, -2149],
                [-6408, -2450, -2149],
                [-6422, -2446, -2145],
                [-6448, -2439, -2138],
                [-6475, -2432, -2131],
                [-6498, -2427, -2126],
            ]
            Reflectivity.long_name = "Reflectivity"
            Reflectivity.units = "dBZ (X100)"

            MeanDopplerVelocity = rootgrp.createVariable(
                "MeanDopplerVelocity", "i2", ("time", "nheights")
            )
            MeanDopplerVelocity[:] = [
                [-865, -296, 273],
                [-865, -296, 273],
                [-864, -288, 288],
                [-863, -275, 312],
                [-861, -262, 337],
                [-860, -251, 358],
            ]
            MeanDopplerVelocity.long_name = "Mean Doppler Velocity"
            MeanDopplerVelocity.units = "m/s (X1000)"

            SpectralWidth = rootgrp.createVariable(
                "SpectralWidth", "i2", ("time", "nheights")
            )
            SpectralWidth[:] = [
                [104, 165, 225],
                [104, 165, 225],
                [104, 167, 230],
                [105, 171, 237],
                [106, 175, 245],
                [106, 179, 251],
            ]
            SpectralWidth.long_name = "Spectral Width"
            SpectralWidth.units = "m/s (X1000)"

            ModeId = rootgrp.createVariable("ModeId", "S1", ("time", "nheights"))
            ModeId[:] = [
                [b"\x03", b"\x03", b"\x03"],
                [b"\x03", b"\x03", b"\x03"],
                [b"\x03", b"\x03", b"\x03"],
                [b"\x03", b"\x03", b"\x03"],
                [b"\x03", b"\x03", b"\x03"],
                [b"\x03", b"\x03", b"\x03"],
            ]
            ModeId.long_name = "Mode I.D. for Merged Time-Height Moments Data"
            ModeId.units = "unitless"

            SignaltoNoiseRatio = rootgrp.createVariable(
                "SignaltoNoiseRatio", "i2", ("time", "nheights")
            )
            SignaltoNoiseRatio[:] = [
                [475, 2745, 3045],
                [475, 2745, 3045],
                [462, 2749, 3049],
                [439, 2757, 3057],
                [415, 2764, 3064],
                [394, 2769, 3069],
            ]
            SignaltoNoiseRatio.long_name = "Signal-to-Noise Ratioo"
            SignaltoNoiseRatio.units = "dB (X100)"
        elif observatory == "eureka" and instrument == "mmcr":
            # Attributes
            print("Creating attributes...")
            rootgrp.Source = "20050810.000000"
            rootgrp.Version = "***1.0***"
            rootgrp.Input_Platforms = ""
            rootgrp.Contact = "***ETL***"
            rootgrp.commenta = "At each height and time, the MMCR reflectivity, velocity, spectral width and signal-to-noise ratio always come from the same mode. The mode in indicated by ModeId."
            rootgrp.commentb = "Missing (i.e., does not exist) data for a particular time period are indicated by a value of 10 for the ModeId. The geophysical variables should contain a value of -32768 at these times."
            rootgrp.commentc = "Note that -32768 is also used for the geophysical variables when there are no significant detections, in which case ModeId is 0."

            # Dimensions
            print("Creating dimensions...")
            time = rootgrp.createDimension("time", 3)
            nheights = rootgrp.createDimension("nheights", 2)  # noqa: F841
            numlayers = rootgrp.createDimension("numlayers", 4)  # noqa: F841
            # Variables

            # base_time
            print("Creating variables...")
            base_time = rootgrp.createVariable("base_time", "f8")
            base_time[:] = 1123632266.0
            base_time.long_name = "Beginning Time of File"
            base_time.units = "seconds since 1970-01-01 00:00 UTC"
            base_time.calendar_date = "20050810_00:04:26"

            time_offset = rootgrp.createVariable("time_offset", "f8", ("time",))
            time_offset[:] = [0.0, 10.0, 20.0]
            time_offset.long_name = "Time Offset from base_time"
            time_offset.units = "seconds"
            time_offset.comment = "none"

            # heights
            heights = rootgrp.createVariable("heights", "f4", ("nheights",))
            heights[:] = [95, 140]
            heights.long_name = "Height of Measured Value; agl"
            heights.units = "m AGL"
            heights.comment = "none"

            # Reflectivity
            Reflectivity = rootgrp.createVariable(
                "Reflectivity", "i2", ("time", "nheights")
            )
            Reflectivity[:] = [
                [-32768, -3852],
                [-10350, -3854],
                [-9549, -3855],
            ]
            Reflectivity.long_name = "MMCR Reflectivity"
            Reflectivity.units = "dBZ(X100)"
            Reflectivity.comment = "Divide Reflectivity by 100 to get dBZ"

            # MeanDopplerVelocity
            MeanDopplerVelocity = rootgrp.createVariable(
                "MeanDopplerVelocity", "i2", ("time", "nheights")
            )
            MeanDopplerVelocity[:] = [
                [-32768, 13880],
                [-1084, 13880],
                [-772, 13880],
            ]
            MeanDopplerVelocity.long_name = "MMCR MeanDopplerVelocity"
            MeanDopplerVelocity.units = "m/s(X1000)"
            MeanDopplerVelocity.comment = (
                "Divide MeanDopplerVelocity by 1000 to get m/s"
            )

            # SpectralWidth
            SpectralWidth = rootgrp.createVariable(
                "SpectralWidth", "i2", ("time", "nheights")
            )
            SpectralWidth[:] = [
                [-32768, 176],
                [-415, 176],
                [97, 176],
            ]
            SpectralWidth.long_name = "MMCR SpectralWidth"
            SpectralWidth.units = "m/s(X1000)"
            SpectralWidth.comment = "Divide SpectralWidth by 1000 to get m/s"

            # SignalToNoiseRatio
            SignalToNoiseRatio = rootgrp.createVariable(
                "SignalToNoiseRatio", "i2", ("time", "nheights")
            )
            SignalToNoiseRatio[:] = [
                [-32768, -32768],
                [-32768, -32768],
                [-32768, -32768],
            ]
            SignalToNoiseRatio.long_name = "MMCR Signal-To-Noise Ratio"
            SignalToNoiseRatio.units = "dB(x100)"
            SignalToNoiseRatio.comment = "Divide SignalToNoiseRatio by 100 to get dB"

            # ModeId
            ModeId = rootgrp.createVariable("ModeId", "i2", ("time", "nheights"))
            ModeId[:] = [
                [0, 0],
                [0, 0],
                [0, 0],
            ]
            ModeId.long_name = "MMCR ModeId"
            ModeId.units = "unitless"
            ModeId.comment = (
                "0 No significant power return, 1-5 Valid modes, 10 Data do not exist"
            )

            # CloudLayerBottomHeight
            CloudLayerBottomHeight = rootgrp.createVariable(
                "CloudLayerBottomHeight", "f4", ("time", "numlayers")
            )
            CloudLayerBottomHeight[:] = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ]
            CloudLayerBottomHeight.long_name = "Bottom Height of Echo Layer"
            CloudLayerBottomHeight.units = "m AGL"
            CloudLayerBottomHeight.comment = "none"

            # CloudLayerTopHeight
            CloudLayerTopHeight = rootgrp.createVariable(
                "CloudLayerTopHeight", "f4", ("time", "numlayers")
            )
            CloudLayerTopHeight[:] = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ]
            CloudLayerTopHeight.long_name = "Top Height of Echo Layer"
            CloudLayerTopHeight.units = "m AGL"
            CloudLayerTopHeight.comment = "none"
        elif observatory == "eureka" and instrument == "ahsrl":
            # Attributes
            print("Creating attributes...")
            rootgrp.code_version = (
                "$Id: processed_netcdf.m,v 1.96 2008/10/29 15:32:21 jpgarcia Exp $"
            )
            rootgrp.load_calibration_version = (
                "$Id: load_calibration.m,v 1.25 2008/10/30 15:04:39 eloranta Exp $"
            )
            rootgrp.get_internal_cal_vals_version = "$Id: get_internal_cal_vals.m,v 1.109 2008/09/12 21:20:05 eloranta Exp $"
            rootgrp.calvals = (
                "$Id: calvals_ahsrl.m,v 1.107 2008/10/10 20:56:18 eloranta Exp $"
            )
            rootgrp.find_new_cal_times_version = (
                "$Id: find_new_cal_times.m,v 1.21 2008/02/25 19:33:32 jpgarcia Exp $"
            )
            rootgrp.radiosonde_profile_version = (
                "$Id: radiosonde_profile.m,v 1.30 2008/04/09 17:04:51 jpgarcia Exp $"
            )
            rootgrp.fetch_cal_version = (
                "$Id: fetch_cal.m,v 1.19 2008/09/04 21:06:16 eloranta Exp $"
            )
            rootgrp.quick_cal_version = (
                "$Id: quick_cal.m,v 1.58 2008/10/30 15:03:20 eloranta Exp $"
            )
            rootgrp.processed_netcdf_version = (
                "$Id: processed_netcdf.m,v 1.96 2008/10/29 15:32:21 jpgarcia Exp $"
            )
            rootgrp.process_data_version = (
                "$Id: process_data.m,v 1.202 2008/10/30 15:04:39 eloranta Exp $"
            )
            rootgrp.timefill_sum_version = (
                "$Id: time_block.cc,v 1.54 2008/04/16 21:33:02 jpgarcia Exp $"
            )
            rootgrp.timefill_average_version = (
                "$Id: time_block.cc,v 1.54 2008/04/16 21:33:02 jpgarcia Exp $"
            )
            rootgrp.file_version = int(20050323)
            rootgrp.time_zone = "UTC"
            rootgrp.file_created = "2008-10-30 22:30:49"
            rootgrp.Conventions = "COARDS"
            rootgrp.time_axis_average_mode = "time"
            rootgrp.time_axis_average_parameter = float(30)
            rootgrp.range_axis_average_parameter = float(30)
            rootgrp.featureset = int(8175)
            rootgrp.featureset_version = "$Revision: 1.13 $"
            rootgrp.processing_parameters__qc_params__mol_lost = float(1)
            rootgrp.processing_parameters__qc_params__lock_level = float(0.6)
            rootgrp.processing_parameters__qc_params__backscat_snr = float(1)
            rootgrp.processing_parameters__particlesettings__alpha_water = float(2)
            rootgrp.processing_parameters__particlesettings__g_water = float(1)
            rootgrp.processing_parameters__particlesettings__alpha_ice = float(1)
            rootgrp.processing_parameters__particlesettings__g_ice = float(1)
            rootgrp.processing_parameters__particlesettings__type = (
                "Bullet Rosettes (Mitchell 1996)"
            )
            rootgrp.processing_parameters__particlesettings__Dr = float(60)
            rootgrp.processing_parameters__particlesettings__sigma_a = float(1)
            rootgrp.processing_parameters__particlesettings__sigma_v = float(0.26)
            rootgrp.processing_parameters__particlesettings__delta_a1 = float(2)
            rootgrp.processing_parameters__particlesettings__delta_v1 = float(3)
            rootgrp.processing_parameters__particlesettings__delta_a2 = float(1.57)
            rootgrp.processing_parameters__particlesettings__delta_v2 = float(2.26)
            rootgrp.processing_parameters__particlesettings__h20_depol_threshold = (
                float(0.05)
            )
            rootgrp.processing_parameters__particlesettings__p180_ice = float(0.035)

            # Dimensions
            print("Creating dimensions...")
            time = rootgrp.createDimension("time", 3)
            altitude = rootgrp.createDimension("altitude", 2)  # noqa: F841
            time_vector = rootgrp.createDimension("time_vector", 8)  # noqa: F841
            calibration = rootgrp.createDimension("calibration", 3)  # noqa: F841
            sondenamelength = rootgrp.createDimension(  # noqa: F841
                "sondenamelength", 6
            )
            i2header = rootgrp.createDimension("i2header", 9)  # noqa: F841
            geoheader = rootgrp.createDimension("geoheader", 20)  # noqa: F841
            apheader = rootgrp.createDimension("apheader", 30)  # noqa: F841

            # Variables
            print("Creating variables...")

            # base_time
            base_time = rootgrp.createVariable("base_time", "i4")
            base_time[:] = int(1123804800)
            base_time.string = "2005-08-12 00:00:00 UTC"
            base_time.long_name = "Base seconds since Unix Epoch"
            base_time.units = "seconds since 1970-01-01 00:00:00 UTC"

            # first_time
            first_time = rootgrp.createVariable("first_time", "i2", ("time_vector",))
            first_time[:] = [2005, 8, 12, 0, 0, 0, 0, 0]
            first_time.long_name = "First Time in file"

            # last_time
            last_time = rootgrp.createVariable("last_time", "i2", ("time_vector",))
            last_time[:] = [2005, 8, 12, 23, 59, 58, 999, 968]
            last_time.long_name = "Last Time in file"

            # time
            time = rootgrp.createVariable("time", "f8", ("time",))
            time[:] = [0.0, 30.0, 60.0]
            time.long_name = "Time"
            time.units = "seconds since 2005-08-12 00:00:00 UTC"

            # time_offset
            time_offset = rootgrp.createVariable("time_offset", "f8", ("time",))
            time_offset[:] = [0.0, 30.0, 60.0]
            time_offset.long_name = "Time offset from base_time"
            time_offset.description = 'same times as "First time in record" '
            time_offset.units = "seconds since 2005-08-12 00:00:00 UTC"

            # start_time
            start_time = rootgrp.createVariable(
                "start_time",
                "i2",
                ("time", "time_vector"),
            )
            start_time[:] = [
                [2005, 8, 12, 0, 0, 0, 0, 0],
                [2005, 8, 12, 0, 0, 30, 0, 0],
                [2005, 8, 12, 0, 1, 0, 0, 0],
            ]
            start_time.long_name = "First Time in record"
            start_time.description = "time of first laser shot in averaging interval"

            # mean_time
            mean_time = rootgrp.createVariable(
                "mean_time",
                "i2",
                ("time", "time_vector"),
            )
            mean_time[:] = [
                [2005, 8, 12, 0, 0, 15, 0, 0],
                [2005, 8, 12, 0, 0, 45, 0, 0],
                [2005, 8, 12, 0, 1, 14, 999, 992],
            ]
            mean_time.long_name = "mean time of record"
            mean_time.description = (
                "mean time of laser shots collected in averaging interval"
            )

            # end_time
            end_time = rootgrp.createVariable(
                "end_time",
                "i2",
                ("time", "time_vector"),
            )
            end_time[:] = [
                [2005, 8, 12, 0, 0, 30, 0, 0],
                [2005, 8, 12, 0, 1, 0, 0, 0],
                [2005, 8, 12, 0, 1, 29, 999, 992],
            ]
            end_time.long_name = "Last Time in record"
            end_time.description = "time of last laser shot in averaging interval"

            # latitude
            latitude = rootgrp.createVariable("latitude", "f4")
            latitude.long_name = "latitude of lidar"
            latitude.units = "degree_N"
            latitude[:] = 79.9903

            # longitude
            longitude = rootgrp.createVariable("longitude", "f4")
            longitude.long_name = "longitude of lidar"
            longitude.units = "degree_W"
            longitude[:] = 85.9389

            # range_resolution
            range_resolution = rootgrp.createVariable("range_resolution", "f4")
            range_resolution.long_name = "Range resolution"
            range_resolution.description = (
                "vertical distance between data points after averaging"
            )
            range_resolution.units = "meters"
            range_resolution[:] = 30.0

            # time_average
            time_average = rootgrp.createVariable("time_average", "f4")
            time_average.long_name = "Time Averaging Width"
            time_average.description = "Time between data points after averaging"
            time_average.units = "seconds"
            time_average[:] = 30.0

            # new_cal_times
            new_cal_times = rootgrp.createVariable(
                "new_cal_times", "i2", ("calibration", "time_vector")
            )
            new_cal_times.long_name = "Time of Calibration Change"
            new_cal_times.description = (
                "New raob or system calibration data triggered recalibration"
            )
            new_cal_times[:] = [
                [2005, 8, 12, 0, 0, 0, 0, 0],
                [2005, 8, 12, 6, 0, 0, 0, 0],
                [2005, 8, 12, 18, 0, 0, 0, 0],
            ]

            # altitude
            altitude = rootgrp.createVariable("altitude", "f4", ("altitude",))
            altitude.long_name = "Height above lidar"
            altitude.units = "meters"
            altitude[:] = [11.25, 41.25]

            # new_cal_trigger
            new_cal_trigger = rootgrp.createVariable(
                "new_cal_trigger", "i1", ("calibration",)
            )
            new_cal_trigger.long_name = "Trigger of Calibration Change"
            new_cal_trigger.description = "reason for recalibration"
            new_cal_trigger.bit_0 = "radiosonde profile"
            new_cal_trigger.bit_1 = "i2 scan"
            new_cal_trigger.bit_2 = "geometry"
            new_cal_trigger[:] = [2, 2, 2]

            # new_cal_offset
            new_cal_offset = rootgrp.createVariable(
                "new_cal_offset", "i2", ("calibration",)
            )
            new_cal_offset.long_name = "Record Dimension equivalent Offset"
            new_cal_offset.min_value = 0
            new_cal_offset[:] = [0, 717, 2157]

            # temperature_profile
            temperature_profile = rootgrp.createVariable(
                "temperature_profile", "f4", ("calibration", "altitude")
            )
            temperature_profile.long_name = "Raob Temperature Profile"
            temperature_profile.description = (
                "Temperature interpolated to requested altitude resolution"
            )
            temperature_profile.units = "degrees Kelvin"
            temperature_profile[:] = [
                [np.nan, 282.7846],
                [np.nan, 280.38013],
                [np.nan, 281.7381],
            ]

            # pressure_profile
            pressure_profile = rootgrp.createVariable(
                "pressure_profile", "f4", ("calibration", "altitude")
            )
            pressure_profile.long_name = "Raob pressure Profile"
            pressure_profile.description = (
                "Pressure interpolated to requested altitude resolution"
            )
            pressure_profile.units = "hectopascals"
            pressure_profile[:] = [
                [np.nan, 1006.3159],
                [np.nan, 1006.2226],
                [np.nan, 1008.2024],
            ]

            # dewpoint_profile
            dewpoint_profile = rootgrp.createVariable(
                "dewpoint_profile", "f4", ("calibration", "altitude")
            )
            dewpoint_profile.long_name = "Raob Dewpoint Temperature Profile"
            dewpoint_profile.description = (
                "Dewpoint interpolated to requested altitude resolution"
            )
            dewpoint_profile.units = "degrees Kelvin"
            dewpoint_profile.missing_value = np.nan
            dewpoint_profile[:] = [
                np.ma.array(
                    np.array([np.nan, 274.8038330078125]),
                    mask=[1, 0],
                    fill_value=np.nan,
                ),
                np.ma.array(
                    np.array([np.nan, 274.64691162109375]),
                    mask=[1, 0],
                    fill_value=np.nan,
                ),
                np.ma.array(np.array([np.nan, 275.0]), mask=[1, 0], fill_value=np.nan),
            ]

            # windspeed_profile
            windspeed_profile = rootgrp.createVariable(
                "windspeed_profile", "f4", ("calibration", "altitude")
            )
            windspeed_profile.long_name = "Raob Wind Speed Profile"
            windspeed_profile.description = (
                "Speeds interpolated to requested altitude resolution"
            )
            windspeed_profile.units = "m/s"
            windspeed_profile.missing_value = np.nan
            windspeed_profile[:] = [
                np.ma.array(
                    np.array([np.nan, 6.625823974609375]),
                    mask=[1, 0],
                    fill_value=np.nan,
                ),
                np.ma.array(
                    np.array([np.nan, 2.6877658367156982]),
                    mask=[1, 0],
                    fill_value=np.nan,
                ),
                np.ma.array(
                    np.array([np.nan, 5.2940473556518555]),
                    mask=[1, 0],
                    fill_value=np.nan,
                ),
            ]

            # winddir_profile
            winddir_profile = rootgrp.createVariable(
                "winddir_profile", "f4", ("calibration", "altitude")
            )
            winddir_profile.long_name = "Raob Wind Direction Profile"
            winddir_profile.description = (
                "Directions interpolated to requested altitude resolution"
            )
            winddir_profile.units = "degrees"
            winddir_profile.missing_value = np.nan
            winddir_profile[:] = [
                np.ma.array(
                    np.array([np.nan, 174.38186645507812]),
                    mask=[1, 0],
                    fill_value=np.nan,
                ),
                np.ma.array(
                    np.array([np.nan, 314.7340393066406]),
                    mask=[1, 0],
                    fill_value=np.nan,
                ),
                np.ma.array(
                    np.array([np.nan, 313.98809814453125]),
                    mask=[1, 0],
                    fill_value=np.nan,
                ),
            ]

            # raob_station
            raob_station = rootgrp.createVariable(
                "raob_station", "S1", ("calibration", "sondenamelength")
            )
            raob_station.long_name = "Radiosonde Station ID"
            raob_station[:] = [
                [b"Y", b"E", b"U", b" ", b" ", b" "],
                [b"Y", b"E", b"U", b" ", b" ", b" "],
                [b"Y", b"E", b"U", b" ", b" ", b" "],
            ]

            # i2_txt_header
            i2_txt_header = rootgrp.createVariable(
                "i2_txt_header", "S1", ("calibration", "i2header")
            )
            i2_txt_header.long_name = "i2_scan_file_text_info"
            i2_txt_header.description = (
                "Contains name of file used to compute calibration"
            )
            i2_txt_header[:] = [
                np.ma.array(np.array([b""] * 9), mask=[1] * 9, fill_value=b""),
                np.ma.array(np.array([b""] * 9), mask=[1] * 9, fill_value=b""),
                np.ma.array(np.array([b""] * 9), mask=[1] * 9, fill_value=b""),
            ]

            # geo_txt_header
            geo_txt_header = rootgrp.createVariable(
                "geo_txt_header", "S1", ("calibration", "geoheader")
            )
            geo_txt_header.long_name = "geometric_correction_file_txt_header."
            geo_txt_header[:] = [
                np.ma.array(np.array([b""] * 20), mask=[1] * 20, fill_value=b""),
                np.ma.array(np.array([b""] * 20), mask=[1] * 20, fill_value=b""),
                np.ma.array(np.array([b""] * 20), mask=[1] * 20, fill_value=b""),
            ]

            # ap_txt_header
            ap_txt_header = rootgrp.createVariable(
                "ap_txt_header", "S1", ("calibration", "apheader")
            )
            ap_txt_header.long_name = "afterpulse_correction_file_txt_header."
            ap_txt_header[:] = [
                np.ma.array(
                    np.array(
                        [
                            b"#",
                            b" ",
                            b"A",
                            b"f",
                            b"t",
                            b"e",
                            b"r",
                            b" ",
                            b"p",
                            b"u",
                            b"l",
                            b"s",
                            b"e",
                            b" ",
                            b"d",
                            b"i",
                            b"s",
                            b"t",
                            b"r",
                            b"i",
                            b"b",
                            b"u",
                            b"t",
                            b"i",
                            b"o",
                            b"n",
                            b" ",
                            b"3",
                            b"1",
                            b"-",
                        ]
                    ),
                    mask=[0] * 30,
                    fill_value=b"",
                ),
                np.ma.array(
                    np.array(
                        [
                            b"#",
                            b" ",
                            b"A",
                            b"f",
                            b"t",
                            b"e",
                            b"r",
                            b" ",
                            b"p",
                            b"u",
                            b"l",
                            b"s",
                            b"e",
                            b" ",
                            b"d",
                            b"i",
                            b"s",
                            b"t",
                            b"r",
                            b"i",
                            b"b",
                            b"u",
                            b"t",
                            b"i",
                            b"o",
                            b"n",
                            b" ",
                            b"3",
                            b"1",
                            b"-",
                        ]
                    ),
                    mask=[0] * 30,
                    fill_value=b"",
                ),
                np.ma.array(
                    np.array(
                        [
                            b"#",
                            b" ",
                            b"A",
                            b"f",
                            b"t",
                            b"e",
                            b"r",
                            b" ",
                            b"p",
                            b"u",
                            b"l",
                            b"s",
                            b"e",
                            b" ",
                            b"d",
                            b"i",
                            b"s",
                            b"t",
                            b"r",
                            b"i",
                            b"b",
                            b"u",
                            b"t",
                            b"i",
                            b"o",
                            b"n",
                            b" ",
                            b"3",
                            b"1",
                            b"-",
                        ]
                    ),
                    mask=[0] * 30,
                    fill_value=b"",
                ),
            ]

            # raob_time_offset
            raob_time_offset = rootgrp.createVariable(
                "raob_time_offset", "f8", ("calibration",)
            )
            raob_time_offset.units = "seconds"
            raob_time_offset.long_name = "Radiosonde Launch time offset"
            raob_time_offset.description = "Time after base time in seconds"
            raob_time_offset[:] = [0.0, 43200.0, 86400.0]

            # raob_time_vector
            raob_time_vector = rootgrp.createVariable(
                "raob_time_vector", "i2", ("calibration", "time_vector")
            )
            raob_time_vector.long_name = "Radiosonde Launch time vector"
            raob_time_vector.description = (
                "Time in [year month day hour min sec ms us] format"
            )
            raob_time_vector[:] = [
                [2005, 8, 12, 0, 0, 0, 0, 0],
                [2005, 8, 12, 12, 0, 0, 0, 0],
                [2005, 8, 13, 0, 0, 0, 0, 0],
            ]

            # Cmc
            Cmc = rootgrp.createVariable("Cmc", "f4", ("calibration", "altitude"))
            Cmc.long_name = "Molecular in Combined Calibration"
            Cmc[:] = [
                [np.nan, 0.9491847],
                [np.nan, 0.94941056],
                [np.nan, 0.94914037],
            ]

            # Cmm
            Cmm = rootgrp.createVariable("Cmm", "f4", ("calibration", "altitude"))
            Cmm.long_name = "Molecular in Molecular Calibration"
            Cmm[:] = [
                [np.nan, 1.971094],
                [np.nan, 1.9666044],
                [np.nan, 1.9722056],
            ]

            # Cam
            Cam = rootgrp.createVariable("Cam", "f4", ("calibration", "altitude"))
            Cam.long_name = "Aerosol in Molecular Calibration"
            Cam[:] = [
                [0.000872, 0.000872],
                [0.000872, 0.000872],
                [0.000872, 0.000872],
            ]

            # beta_m
            beta_m = rootgrp.createVariable("beta_m", "f4", ("calibration", "altitude"))
            beta_m.long_name = "Aerosol in Molecular Calibration"
            beta_m.units = "1/meter"
            beta_m.plot_scale = "logarithmic"
            beta_m[:] = [
                [1.3551449e-05, 1.3394016e-05],
                [1.3619099e-05, 1.3491385e-05],
                [1.3584644e-05, 1.3519524e-05],
            ]

            # transmitted_energy
            transmitted_energy = rootgrp.createVariable(
                "transmitted_energy", "f4", ("time",)
            )
            transmitted_energy.long_name = "Transmitted Energy"
            transmitted_energy.units = "Joules"
            transmitted_energy.missing_value = np.nan
            transmitted_energy[:] = (
                np.ma.array(np.array([np.nan] * 3), mask=[1] * 3, fill_value=np.nan),
            )

            # piezovoltage
            piezovoltage = rootgrp.createVariable("piezovoltage", "f4", ("time",))
            piezovoltage.long_name = "piezovoltage"
            piezovoltage.units = "Volts"
            piezovoltage.missing_value = np.nan
            piezovoltage[:] = (
                np.ma.array(np.array([np.nan] * 3), mask=[1] * 3, fill_value=np.nan),
            )

            # num_seeded_shots
            num_seeded_shots = rootgrp.createVariable(
                "num_seeded_shots", "i4", ("time",)
            )
            num_seeded_shots.long_name = "Number of Seeded Shots"
            num_seeded_shots.missing_value = -1
            num_seeded_shots[:] = (
                np.ma.array(np.array([-1] * 3), mask=[1] * 3, fill_value=-1),
            )

            # c_pol_dark_count
            c_pol_dark_count = rootgrp.createVariable(
                "c_pol_dark_count", "f4", ("time",)
            )
            c_pol_dark_count.long_name = "Cross Polarization Dark Count"
            c_pol_dark_count.description = (
                "total counts per averaging interval(eg. one altitude, one time)"
            )
            c_pol_dark_count.units = "counts"
            c_pol_dark_count.missing_value = np.nan
            c_pol_dark_count[:] = (
                np.ma.array(np.array([np.nan] * 3), mask=[1] * 3, fill_value=np.nan),
            )

            # mol_dark_count
            mol_dark_count = rootgrp.createVariable("mol_dark_count", "f4", ("time",))
            mol_dark_count.long_name = "Molecular Dark Count"
            mol_dark_count.description = (
                "total counts per averaging interval(eg. one altitude, one time)"
            )
            mol_dark_count.units = "counts"
            mol_dark_count.missing_value = np.nan
            mol_dark_count[:] = (
                np.ma.array(np.array([np.nan] * 3), mask=[1] * 3, fill_value=np.nan),
            )

            # combined_dark_count_lo
            combined_dark_count_lo = rootgrp.createVariable(
                "combined_dark_count_lo", "f4", ("time",)
            )
            combined_dark_count_lo.long_name = "Low Gain Combined Dark Count"
            combined_dark_count_lo.description = (
                "total counts per averaging interval(eg. one altitude, one time)"
            )
            combined_dark_count_lo.units = "counts"
            combined_dark_count_lo.missing_value = np.nan
            combined_dark_count_lo[:] = (
                np.ma.array(np.array([np.nan] * 3), mask=[1] * 3, fill_value=np.nan),
            )

            # combined_dark_count_hi
            combined_dark_count_hi = rootgrp.createVariable(
                "combined_dark_count_hi", "f4", ("time",)
            )
            combined_dark_count_hi.long_name = "High Gain Combined Dark Count"
            combined_dark_count_hi.description = (
                "total counts per averaging interval(eg. one altitude, one time)"
            )
            combined_dark_count_hi.units = "counts"
            combined_dark_count_hi.missing_value = np.nan
            combined_dark_count_hi[:] = (
                np.ma.array(np.array([np.nan] * 3), mask=[1] * 3, fill_value=np.nan),
            )

            # combined_gain
            combined_gain = rootgrp.createVariable(
                "combined_gain", "f4", ("calibration",)
            )
            combined_gain.long_name = "Combined Gain Factor"
            combined_gain.description = "Low Gain level * Factor ~ High Gain level"
            combined_gain[:] = [16.0, 16.0, 16.0]

            # combined_merge_threshhold
            combined_merge_threshhold = rootgrp.createVariable(
                "combined_merge_threshhold", "f4", ("calibration",)
            )
            combined_merge_threshhold.long_name = "Combined Merge Threshhold"
            combined_merge_threshhold[:] = [0.05, 0.05, 0.05]

            # geo_cor
            geo_cor = rootgrp.createVariable(
                "geo_cor", "f4", ("calibration", "altitude")
            )
            geo_cor.long_name = "Overlap correction"
            geo_cor.description = (
                "Geometric overlap correction averaged to requested altitude resolution"
            )
            geo_cor.units = ""
            geo_cor.missing_value = np.nan
            geo_cor.plot_scale = "logarithmic"
            geo_cor[:] = [
                np.ma.array(np.array([np.nan, np.inf]), mask=[1, 0], fill_value=np.nan),
                np.ma.array(np.array([np.nan, np.inf]), mask=[1, 0], fill_value=np.nan),
                np.ma.array(np.array([np.nan, np.inf]), mask=[1, 0], fill_value=np.nan),
            ]

            # od
            od = rootgrp.createVariable("od", "f4", ("time", "altitude"))
            od.long_name = "Optical depth of particulate"
            od.units = ""
            od.missing_value = np.nan
            od.insufficient_data = np.inf
            od.plot_scale = "logarithmic"
            od[:] = [
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
            ]

            # profile_od
            profile_od = rootgrp.createVariable("profile_od", "f4", ("altitude",))
            profile_od.long_name = "Optical depth of particulate Profile"
            profile_od.units = ""
            profile_od.missing_value = np.nan
            profile_od.insufficient_data = np.inf
            profile_od.plot_scale = "logarithmic"
            profile_od[:] = [
                [4.8468604, -np.inf],
            ]

            # beta_a
            beta_a = rootgrp.createVariable("beta_a", "f4", ("time", "altitude"))
            beta_a.long_name = "Particulate extinction cross section per unit volume"
            beta_a.units = "1/m"
            beta_a.missing_value = np.nan
            beta_a.plot_scale = "logarithmic"
            beta_a[:] = [
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
            ]

            # atten_beta_r_backscat
            atten_beta_r_backscat = rootgrp.createVariable(
                "atten_beta_r_backscat", "f4", ("time", "altitude")
            )
            atten_beta_r_backscat.long_name = "Attenuated Molecular return"
            atten_beta_r_backscat.units = "1/(m sr)"
            atten_beta_r_backscat.missing_value = np.nan
            atten_beta_r_backscat.plot_scale = "logarithmic"
            atten_beta_r_backscat[:] = [
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
            ]

            # profile_atten_beta_r_backscat
            profile_atten_beta_r_backscat = rootgrp.createVariable(
                "profile_atten_beta_r_backscat", "f4", ("altitude",)
            )
            profile_atten_beta_r_backscat.long_name = "Attenuated Molecular Profile"
            profile_atten_beta_r_backscat.units = "1/(m sr)"
            profile_atten_beta_r_backscat.missing_value = np.nan
            profile_atten_beta_r_backscat.plot_scale = "logarithmic"
            profile_atten_beta_r_backscat[:] = (
                np.ma.array(np.array([np.nan, np.inf]), mask=[1, 0], fill_value=np.nan),
            )

            # depol
            depol = rootgrp.createVariable("depol", "f4", ("time", "altitude"))
            depol.long_name = "Circular depolarization ratio for particulate"
            depol.description = "left circular return divided by right circular return"
            depol.units = ""
            depol.missing_value = np.nan
            depol.plot_scale = "logarithmic"
            depol[:] = [
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
            ]

            # molecular_counts
            molecular_counts = rootgrp.createVariable(
                "molecular_counts", "i4", ("time", "altitude")
            )
            molecular_counts.long_name = "Molecular Photon Counts"
            molecular_counts.description = "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
            molecular_counts.units = "counts"
            molecular_counts.missing_value = -1
            molecular_counts.plot_scale = "logarithmic"
            molecular_counts[:] = [
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
            ]

            # combined_counts_lo
            combined_counts_lo = rootgrp.createVariable(
                "combined_counts_lo", "i4", ("time", "altitude")
            )
            combined_counts_lo.long_name = "Low Gain Combined Photon Counts"
            combined_counts_lo.description = "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
            combined_counts_lo.units = "counts"
            combined_counts_lo.missing_value = -1
            combined_counts_lo.plot_scale = "logarithmic"
            combined_counts_lo[:] = [
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
            ]

            # combined_counts_hi
            combined_counts_hi = rootgrp.createVariable(
                "combined_counts_hi", "i4", ("time", "altitude")
            )
            combined_counts_hi.long_name = "High Gain Combined Photon Counts"
            combined_counts_hi.description = "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
            combined_counts_hi.units = "counts"
            combined_counts_hi.missing_value = -1
            combined_counts_hi.plot_scale = "logarithmic"
            combined_counts_hi[:] = [
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
            ]

            # cross_counts
            cross_counts = rootgrp.createVariable(
                "cross_counts", "i4", ("time", "altitude")
            )
            cross_counts.long_name = "Cross Polarized Photon Counts"
            cross_counts.description = "Raw counts, per averaging interval with pileup, afterpulse, and darkcount corrections applied"
            cross_counts.units = "counts"
            cross_counts.missing_value = -1
            cross_counts.plot_scale = "logarithmic"
            cross_counts[:] = [
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
                np.ma.array(np.array([-1] * 2), mask=[1] * 2, fill_value=-1),
            ]

            # beta_a_backscat
            beta_a_backscat = rootgrp.createVariable(
                "beta_a_backscat", "f4", ("time", "altitude")
            )
            beta_a_backscat.long_name = (
                "Particulate backscatter cross section per unit volume"
            )
            beta_a_backscat.units = "1/(m sr)"
            beta_a_backscat.missing_value = np.nan
            beta_a_backscat.plot_scale = "logarithmic"
            beta_a_backscat[:] = [
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
            ]

            # profile_beta_a_backscat
            profile_beta_a_backscat = rootgrp.createVariable(
                "profile_beta_a_backscat", "f4", ("altitude",)
            )
            profile_beta_a_backscat.long_name = (
                "Particulate backscatter cross section profile"
            )
            profile_beta_a_backscat.units = "1/(m sr)"
            profile_beta_a_backscat.missing_value = np.nan
            profile_beta_a_backscat.plot_scale = "logarithmic"
            profile_beta_a_backscat[:] = np.ma.array(
                np.array([np.nan, -1.642587044159427e-08]),
                mask=[1, 0],
                fill_value=np.nan,
            )

            # profile_beta_m
            profile_beta_m = rootgrp.createVariable(
                "profile_beta_m", "f4", ("altitude",)
            )
            profile_beta_m.long_name = "Raob molecular scattering cross section profile"
            profile_beta_m.units = "1/meter"
            profile_beta_m.plot_scale = "logarithmic"
            profile_beta_m[:] = [1.3584644e-05, 1.3519524e-05]

            # qc_mask
            qc_mask = rootgrp.createVariable("qc_mask", "i4", ("time", "altitude"))
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
                [65496, 65496],
                [65496, 65496],
                [65496, 65496],
            ]

            # std_beta_a_backscat
            std_beta_a_backscat = rootgrp.createVariable(
                "std_beta_a_backscat", "f4", ("time", "altitude")
            )
            std_beta_a_backscat.long_name = (
                "Std dev of backscat cross section (photon counting)"
            )
            std_beta_a_backscat.units = "1/(m sr)"
            std_beta_a_backscat.missing_value = np.nan
            std_beta_a_backscat.plot_scale = "logarithmic"
            std_beta_a_backscat[:] = [
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
                np.ma.array(np.array([np.nan] * 2), mask=[1] * 2, fill_value=np.nan),
            ]

    print("Closing file...")


if __name__ == "__main__":
    print("Running main...")
    observatory = sys.argv[1]
    instrument = sys.argv[2]
    print(f"Observatory: {observatory} and Instrument: {instrument}")
    main(observatory, instrument)
    print("Done.")
