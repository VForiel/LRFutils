from math import ceil
import os
from .color import Color
from time import time
import datetime
import re

try:
    term_size = os.get_terminal_size()
    term_size = term_size.columns
except: term_size = 80

class progress():
    def __init__(self, max = 1, width = 80, prefix = "", eta = True, decimals = 0, duration = True):
        self.max = max
        self.width = width if type(width) == int else 80
        self.prefix = prefix
        self.eta = eta
        self.decimals = decimals
        self.lastProgress = 0
        self.lastUpdate = None
        self.lastETA = "-"
        self.start_at = time()
        self.duration = duration

    def update_eta(self, progress):
        if self.lastUpdate is not None and time()-self.lastUpdate < 1: return self.lastETA

        progression = progress - self.lastProgress
        left = (self.max-progress)

        if progression == 0 or self.lastUpdate is None:
            self.lastUpdate = time()
            self.lastProgress = progress
            self.lastETA = "-"
            return self.lastETA

        seconds = left/progression * (time() - self.lastUpdate)
        self.lastUpdate = time()
        self.lastProgress = progress
        if seconds < 0: self.lastETA = "-"
        else: self.lastETA = str(datetime.timedelta(seconds=seconds)).split(".")[0]
        return self.lastETA

    def __call__(self, progress: float, stop=False):

        progress_normed = progress / self.max
        if progress == self.max : stop = True
        color = Color.Yellow if stop and progress_normed != 1 else Color.LightGreen 

        if stop: end = Color.NC + "\n"
        else:    end = "\r"

        percent  = f" {color}{round(progress_normed*100,self.decimals)                                        if self.decimals > 0 else int(progress_normed*100)}%"
        frac     = f" {Color.LightRed}{progress}/{self.max}"                                                  if self.max is not None else ''
        eta      = f" {Color.NC}eta {Color.Blue}{self.update_eta(progress)}"                                  if not stop else ''
        duration = f" {Color.Purple}{str(datetime.timedelta(seconds=time() - self.start_at)).split('.')[0]}"  if self.duration else ''

        prefix  = '' if self.prefix == '' else Color.NC + self.prefix + ' '
        suffix  = f"{percent}{frac}{duration}{eta}"

        barwidth = self.width - len(Color.clear(suffix)) - len(Color.clear(prefix))
        barwidth = max(barwidth,10)

        currentBar = int(round(min(progress_normed*barwidth,barwidth)))
        minBar     = int(min(progress_normed*barwidth,barwidth))

        if progress_normed == 0:   bar = Color.White      + '━' * barwidth
        elif progress_normed == 1: bar = Color.LightGreen + '━' * barwidth
        elif currentBar == minBar: bar = color + '━' * currentBar       + Color.White      + '╺' + Color.White + '━' * (barwidth - currentBar - 1)
        else:                      bar = color + '━' * (currentBar - 1) + color + '╸' + Color.White + '━' * (barwidth - currentBar)

        msg = f"{prefix}{bar}{suffix}"
        print(msg, end=end)

    def stop(self):
        self(self.lastProgress, stop=True)
        self.lastProgress = 0
        self.lastUpdate = None