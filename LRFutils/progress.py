from . import color
from time import time
import datetime

class Bar():
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

    def __call__(self, progress: float, prefix=None, stop=False):
        if prefix is None: prefix = self.prefix
        else: prefix = str(prefix)

        progress_normed = progress / self.max
        if progress == self.max : stop = True
        c = color.fg.yellow if stop and progress_normed != 1 else color.fg.lightgreen 

        if stop: end = "\n"
        else:    end = "\r"

        if type(progress) == float: progress = round(progress, self.decimals)
        percent  = f" {c}{round(progress_normed*100,self.decimals)                                        if self.decimals > 0 else int(progress_normed*100)}%"
        frac     = f" {color.fg.lightred}{progress}/{self.max}"                                                  if self.max is not None else ''
        eta      = f" {color.stop}eta {color.fg.blue}{self.update_eta(progress)}"                                  if not stop else ''
        duration = f" {color.fg.purple}{str(datetime.timedelta(seconds=time() - self.start_at)).split('.')[0]}"  if self.duration else ''

        prefix  = '' if prefix == '' else color.stop + prefix + ' '
        suffix  = f"{percent}{frac}{duration}{eta}"

        barwidth = self.width - len(color.clear(suffix)) - len(color.clear(prefix))
        barwidth = max(barwidth,10)

        currentBar = int(round(min(progress_normed*barwidth,barwidth)))
        minBar     = int(min(progress_normed*barwidth,barwidth))

        if progress_normed == 0:   bar = color.fg.lightgrey      + '━' * barwidth
        elif progress_normed == 1: bar = color.fg.lightgreen + '━' * barwidth
        elif currentBar == minBar: bar = c + '━' * currentBar       + color.fg.lightgrey      + '╺' + color.fg.lightgrey  + '━' * (barwidth - currentBar - 1)
        else:                      bar = c + '━' * (currentBar - 1) + c + '╸' + color.fg.lightgrey  + '━' * (barwidth - currentBar)

        msg = f"{prefix}{bar}{suffix}{color.stop}"
        print(msg, end=end)

    def stop(self):
        self(self.lastProgress, stop=True)
        self.lastProgress = 0
        self.lastUpdate = None