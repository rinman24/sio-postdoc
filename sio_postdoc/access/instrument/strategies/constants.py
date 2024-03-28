"""Constants for Instrument Access Strategies."""

from sio_postdoc.access.instrument.strategies.contracts import RawDataParams, ValidRange


def _convert_bytes(value: bytes | float) -> int:
    result: int
    try:
        result = int.from_bytes(value)
    except TypeError:
        result = 0
    return result


ShebaDabulRawVectorParams: dict[str, RawDataParams] = {
    "altitude": RawDataParams(
        units="meters",
        name="altitude",
        long_name="Platform Altitude",
        scale=1,
        dtype="i2",
        valid_range=ValidRange(min=-750, max=20000),
        flag=-999,
        strategy=int,
    ),
    "azimuth": RawDataParams(
        units="degrees",
        name="azimuth",
        long_name="Beam Azimuth Angle",
        scale=1e5,
        dtype="i4",
        valid_range=ValidRange(min=0, max=int(359.99999e5)),
        flag=360 * 1e5,
        strategy=int,
    ),
    "elevation": RawDataParams(
        units="degrees",
        name="elevation",
        long_name="Beam Elevation Angle",
        scale=1e5,
        dtype="i4",
        valid_range=ValidRange(min=0, max=int(180e5)),
        flag=360 * 1e5,
        strategy=int,
    ),
    "latitude": RawDataParams(
        units="degrees north",
        name="latitude",
        long_name="Platform Latitude",
        scale=1e5,
        dtype="i4",
        valid_range=ValidRange(min=int(-90e5), max=int(90e5)),
        flag=360 * 1e5,
        strategy=int,
    ),
    "longitude": RawDataParams(
        units="degrees east",
        name="longitude",
        long_name="Platform Longitude",
        scale=1e5,
        dtype="i4",
        valid_range=ValidRange(min=int(-180e5), max=int(180e5)),
        flag=360 * 1e5,
        strategy=int,
    ),
    "scanmode": RawDataParams(
        units="unitless",
        name="scanmode",
        long_name="Scan Mode",
        scale=1,
        dtype="i2",
        valid_range=ValidRange(min=0, max=10),
        flag=-999,
        strategy=int,
    ),
}

ShebaDabulRawMatrixParams: dict[str, RawDataParams] = {
    "depolarization": RawDataParams(
        units="unitless",
        name="depolarization",
        long_name="Depolarization Ratio",
        scale=1000,
        dtype="i2",
        valid_range=ValidRange(min=0, max=1000),
        flag=-999,
        strategy=int,
    ),
    "far_parallel": RawDataParams(
        units="unknown",
        name="far_parallel",
        long_name="Far Parallel Returned Power",
        scale=1000,
        dtype="i4",
        valid_range=ValidRange(min=0, max=int(2**32 / 2) - 1),
        flag=-999,
        strategy=int,
    ),
}

ShebaMmcrRawMatrixParams: dict[str, RawDataParams] = {
    "MeanDopplerVelocity": RawDataParams(
        units="m/s",
        name="mean_doppler_velocity",
        long_name="Mean Doppler Velocity",
        scale=1000,
        dtype="i2",
        valid_range=ValidRange(min=-int(15e3), max=int(15e3)),
        flag=-int(2**16 / 2),
        strategy=int,
    ),
    "ModeId": RawDataParams(
        units="unitless",
        name="mode_id",
        long_name="Mode I.D. for Merged Time-Height Moments Data",
        scale=1,
        dtype="S1",
        valid_range=ValidRange(min=1, max=4),
        flag=0,
        strategy=_convert_bytes,
    ),
    "Qc": RawDataParams(
        units="unitless",
        name="qc",
        long_name="Quality Control Flags",
        scale=1,
        dtype="S1",
        valid_range=ValidRange(min=1, max=4),
        flag=0,
        strategy=_convert_bytes,
    ),
    "Reflectivity": RawDataParams(
        units="dBZ",
        name="reflectivity",
        long_name="Reflectivity",
        scale=100,
        dtype="i2",
        valid_range=ValidRange(min=int(-10e3), max=0),
        flag=-int(2**16 / 2),
        strategy=int,
    ),
    "SignaltoNoiseRatio": RawDataParams(
        units="dB",
        name="signal_to_noise",
        long_name="Signal-to-Noise Ratio",
        scale=100,
        dtype="i2",
        valid_range=ValidRange(min=-int(10e3), max=int(10e3)),
        flag=-int(2**16 / 2),
        strategy=int,
    ),
    "SpectralWidth": RawDataParams(
        units="m/s",
        name="spectral_width",
        long_name="Spectral Width",
        scale=1000,
        dtype="i2",
        valid_range=ValidRange(min=0, max=int(10e3)),
        flag=-int(2**16 / 2),
        strategy=int,
    ),
}
