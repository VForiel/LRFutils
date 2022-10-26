from . import color
from time import time
import datetime

class Bar():



    # ________________________________________________________________________________
    # Create a progress bar

    def __init__(self, max:float|int = 1, width:int = 80, prefix:str = "", eta:bool = True,  decimals:int = 0, show_duration:bool = True, average_ETA:int = 10):
        self.max = max
        self.width = width if isinstance(width,int) else 80
        self.prefix = prefix
        self.eta = eta
        self.decimals = decimals
        self.previous_progress = [0]
        self.previous_update = []
        self.lastETA = "-"
        self.start_at = time()
        self.duration = show_duration
        self.average_ETA = average_ETA


    # ________________________________________________________________________________
    # Compute the ETA

    def update_eta(self, progress):

        # Get index of the i-th revious update to average the ETA on i updates
        if len(self.previous_progress) <= self.average_ETA:
            i = 0
        else:
            i = -self.average_ETA

         # Compute progression since the i-th previous update
        progression = progress - self.previous_progress[i]
        todo = self.max - progress

        # If there is no progression or the bar was just created, it update the data but return the same ETA
        if progression == 0 or self.previous_update == []:
            self.previous_update.append(time())
            self.previous_progress.append(progress)
            self.lastETA = "-"
            return self.lastETA

        # If the bar was updated less than one second before,
        # we don't update it again to not slow the program
        if time()-self.previous_update[-1] < 1:
            return self.lastETA

        # Compute the ETA in seconds
        try:
            seconds = todo / progression * (time() - self.previous_update[i])
        except:
            print(len(self.previous_update), i)

        # Update bar data
        self.previous_update.append(time())
        self.previous_progress.append(progress)

        # If the ETA is negative, then we show an undefined ETA
        if seconds < 0:
            self.lastETA = "-"
        # Else we return the number of seconds
        else:
            self.lastETA = str(datetime.timedelta(seconds=seconds)).split(".")[0]
        
        return self.lastETA

    

    # ________________________________________________________________________________
    # Update the progress bar

    def __call__(self, progress: float, prefix=None, stop=False):
        if prefix is None: prefix = self.prefix
        else: prefix = str(prefix)

        progress_normed = progress / self.max
        if progress == self.max : stop = True
        color_bar = color.Yellow if stop and progress_normed != 1 else color.LightGreen 

        if stop: end = "\n"
        else:    end = "\r"

        if type(progress) == float: progress = round(progress, self.decimals)
        percent  = f" {color_bar}{round(progress_normed*100,self.decimals)                                        if self.decimals > 0 else int(progress_normed*100)}%"
        frac     = f" {color.LightRed}{progress}/{self.max}"                                                  if self.max is not None else ''
        eta      = f" {color.NC}eta {color.Blue}{self.update_eta(progress)}"                                  if not stop else ''
        duration = f" {color.Purple}{str(datetime.timedelta(seconds=time() - self.start_at)).split('.')[0]}"  if self.duration else ''

        prefix  = '' if prefix == '' else color.NC + prefix + ' '
        suffix  = f"{percent}{frac}{duration}{eta}"

        barwidth = self.width - len(color.clear(suffix)) - len(color.clear(prefix))
        barwidth = max(barwidth,10)

        currentBar = int(round(min(progress_normed*barwidth,barwidth)))
        minBar     = int(min(progress_normed*barwidth,barwidth))

        if progress_normed == 0:   bar = color.White      + '━' * barwidth
        elif progress_normed == 1: bar = color.LightGreen + '━' * barwidth
        elif currentBar == minBar: bar = color_bar + '━' * currentBar       + color.White      + '╺' + color.White + '━' * (barwidth - currentBar - 1)
        else:                      bar = color_bar + '━' * (currentBar - 1) + color_bar + '╸' + color.White + '━' * (barwidth - currentBar)

        msg = f"{prefix}{bar}{suffix}{color.NC}"
        print(msg, end=end)



    # ________________________________________________________________________________
    # Stop the progress bar

    def stop(self):
        self(self.previous_progress[-1], stop=True)
        self.previous_progress = [0]
        self.lastUpdate = None