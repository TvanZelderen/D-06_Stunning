import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sc
import pandas as pd
import load as ld
from math import isnan
from load import Data as dt
from shape import *

for i in range(1,13):
    all_peaks = []
    for a in range(1,7):
        try:
            obj = dt(i, 2, a, 1)
        except:
            continue
        else:
            if 'Power' not in obj.frame.keys() or len(obj.frame['Power'].dropna())==0:
                continue
            else:
                obj.smoothing()
                peaks = get_peaks(obj)
                all_peaks += peaks
    print(str(i)+str(all_peaks))
    if len(all_peaks)!= 0:
        roots, values, second_devs = zip(*all_peaks)
        plt.scatter(roots, values)
plt.show()
    
