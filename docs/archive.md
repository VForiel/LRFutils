# Run archives

`archive.new` creates a directory for the results of a run and describes it in a `metadata.yml` file. It never
copies or moves data: write your files into the directory it returns.

```python
from LRFutils import archive

run = archive.new(
    "calibration",
    metadata={"operator": "Vincent", "instrument": "bench-A"},
    exposure_ms=25,
    filter="H",
)
(run.path / "measurement.csv").write_text("...")
```

This creates:

```text
archives/
└── 2026-10-28_1a2b3c4/              # UTC date and short Git commit (when run inside a repository)
    └── 0001-calibration-exposure_ms=25-filter=H/
        └── metadata.yml
```

- Runs of the same day and commit are numbered `0001`, `0002`… in creation order.
- The name and the scalar parameters (`bool`, `int`, `float`, `str`) are added to the directory name, with
  characters that are unsafe in file names replaced by `-`.
- `metadata.yml` holds `created_at` (UTC, ISO 8601), `python_version`, `git_commit`, `git_branch`, `parameters`, then
  the entries of `metadata`, which win over the generated ones when a key is repeated.
- `root` sets the parent directory (`archives` in the current directory by default); `verbose=True` prints the path.

The returned {class}`~LRFutils.archive.Archive` exposes `path` (a `pathlib.Path`) and `metadata`, and can be given
directly to file-system functions (`os.fspath(run)`, `os.path.join(run, "x.txt")`).

`archive.latest()` returns the most recently modified archive under a root, or `None`.

Git is called through the `git` command when it is available; outside a repository, the commit and branch are `null`.
