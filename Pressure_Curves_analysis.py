from load import Data as dt
import numpy as np
import matplotlib.pyplot as plt
from load import *
a = dt('08', '03', '01', 1) #choose (frame_no, stringer_no, weld_no, type) for pressure graphs


def boxplots(): #boxplots of upper pressure graph peaks
    atotal = iterate_points(type=1, frames=[8], stringers='All', welds = [1]) #choose type, frames, stringers, welds
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

    
        if i == atotal[0]:
            ax.set_ylabel("Pressure peaks [bar]")

        text = f"Weld {i.weld_no}, Stringer {i.stringer_no}, Frame {i.frame_no}"
        ax.text(0.5, -0.2, text, fontsize=6, ha='center', transform=ax.transAxes)

        for i in atotal:
            ax.tick_params(
            axis='x', 
            bottom = False,  
            labelbottom = False)
    
   

    plt.tight_layout()
    plt.show()

def peakvalues(a): #pressure graph, with its corresponding upper peak values and number of upper peak values
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

    return t_peak
    return Vp_peak
    

def peakvalues2(a): #pressure graph, with its corresponding upper and lower peak values and number of upper and lower peak values
    a.create_array()

    p = a.frame['Pressure'].to_numpy()
    t = a.frame['Time'].to_numpy()
    avg = np.average(p) #average of pressure graphs
    std = np.std(p) #standard deviation of pressure graphs
    n = 2

    p_peak_high = p[np.where(p > (avg+n*std))]
    t_peak_high = t[np.where(p > (avg+n*std))]

    p_peak_low = p[np.where(p < (avg-n*std))]
    t_peak_low = t[np.where(p < (avg-n*std))]

    p_peak_merged = np.concatenate((p_peak_high, p_peak_low))
    t_peak_merged = np.concatenate((t_peak_high, t_peak_low))


    Np_peak_merged = len(np.unique(p_peak_merged)) #number of peaks in merged pressure graph
    Vp_peak_merged = np.unique(p_peak_merged) #array of peak values for merged pressure

    plt.scatter(t_peak_merged, p_peak_merged)
    print("The merged peak values are:", Vp_peak_merged)
    print("The number of merged peak values are:", Np_peak_merged)

    plt.plot(t, p)
    plt.show()


def boxplots2(): #boxplots of upper and lower pressure graph peaks
    atotal = iterate_points(type=1, frames='All', stringers='05', welds = [1]) #choose type, frames, stringers, welds
    fig, axs = plt.subplots(nrows=1, ncols=len(atotal), figsize=(25, 4))

    for i, ax in zip(atotal, axs):

        p = i.frame['Pressure'].to_numpy()
        t = i.frame['Time'].to_numpy()
        avg = np.average(p) #average of pressure graphs
        std = np.std(p) #standard deviation of pressure graphs
        n = 2

        p_peak_high = p[np.where(p > (avg+n*std))]

        p_peak_low = p[np.where(p < (avg-n*std))]

        p_peak_merged = np.concatenate((p_peak_high, p_peak_low))

        Vp_peak_merged = np.unique(p_peak_merged) #array of peak values for merged pressure

        ax.boxplot([np.unique(Vp_peak_merged)])

    
        if i == atotal[0]:
            ax.set_ylabel("Pressure peaks [bar]")

        text = f"Weld {i.weld_no}, Stringer {i.stringer_no}, Frame {i.frame_no}"
        ax.text(0.5, -0.2, text, fontsize=6, ha='center', transform=ax.transAxes)

        for i in atotal:
            ax.tick_params(
            axis='x', 
            bottom = False,  
            labelbottom = False)
    
   

    plt.tight_layout()
    plt.show()


boxplots()
#peakvalues(a)
#peakvalues2(a)
#boxplots2()