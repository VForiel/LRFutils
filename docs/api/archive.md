# 🗃️ `LRFutils.archive`

```{eval-rst}
.. automodule:: LRFutils.archive
   :no-members:
```

## ➕ Create an archive

```{eval-rst}
.. autofunction:: LRFutils.archive.new
```

## 📦 The `Archive` object

```{eval-rst}
.. autoclass:: LRFutils.archive.Archive
   :members:
   :special-members: __fspath__
```

Example:

```python
run = archive.new("scan")
run.path / "data.npy"            # a pathlib.Path
os.path.join(run, "data.npy")    # works too: an Archive is path-like
run.metadata["git_commit"]
```

## 🔎 Find the last archive

```{eval-rst}
.. autofunction:: LRFutils.archive.latest
```

## 🏷️ Describe parameters

```{eval-rst}
.. autofunction:: LRFutils.archive.description
```
