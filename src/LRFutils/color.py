import re

stop = '\033[0m'
bold = '\033[01m'
disable = '\033[02m'
underline = '\033[04m'
reverse = '\033[07m'
strikethrough = '\033[09m'
invisible = '\033[08m'
 
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
    brightblack = '\033[30;1m'
    brightred = '\033[31;1m'
    brightgreen = '\033[32;1m'
    brightyellow = '\033[33;1m'
    brightblue = '\033[34;1m'
    brightpurple = '\033[35;1m'
    brightcyan = '\033[36;1m'
    brightwhite = '\033[37;1m'

def black(text): return fg.black + text + stop
def red(text): return fg.red + text + stop
def green(text): return fg.green + text + stop
def orange(text): return fg.orange + text + stop
def blue(text): return fg.blue + text + stop
def purple(text): return fg.purple + text + stop
def cyan(text): return fg.cyan + text + stop
def lightgrey(text): return fg.lightgrey + text + stop
def darkgrey(text): return fg.darkgrey + text + stop
def lightred(text): return fg.lightred + text + stop
def lightgreen(text): return fg.lightgreen + text + stop
def yellow(text): return fg.yellow + text + stop
def lightblue(text): return fg.lightblue + text + stop
def pink(text): return fg.pink + text + stop
def lightcyan(text): return fg.lightcyan + text + stop
def brightblack(text): return fg.brightblack + text + stop
def brightred(text): return fg.brightred + text + stop
def brightgreen(text): return fg.brightgreen + text + stop
def brightyellow(text): return fg.brightyellow + text + stop
def brightblue(text): return fg.brightblue + text + stop
def brightpurple(text): return fg.brightpurple + text + stop
def brightcyan(text): return fg.brightcyan + text + stop
def brightwhite(text): return fg.brightwhite + text + stop

class bg:
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    orange = '\033[43m'
    blue = '\033[44m'
    purple = '\033[45m'
    cyan = '\033[46m'
    lightgrey = '\033[47m'

def on_black(text): return bg.black + text + stop
def on_red(text): return bg.red + text + stop
def on_green(text): return bg.green + text + stop
def on_orange(text): return bg.orange + text + stop
def on_blue(text): return bg.blue + text + stop
def on_purple(text): return bg.purple + text + stop
def on_cyan(text): return bg.cyan + text + stop
def on_lightgrey(text): return bg.lightgrey + text + stop

def clear(text):
    text = re.sub("\033\[[0-9][0-9]?m", "", text)
    text = re.sub("\\u001b\[[0-9][0-9]?m", "", text)
    text = re.sub("\\u001b\[[0-9][0-9]?;1m", "", text)
    return text
