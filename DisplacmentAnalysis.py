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
while FrameNumber != 2 : 

    data = iterate_points(frames=[FrameNumber] ,type = True)

    d = []
    kAlarm = []
    iAlarm = []
    aAlarm = []
    print("e0")
    for i in data:
        d.append(i.frame['Displacement'].dropna().to_numpy())
        t = (i.frame['Time'].drop(i.frame['Displacement'].isna()*range(len(i.frame['Displacement']))).to_numpy())
        dt = t[1]-t[0]

    i = 1
    k = 0
    b = 0
    y = 0

    # while b != len(d):

        # while y != (len(d[b]) - 10) :
        #     d[b][y] = (d[b][y + 1] + d[b][y + 2] + d[b][y + 3] + d[b][y + 4] + d[b][y + 5] + d[b][y + 6] + d[b][y + 7] + d[b][y + 8] )/8
        #     y = y + 1

        # b = b+1
        # y = 0

    while k != len(d) :
        while i != len(d[k]) :
            if d[k][i-1] > d[k][i] and d[k][i] != d[k][i+1] and d[k][i] != d[k][i+2] and d[k][i] != d[k][i+3] :
                print("Positive slope Alarm! i = ", i,"k = ", k)
                iAlarm.append(i)
                kAlarm.append(k)
                aAlarm.append(d[k][i])
            i = i + 1
        
        k = k + 1
        i = 1

    q = 0
    while q != len(kAlarm) :
        plt.plot(d[kAlarm[q]])
        # print(len(kAlarm))
        # print(q, iAlarm[q])
        plt.annotate('Positive slope',xy=(iAlarm[q] -1, d[kAlarm[q]][iAlarm[q] -1]), xycoords='data',xytext=(0.1, 0.95), textcoords='axes fraction', arrowprops=dict(arrowstyle="->",connectionstyle="angle3,angleA=0,angleB=-90"),horizontalalignment='right', verticalalignment='top')
        # plt.show()
        q = q + 1

    
    print("Clip-to-frame||" , "TotalFrameNumber = ", FrameNumber, "TotalWeldsNumber = ", k)
    # plt.plot(d[1])
    plt.show()
    TotalWelds = TotalWelds + k
    FrameNumber = FrameNumber +1


# 29 stringers and 13 frames 300 welds

print(TotalWelds)