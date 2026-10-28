# 📏 `LRFutils.term`

## ↔️ Separators

```{eval-rst}
.. autofunction:: LRFutils.term.hline
```

## 📐 Terminal width

```{eval-rst}
.. autodata:: LRFutils.term.term_size
   :annotation: = number of columns of the terminal (80 when unknown)
```

Example:

```python
from LRFutils import term

title = " Results "
print(title.center(term.term_size, "─"))
```
