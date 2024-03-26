"""Test repr of instrument access contracts."""

from datetime import datetime

from sio_postdoc.access.instrument.contracts import (
    InstrumentData,
    PhysicalMatrix,
    PhysicalVector,
    TemporalVector,
)

# pylint: disable=missing-function-docstring

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


def test_instrument_data_repr():
    # Arrange
    data = InstrumentData(
        time=TIME,
        axis=AXIS,
        matrices=PHYSICAL_MATRICES,
        vectors=PHYSICAL_VECTORS,
        name="test_name",
        observatory="test_observatory",
        notes="test notes",
    )
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
    # Act
    result: str = data.__repr__()
    # Assert
    for substring in expected:
        assert substring in result


def test_instrument_data_str():
    # Arrange
    data = InstrumentData(
        time=TIME,
        axis=AXIS,
        matrices=PHYSICAL_MATRICES,
        vectors=PHYSICAL_VECTORS,
        name="test_name",
        observatory="test_observatory",
        notes="test notes",
    )
    expected: tuple[str, ...] = (
        "<class 'sio_postdoc.access.instrument.contracts.InstrumentData'>",
        "    Data for 'test_name' located at 'test_observatory'",
        "    Initial time: ",
    )
    # Act
    result: str = data.__str__()
    # Assert
    for substring in expected:
        assert substring in result
