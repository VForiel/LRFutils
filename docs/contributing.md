# 🤝 Contributing

Contributions are welcome: bug reports, ideas, documentation fixes and code.

## 🐛 Report a bug or suggest an idea

Open an [issue on GitHub](https://github.com/VForiel/LRFutils/issues) with what you did, what you expected and what
happened (the LRFutils, Python and matplotlib versions help: `python -c "import LRFutils; print(LRFutils.__version__)"`).

## 🛠️ Set up the project

```console
git clone https://github.com/VForiel/LRFutils.git
cd LRFutils
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev,docs]"     # .venv/bin/python on Linux and macOS
```

## ✅ Run the tests

```console
.venv/Scripts/python -m pytest
```

Every change of behaviour comes with a test in `tests/`. The continuous integration runs them on Linux and Windows,
with the oldest and newest supported Python versions.

## 📖 Build the documentation

```console
.venv/Scripts/python -m sphinx -W -b html docs docs/_build/html
```

Then open `docs/_build/html/index.html`. Warnings are errors, as on Read the Docs. The documentation is written in
Markdown (MyST); the reference pages come from the docstrings (NumPy style, with an `Examples` section).

## 📬 Propose a change

1. Fork the repository and create a branch.
2. Keep the change focused, with its tests and documentation.
3. Add a line to the {doc}`changelog` under a new or the upcoming version.
4. Open a pull request explaining the why.

## 🎨 Conventions

- Code, comments and documentation in English.
- Public functions have type hints and a docstring with an example.
- Never delete or overwrite user data implicitly: archives and figures are scientific records.
- The desktop editor of PltEdit lives in `src/LRFutils/pltedit/desktop` (Electron; `npm install` then `npm start`).

## 🚢 Releases

The maintainer bumps `version` in `pyproject.toml`, completes the changelog and publishes a GitHub release: the
`Publish` workflow uploads the package to PyPI (secret `PYPI_API_TOKEN`).
