"""Small tools for everyday scientific work by Vincent Foriel.

- :mod:`LRFutils.archive`: dated, Git-aware run directories with a ``metadata.yml`` manifest;
- :mod:`LRFutils.pltedit`: matplotlib figures saved as editable ``.plt`` files, and their desktop editor;
- :mod:`LRFutils.progress`, :mod:`LRFutils.logs`, :mod:`LRFutils.color`, :mod:`LRFutils.term`: terminal helpers.
"""

from importlib.metadata import PackageNotFoundError, version

from . import archive, color, logs, progress, term

try:
    __version__ = version("LRFutils")
except PackageNotFoundError:  # source tree that is not installed
    __version__ = "0.0.0"

__all__ = ["__version__", "archive", "color", "logs", "progress", "term"]
