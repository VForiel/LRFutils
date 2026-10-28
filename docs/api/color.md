# 🌈 `LRFutils.color`

ANSI codes to colour terminal text. Every function returns a new string: the text between a colour code and the reset
code `color.stop`.

## 🎨 Foreground colours

| Function | Example | Constant |
|---|---|---|
| `black(text)` | `print(color.black("text"))` | `color.fg.black` |
| `red(text)` | `print(color.red("error"))` | `color.fg.red` |
| `green(text)` | `print(color.green("passed"))` | `color.fg.green` |
| `orange(text)` | `print(color.orange("pending"))` | `color.fg.orange` |
| `blue(text)` | `print(color.blue("info"))` | `color.fg.blue` |
| `purple(text)` | `print(color.purple("12.5 s"))` | `color.fg.purple` |
| `cyan(text)` | `print(color.cyan("path/to/file"))` | `color.fg.cyan` |
| `lightgrey(text)` | `print(color.lightgrey("details"))` | `color.fg.lightgrey` |
| `darkgrey(text)` | `print(color.darkgrey("skipped"))` | `color.fg.darkgrey` |
| `lightred(text)` | `print(color.lightred("3 warnings"))` | `color.fg.lightred` |
| `lightgreen(text)` | `print(color.lightgreen("done"))` | `color.fg.lightgreen` |
| `yellow(text)` | `print(color.yellow("warning"))` | `color.fg.yellow` |
| `lightblue(text)` | `print(color.lightblue("link"))` | `color.fg.lightblue` |
| `pink(text)` | `print(color.pink("new"))` | `color.fg.pink` |
| `lightcyan(text)` | `print(color.lightcyan("value"))` | `color.fg.lightcyan` |

## 🖍️ Background colours

| Function | Example | Constant |
|---|---|---|
| `on_black(text)` | `print(color.on_black(" CLI "))` | `color.bg.black` |
| `on_red(text)` | `print(color.on_red(" FAIL "))` | `color.bg.red` |
| `on_green(text)` | `print(color.on_green(" OK "))` | `color.bg.green` |
| `on_orange(text)` | `print(color.on_orange(" WAIT "))` | `color.bg.orange` |
| `on_blue(text)` | `print(color.on_blue(" INFO "))` | `color.bg.blue` |
| `on_purple(text)` | `print(color.on_purple(" TIME "))` | `color.bg.purple` |
| `on_cyan(text)` | `print(color.on_cyan(" DATA "))` | `color.bg.cyan` |
| `on_lightgrey(text)` | `print(color.on_lightgrey(" NOTE "))` | `color.bg.lightgrey` |

Colours combine: `color.on_red(color.lightgrey(" FAIL "))`.

## ✍️ Text styles

Constants to put before the text, ended by `color.stop`:

```python
print(color.bold + "bold" + color.stop, color.underline + "underlined" + color.stop)
```

`bold`, `disable` (dim), `underline`, `reverse`, `strikethrough`, `invisible`, and `stop` (reset).

## 🧽 Remove the colours

```{eval-rst}
.. autofunction:: LRFutils.color.clear
```

Example:

```python
text = color.red("error") + " " + color.on_green("ok")
len(text)                 # 26: the codes count
len(color.clear(text))    # 8: what is shown
```
