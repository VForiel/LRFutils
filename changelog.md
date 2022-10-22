# 0.0.11

> **Warning**
> 
> This update include breaking changes 💥

## 📢 Announcements
- This module is now available on Pypi!
https://pypi.org/project/LRFutils/0.0.11/
    - You can then install it using `pip install LRFutils`

## ➕ Additions
- Added `average_ETA` parameter on progress bar to prevent variating ETA. By default, this parameter is set to 10

## 🔧 Tweaks
- 💥 `LRFutils.progress.Bar()`'s `duration` parameter was renamed in `show_duration` to be more explicit.
- 💥 `LRFutils.log` module was renamed `LRFutils.logs` in order to have a conveniant import line (`from LRFutils import logs`) while avoiding conflict with mathematical log function.
- 💥 `LRFutils.color.Color` class, was removed. All the attribute are now directly in the module `LRFutils.color` (which allow to import the module on the same line than other ones `from LRFutils import color, logs, archive [...]`)

# 0.0.10

> 🔎 Changelog doesn't go that far...