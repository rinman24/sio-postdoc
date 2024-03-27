"""Test methods in BlobAccess Protocol."""

import os
from pathlib import Path
from typing import Generator

import pytest
from azure.core.exceptions import ResourceNotFoundError
from dotenv import load_dotenv

from sio_postdoc.access.instrument.service import InstrumentAccess

# pylint: disable=redefined-outer-name

CWD: Path = Path(os.getcwd())
EMPTY_CONTAINTER: str = "emptycontainer"
PRE_POPULATED_CONTAINER: str = "prepopulated"
DATA_DIRECTORY: Path = Path(
    os.getcwd() + "/tests/access/instrument/integration/test_blobs/"
)
FILE_NAMES: tuple[str, ...] = (
    "eureka.txt",
    "sheba.txt",
    "utqiagvik.txt",
)
IMAGINARY_CONTAINER: str = "imaginary"


@pytest.fixture(scope="module")
def service() -> Generator[InstrumentAccess, None, None]:
    """Module level service for testing."""
    # Setup
    load_dotenv(override=True)
    _service: InstrumentAccess = InstrumentAccess()
    # Empty container
    _service.create_container(EMPTY_CONTAINTER)
    # Pre populated container
    _service.create_container(PRE_POPULATED_CONTAINER)
    for file_name in FILE_NAMES:
        _service.add_blob(PRE_POPULATED_CONTAINER, DATA_DIRECTORY / file_name)
    # Test
    yield _service
    # Teardown
    for container in _service.blob_service.list_containers():
        _service.blob_service.delete_container(container["name"])


def test_create_non_existing_container(service):
    """Test creation of a container that does not exist."""
    assert service.create_container("notexist") == "Success."


def test_create_existing_container(service):
    """Test creation of a container that exists."""
    assert service.create_container(EMPTY_CONTAINTER) == "Container already exists."


def test_create_invalid_characters_container(service):
    """Test creation of a container with invalid characters."""
    assert (
        service.create_container("Invalid")
        == "Container name contains invalid characters."
    )


def test_list_blobs(service):
    """Test that container contents are listed correctly."""
    assert service.list_blobs(PRE_POPULATED_CONTAINER) == FILE_NAMES


def test_list_blobs_resource_not_found(service):
    """Test that an empty tuple is returned if the container is not found."""
    with pytest.raises(ResourceNotFoundError) as excinfo:
        service.list_blobs(IMAGINARY_CONTAINER)
    assert "Specified container not found: 'imaginary'" in str(excinfo.value)


def test_add_blob(service):
    """Test that files are successfully uploaded to blob storage."""
    service.add_blob(EMPTY_CONTAINTER, DATA_DIRECTORY / FILE_NAMES[0])
    assert service.list_blobs(EMPTY_CONTAINTER) == (FILE_NAMES[0],)


def test_download_blob(service):
    """Test that a blob can be downloaded and saved."""

    before: list[str] = set(CWD.iterdir())
    service.download_blob(PRE_POPULATED_CONTAINER, FILE_NAMES[0])
    after: list[str] = set(CWD.iterdir())
    difference: set = after.difference(before)
    new: Path = next(iter(difference))
    os.remove(new)
    assert new.name == FILE_NAMES[0]
