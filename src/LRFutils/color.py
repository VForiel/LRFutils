import re

NC          = '\033[0m'  # No Color, reset all

Bold        = '\033[1m'
Underlined  = '\033[4m'
Blink       = '\033[5m'
Inverted    = '\033[7m'
Hidden      = '\033[8m'

Black       = '\033[30m'
Red         = '\033[31m'
Green       = '\033[32m'
Yellow      = '\033[33m'
Blue        = '\033[34m'
Purple      = '\033[35m'
Cyan        = '\033[36m'
LightGray   = '\033[37m'

Gray         = "\u001b[30;1m"
LightRed     = "\u001b[31;1m"
LightGreen   = "\u001b[32;1m"
LightYellow  = "\u001b[33;1m"
LightBlue    = "\u001b[34;1m"
LightMagenta = "\u001b[35;1m"
LightCyan    = "\u001b[36;1m"
White        = "\u001b[37;1m"


on_Black     = "\u001b[40m"
on_Red       = "\u001b[41m"
on_Green     = "\u001b[42m"
on_Yellow    = "\u001b[43m"
on_Blue      = "\u001b[44m"
on_Magenta   = "\u001b[45m"
on_Cyan      = "\u001b[46m"
on_LightGray = "\u001b[47m"


on_Gray         = "\u001b[40;1m"
on_LightRed     = "\u001b[41;1m"
on_LightGreen   = "\u001b[42;1m"
on_LightYellow  = "\u001b[43;1m"
on_LightBlue    = "\u001b[44;1m"
on_LightMagenta = "\u001b[45;1m"
on_LightCyan    = "\u001b[46;1m"
on_White        = "\u001b[47;1m"

def clear(txt):
    txt = re.sub("\033\[[0-9][0-9]?m", "", txt)
    txt = re.sub("\\u001b\[[0-9][0-9]?m", "", txt)
    txt = re.sub("\\u001b\[[0-9][0-9]?;1m", "", txt)
    return txt