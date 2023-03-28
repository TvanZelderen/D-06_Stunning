# Small summary, IT does what it needs to do, but not for the clip to frame. Still need to make a list of border 
# 

from load import Data
from scipy.integrate import simpson
import pandas as pd
from load import iterate_points
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pylab as py

TotalWelds = 0
FrameNumber= 1
while FrameNumber != 13 : 

    data = iterate_points(frames=[FrameNumber] ,type = False)

    d = []
    kAlarm = []
    iAlarm = []
    aAlarm = []

    for i in data:
        d.append(i.frame['Displacement'].dropna().to_numpy())
        t = (i.frame['Time'].drop(i.frame['Displacement'].isna()*range(len(i.frame['Displacement']))).to_numpy())
        dt = t[1]-t[0]
        

    # print(len(d))

    i = 1
    k = 0

    while k != len(d) :
        while i != len(d[k]) :
            if d[k][i-1] > d[k][i] :
                print("Positive slope Alarm! i = ", i,"k = ", k)
                iAlarm.append(i)
                kAlarm.append(k)
                aAlarm.append(d[k][i])
            i = i + 1
        
        k = k + 1
        i = 1

    # print(k, i)
    q = 0
    while q != len(kAlarm) :
        plt.plot(d[kAlarm[q]])
        # print(len(kAlarm))
        # print(q, iAlarm[q])
        # plt.annotate('Positive slope',xy=(iAlarm[q] -1, d[kAlarm[q]][iAlarm[q] -1]), xycoords='data',xytext=(0.1, 0.95), textcoords='axes fraction',
                    # arrowprops=dict(arrowstyle="->",connectionstyle="angle3,angleA=0,angleB=-90"),horizontalalignment='right', verticalalignment='top')
        # plt.show()
        q = q + 1

    
    print("Clip-to-frame||" , "TotalFrameNumber = ", FrameNumber, "TotalWeldsNumber = ", k)
    # plt.plot(d[1])
    plt.show()
    TotalWelds = TotalWelds + k

    FrameNumber = FrameNumber +1
print(TotalWelds)