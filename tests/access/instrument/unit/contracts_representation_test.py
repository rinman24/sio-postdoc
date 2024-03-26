"""Test repr of instrument access contracts."""

from datetime import datetime

from sio_postdoc.access.instrument.contracts import (
    InstrumentData,
    PhysicalMatrix,
    PhysicalVector,
    TemporalVector,
)

TIME: TemporalVector = TemporalVector(
    initial=datetime.now(),
    offsets=(10, 20, 30),
    units="seconds",
    name="time",
    scale=1,
    flag=-999,
    dtype="f4",
)

AXIS: tuple[PhysicalVector, ...] = (
    PhysicalVector(
        values=(45, 90),
        units="meters",
        name="range",
        scale=1,
        flag=-999,
        dtype="f4",
    ),
)

PHYSICAL_VECTORS: tuple[PhysicalVector, ...] = (
    PhysicalVector(
        values=(32.88, 32.881, 32.8812),
        units="degrees",
        name="latitude",
        scale=1,
        flag=-999,
        dtype="f4",
    ),
    PhysicalVector(
        values=(117.23, 117.234, 117.2344),
        units="degrees",
        name="longitude",
        scale=1,
        flag=-999,
        dtype="f4",
    ),
)

PHYSICAL_MATRICES: tuple[PhysicalMatrix, ...] = (
    PhysicalMatrix(
        values=((-9, -24), (-1, -7), (-3, -20)),
        units="dBZ",
        name="reflectivity",
        scale=1,
        flag=-999,
        dtype="f4",
    ),
    PhysicalMatrix(
        values=((24, 84), (7, 89), (3, 87)),
        units="unknown",
        name="far_parallel",
        scale=1,
        flag=-999,
        dtype="f4",
    ),
)

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


def test_physical_vector_repr():
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


def test_physical_matrix_repr():
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


def test_instrument_data_repr():
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
