#!/usr/bin/env python
# coding=utf-8

from datetime import datetime
import os
import platform
from LRFutils import color as C
import sys
import traceback

hide_traceback = False

# Get current time as string
def now(human=False, color=False):
    time = str(datetime.now())
    if human:
        if color:
            return f"{C.Blue}{time[8:10]}/{time[5:7]}/{time[0:4]}{C.NC} at {C.Purple}{time[11:13]}:{time[14:16]}:{time[17:19]}{C.NC}"
        else:
            return f"{time[8:10]}/{time[5:7]}/{time[0:4]} at {time[11:13]}:{time[14:16]}:{time[17:19]}"
    else:
        return time.replace(" ", "_").replace(":", ".")

startTime = now()
filename = f"logs/{startTime}.logs"
if not os.path.isdir("logs"): os.makedirs(f"logs/")

# Getting the current environment
with open(filename, "a") as logsFile:
    logsFile.write(f"ENVIRONMENT: {platform.uname()}\n\n")

# Print message in log file
def logSave(message):
    currentTime = now(human = True, color=False)
    with open(filename, "a", encoding="utf-8") as logsFile:
        logsFile.write(f"{currentTime} | {message}\n")

# Print message in terminal
def logPrint(message):
    currentTime = now(human = True, color=True)
    print(f'{currentTime} | {message}')

# Info-styled messages
def info(message):
    logSave(f"[INFO] {message}")
    message = C.Green + "[INFO] " + C.NC + message
    logPrint(message)
    
# Warning-styled messages
def warn(message):
    message = f"[WARNING] {message}"
    logSave(message)
    message = C.Yellow + message + C.NC
    logPrint(message)

# Error-styled messages
def error(message, etype = None, value = None, tb=None):
    message = f"[ERROR] {message}"
    logSave(message)
    message = C.on_Red + message + C.NC

    if etype is None or value is None or tb is None: tb = traceback.format_exc()
    else: tb = ''.join(traceback.format_exception(etype, value, tb))
    logSave(f"Full traceback below.\n\n{tb}")

    logPrint(message + f"\n -> Look at {C.Green}{filename}{C.NC} for more information.\n")

# Catch unexpected crashes
def myexcepthook(etype, value, tb):
    global hide_traceback
    error(f"🤕 Uh, there is an unexpected error somewhere: {value} ({type})", etype=etype, value=value, tb=tb)
    if not hide_traceback: sys.__excepthook__(etype, value, tb)

sys.excepthook = myexcepthook