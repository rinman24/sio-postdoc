"""TODO: Docstring."""

import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

import pytest

from sio_postdoc.manager.observation.service import ObservationManager

Content = tuple[str, ...]


@dataclass
class _TestData:
    raw: Content
    formatted: Content


TEMP_DIRECTORY: Path = Path(
    os.getcwd() + "/tests/manager/observation/integration/temp_files/"
)

SUFFIX: str = ".txt"

TEST_DATA: _TestData = _TestData(
    raw=(
        TEMP_DIRECTORY / "mmcr.20240107.180455.txt",
        TEMP_DIRECTORY / "mmcr.20240229.064020.txt",
    ),
    formatted=(
        TEMP_DIRECTORY / "mmcr.D2024-01-07T18-04-55.txt",
        TEMP_DIRECTORY / "mmcr.D2024-02-29T06-40-20.txt",
    ),
)

YEAR: str = "2024"


@pytest.fixture(scope="module")
def service() -> Generator[ObservationManager, None, None]:
    """Yield a module level service for testing."""
    _service: ObservationManager = ObservationManager()
    # Setup
    try:
        os.mkdir(TEMP_DIRECTORY)
    except FileExistsError:
        pass
    for path in TEST_DATA.raw:
        with open(TEMP_DIRECTORY / path.name, mode="w", encoding="utf-8") as file:
            file.write(f"Original name: {path.name}")
    # Test
    yield _service
    # Teardown
    shutil.rmtree(TEMP_DIRECTORY)


def test_format_directory(service):
    """Test that all files in a directory with a given extention are formatted."""
    service.format_dir(TEMP_DIRECTORY, SUFFIX, YEAR)
    assert (
        service.local_access.list_files(TEMP_DIRECTORY, SUFFIX) == TEST_DATA.formatted
    )
