"""Instrument Access Service."""

import dataclasses
import os
from pathlib import Path
from typing import Protocol

import netCDF4 as nc
from azure.core.exceptions import (
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
)
from azure.storage.blob import BlobServiceClient


class BlobAccess(Protocol):
    """Define protocol for Azure Blob Storage."""

    # pylint: disable=missing-function-docstring
    def create_container(self, name: str) -> str: ...
    def add_blob(self, name: str, path: Path, directory: str = "") -> None: ...
    def list_blobs(
        self, container: str, name_starts_with: str | None = None
    ) -> tuple[str, ...]: ...
    def download_blob(self, container: str, name: str) -> str: ...


@dataclasses.dataclass
class Account:
    """Azure Account Details."""

    name: str
    key: str


@dataclasses.dataclass
class Endpoint:
    """Azure Endpoint Details."""

    protocol: str
    blob: str


class InstrumentAccess(BlobAccess):
    """Concrete implementation of Blob Access."""

    def __init__(self) -> None:
        """Initialize `InstrumentAccess`."""
        self._account: Account = Account(
            name=os.environ["STORAGE_ACCOUNT_NAME"],
            key=os.environ["STORAGE_ACCOUNT_KEY"],
        )
        self._endpoint: Endpoint = Endpoint(
            protocol=os.environ["DEFAULT_ENDPOINTS_PROTOCOL"],
            blob=os.environ["BLOB_STORAGE_ENDPOINT"],
        )

        self._blob_service: BlobServiceClient = (
            BlobServiceClient.from_connection_string(conn_str=self.connection_string)
        )

    @property
    def connection_string(self) -> str:
        """Return the Connection String."""
        return (
            f"DefaultEndpointsProtocol={self._endpoint.protocol};"
            + f"AccountName={self._account.name};"
            + f"AccountKey={self._account.key};"
            + f"BlobEndpoint={self._endpoint.blob};"
        )

    @property
    def blob_service(self) -> BlobServiceClient:
        """Return instance of Azure BlobServiceClient."""
        return self._blob_service

    def create_container(self, name: str) -> str:
        """Create a new blob container."""
        message: str = "Success."
        try:
            with self.blob_service.get_container_client(name) as container_client:
                container_client.create_container()
        except ResourceExistsError:
            message = "Container already exists."
        except HttpResponseError:
            message = "Container name contains invalid characters."
        return message

    def add_blob(self, name: str, path: Path, directory: str = "") -> None:
        """Add a blob to the given container."""
        remote_name: str = directory + path.name
        with self.blob_service.get_container_client(name) as container:
            with open(path, "rb") as data:
                container.upload_blob(name=remote_name, data=data)

    def list_blobs(
        self, container: str, name_starts_with: str | None = None
    ) -> tuple[str, ...]:
        """List the contents of the container."""
        blobs: tuple[str, ...]
        try:
            with self.blob_service.get_container_client(container) as container:
                blobs = tuple(
                    sorted(
                        [
                            str(blob.name)
                            for blob in container.list_blobs(name_starts_with)
                        ]
                    )
                )
        except ResourceNotFoundError as exc:
            raise ResourceNotFoundError(
                f"Specified container not found: '{container}'"
            ) from exc
        return blobs

    def download_blob(self, container: str, name: str) -> str:
        """Download the blob with a given name from the container."""
        localname: str = name.split("/")[-1]
        with self.blob_service.get_blob_client(
            container=container, blob=name
        ) as blob_client:
            with open(localname, mode="wb") as blob:
                download_stream = blob_client.download_blob()
                blob.write(download_stream.readall())
        return localname
