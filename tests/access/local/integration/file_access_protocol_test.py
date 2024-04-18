"""Test methods in FileAccess Protocol."""

import os
from pathlib import Path
from typing import Generator

import pytest

from sio_postdoc.access import DataSet
from sio_postdoc.access.local.service import LocalAccess

DIRECTORY: Path = Path(os.getcwd() + "/tests/access/local/integration/test_files/")

FILES: dict[str, tuple[Path, ...]] = {
    ".txt": (
        DIRECTORY / "body.txt",
        DIRECTORY / "conclusion.txt",
        DIRECTORY / "intro.txt",
    ),
    ".csv": (
        DIRECTORY / "left.csv",
        DIRECTORY / "right.csv",
    ),
    ".invalid": (),
}

DATASET: str = "sheba_mmcr.nc"


@pytest.fixture(scope="module")
def service() -> LocalAccess:
    """Return a module level instance of `LocalAccess` for testing."""
    return LocalAccess()


@pytest.fixture(scope="module")
def dataset(service) -> Generator[DataSet, None, None]:
    """Return a module level instance of `DataSet` for testing."""
    _dataset: DataSet = service.open_dataset(DIRECTORY, DATASET)
    yield _dataset
    _dataset.close()


@pytest.mark.parametrize("extension", list(FILES.keys()))
def test_list_files(service, extension):
    """Ensure `list_files` returns correct files."""
    assert service.list_files(DIRECTORY, extension) == FILES[extension]


def test_no_period_in_extention(service):
    """Ensure extension includes a period."""
    no_period: str = "txt"
    with pytest.raises(ValueError) as excinfo:
        service.list_files(DIRECTORY, no_period)
    assert f"Extension does not start with a period: '{no_period}'" in str(
        excinfo.value
    )


def test_not_a_directory(service):
    """Ensure directory is a directory."""
    file_path: Path = FILES[".txt"][0]
    with pytest.raises(NotADirectoryError) as excinfo:
        service.list_files(file_path, ".txt")
    assert f"Not a directory: '{file_path}'" in str(excinfo)


def test_file_not_found(service):
    """Ensure exception is raised if file was not found."""
    file_path: Path = Path("imaginary-file.txt")
    with pytest.raises(FileNotFoundError) as excinfo:
        service.list_files(file_path, ".txt")
    assert f"No such file or directory: '{file_path}'" in str(excinfo)


def test_open_dataset(dataset):
    """Ensure that `open_dataset` returns a `DataSet`."""
    assert isinstance(dataset, DataSet)


def test_dataset_not_found(service):
    """Ensure exception is raised if dataset not found."""
    with pytest.raises(FileNotFoundError) as excinfo:
        service.open_dataset(DIRECTORY, name="imaginary.nc")
    assert "No such file or directory: " in str(excinfo)


def test_wrong_dataset_type(service):
    """Ensure exception is raised if filename is not a valid format."""
    with pytest.raises(FileNotFoundError) as excinfo:
        service.open_dataset(Path(), name="")
    assert "'' not a valid format for DataSet" in str(excinfo)
