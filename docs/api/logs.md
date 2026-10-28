# 📝 `LRFutils.logs`

Messages are printed with the date and appended to `logs/<start time>.log` (in the current directory), created at the
first message with a description of the machine.

## 💬 Messages

```{eval-rst}
.. autofunction:: LRFutils.logs.info
.. autofunction:: LRFutils.logs.warn
.. autofunction:: LRFutils.logs.error
```

## 💥 Uncaught exceptions

```{eval-rst}
.. autofunction:: LRFutils.logs.replace_excepthook
.. autofunction:: LRFutils.logs.myexcepthook
.. autodata:: LRFutils.logs.hide_traceback
   :annotation: = False
```

## 🔧 Lower-level helpers

```{eval-rst}
.. autofunction:: LRFutils.logs.logPrint
.. autofunction:: LRFutils.logs.logSave
.. autofunction:: LRFutils.logs.now
.. autofunction:: LRFutils.logs.ensure_path
.. autodata:: LRFutils.logs.filename
   :annotation: = "logs/<start time>.log"
```
