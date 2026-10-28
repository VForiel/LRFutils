"""Command-line entry point for the PltEdit desktop application."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Launch Electron and optionally open a ``.plt`` file."""
    desktop = Path(__file__).resolve().parent / "desktop"
    if not desktop.is_dir():
        raise SystemExit(f"The PltEdit desktop application is missing: {desktop}")
    # The figure service of the desktop application runs with this interpreter, where LRFutils is installed
    env = {**os.environ, "PLTEDIT_PYTHON": os.environ.get("PLTEDIT_PYTHON", sys.executable)}

    electron = os.environ.get("PLTEDIT_ELECTRON")
    if electron:
        command = [electron, ".", *sys.argv[1:]]
    else:
        npm = shutil.which("npm")
        if npm is None:
            raise SystemExit(
                "npm is required to launch PltEdit. Install Node.js and run "
                "'npm install' in the desktop directory."
            )
        command = [npm, "start", "--", *sys.argv[1:]]
    raise SystemExit(subprocess.call(command, cwd=desktop, env=env))


if __name__ == "__main__":
    main()
