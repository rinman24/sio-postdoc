"""Create test files."""

import sys

from netCDF4 import Dataset

filename: str = "raw.D2024-01-07T06-00-00.sheba_mmcr_example.nc"


def main(observatory, instrument):
    """Create test netCDF files."""
    print("Creating NCDF file...")

    if observatory not in ["sheba"]:
        print("invalid observatory...")
        return False
    if instrument not in ["dabul", "mmcr"]:
        print("invalid instrument...")
        return False

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
            record = rootgrp.createDimension("record", 6)
            level = rootgrp.createDimension("level", 3)
            filename_size = rootgrp.createDimension("filename_size", len(filename))
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
            base_time = rootgrp.createVariable("base_tiime", "i4")
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
            units: "dBZ (X100)"

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
    print("Closing file...")


if __name__ == "__main__":
    print("Running main...")
    observatory = sys.argv[1]
    instrument = sys.argv[2]
    print(f"Observatory: {observatory} and Instrument: {instrument}")
    main(observatory, instrument)
    print("Done.")
