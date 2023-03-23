from load import Data as dt
import numpy as np
import matplotlib.pyplot as plt
from load import *



def boxplots(): #boxplots of pressure graph peaks
    atotal = iterate_points(type=1, frames=[8], stringers='All', welds = [1])
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

        text = f"Weld {i.weld_no}, Stringer {i.stringer_no}, Frame {i.frame_no}"
        ax.text(0.5, -0.2, text, fontsize=6, ha='center', transform=ax.transAxes)

    plt.tight_layout()
    plt.show()

def peakvalues(): #pressure graphs, with its corresponding peak values and number of peak values
    a = dt('08', '03', '01', 1) #choose (frame_no, stringer_no, weld_no, type)
    a.create_array()

    p = a.frame['Pressure'].to_numpy()
    t = a.frame['Time'].to_numpy()
    avg = np.average(p) #average of pressure graphs
    std = np.std(p) #standard deviation of pressure graphs
    n = 2

    p_peak = p[np.where(p > (avg+n*std))]
    t_peak = t[np.where(p > (avg+n*std))]


    Np_peak = len(np.unique(p_peak)) #number of peaks in pressure graph
    Vp_peak = np.unique(p_peak) #array of peak values pressure

    plt.scatter(t_peak, p_peak)
    print("The peak values are:", Vp_peak)
    print("The number of peak values are:", Np_peak)

    plt.plot(t, p)
    plt.show()

boxplots()