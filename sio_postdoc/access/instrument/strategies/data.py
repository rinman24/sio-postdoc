"""Strategies to construct InstrumentData from netCDF4.Datasets."""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Callable

import netCDF4 as nc

import sio_postdoc.utility.service as utility
from sio_postdoc.access.instrument.contracts import (
    InstrumentData,
    PhysicalMatrix,
    PhysicalVector,
    TemporalVector,
)

REF_DATE: datetime = datetime(1970, 1, 1, 0, 0)
FLAG: float = float(-999)
SECONDS_PER_DAY: int = 86400
FLAGS: dict[str, int] = {
    "S1": 0,
    "u2": 2**16 - 1,
    "i2": int(-(2**16) / 2),
    "i4": -999,
    "f4": -999,
}
METHODS: dict[str, Callable] = {
    "S1": int.from_bytes,
    "i2": int,
    "i4": int,
    "f4": float,
}


class AbstractDataStrategy(ABC):
    """TODO: docstring."""

    @abstractmethod
    def extract(  # pylint: disable=missing-function-docstring
        self,
        name: str,
    ) -> InstrumentData: ...

    @staticmethod
    def monotonic_times(times: list[float], units: str) -> tuple[int, ...]:
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

    @staticmethod
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


class Default(AbstractDataStrategy):
    """TODO: Docstring."""

    def extract(
        self,
        name: str,
    ) -> InstrumentData: ...


class ShebaDabulRaw(AbstractDataStrategy):
    """TODO: Docstring."""

    variable_names: tuple[str] = (
        "altitude",
        "azimuth",
        "elevation",
        "latitude",
        "longitude",
        "scanmode",
    )
    matrix_names: tuple[str] = (
        "depolarization",
        "far_parallel",
    )

    def extract(self, name: str) -> InstrumentData:
        """TODO: Docstring."""
        units: str
        long_name: str
        scale: int
        flag: int
        dtype: str
        valid_range: list[int]
        # Open the nc file
        dataset = nc.Dataset(name)  # pylint: disable=no-member
        # Extract initial timestamp and notes for the filename.
        initial_datetime: datetime = utility.extract_datetime(name)
        notes: str = self._get_notes(name)
        # Construct the Temporal Vector
        offsets: list[float] = [float(i) for i in dataset["time"]]
        time: TemporalVector = TemporalVector(
            initial=initial_datetime,
            offsets=self.monotonic_times(offsets, units="hours"),
            units="seconds",
            name="offsets",
            long_name="seconds since initial time",
            scale=1,
            flag=FLAGS["i4"],
            dtype="i4",
        )
        axis: PhysicalVector = PhysicalVector(
            values=tuple(int(i) for i in dataset["range"]),
            units="meters",
            name="range",
            long_name="vertical range of measurement",
            scale=1,
            flag=FLAGS["u2"],
            dtype="u2",
        )
        # Vectors
        vectors: dict[str, PhysicalVector] = {}
        for variable in self.variable_names:
            match variable:
                case "altitude":
                    units = "meters"
                    long_name = "platform altitude"
                    scale = 1
                    dtype = "i2"
                    valid_range = [-750, 20000]
                    flag = -999
                case "azimuth":
                    units = "degrees"
                    long_name = "beam azimuth angle"
                    scale = 1e5
                    dtype = "i4"
                    valid_range = [0, int(359.99999e5)]
                    flag = 360 * 1e5
                case "elevation":
                    units = "degrees"
                    long_name = "beam elevation angle"
                    scale = 1e5
                    dtype = "i4"
                    valid_range = [0, int(180e5)]
                    flag = 360 * 1e5
                case "latitude":
                    units = "degrees north"
                    long_name = "platform latitude"
                    scale = 1e5
                    dtype = "i4"
                    valid_range = [int(-90e5), int(90e5)]
                    flag = 360 * 1e5
                case "longitude":
                    units = "degrees east"
                    long_name = "platform longitude"
                    scale = 1e5
                    dtype = "i4"
                    valid_range = [int(-180e5), int(180e5)]
                    flag = 360 * 1e5
                case "scanmode":
                    units = "unitless"
                    long_name = "scan mode"
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

        matrices: dict[str, PhysicalMatrix] = {}
        for variable in self.matrix_names:
            match variable:
                case "depolarization":
                    units = "unitless"
                    long_name = "depolarization ratio"
                    scale = 1000
                    dtype = "i2"
                    valid_range = [0, 1000]
                    flag = -999
                case "far_parallel":
                    units = "unknown"
                    long_name = "far parallel reflected power"
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


class ShebaMmcrRaw(AbstractDataStrategy):
    """TODO: Docstring."""

    matrix_names: tuple[str] = (
        "Qc",
        "Reflectivity",
        "MeanDopplerVelocity",
        "SpectralWidth",
        "ModeId",
        "SignaltoNoiseRatio",
    )
    matrix_map: dict[str, str] = dict(
        Qc="qc",
        Reflectivity="reflectivity",
        MeanDopplerVelocity="mean_doppler_velocity",
        SpectralWidth="spectral_width",
        ModeId="mode_id",
        SignaltoNoiseRatio="signal_to_noise_ratio",
    )

    def extract(self, name: str) -> InstrumentData:
        # Open the nc file
        dataset = nc.Dataset(name)  # pylint: disable=no-member
        # Extract initial timestamp and notes for the filename.
        base_time: int = int(dataset["base_time"][0])
        initial_datetime: datetime = REF_DATE + timedelta(seconds=base_time)
        notes: str = self._get_notes(name)
        # Construct the Temporal Vector
        offsets: list[float] = [float(i) for i in dataset["time_offset"]]
        time: TemporalVector = TemporalVector(
            initial=initial_datetime,
            offsets=self.monotonic_times(offsets, units="seconds"),
            units="seconds",
            name="seconds since initial time",
            scale=1,
            flag=FLAGS["i2"],
            dtype="i2",
        )
        axis: PhysicalVector = PhysicalVector(
            values=tuple(int(i) for i in dataset["Heights"]),
            units="meters",
            name="range",
            # long_name="Height of Measured Value; agl"
            scale=1,
            flag=FLAGS["i2"],
            dtype="i2",
        )
        # Vectors
        # Matrices
        matrices: list[PhysicalMatrix] = []
        for variable in self.matrix_names:
            scale: int
            units: str
            dtype: str
            scale: int
            match variable:
                case "Qc":
                    units = "none"
                    # notes = (
                    #     "Quality Control Flags: 0 - No Data, "
                    #     "1 - Good Data, "
                    #     "2 - Second Trip Echo Problems, "
                    #     "3 - Coherent Integration Problems, "
                    #     "4 - Second Trip Echo and Coherent Integration Problems"
                    # )
                    dtype = "S1"
                    scale = 1
                case "Reflectivity":
                    units = "dBZ"
                    dtype = "i2"
                    scale = 100
                case "MeanDopplerVelocity":
                    units = "m/s"
                    dtype = "i2"
                    scale = 1000
                case "SpectralWidth":
                    units = "m/s"
                    dtype = "i2"
                    scale = 1000
                case "ModeId":
                    units = "none"
                    dtype = "S1"
                    scale = 1
                case "SignaltoNoiseRatio":
                    units = "dB"
                    dtype = "i2"
                    scale = 100

            values: list[list[int | float]] = []
            for row in dataset[variable]:
                values.append(tuple(METHODS[dtype](i) for i in row))

            matrix: PhysicalMatrix = PhysicalMatrix(
                values=tuple(values),
                units=units,
                name=self.matrix_map[variable],
                scale=scale,
                flag=FLAGS[dtype],
                dtype=dtype,
            )
            matrices.append(matrix)

        result: InstrumentData = InstrumentData(
            time=time,
            axis=(axis,),
            matrices=tuple(matrices),
            vectors=tuple(),  # No Vectors
            name="MMCR",
            observatory="SHEBA",
            notes=notes,
        )

        return result


class DabulData(AbstractDataStrategy):
    """TODO: Docstring."""

    def extract(self, name: str) -> InstrumentData:
        """TODO: Docstring."""
        dataset = nc.Dataset(name)  # pylint: disable=no-member
        initial_datetime: datetime = utility.extract_datetime(name)
        prefix: str = utility.extract_prefix(name)
        suffix: str = utility.extract_suffix(name)
        notes: str = ""
        if prefix and suffix:
            notes = f"{prefix}.{suffix}"
        elif not prefix:
            notes = f"{suffix}"
        elif not suffix:
            notes = f"{prefix}"
        offsets: list[float] = [float(i) for i in dataset["offsets"]]
        # seconds: tuple[int, ...] = self.monotonic_times(offsets, units="hours")
        time: TemporalVector = TemporalVector(
            initial=initial_datetime,
            offsets=offsets,
            units="seconds",
            name="seconds since initial time",
            scale=1,
            flag=-999,
            dtype="TODO",
        )
        axis: PhysicalVector = PhysicalVector(
            values=tuple(float(i) for i in dataset["range"]),
            units="meters",
            name="range",
            scale=1,
            flag=-999,
            dtype="TODO",
        )
        vectors: list[PhysicalVector] = []
        for variable in (
            # "latitude",
            # "longitude",
            # "altitude",
            # "elevation",
            # "azimuth",
            # "scanmode",
        ):
            name: str = variable
            value_type: type = float
            flag: int = -999
            scale: int = 1
            match variable:
                case "latitude":
                    units = "degrees north"
                case "longitude":
                    units = "degrees east"
                case "altitude":
                    units = "meters"
                case "elevation":
                    units = "degrees"
                    name = "beam elevation angle"
                case "azimuth":
                    units = "degrees"
                    name = "beam azimuth angle"
                case "scanmode":
                    units = "none"
                    name = "scan mode"
                    value_type = int
            values: tuple[int | float, ...] = tuple(
                value_type(i) for i in dataset[variable]
            )
            vector: PhysicalVector = PhysicalVector(
                values=values,
                units=units,
                name=name,
                scale=scale,
                flag=flag,
                dtype="TODO",
            )
            vectors.append(vector)

        matrices: list[PhysicalMatrix] = []
        for variable in ("depolarization", "far_parallel"):
            name: str = variable
            values: list[list[float]] = []
            for row in dataset[variable]:
                values.append(tuple(float(i) for i in row))
            flag: int = -999
            scale: int = 1
            match variable:
                case "depolarization":
                    name = "depolarization"
                    units = "none"
                case "far_parallel":
                    name = "far_parallel"
                    units = "unknown"
            matrix: PhysicalMatrix = PhysicalMatrix(
                values=tuple(values),
                units=units,
                name=name,
                scale=scale,
                flag=flag,
                dtype="TODO",
            )
            matrices.append(matrix)

        result: InstrumentData = InstrumentData(
            time=time,
            axis=(axis,),
            matrices=tuple(matrices),
            vectors=tuple(vectors),
            name="dabul",
            observatory="SHEBA",
            notes=notes,
        )

        return result
