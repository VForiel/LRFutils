# ⌛ Progress

This module allow to create a progress bar when you are performing a long task.

## Example
```python
from LRFutils import progress
from time import time

N = 1000
# creation
myBar = progress.bar(max = N, width = 80, prefix = "Demo progress bar", eta = True, decimals = 0, duration = True)

for i in range(N)
    # update
    myBar(i)
    time.sleep(0.01)
```

---

## Class attributes

Nothing here...

---

## Class methods

### Builder

Create a progress bar object

```python
progress.Bar(max = 1, width = 80, prefix = "", eta = True, decimals = 0, duration = True)
```
**Parameters:**
- `max : float` maximum value of the bar. By default, this value is 1, so you have to update the bar using a ratio.
- `widht : int` bar's total lenght (80 characters by default)
- `prefix : str` short message displayed before the bar
- `eta : boolean` display or not the estimation of remaining time
- `decimals : int` number of decimals showed for the percentage
- `duration : boolean` display or not the spent time

**Return types:**
- `Bar` progress bar object

---

## Object attributes

- `max : float` maximum value of the bar. By default, this value is 1, so you have to update the bar using a ratio.
- `widht : int` bar's total lenght (80 characters by default)
- `prefix : str` short message displayed before the bar
- `eta : boolean` display or not the estimation of remaining time
- `decimals : int` number of decimals showed for the percentage
- `duration : boolean` display or not the spent time
- `lastProgress : float` last recorded `progress` value
- `lastUpdate : float` date (in second) of the last update
- `start_at : float` date (in second) of the creation of the bar
- `lastETA : float | str` last estimation of remaining time (in second). If there is no previous one, lastETA store `"-"`

---

## Object methods

### Updater
Update the bar (print it in the terminal)
```python
myBar(progress: float, prefix=None, stop=False)
```

**Parameters:**
- `progress : float` the progression of the computation. Tha bar will be filed according to the ratio `progress / max`
- `prefix : str` short message displayed before the bar

> Note: if the `progress` reach the `max` value, the bar will automatically stop. A running progress bar ends with a '\r' character in order to be overwritten by the next update. When the bar is stopped, the printed line ends with '\n' so you can continue to print other stuff. If you update the bar after the bar stoped, it will display a new bar.

**Return types:** None

### Force stop

Update and stop the bar by putting it in an incomplet mode.

```python
stop()
```

> Once a bar is stopped, the line cannot be overwritten, so it cannot be updated anymore. If you update the bar, it will display a new bar.

**Parameters:** None

**Return types:** None


