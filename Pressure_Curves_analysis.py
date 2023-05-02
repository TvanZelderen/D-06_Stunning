from load import Data as dt
import numpy as np
import matplotlib.pyplot as plt
from load import *
import pandas as pd
from scipy.integrate import trapz
a = dt('03', '02', '01', 1) #choose (frame_no, stringer_no, weld_no, type) for pressure graphs

def boxplots(): #boxplots of upper pressure graph peaks
    atotal = iterate_points(type=1, frames='03', stringers='All', welds = [1]) #choose type, frames, stringers, welds
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
        ax.text(0.5, -0.2, text, fontsize=5, ha='center', transform=ax.transAxes)

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
    atotal = iterate_points(type=1, frames='03', stringers='All', welds = [1]) #choose type, frames, stringers, welds
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
        ax.text(0.5, -0.2, text, fontsize=5, ha='center', transform=ax.transAxes)

        for i in atotal:
            ax.tick_params(
            axis='x', 
            bottom = False,  
            labelbottom = False)
    
   

    plt.tight_layout()
    plt.show()
    
def boxplots22(): 
    atotal = iterate_points(type='01', frames='03', stringers='All', welds='01') 
    fig, axs = plt.subplots(nrows=1, ncols=len(atotal), figsize=(25, 4))
    outliers_list = []  # initialize an empty list to store outliers

    for i, ax in zip(atotal, axs):
        p = i.frame['Pressure'].to_numpy()
        t = i.frame['Time'].to_numpy()
        avg = np.average(p)
        std = np.std(p)
        n = 2

        p_peak_high = p[np.where(p > (avg+n*std))]
        p_peak_low = p[np.where(p < (avg-n*std))]
        p_peak_merged = np.concatenate((p_peak_high, p_peak_low))
        Vp_peak_merged = np.unique(p_peak_merged)

        # identify outliers and append information to the list
        box = ax.boxplot([np.unique(Vp_peak_merged)])
        outliers = box["fliers"][0].get_data()[1]
        if len(outliers) > 0:
            outliers_list.append({
                'type': i.type,
                'frame': i.frame_no,
                'stringer': i.stringer_no,
                'weld': i.weld_no
            })
        if i == atotal[0]:
            ax.set_ylabel("Pressure peaks [bar]")
        text = f"Weld {i.weld_no}, Stringer {i.stringer_no}, Frame {i.frame_no}"
        ax.text(0.5, -0.2, text, fontsize=5, ha='center', transform=ax.transAxes)
        for i in atotal:
            ax.tick_params(
                axis='x', 
                bottom=False,  
                labelbottom=False
            )

    plt.tight_layout()
    plt.show()

    for item in outliers_list:
        outlists = [np.array([item['type'], item['weld'], item['stringer'], item['frame']])]

        for outlist in outlists:
            print(outlist)
            return(outlist)

#with open('suspectwelds_pressure.txt', 'w') as f:
    #print(f'Opened {f.name} for writing')
    #for i in suspectwelds_2:
        #f.write(str(i)+'\n')


#boxplots()  #boxplots of upper pressure peaks
#peakvalues(a)  #plots of pressure peaks with upper maximum values
#peakvalues2(a) #plots of pressure peaks with upper and lower maximum values
boxplots22() #boxplots of upper and lower pressure peaks