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
    if not os.path.isdir("logs"):
        os.makedirs(f"logs/")
        # Saving the current environment information
        with open(filename, "a") as logFile:
            logFile.write(f"ENVIRONMENT: {platform.uname()}\n\n")


# Print message in log file
def logSave(message):
    ensure_path()
    currentTime = now(human = True, c=False)
    with open(filename, "a", encoding="utf-8") as logFile:
        logFile.write(f"{currentTime} | {message}\n")

# Print message in terminal
def logPrint(message):
    currentTime = now(human = True, c=True)
    print(f'{currentTime} | {message}')

# Info-styled messages
def info(message):
    logSave(f"[INFO] {message}")
    message = color.green("[INFO] ") + message
    logPrint(message)
    
# Warning-styled messages
def warn(message):
    message = f"[WARNING] {message}"
    logSave(message)
    message = color.yellow(message)
    logPrint(message)

# Error-styled messages
def error(message, etype = None, value = None, tb=None):
    logSave(f"[ERROR] {message}")
    message = color.on_red("[ERROR]") + color.red(f" {message}")

    if etype is None or value is None or tb is None: tb = traceback.format_exc()
    else: tb = ''.join(traceback.format_exception(etype, value, tb))
    logSave(f"Full traceback below.\n\n{tb}")

    logPrint(message + f"\n -> Look at {color.fg.green}{filename}{color.stop} for more information.\n")

# Catch unexpected crashes
def myexcepthook(etype, value, tb):
    global hide_traceback
    error(f"🤕 Uh, there is an unexpected error somewhere: {value} ({type})", etype=etype, value=value, tb=tb)
    if not hide_traceback: sys.__excepthook__(etype, value, tb)

def replace_excepthook(value=True):
    if value: sys.excepthook = myexcepthook
    else: sys.excepthook = sys.__excepthook__