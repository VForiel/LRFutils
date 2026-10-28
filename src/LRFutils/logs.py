#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
import os
import platform
from . import color
import sys
import traceback

hide_traceback = False

# Get current time as string
def now(human=False, c=False):
    """Return the current local time as a string.

    Parameters
    ----------
    human : bool
        ``"28/10/2026 at 11:42:07"`` instead of the file-name friendly ``"2026-10-28_11.42.07.123456"``.
    c : bool
        Colour the human-readable form (date in blue, time in purple).

    Examples
    --------
    >>> from LRFutils import logs
    >>> logs.now()
    '2026-10-28_11.42.07.123456'
    >>> logs.now(human=True)
    '28/10/2026 at 11:42:07'
    """
    time = str(datetime.now())
    if human:
        if c:
            return f"{color.fg.blue}{time[8:10]}/{time[5:7]}/{time[0:4]}{color.stop} at {color.fg.purple}{time[11:13]}:{time[14:16]}:{time[17:19]}{color.stop}"
        else:
            return f"{time[8:10]}/{time[5:7]}/{time[0:4]} at {time[11:13]}:{time[14:16]}:{time[17:19]}"
    else:
        return time.replace(" ", "_").replace(":", ".")

startTime = now()
filename = f"logs/{startTime}.log"

def ensure_path():
    """Create the ``logs`` directory and the log file, with the machine description, when missing.
    """
    if not os.path.isdir("logs"):
        os.makedirs(f"logs/")
        # Saving the current environment information
        with open(filename, "a") as logFile:
            logFile.write(f"ENVIRONMENT: {platform.uname()}\n\n")


# Print message in log file
def logSave(message):
    """Append ``message`` to the log file, after the date and time (nothing is printed).

    Examples
    --------
    >>> from LRFutils import logs
    >>> logs.logSave("raw line, written to the file only")
    """
    ensure_path()
    currentTime = now(human = True, c=False)
    with open(filename, "a", encoding="utf-8") as logFile:
        logFile.write(f"{currentTime} | {message}\n")

# Print message in terminal
def logPrint(message):
    """Print ``message`` after the coloured date and time (nothing is written to the file).

    Examples
    --------
    >>> from LRFutils import logs
    >>> logs.logPrint("printed only")
    28/10/2026 at 11:42:07 | printed only
    """
    currentTime = now(human = True, c=True)
    print(f'{currentTime} | {message}')

# Info-styled messages
def info(message):
    """Print and log an information message (green ``[INFO]`` tag).

    Examples
    --------
    >>> from LRFutils import logs
    >>> logs.info("Simulation started")
    28/10/2026 at 11:42:07 | [INFO] Simulation started
    """
    logSave(f"[INFO] {message}")
    message = color.green("[INFO] ") + message
    logPrint(message)
    
# Warning-styled messages
def warn(message):
    """Print and log a warning (in yellow, with a ``[WARNING]`` tag).

    Examples
    --------
    >>> from LRFutils import logs
    >>> logs.warn("Signal below the noise floor")
    28/10/2026 at 11:42:07 | [WARNING] Signal below the noise floor
    """
    message = f"[WARNING] {message}"
    logSave(message)
    message = color.yellow(message)
    logPrint(message)

# Error-styled messages
def error(message, etype = None, value = None, tb=None):
    """Print and log an error, and write the traceback to the log file.

    Parameters
    ----------
    message : str
        Description of the error.
    etype, value, tb
        An exception given explicitly (as received by ``sys.excepthook``); by default, the exception being handled.

    Examples
    --------
    >>> from LRFutils import logs
    >>> try:
    ...     1 / 0
    ... except ZeroDivisionError:
    ...     logs.error("Normalisation failed")
    28/10/2026 at 11:42:07 | [ERROR] Normalisation failed
     -> Look at logs/2026-10-28_11.42.01.004512.log for more information.
    """
    logSave(f"[ERROR] {message}")
    message = color.on_red("[ERROR]") + color.red(f" {message}")

    if etype is None or value is None or tb is None: tb = traceback.format_exc()
    else: tb = ''.join(traceback.format_exception(etype, value, tb))
    logSave(f"Full traceback below.\n\n{tb}")

    logPrint(message + f"\n -> Look at {color.fg.green}{filename}{color.stop} for more information.\n")

# Catch unexpected crashes
def myexcepthook(etype, value, tb):
    """Exception hook installed by :func:`replace_excepthook`: log the uncaught exception with :func:`error`,
    then show Python's usual report unless :data:`hide_traceback` is true.
    """
    global hide_traceback
    error(f"🤕 Uh, there is an unexpected error somewhere: {value} ({etype.__name__})", etype=etype, value=value, tb=tb)
    if not hide_traceback: sys.__excepthook__(etype, value, tb)

def replace_excepthook(value=True):
    """Log uncaught exceptions with :func:`error`; ``value=False`` restores Python's hook.

    Examples
    --------
    >>> from LRFutils import logs
    >>> logs.replace_excepthook()
    >>> logs.hide_traceback = True  # short message in the terminal, full traceback in the log file
    """
    if value: sys.excepthook = myexcepthook
    else: sys.excepthook = sys.__excepthook__