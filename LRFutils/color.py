import re

def clear(text):
    txt = re.sub("\033\[[0-9][0-9]?m", "", text)
    txt = re.sub("\\u001b\[[0-9][0-9]?m", "", text)
    txt = re.sub("\\u001b\[[0-9][0-9]?;1m", "", text)
    return txt

def black(text): return '\033[30m' + text + '\033[0m'
def red(text): return '\033[31m' + text + '\033[0m'
def green(text): return '\033[32m' + text + '\033[0m'
def yellow(text): return '\033[33m' + text + '\033[0m'
def blue(text): return '\033[34m' + text + '\033[0m'
def purple(text): return '\033[35m' + text + '\033[0m'
def cyan(text): return '\033[36m' + text + '\033[0m'
def lightgrey(text): return '\033[37m' + text + '\033[0m'
def darkgrey(text): return '\033[90m' + text + '\033[0m'
def lightred(text): return '\033[91m' + text + '\033[0m'
def lightgreen(text): return '\033[92m' + text + '\033[0m'
def yellow(text): return '\033[93m' + text + '\033[0m'
def lightblue(text): return '\033[94m' + text + '\033[0m'
def pink(text): return '\033[95m' + text + '\033[0m'
def lightcyan(text): return '\033[96m' + text + '\033[0m'

def bold(text): return '\033[01m' + text + '\033[0m'
def disable(text): return '\033[02m' + text + '\033[0m'
def underline(text): return '\033[04m' + text + '\033[0m'
def reverse(text): return '\033[07m' + text + '\033[0m'
def strikethrough(text): return '\033[09m' + text + '\033[0m'
def invisible(text): return '\033[08m' + text + '\033[0m'

def on_black(text): return '\033[40m' + text + '\033[0m'
def on_red(text): return '\033[41m' + text + '\033[0m'
def on_green(text): return '\033[42m' + text + '\033[0m'
def on_yellow(text): return '\033[43m' + text + '\033[0m'
def on_blue(text): return '\033[44m' + text + '\033[0m'
def on_purple(text): return '\033[45m' + text + '\033[0m'
def on_cyan(text): return '\033[46m' + text + '\033[0m'
def on_lightgrey(text): return '\033[47m' + text + '\033[0m'

stop = '\033[0m'
class fg:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'

class bg:
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    orange = '\033[43m'
    blue = '\033[44m'
    purple = '\033[45m'
    cyan = '\033[46m'
    lightgrey = '\033[47m'