from load import Data as dt
import numpy as np
import matplotlib.pyplot as plt
from load import *
#boxplot of pressure graphs

atotal = iterate_points(type=1, frames=[2], stringers=range(1,11)) #choose type/frames
fig, axs = plt.subplots(nrows=1, ncols=len(atotal), figsize=(25, 4))

for i, ax in zip(atotal, axs):

    p = i.frame['Pressure'].to_numpy()
    t = i.frame['Time'].to_numpy()
    avg = np.average(p) #average of pressure graphs
    std = np.std(p) #standard deviation of pressure graphs
    n = 2

    p_peak = p[np.where(p > (avg+n*std))]
    t_peak = t[np.where(p > (avg+n*std))]

    ax.boxplot([np.unique(p_peak)])

plt.tight_layout()
plt.show()