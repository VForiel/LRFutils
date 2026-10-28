"""
Save and load matplotlib figures as .plt files.

A .plt file is a NumPy archive (.npz) renamed to .plt.  It contains:

- ``figure``: a 1-D uint8 array holding the pickle-serialised
  :class:`matplotlib.figure.Figure` object.
- ``metadata``: a 0-D object array whose single element is a JSON string
  with the following keys:

  ``created_at``
      ISO-8601 timestamp of when the file was saved.
  ``python_version``
      Full Python version string (e.g. ``"3.12.3"``).
  ``matplotlib_version``
      Matplotlib version string (e.g. ``"3.10.1"``).
  ``pltedit_version``
      PltEdit version string (e.g. ``"0.1.0"``).
"""

from __future__ import annotations

import io
import json
import os
import pickle
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Union

import matplotlib
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ._version import __version__


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def save(fig: Union[Figure, Axes], path: Union[str, os.PathLike]) -> None:
    """Serialise *fig* to a ``.plt`` file at *path*.

    Parameters
    ----------
    fig:
        A :class:`~matplotlib.figure.Figure` or
        :class:`~matplotlib.axes.Axes` instance.  When an
        :class:`~matplotlib.axes.Axes` is supplied the parent figure is saved.
    path:
        Destination file path.  The ``.plt`` extension is appended
        automatically if it is missing.

    Raises
    ------
    TypeError
        If *fig* is neither a :class:`~matplotlib.figure.Figure` nor an
        :class:`~matplotlib.axes.Axes`.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from LRFutils import pltedit
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [4, 5, 6])
    >>> pltedit.save(fig, "result.plt")
    """
    if isinstance(fig, Axes):
        fig = fig.get_figure()
    if not isinstance(fig, Figure):
        raise TypeError(
            f"Expected a matplotlib Figure or Axes, got {type(fig)!r}."
        )

    path = Path(path)
    if path.suffix.lower() != ".plt":
        path = path.with_suffix(".plt")

    # ---- serialise the figure -------------------------------------------
    buf = io.BytesIO()
    pickle.dump(fig, buf)
    figure_bytes = np.frombuffer(buf.getvalue(), dtype=np.uint8)

    # ---- build metadata -------------------------------------------------
    metadata_dict = {
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
        "python_version": sys.version,
        "matplotlib_version": matplotlib.__version__,
        "pltedit_version": __version__,
    }
    metadata_array = np.array(json.dumps(metadata_dict))

    # ---- write as npz with .plt extension --------------------------------
    # np.savez writes a .npz file; we write to a temporary file and rename.
    with tempfile.NamedTemporaryFile(suffix=".npz", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        np.savez(tmp_path, figure=figure_bytes, metadata=metadata_array)
        shutil.move(tmp_path, path)
    except Exception:
        # Clean up temp file on failure
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def load(path: Union[str, os.PathLike]) -> Figure:
    """Deserialise a ``.plt`` file and return the stored figure.

    .. warning::

        ``.plt`` files are deserialised with :mod:`pickle`.  Only load files
        from sources you trust.  A maliciously crafted ``.plt`` file could
        execute arbitrary code when loaded.

    Parameters
    ----------
    path:
        Path to a ``.plt`` file.

    Returns
    -------
    matplotlib.figure.Figure
        The reconstructed figure.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    ValueError
        If *path* is not a valid ``.plt`` file.

    Examples
    --------
    >>> from LRFutils import pltedit
    >>> fig = pltedit.load("result.plt")
    >>> fig.axes[0].set_title("Calibrated result")
    >>> fig.savefig("result.pdf")
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No such file: {path!r}")

    try:
        archive = np.load(path, allow_pickle=False)
    except Exception as exc:
        raise ValueError(f"{path!r} is not a valid .plt file: {exc}") from exc

    if "figure" not in archive:
        raise ValueError(
            f"{path!r} is missing the 'figure' array — not a valid .plt file."
        )

    # Matplotlib >=3.10 expects `_axlim_clip` on 3D collections.
    # Older pickles may deserialize objects/classes without this attribute.
    try:
        from mpl_toolkits.mplot3d import art3d
        for cls_name in ("Line3DCollection", "Poly3DCollection"):
            cls = getattr(art3d, cls_name, None)
            if cls is not None and not hasattr(cls, "_axlim_clip"):
                setattr(cls, "_axlim_clip", False)
    except Exception:
        pass

    figure_bytes = bytes(archive["figure"].tobytes())
    fig = pickle.loads(figure_bytes)  # noqa: S301 — trusted .plt files only

    if not isinstance(fig, Figure):
        raise ValueError(
            "The deserialized object is not a matplotlib Figure."
        )


    # Cross-version compatibility patch (e.g., matplotlib 3.9 -> 3.10+)
    # Matplotlib 3.10+ added the `_parent_figure` attribute to Artist and `_root_figure` to Figure.
    # Older pickled figures won't have it, so we inject it.
    if not hasattr(fig, '_root_figure'):
        fig._root_figure = fig

    def _ensure_colorizer(artist):
        """Ensure modern Matplotlib color-mapped artists have a colorizer."""
        if hasattr(artist, "_colorizer"):
            return

        # Prefer raw pickled attributes to avoid triggering properties that
        # already expect `_colorizer` to exist (Matplotlib 3.10+).
        artist_dict = getattr(artist, "__dict__", {})
        cmap = artist_dict.get("cmap", None)
        norm = artist_dict.get("_norm", None)

        if cmap is None:
            try:
                cmap = artist.get_cmap()
            except Exception:
                cmap = None
        if norm is None:
            try:
                norm = artist.get_norm()
            except Exception:
                norm = None

        if cmap is None:
            return

        try:
            from matplotlib.colorizer import Colorizer
            artist._colorizer = Colorizer(cmap, norm)
        except Exception:
            # Older matplotlib versions may not provide Colorizer.
            pass

    def patch_artist(artist, parent_fig, seen=None):
        if seen is None:
            seen = set()
        if id(artist) in seen:
            return
        seen.add(id(artist))
        
        if not hasattr(artist, '_parent_figure'):
            artist._parent_figure = parent_fig
        if not hasattr(artist, '_axlim_clip'):
            artist._axlim_clip = False
            
        # In case of subfigures
        if type(artist).__name__ == "SubFigure" and not hasattr(artist, '_root_figure'):
            artist._root_figure = parent_fig
            
        if hasattr(artist, 'get_children'):
            for child in artist.get_children():
                patch_artist(child, parent_fig, seen)
                
        # Fix missing colorizer on colormapped artists (PathCollection, images, etc.)
        _ensure_colorizer(artist)
                
        # Handle Axes specific missing attributes
        if isinstance(artist, matplotlib.axis.Axis):
            if not hasattr(artist, '_converter'):
                artist._converter = None
            if not hasattr(artist, 'units'):
                artist.units = None
            if not hasattr(artist, '_converter_is_explicit'):
                artist._converter_is_explicit = False
            # Explicitly patch ticks which might not be returned by get_children
            for attr in ['majorTicks', 'minorTicks']:
                if hasattr(artist, attr):
                    for tick in getattr(artist, attr):
                        patch_artist(tick, parent_fig, seen)
                        
        # Explicitly patch Tick internals (label1, label2, etc.)
        if isinstance(artist, matplotlib.axis.Tick):
            for attr in ['tick1line', 'tick2line', 'gridline', 'label1', 'label2']:
                if hasattr(artist, attr):
                    child = getattr(artist, attr)
                    if child is not None:
                        patch_artist(child, parent_fig, seen)

        # Matplotlib 3.10 expects hatch linewidth on Patch-based artists.
        if isinstance(artist, matplotlib.patches.Patch):
            if not hasattr(artist, '_hatch_linewidth'):
                artist._hatch_linewidth = matplotlib.rcParams.get('hatch.linewidth', 1.0)
    
    patch_artist(fig, fig)

    # Ensure defaults on every artist, including detached 3D collections.
    for artist in fig.findobj(match=lambda a: isinstance(a, matplotlib.artist.Artist)):
        if not hasattr(artist, '_axlim_clip'):
            artist._axlim_clip = False

    # Some artists are not always reached by generic children traversal.
    for ax in fig.get_axes():
        for coll in ax.collections:
            _ensure_colorizer(coll)
        for img in ax.images:
            _ensure_colorizer(img)

    # Last-resort pass: include detached/proxy artists (e.g. legend scatter handles).
    for artist in fig.findobj(match=lambda a: isinstance(a, matplotlib.cm.ScalarMappable)):
        _ensure_colorizer(artist)

    import matplotlib.pyplot as plt
    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)

    return fig


def get_metadata(path: Union[str, os.PathLike]) -> dict:
    """Return the metadata stored inside a ``.plt`` file.

    Parameters
    ----------
    path:
        Path to a ``.plt`` file.

    Returns
    -------
    dict
        Dictionary with keys ``created_at``, ``python_version``,
        ``matplotlib_version``, and ``pltedit_version``.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    ValueError
        If *path* is not a valid ``.plt`` file or has no metadata.

    Examples
    --------
    >>> from LRFutils import pltedit
    >>> pltedit.get_metadata("result.plt")["matplotlib_version"]
    '3.10.1'
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No such file: {path!r}")

    try:
        archive = np.load(path, allow_pickle=False)
    except Exception as exc:
        raise ValueError(f"{path!r} is not a valid .plt file: {exc}") from exc

    if "metadata" not in archive:
        raise ValueError(
            f"{path!r} is missing the 'metadata' array — not a valid .plt file."
        )

    return json.loads(str(archive["metadata"]))
