import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sc
import pandas as pd
import load as ld
from math import isnan
from load import Data as dt
from shape import *

colors = ['xkcd:red', 'xkcd:green', 'xkcd:blue', 'xkcd:cyan', 'xkcd:magenta', 'xkcd:periwinkle', 'xkcd:dark blue', 'xkcd:light blue', 'xkcd:orange', 'xkcd:lime', 'xkcd:pink', 'xkcd:salmon']

for frame in range(1,13):
    for weld in range(1,7):
        all_peaks = []
        try:
            obj = dt(frame, 20, weld, 1)
        except:
            continue
        else:
            if 'Power' not in obj.frame.keys() or len(obj.frame['Power'].dropna())==0:
                continue
            else:
                obj.smoothing()
                peaks = get_peaks(obj)
                all_peaks += peaks
        #print(str(i)+str(all_peaks))
        if len(all_peaks)!= 0:
            roots, values, second_devs = zip(*all_peaks)
            plt.scatter(roots, values, color=colors[frame-1])
            plt.plot(roots, values, color=colors[frame-1])

plt.show()
