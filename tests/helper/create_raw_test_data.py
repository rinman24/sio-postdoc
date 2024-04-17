"""Create test files."""

import sys

import netCDF4 as nc

from tests.helper.builder.raw.constants import FILENAMES
from tests.helper.builder.raw.context import RawDataContext
from tests.helper.builder.raw.types import Instrument, Observatory

Dataset = nc.Dataset


def _get_observatory(observatory: str) -> Observatory:
    match observatory:
        case "sheba":
            return Observatory.SHEBA
        case "eureka":
            return Observatory.EUREKA
        case "utqiagvik":
            return Observatory.UTQIAGVIK
        case _:
            return observatory


def _get_instrument(instrument: str) -> Instrument:
    match instrument:
        case "ahsrl":
            return Instrument.AHSRL
        case "dabul":
            return Instrument.DABUL
        case "mmcr":
            return Instrument.MMCR
        case "mpl":
            return Instrument.MPL
        case _:
            return instrument


def main(observatory_name, instrument_name):  # noqa: PLR0915
    """Create test netCDF files."""
    observatory: Observatory = _get_observatory(observatory_name)
    instrument: Instrument = _get_instrument(instrument_name)

    try:
        filename: str = FILENAMES[observatory][instrument]
    except KeyError:
        return f"Invalid combination of observatory and instrument: {observatory_name} {instrument_name}"

    print(f"Creating: {filename}")

    context: RawDataContext = RawDataContext(observatory, instrument)
    context.hydrate()
    print("Done")


if __name__ == "__main__":
    observatory: str = sys.argv[1]
    instrument: str = sys.argv[2]
    main(observatory, instrument)
