# LRFutils

Small tools for everyday scientific work, by Vincent Foriel:

- **{doc}`archive`**: one dated directory per run, named after its parameters, with a `metadata.yml` manifest
  (date, Python version, Git commit and branch, parameters);
- **{doc}`pltedit`**: matplotlib figures saved as editable `.plt` files, reopened in Python or in a desktop editor;
- **{doc}`terminal`**: progress bars, coloured text and logs for scripts.

```console
pip install LRFutils
```

```python
from LRFutils import archive, pltedit, progress
```

LRFutils 0.2 merges VFSciTools, which it replaces: `vfscitools.archive` and `pltedit` are now
`LRFutils.archive` and `LRFutils.pltedit` (see the {doc}`changelog`).

```{toctree}
:maxdepth: 2
:hidden:

archive
pltedit
terminal
api
changelog
```
