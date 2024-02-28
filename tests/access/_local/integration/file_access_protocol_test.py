"""Test methods in FileAccess Protocol."""

import os
from pathlib import Path

import pytest

from sio_postdoc.access._local.service import LocalAccess

# pylint: disable=redefined-outer-name

DATA_DIRECTORY: Path = Path(
    os.getcwd() + "/tests/access/_local/integration/test_files/"
)


FILES: dict[str, tuple[Path, ...]] = {
    ".txt": (
        DATA_DIRECTORY / "body.txt",
        DATA_DIRECTORY / "conclusion.txt",
        DATA_DIRECTORY / "intro.txt",
    ),
    ".csv": (
        DATA_DIRECTORY / "left.csv",
        DATA_DIRECTORY / "right.csv",
    ),
    ".invalid": (),
}


@pytest.fixture(scope="module")
def service() -> LocalAccess:
    """Module level service for testing."""
    return LocalAccess()


@pytest.mark.parametrize("extension", list(FILES.keys()))
def test_list_files(service, extension):
    """Ensure `list_files` returns correct files."""
    assert service.list_files(DATA_DIRECTORY, extension) == FILES[extension]


def test_no_period_in_extention(service):
    """Ensure extension includes a period."""
    no_period: str = "txt"
    with pytest.raises(ValueError) as excinfo:
        service.list_files(DATA_DIRECTORY, no_period)
    assert f"Extension does not start with a period: '{no_period}'" in str(
        excinfo.value
    )


def test_not_a_directory(service):
    """Ensure directory is a directory."""
    file_path: Path = FILES[".txt"][0]
    with pytest.raises(NotADirectoryError) as excinfo:
        service.list_files(file_path, ".txt")
    assert f"Not a directory: '{file_path}'" in str(excinfo)
