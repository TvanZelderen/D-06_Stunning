import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sc
import pandas as pd
import load as ld
from math import isnan
from load import Data as dt
from shape import *

for i in range():
    all_peaks = []
    for a in range():
        obj = dt(i, 1, a, 1)
        obj.smoothing()
        peaks = get_peaks(obj)
        all_peaks += peaks
    roots, values, second_devs = zip(*all_peaks)
    plt.scatter(roots, values)
plt.show()
    
