"""Test methods in BlobAccess Protocol."""

import os
from pathlib import Path
from typing import Generator

import pytest
from dotenv import load_dotenv

from sio_postdoc.access.instrument.service import InstrumentAccess

# pylint: disable=redefined-outer-name

EMPTY_CONTAINTER: str = "emptycontainer"
PRE_POPULATED_CONTAINER: str = "prepopulated"
DATA_DIRECTORY: Path = Path(
    os.getcwd() + "/tests/access/instrument/integration/test_blobs/"
)
FILE_NAMES: tuple[Path, ...] = (
    "eureka.txt",
    "sheba.txt",
    "utqiagvik.txt",
)


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
    print(f"This is the Connection String: {service.connection_string}")
    assert service.create_container("notexist") == "Success."


@pytest.mark.skip(reason="Need to set up Azurite or equivalent in CI/CD build.")
def test_create_existing_container(service):
    """Test creation of a container that exists."""
    assert service.create_container(EMPTY_CONTAINTER) == "Container already exists."


@pytest.mark.skip(reason="Need to set up Azurite or equivalent in CI/CD build.")
def test_create_invalid_characters_container(service):
    """Test creation of a container with invalid characters."""
    assert (
        service.create_container("Invalid")
        == "Container name contains invalid characters."
    )


@pytest.mark.skip(reason="Need to set up Azurite or equivalent in CI/CD build.")
def test_list_blobs(service):
    """Test that container contents are listed correctly."""
    assert service.list_blobs(PRE_POPULATED_CONTAINER) == FILE_NAMES


@pytest.mark.skip(reason="Need to set up Azurite or equivalent in CI/CD build.")
def test_add_blob(service):
    """Test that files are successfully uploaded to blob storage."""
    service.add_blob(EMPTY_CONTAINTER, DATA_DIRECTORY / FILE_NAMES[0])
    assert service.list_blobs(EMPTY_CONTAINTER) == (FILE_NAMES[0],)
