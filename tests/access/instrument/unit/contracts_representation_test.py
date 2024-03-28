"""Test repr of instrument access contracts."""

from datetime import datetime

from sio_postdoc.access.instrument.constants import REFERENCE_TIME
from sio_postdoc.access.instrument.contracts import (
    InstrumentData,
    PhysicalMatrix,
    PhysicalVector,
    TemporalVector,
)

CURRENT: datetime = datetime.now()
BASE_TIME: int = int((CURRENT - REFERENCE_TIME).total_seconds())

TIME: TemporalVector = TemporalVector(
    base_time=BASE_TIME,
    initial=CURRENT,
    offsets=(10, 20, 30),
    units="seconds",
    name="time",
    long_name="seconds since initial time",
    scale=1,
    flag=-999,
    dtype="f4",
)

AXIS: PhysicalVector = PhysicalVector(
    values=(45, 90),
    units="meters",
    name="range",
    long_name="vertical range of data",
    scale=1,
    flag=(2**16 - 1),
    dtype="u2",
)

PHYSICAL_VECTORS: dict[str, PhysicalVector] = {
    "latitude": PhysicalVector(
        values=(3288000, 3288100, 3288120),
        units="degrees",
        name="latitude",
        long_name="platform latitude",
        scale=int(1e5),
        flag=int(360 * 1e5),
        dtype="i4",
    ),
    "longitude": PhysicalVector(
        values=(11723000, 11723400, 11723440),
        units="degrees",
        name="longitude",
        long_name="platform longitude",
        scale=int(1e5),
        flag=int(360 * 1e5),
        dtype="i4",
    ),
}

PHYSICAL_MATRICES: dict[str, PhysicalMatrix] = {
    "reflectivity": PhysicalMatrix(
        values=((-9, -24), (-1, -7), (-3, -20)),
        units="dBZ",
        name="reflectivity",
        long_name="reflectivity",
        scale=1,
        flag=-999,
        dtype="f4",
    ),
    "far_parallel": PhysicalMatrix(
        values=((24, 84), (7, 89), (3, 87)),
        units="unknown",
        name="far_parallel",
        long_name="far parallel",
        scale=1,
        flag=-999,
        dtype="f4",
    ),
}

INSTRUMENT_DATA: InstrumentData = InstrumentData(
    time=TIME,
    axis=AXIS,
    matrices=PHYSICAL_MATRICES,
    vectors=PHYSICAL_VECTORS,
    name="test_name",
    observatory="test_observatory",
    notes="test notes",
)

# pylint: disable=missing-function-docstring


def test_temporal_vector_repr():  # noqa: D103
    expected: tuple[str, ...] = (
        "<class 'sio_postdoc.access.instrument.contracts.TemporalVector'>",
        "    dimensions(sizes): (3,)",
        "    units: seconds",
        "    name: time",
        "    base_time: ",
        "    initial: ",
    )
    result: str = repr(TIME)
    for substring in expected:
        assert substring in result


def test_physical_vector_repr():  # noqa: D103
    expected: tuple[str, ...] = (
        "<class 'sio_postdoc.access.instrument.contracts.PhysicalVector'>",
        "    dimensions(sizes): (3,)",
        "    units: degrees",
        "    name: latitude",
        "    name: longitude",
    )
    result: str = repr(PHYSICAL_VECTORS)
    for substring in expected:
        assert substring in result


def test_physical_matrix_repr():  # noqa: D103
    expected: tuple[str, ...] = (
        "<class 'sio_postdoc.access.instrument.contracts.PhysicalMatrix'>",
        "    dimensions(sizes): (3, 2)",
        "    units: dBZ",
        "    units: unknown",
        "    name: reflectivity",
        "    name: far_parallel",
    )
    result: str = repr(PHYSICAL_MATRICES)
    for substring in expected:
        assert substring in result


def test_instrument_data_repr():  # noqa: D103
    expected: tuple[str, ...] = (
        "<class 'sio_postdoc.access.instrument.contracts.InstrumentData'>",
        "    instrument name: test_name",
        "    observatory name: test_observatory",
        "    notes: test notes",
        "    initial time: ",
        "    dimensions(sizes): time(3), range(2)",
        "    vectors(dimensions): latitude(time), longitude(time)",
        "    matrices(dimensions): reflectivity(time, range), far_parallel(time, range)",
    )
    result: str = repr(INSTRUMENT_DATA)
    for substring in expected:
        assert substring in result
