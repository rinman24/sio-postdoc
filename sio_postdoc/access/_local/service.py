"""Local Access Service."""

from pathlib import Path
from typing import Protocol


class DiskAccess(Protocol):
    """Define protocol for Local Disk Access."""

    # pylint: disable=missing-function-docstring
    def list_files(self, directory: Path, extension: str) -> tuple[Path, ...]: ...
    def rename_files(self, directory: Path) -> None: ...


class LocalAccess(DiskAccess):
    """Concrete implementation of Disk Access."""

    def list_files(self, directory: Path, extension: str) -> tuple[Path, ...]:
        """List all the files in the directory with the given extension."""
        if not extension.startswith("."):
            raise ValueError(f"Extension does not start with a period: '{extension}'")
        try:
            return tuple(
                sorted(
                    [path for path in directory.iterdir() if path.suffix == extension]
                )
            )
        except NotADirectoryError as exc:
            raise NotADirectoryError(f"Not a directory: '{directory}'") from exc

    def rename_files(self, directory: Path) -> None:
        """TODO: Implement."""
