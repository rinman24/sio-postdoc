"""Local Access Service."""

import os
from pathlib import Path
from typing import Protocol

Contents = tuple[Path, ...]


class DiskAccess(Protocol):
    """Define protocol for Local Disk Access."""

    # pylint: disable=missing-function-docstring

    def list_files(
        self,
        directory: Path,
        extension: str,
    ) -> Contents: ...
    def rename_files(
        self,
        current: Contents,
        new: Contents,
    ) -> None: ...


class LocalAccess(DiskAccess):
    """Concrete implementation of Disk Access."""

    def list_files(self, directory: Path, extension: str) -> Contents:
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
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"No such file or directory: '{directory}'"
            ) from exc

    def rename_files(self, current: Contents, new: Contents) -> None:
        """Change the current names to the new names."""
        for src, dst in zip(current, new):
            os.rename(src, dst)
