# 📜 Changelog

## 0.1.2

### progress

#### 🐛 Bug fixes

- The Bar initialization was using a pipe in type hints which is not supported in python before 3.10. This is now fixed.


## 0.1.0
---

```{admonition} Breaking changes
:class: warning

This version contain a lot of breaking changes that are identifies below with the {bdg-danger}`BREAKING` badge.
```

### LRFutils.color

#### ➕ Additions

- Colors can now be applied using functions such as `LRFutils.color.yellow("Hello World!")"

#### 🔀 Tweaks
- {bdg-danger}`BREAKING` Color variables move from class "Color" to "fg" and "bg" classes (respectively for foreground and background colors).
- {bdg-danger}`BREAKING` most of color variable were renamed (mostly due to application of pep8 rules).

### LRFutils.logs

#### 🔀 Tweaks
- {bdg-danger}`BREAKING` `log` module was renamed `logs` to avoid conflict with the mathematical `log` function when the lib is imported with `*`.
- Log folder and file are now created only if one log message is recorded (not anymore at the import of the module).
- The custom hookexcept is no more applied by default. Now, you have to call `LRFutils.logs.replace_hookexcept()` to apply it.

## Before 0.1.0
---

In a nutshell:

- Added everything that was here before 0.1.0.