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

from sio_postdoc.access.instrument.contexts.binary import NcdfContext
from sio_postdoc.access.instrument.contexts.data import DataContext
from sio_postdoc.access.instrument.strategies.data import ShebaDabulRaw
from sio_postdoc.access.instrument.strategies.hardware import DabulHardware
from sio_postdoc.access.instrument.strategies.location import MobileLocationStrategy


class BlobAccess(Protocol):
    """Define protocol for Azure Blob Storage."""

    # pylint: disable=missing-function-docstring
    def create_container(self, name: str) -> str: ...
    def add_blob(self, name: str, path: Path) -> None: ...
    def list_blobs(self, name: str) -> tuple[str, ...]: ...
    def download_blob(self, container: str, name: str) -> None: ...
    def get_datasets(
        self,
        container: str,
        names: tuple[nc.Dataset, ...],  # pylint: disable=no-member
    ) -> None: ...


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

        self._data_context: DataContext = DataContext(ShebaDabulRaw())

        self._ncdf_context: NcdfContext = NcdfContext(
            location=MobileLocationStrategy(),
            instrument=DabulHardware(),
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

    @property
    def data_context(self) -> DataContext:
        """Return instance of `DataContext`."""
        return self._data_context

    @property
    def ncdf_context(self) -> NcdfContext:
        """Return instance of `NcdfContext`."""
        return self._ncdf_context

    def create_container(self, name: str) -> None:
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

    def add_blob(self, name: str, path: Path) -> None:
        """Add a blob to the given container."""
        with self.blob_service.get_container_client(name) as container:
            with open(path, "rb") as data:
                container.upload_blob(name=path.name, data=data)

    def list_blobs(self, name: str) -> tuple[str, ...]:
        """List the contents of the container."""
        blobs: tuple[str, ...]
        try:
            with self.blob_service.get_container_client(name) as container:
                blobs = tuple(
                    sorted([str(blob.name) for blob in container.list_blobs()])
                )
        except ResourceNotFoundError as exc:
            raise ResourceNotFoundError(
                f"Specified container not found: '{name}'"
            ) from exc
        return blobs

    def download_blob(self, container: str, name: str) -> None:
        localname: str = name.split("/")[-1]
        with self.blob_service.get_blob_client(
            container=container, blob=name
        ) as blob_client:
            with open(localname, mode="wb") as blob:
                download_stream = blob_client.download_blob()
                blob.write(download_stream.readall())
