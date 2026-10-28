# 📜 Changelog

## 0.2.0

LRFutils absorbs VFSciTools, which is no longer maintained.

- **Breaking**: `archive.new` is the VFSciTools version. It returns an `Archive` (path and metadata) instead of a
  string, writes `metadata.yml`, uses the UTC date, numbers runs `0001`, `0002`… and joins the name and parameters
  with `-` (`0001-scan-x=1`, formerly `1_scan-x=1`). The `name`, `verbose` and keyword parameters are unchanged.
  New `root` and `metadata` arguments, and `archive.latest()`. GitPython is no longer needed.
- New `LRFutils.pltedit` (formerly the `pltedit` package of VFSciTools): editable `.plt` figures and the `pltedit`
  desktop editor, and `pltedit.get_metadata`. The file format is unchanged.
- `color.clear` removes every colour code; the progress bar no longer fails on its first estimate; uncaught
  exceptions are reported with their type.
- Python 3.10 or later; dependencies: NumPy, matplotlib, PyYAML.
- New documentation (guides, a reference page per module with an example for every function, contributing guide),
  tests and continuous integration.

## 0.1.2

### progress

#### 🐛 Bug fixes

- The Bar initialization was using a pipe in type hints which is not supported in python before 3.10. This is now fixed.


## 0.1.0

```{admonition} Breaking changes
:class: warning

This version contain a lot of breaking changes that are identifies below with **Breaking**.
```

### LRFutils.color

#### ➕ Additions

- Colors can now be applied using functions such as `LRFutils.color.yellow("Hello World!")`

#### 🔀 Tweaks
- **Breaking**: Color variables move from class "Color" to "fg" and "bg" classes (respectively for foreground and background colors).
- **Breaking**: most of color variable were renamed (mostly due to application of pep8 rules).

### LRFutils.logs

#### 🔀 Tweaks
- **Breaking**: `log` module was renamed `logs` to avoid conflict with the mathematical `log` function when the lib is imported with `*`.
- Log folder and file are now created only if one log message is recorded (not anymore at the import of the module).
- The custom hookexcept is no more applied by default. Now, you have to call `LRFutils.logs.replace_excepthook()` to apply it.

## Before 0.1.0

In a nutshell:

- Added everything that was here before 0.1.0.
