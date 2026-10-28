"""Create dated, metadata-rich directories for scientific work.

``new`` keeps the calling convention of the first ``LRFutils.archive.new`` (a
name, ``verbose`` and scalar parameters) and makes the archive self-describing
with a ``metadata.yml`` manifest.  Creating an archive does not
move or copy experiment data: callers can write their files to the returned
directory using the format that best fits their experiment.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import yaml


_SAFE_NAME = re.compile(r"[^A-Za-z0-9._=-]+")


@dataclass(frozen=True)
class Archive:
    """A newly created scientific archive and its recorded metadata."""

    path: Path
    metadata: Mapping[str, Any]

    def __fspath__(self) -> str:
        """Allow an archive to be passed directly to filesystem APIs."""
        return os.fspath(self.path)

    def __str__(self) -> str:
        """Return the archive directory as a string."""
        return str(self.path)


def _git_metadata() -> dict[str, str | None]:
    """Read the current Git commit without requiring GitPython."""
    metadata: dict[str, str | None] = {"commit": None, "branch": None}
    commands = {
        "commit": ["git", "rev-parse", "HEAD"],
        "branch": ["git", "branch", "--show-current"],
    }
    for key, command in commands.items():
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        value = result.stdout.strip()
        if value:
            metadata[key] = value
    return metadata


def _description(parameters: Mapping[str, Any]) -> str:
    """Format simple parameters as a stable, filesystem-safe suffix."""
    parts = []
    for key, value in parameters.items():
        if isinstance(value, (bool, int, float, str)):
            parts.append(f"{key}={value}")
    return _SAFE_NAME.sub("-", "-".join(parts))


def _next_number(day_root: Path) -> int:
    """Return the next numeric archive prefix in *day_root*."""
    numbers = []
    for child in day_root.iterdir():
        match = re.match(r"^(\d+)", child.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def new(
    name: str | None = None,
    verbose: bool = False,
    root: str | os.PathLike[str] = "archives",
    metadata: Mapping[str, Any] | None = None,
    **parameters: Any,
) -> Archive:
    """Create and describe a dated archive directory.

    Parameters
    ----------
    name:
        Optional human-readable suffix of the directory name.
    verbose:
        Print the created path when true.
    root:
        Parent directory in which the dated ``archives`` tree is created.
    metadata:
        Optional custom metadata to merge with the generated base metadata.
        Custom keys take precedence when a key is intentionally repeated.
    **parameters:
        Simple scalar experiment parameters.  They are recorded in the YAML
        manifest and included in the directory name.

    Returns
    -------
    Archive
        An object that behaves like a path and exposes the metadata.
    """
    created_at = datetime.now(timezone.utc)
    git = _git_metadata()
    day_root = Path(root).expanduser() / created_at.strftime("%Y-%m-%d")
    if git["commit"]:
        day_root = day_root.with_name(f"{day_root.name}_{git['commit'][:7]}")
    day_root.mkdir(parents=True, exist_ok=True)

    suffix_parts = [part for part in (name, _description(parameters)) if part]
    suffix = "-".join(_SAFE_NAME.sub("-", part).strip("-") for part in suffix_parts)
    archive_path = day_root / f"{_next_number(day_root):04d}"
    if suffix:
        archive_path = archive_path.with_name(f"{archive_path.name}-{suffix}")
    archive_path.mkdir()

    base_metadata: dict[str, Any] = {
        "created_at": created_at.isoformat(),
        "python_version": sys.version,
        "git_commit": git["commit"],
        "git_branch": git["branch"],
        "parameters": dict(parameters),
    }
    merged_metadata = {**base_metadata, **dict(metadata or {})}
    metadata_path = archive_path / "metadata.yml"
    metadata_path.write_text(
        yaml.safe_dump(merged_metadata, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    archive = Archive(archive_path, merged_metadata)
    if verbose:
        print(f"Archive created at {archive.path}")
    return archive


def description(**parameters: Any) -> str:
    """Return the historical compact description for archive parameters."""
    return _description(parameters)


def latest(root: str | os.PathLike[str] = "archives") -> Archive | None:
    """Return the most recently modified archive, or ``None`` if empty."""
    candidates = [path for path in Path(root).expanduser().glob("**/metadata.yml")]
    if not candidates:
        return None
    # Archives created within the timestamp resolution of the file system: the higher number wins
    metadata_path = max(candidates, key=lambda path: (path.stat().st_mtime, path.parent.name))
    metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    return Archive(metadata_path.parent, metadata)


__all__ = ["Archive", "description", "latest", "new"]