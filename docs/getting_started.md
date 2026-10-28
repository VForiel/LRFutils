# 🚀 Getting started

## 📦 Installation

LRFutils needs Python 3.10 or later.

```console
pip install LRFutils
```

It brings NumPy, matplotlib and PyYAML. The desktop figure editor also needs [Node.js](https://nodejs.org) (see
{doc}`guides/pltedit`).

```{tip}
LRFutils is a personal toolbox that still evolves: pin the version in your project (`LRFutils==0.2.*`) and read the
{doc}`changelog` before upgrading.
```

## 👋 Your first archive

```python
from LRFutils import archive

run = archive.new("first-try", exposure_ms=25)
print(run.path)          # archives/2026-10-28_1a2b3c4/0001-first-try-exposure_ms=25
(run.path / "notes.txt").write_text("It works!")
```

Open `metadata.yml` in that folder: the date, your Python version, the Git commit of your code and the parameters are
there. Everything about archives: {doc}`guides/archive`.

## 🎨 Your first editable figure

```python
import matplotlib.pyplot as plt
from LRFutils import pltedit

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
pltedit.save(fig, "squares.plt")

fig = pltedit.load("squares.plt")   # tomorrow, next month…
fig.axes[0].set_xlabel("n")
fig.savefig("squares.png")
```

More in {doc}`guides/pltedit`.

## ⏳ Your first progress bar

```python
from LRFutils import progress

bar = progress.Bar(max=1000, prefix="Computing")
for i in range(1001):
    bar(i)
```

The other terminal helpers are in {doc}`guides/terminal`, and every function is described with an example in the
{doc}`api/index`.
