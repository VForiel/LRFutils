# 🖥️ Terminal helpers

## ⏳ Progress bars

```python
from LRFutils import progress

bar = progress.Bar(max=1000, prefix="Simulation")
for i in range(1001):
    ...
    bar(i)
```

The bar shows the percentage, `i/max`, the elapsed time and an estimated time of arrival averaged over the last
`average_ETA` updates (10 by default). `bar(i, stop=True)` or `bar.stop()` ends it early (in yellow). Options:
`width` (80 characters), `decimals` of the percentage, `eta` and `show_duration`.

## 🌈 Colours

```python
from LRFutils import color

print(color.red("error"), color.on_green("ok"), color.bold + "bold" + color.stop)
color.clear(text)   # removes the colour codes
```

Foreground functions: `black`, `red`, `green`, `orange`, `blue`, `purple`, `cyan`, `lightgrey`, `darkgrey`,
`lightred`, `lightgreen`, `yellow`, `lightblue`, `pink`, `lightcyan`; backgrounds: `on_black`, `on_red`, … The raw codes
are in `color.fg`, `color.bg` and the module (`bold`, `underline`, `stop`…).

## 📝 Logs

```python
from LRFutils import logs

logs.info("Starting")
logs.warn("Low signal")
logs.replace_excepthook()   # uncaught exceptions are logged too
```

Messages are printed with the date and written to `logs/<start time>.log`, which begins with the machine description.
`logs.error(message)` also records the current traceback.

## 📏 Separators

`term.hline("─")` returns a line as wide as the terminal.

```{seealso}
The reference pages {doc}`../api/progress`, {doc}`../api/logs`, {doc}`../api/color` and {doc}`../api/term`.
```
