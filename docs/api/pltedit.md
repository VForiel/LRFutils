# 🎨 `LRFutils.pltedit`

```{eval-rst}
.. automodule:: LRFutils.pltedit
   :no-members:
```

## 💾 Save a figure

```{eval-rst}
.. autofunction:: LRFutils.pltedit.save
```

## 📂 Load a figure

```{eval-rst}
.. autofunction:: LRFutils.pltedit.load
```

## 🏷️ Read the metadata

```{eval-rst}
.. autofunction:: LRFutils.pltedit.get_metadata
```

## 🖌️ Change the style

```{eval-rst}
.. autofunction:: LRFutils.pltedit.set_style
```

## 🖥️ The `pltedit` command

`pltedit [file.plt]` opens the desktop editor (see {doc}`../guides/pltedit`).

| Environment variable | Effect |
|---|---|
| `PLTEDIT_PYTHON` | Python interpreter of the figure service (default: the one running `pltedit`) |
| `PLTEDIT_ELECTRON` | Electron executable to use instead of `npm start` |
