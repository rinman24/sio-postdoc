"""Test that access can rename local files."""

import os
import shutil
from pathlib import Path

import pytest

from sio_postdoc.access._local.service import LocalAccess

FILE_NAMES: tuple[str, ...] = ("mmcr.txt", "dabul.txt")
TEMP_DIRECTORY: Path = Path(
    os.getcwd() + "/tests/access/_local/integration/temp_files/"
)


@pytest.fixture(scope="module")
def service():
    """Module level instance of LocalAccess."""
    _service: LocalAccess = LocalAccess()
    # Setup
    try:
        os.mkdir(TEMP_DIRECTORY)
    except FileExistsError:
        pass
    for name in FILE_NAMES:
        with open(TEMP_DIRECTORY / f"{name}", mode="w", encoding="utf-8") as file:
            file.write(f"Original name: {name}")
    # Test
    yield _service
    # Cleanup
    shutil.rmtree(TEMP_DIRECTORY)


def test_rename_files(service):
    """Test that files are renamed correctly."""
    current: tuple[Path, ...] = service.list_files(TEMP_DIRECTORY, ".txt")
    new: tuple[Path, ...] = tuple(
        name.parent / f"{name.stem.upper()}{name.suffix}" for name in current
    )
    service.rename_files(current, new)
    assert service.list_files(TEMP_DIRECTORY, ".txt") == new
