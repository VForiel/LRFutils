"""PltEdit: save and load matplotlib figures as editable ``.plt`` files.

A ``.plt`` file is a NumPy archive holding the pickled figure and metadata (creation date, Python,
matplotlib and PltEdit versions). Loading a file unpickles it: only open files you trust.

Basic usage::

    import matplotlib.pyplot as plt
    from LRFutils import pltedit

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    pltedit.save(fig, "my_figure.plt")

    fig2 = pltedit.load("my_figure.plt")
    plt.show()

The ``pltedit`` command opens a file in the desktop editor (Electron, see the documentation).
"""

from ._io import get_metadata, load, save
from ._style import set_style
from ._version import __version__

__all__ = ["__version__", "get_metadata", "load", "save", "set_style"]
