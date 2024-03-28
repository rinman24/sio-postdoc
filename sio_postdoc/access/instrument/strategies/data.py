"""Strategies to construct InstrumentData from netCDF4.Datasets."""

from datetime import datetime
from typing import Protocol

import netCDF4 as nc

import sio_postdoc.utility.service as utility
from sio_postdoc.access.instrument.constants import REFERENCE_TIME
from sio_postdoc.access.instrument.contracts import (
    InstrumentData,
    PhysicalMatrix,
    PhysicalVector,
    TemporalVector,
)

Dataset = nc.Dataset  # pylint: disable=no-member

FLAG: float = float(-999)
SECONDS_PER_DAY: int = 86400
FLAGS: dict[str, int] = {
    "S1": 0,
    "u2": 2**16 - 1,
    "i2": int(-(2**16) / 2),
    "i4": -999,
    "f4": -999,
}


# pylint: disable=protected-access


def _get_notes(name: str) -> str:
    prefix: str = utility.extract_prefix(name)
    suffix: str = utility.extract_suffix(name)
    notes: str = ""
    if prefix and suffix:
        notes = f"{prefix}.{suffix}"
    elif not prefix:
        notes = f"{suffix}"
    elif not suffix:
        notes = f"{prefix}"
    return notes


def _monotonic_times(times: list[float], units: str) -> tuple[int, ...]:
    """TODO: Docstring."""
    # Convert to seconds (potentially non-monotonic)
    scale: int
    match units:
        case "hours":
            scale = 3600
        case "seconds":
            scale = 1
    seconds = [round(i * scale) for i in times]

    # Convert to monotonic seconds
    previous: float = float(FLAG)  # Large negative number
    datum: int = 0  # Initially on same day
    monotonic_seconds: list[float] = []
    for item in seconds:
        if item < previous:
            datum += SECONDS_PER_DAY
        monotonic_seconds.append(int(datum + item))
        previous = item
    return tuple(monotonic_seconds)


def _convert_bytes(value: bytes | float) -> int:
    result: int
    try:
        result = int.from_bytes(value)
    except TypeError:
        result = 0
    return result


class InstrumentDataStrategy(Protocol):
    """Define protocol for constructing InstrumentData."""

    def extract(self, name: str) -> InstrumentData: ...  # noqa: D102


class ShebaDabulRaw(InstrumentDataStrategy):  # pylint: disable=too-few-public-methods
    """TODO: Docstring."""

    @staticmethod
    def _construct_time(name: str, dataset: Dataset) -> TemporalVector:
        initial_datetime: datetime = utility.extract_datetime(name)
        base_time: int = int((initial_datetime - REFERENCE_TIME).total_seconds())
        offsets: list[float] = [float(i) for i in dataset["time"]]
        time: TemporalVector = TemporalVector(
            base_time=base_time,
            offsets=_monotonic_times(offsets, units="hours"),
            units="seconds",
            name="offsets",
            long_name="Seconds Since Initial Time",
            scale=1,
            flag=FLAGS["i4"],
            dtype="i4",
        )
        return time

    @staticmethod
    def _construct_axis(dataset: Dataset) -> TemporalVector:
        # Axis
        axis: PhysicalVector = PhysicalVector(
            values=tuple(int(i) for i in dataset["range"]),
            units="meters",
            name="range",
            long_name="Height of Measured Value; agl",
            scale=1,
            flag=FLAGS["u2"],
            dtype="u2",
        )
        return axis

    @staticmethod
    def _construct_vectors(dataset: Dataset) -> dict[str, PhysicalVector]:
        vectors: dict[str, PhysicalVector] = {}
        variable_names: list[str] = [
            "altitude",
            "azimuth",
            "elevation",
            "elevation",
            "latitude",
            "longitude",
            "scanmode",
        ]
        for variable in variable_names:
            match variable:
                case "altitude":
                    units = "meters"
                    long_name = "Platform Altitude"
                    scale = 1
                    dtype = "i2"
                    valid_range = [-750, 20000]
                    flag = -999
                case "azimuth":
                    units = "degrees"
                    long_name = "Beam Azimuth Angle"
                    scale = 1e5
                    dtype = "i4"
                    valid_range = [0, int(359.99999e5)]
                    flag = 360 * 1e5
                case "elevation":
                    units = "degrees"
                    long_name = "Beam Elevation Angle"
                    scale = 1e5
                    dtype = "i4"
                    valid_range = [0, int(180e5)]
                    flag = 360 * 1e5
                case "latitude":
                    units = "degrees north"
                    long_name = "Platform Latitude"
                    scale = 1e5
                    dtype = "i4"
                    valid_range = [int(-90e5), int(90e5)]
                    flag = 360 * 1e5
                case "longitude":
                    units = "degrees east"
                    long_name = "Platform Longitude"
                    scale = 1e5
                    dtype = "i4"
                    valid_range = [int(-180e5), int(180e5)]
                    flag = 360 * 1e5
                case "scanmode":
                    units = "unitless"
                    long_name = "Scan Mode"
                    scale = 1
                    dtype = "i2"
                    valid_range = [0, 10]
                    flag = -999
            values: tuple[int, ...] = tuple(
                (
                    int(element * scale)
                    if valid_range[0] <= element * scale <= valid_range[1]
                    else flag
                )
                for element in dataset[variable][:]
            )
            vector: PhysicalVector = PhysicalVector(
                values=values,
                units=units,
                name=variable,
                long_name=long_name,
                scale=scale,
                flag=flag,
                dtype=dtype,
            )
            vectors[variable] = vector
        return vectors

    @staticmethod
    def _construct_matrices(dataset: Dataset) -> dict[str, PhysicalMatrix]:
        matrices: dict[str, PhysicalMatrix] = {}
        variable_names: list[str] = [
            "depolarization",
            "far_parallel",
        ]
        for variable in variable_names:
            match variable:
                case "depolarization":
                    units = "unitless"
                    long_name = "Depolarization Ratio"
                    scale = 1000
                    dtype = "i2"
                    valid_range = [0, 1000]
                    flag = -999
                case "far_parallel":
                    units = "unknown"
                    long_name = "Far Parallel Returned Power"
                    scale = 1000
                    dtype = "i4"
                    valid_range = [0, int(2**32 / 2) - 1]
                    flag = -999
            values: list[list[int]] = []
            for row in dataset[variable][:]:
                values.append(
                    tuple(
                        (
                            int(element * scale)
                            if valid_range[0] <= element * scale <= valid_range[1]
                            else flag
                        )
                        for element in row[:]
                    )
                )
            matrix: PhysicalMatrix = PhysicalMatrix(
                values=tuple(values),
                units=units,
                name=variable,
                long_name=long_name,
                scale=scale,
                flag=flag,
                dtype=dtype,
            )
            matrices[variable] = matrix
        return matrices

    def extract(self, name: str) -> InstrumentData:
        """Extract raw SHEBA DABUL data."""
        dataset: Dataset = Dataset(name)
        notes: str = _get_notes(name)
        time: TemporalVector = self._construct_time(name, dataset)
        axis: PhysicalVector = self._construct_axis(dataset)
        vectors: dict[str, PhysicalVector] = self._construct_vectors(dataset)
        matrices: dict[str, PhysicalMatrix] = self._construct_matrices(dataset)
        result: InstrumentData = InstrumentData(
            time=time,
            axis=axis,
            matrices=matrices,
            vectors=vectors,
            name="DABUL",
            observatory="SHEBA",
            notes=notes,
        )
        return result


class ShebaMmcrRaw:  # pylint: disable=too-few-public-methods
    """TODO: Docstring."""

    @staticmethod
    def _construct_time(dataset: Dataset) -> TemporalVector:
        base_time: int = int(dataset["base_time"][0])
        offsets: list[float] = [float(i) for i in dataset["time_offset"]]
        time: TemporalVector = TemporalVector(
            base_time=base_time,
            offsets=_monotonic_times(offsets, units="seconds"),
            units="seconds",
            name="offsets",
            long_name="Seconds Since Initial Time",
            scale=1,
            flag=-999,
            dtype="i4",
        )
        return time

    @staticmethod
    def _construct_axis(dataset: Dataset) -> TemporalVector:
        axis: PhysicalVector = PhysicalVector(
            values=tuple(int(i) for i in dataset["Heights"]),
            units="meters",
            name="range",
            long_name="Height of Measured Value; agl",
            scale=1,
            flag=FLAGS["u2"],
            dtype="u2",
        )
        return axis

    @staticmethod
    def _construct_matrices(dataset: Dataset) -> dict[str, PhysicalMatrix]:
        # TODO: too many statements (break this up, you may need ABC again).
        matrices: dict[str, PhysicalMatrix] = {}
        variable_names: list[str] = [
            "MeanDopplerVelocity",
            "ModeId",
            "Qc",
            "Reflectivity",
            "SignaltoNoiseRatio",
            "SpectralWidth",
        ]
        for variable in variable_names:
            match variable:
                # TODO: What you could do is return a dataclass
                # that holds these things and move all of this to another method
                case "MeanDopplerVelocity":
                    units = "m/s"  # TODO: Change all units to single letters
                    name = "mean_doppler_velocity"
                    long_name = "Mean Doppler Velocity"
                    scale = 1000
                    dtype = "i2"
                    valid_range = [-int(15e3), int(15e3)]
                    flag = -int(2**16 / 2)
                    strategy = int
                case "ModeId":
                    units = "unitless"
                    name = "mode_id"
                    long_name = "Mode I.D. for Merged Time-Height Moments Data"
                    scale = 1
                    dtype = "S1"
                    valid_range = [1, 4]
                    flag = 0
                    strategy = _convert_bytes
                case "Qc":
                    units = "unitless"
                    name = "qc"
                    long_name = "Quality Control Flags"
                    scale = 1
                    dtype = "S1"
                    valid_range = [1, 4]
                    flag = 0
                    strategy = _convert_bytes
                case "Reflectivity":
                    units = "dBZ"
                    name = "reflectivity"
                    long_name = "Reflectivity"
                    scale = 100
                    dtype = "i2"
                    valid_range = [int(-10e3), 0]
                    flag = -int(2**16 / 2)
                    strategy = int
                case "SignaltoNoiseRatio":
                    units = "dB"
                    name = "signal_to_noise"
                    long_name = "Signal-to-Noise Ratio"
                    scale = 100
                    dtype = "i2"
                    valid_range = [-int(10e3), int(10e3)]
                    flag = -int(2**16 / 2)
                    strategy = int
                case "SpectralWidth":
                    units = "m/s"
                    name = "spectral_width"
                    long_name = "Spectral Width"
                    scale = 1000
                    dtype = "i2"
                    valid_range = [0, int(10e3)]
                    flag = -int(2**16 / 2)
                    strategy = int
            values: list[list[int]] = []
            for row in dataset[variable][:]:
                row_values: list[int] = []
                for element in row[:]:
                    value: int = strategy(element)
                    row_values.append(
                        value if valid_range[0] <= value <= valid_range[1] else flag
                    )
                values.append(tuple(row_values))
            matrix: PhysicalMatrix = PhysicalMatrix(
                values=tuple(values),
                units=units,
                name=name,
                long_name=long_name,
                scale=scale,
                flag=flag,
                dtype=dtype,
            )
            matrices[name] = matrix
        return matrices

    def extract(self, name: str) -> InstrumentData:
        """Extract raw SHEBA MMCR data."""
        dataset = Dataset(name)
        notes: str = _get_notes(name)
        time: TemporalVector = self._construct_time(dataset)
        axis: PhysicalVector = self._construct_axis(dataset)
        matrices: list[PhysicalMatrix] = self._construct_matrices(dataset)
        result: InstrumentData = InstrumentData(
            time=time,
            axis=axis,
            matrices=matrices,
            vectors={},  # No Vectors
            name="MMCR",
            observatory="SHEBA",
            notes=notes,
        )
        return result
