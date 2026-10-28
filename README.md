# LRFutils

[![PyPI](https://img.shields.io/pypi/v/LRFutils)](https://pypi.org/project/LRFutils/)
[![Documentation](https://readthedocs.org/projects/lrfutils/badge/?version=latest)](https://lrfutils.readthedocs.io)
[![Sponsor](https://img.shields.io/badge/sponsor-%E2%9D%A4-bf3989)](https://github.com/sponsors/VForiel)

Small tools for everyday scientific work, by Vincent Foriel.

- `LRFutils.archive`: one dated directory per run, named after its parameters, with a `metadata.yml` manifest
  (date, Python version, Git commit and branch, parameters).
- `LRFutils.pltedit`: matplotlib figures saved as editable `.plt` files, reopened in Python or in the `pltedit`
  desktop editor.
- `LRFutils.progress`, `logs`, `color`, `term`: progress bars, logs and coloured text for scripts.

```console
pip install LRFutils
```

```python
from LRFutils import archive, pltedit

run = archive.new("scan", wavelength_nm=1550)       # archives/2026-10-28_1a2b3c4/0001-scan-wavelength_nm=1550/
pltedit.save(fig, run.path / "spectrum.plt")
```

Documentation: https://lrfutils.readthedocs.io

LRFutils 0.2 replaces [VFSciTools](https://github.com/VForiel/VFSciTools): `vfscitools.archive` and `pltedit` are now
`LRFutils.archive` and `LRFutils.pltedit`, with the same behaviour and file formats.

## Development

```console
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev,docs]"      # .venv/bin/python on Linux and macOS
.venv/Scripts/python -m pytest
.venv/Scripts/python -m sphinx -W -b html docs docs/_build/html
```

A GitHub release publishes the package on PyPI (`.github/workflows/publish.yml`); Read the Docs builds the documentation
of every push to `main`.

MIT license.

If LRFutils helps your work, you can [sponsor its development](https://github.com/sponsors/VForiel) ❤️
