# 🧰 LRFutils

Small tools for everyday scientific work: keep every run traceable, keep every figure editable, and see what your
scripts are doing.

```console
pip install LRFutils
```

<div class="lrf-cards">
  <a href="guides/archive.html"><strong>🗃️ Run archives</strong>One dated folder per run, named after its parameters, with a <code>metadata.yml</code> (date, Git commit, Python, parameters).</a>
  <a href="guides/pltedit.html"><strong>🎨 Editable figures</strong>Save matplotlib figures as <code>.plt</code> files and change them months later, in Python or in the desktop editor.</a>
  <a href="guides/terminal.html"><strong>🖥️ Terminal helpers</strong>Progress bars with an ETA, logs written to a file, coloured text and separators.</a>
</div>

## ✨ In one example

```python
import matplotlib.pyplot as plt
import numpy as np
from LRFutils import archive, logs, pltedit, progress

run = archive.new("sweep", wavelength_nm=1550)   # archives/<date>_<commit>/0001-sweep-…
logs.info(f"Results in {run.path}")

bar = progress.Bar(max=200, prefix="Sweep")
signal = []
for i in range(200):
    signal.append(np.sin(i / 20))
    bar(i + 1)

fig, ax = plt.subplots()
ax.plot(signal)
pltedit.save(fig, run.path / "signal.plt")       # reopen it with pltedit.load
```

New here? Start with {doc}`getting_started`.

## 🗺️ Contents

```{toctree}
:maxdepth: 2
:caption: Guides

getting_started
guides/archive
guides/pltedit
guides/terminal
```

```{toctree}
:maxdepth: 2
:caption: Reference

api/index
changelog
```

```{toctree}
:maxdepth: 1
:caption: Community

contributing
support
```

```{note}
LRFutils 0.2 merges [VFSciTools](https://github.com/VForiel/VFSciTools), which it replaces: `vfscitools.archive` and
`pltedit` are now `LRFutils.archive` and `LRFutils.pltedit`, with the same behaviour and file formats.
```
