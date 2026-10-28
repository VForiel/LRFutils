# 🎨 Editable figures (PltEdit)

`pltedit.save` stores a matplotlib figure in a `.plt` file, from which `pltedit.load` gives back a live figure that
can still be modified: change a title, a colour or a limit months later without re-running the computation.

```python
import matplotlib.pyplot as plt
from LRFutils import pltedit

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
pltedit.save(fig, "result.plt")       # an Axes is accepted too; ".plt" is added when missing

fig = pltedit.load("result.plt")
fig.axes[0].set_title("Result")
plt.show()
```

`pltedit.get_metadata("result.plt")` tells when and with which versions a file was saved, and
`pltedit.set_style(fig, "dark_background")` redraws a figure with another matplotlib style.

## 📄 File format

A `.plt` file is a NumPy archive (`.npz`) holding the pickled figure (`figure`) and a JSON document (`metadata`):
creation date, Python, matplotlib and PltEdit versions.

```{warning}
Loading a file unpickles it, which can run code: **only open files you trust**. Figures pickled with a very different
matplotlib version may not load.
```

## 🖥️ Desktop editor

The `pltedit` command opens the desktop editor (Electron), optionally on a file:

```console
pltedit result.plt
```

It needs Node.js. Install the editor once, in the `desktop` directory of the installed package:

```console
cd "$(python -c "import LRFutils.pltedit, pathlib; print(pathlib.Path(LRFutils.pltedit.__file__).parent / 'desktop')")"
npm install
```

The editor runs its figure service with the Python interpreter that launched `pltedit` (or `PLTEDIT_PYTHON` when set);
`PLTEDIT_ELECTRON` can point to an Electron executable instead of `npm start`.

```{seealso}
{doc}`../api/pltedit` for every function and its parameters.
```
