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

    d = []          #
    kAlarm = []     #
    iAlarm = []     #
    aAlarm = []     #
    Delete = []     #

    for i in data:
        d.append(i.frame['Displacement'].dropna().to_numpy())
        t = (i.frame['Time'].drop(i.frame['Displacement'].isna()*range(len(i.frame['Displacement']))).to_numpy())
        dt = t[1]-t[0]

    i = 1
    k = 0
    b = 0
    y = 0
    
    # print(d, "data")
    # print(len(d), "ddd")
    # print(d)
    # print(len(d[k]), "ttt")
    while k != len(d) :
        while i != (len(d[k]) - 500) :
            if d[k][i-1] > d[k][i] and d[k][i-1] != d[k][i] and d[k][i-1] != d[k][i+1] and d[k][i-1] != d[k][i+2] and d[k][i-1] != d[k][i+3] and d[k][i-1] != d[k][i+4] and d[k][i-1] != d[k][i+5] and d[k][i-1] != d[k][i+6]  :
                # print("Positive slope Alarm! i = ", i,"k = ", k)
                iAlarm.append(i) 
                kAlarm.append(k) 
                aAlarm.append(d[k][i])
                b = b +1

            i = i + 1
        
        k = k + 1
        i = 1

    y = 0

    print("What the numbers mean", i, b, k)
    while y != len(aAlarm) :
        # print(aAlarm[y], aAlarm[y-1])
        if aAlarm[y] == aAlarm[y-1]:
            Delete.append(y)
            Delete.append(y - 1)

        y = y + 1
    
    z = 0

    for File in Delete :
        aAlarm[File] = 0 
        iAlarm[File] = 0 
        kAlarm[File] = 0 

    list(filter(lambda a: a != 0, aAlarm))
    list(filter(lambda a: a != 0, iAlarm))
    list(filter(lambda a: a != 0, kAlarm))

    q = 0
    while q != len(kAlarm) :
        plt.plot(d[kAlarm[q]])
        plt.annotate('Positive slope',xy=(iAlarm[q] -1, d[kAlarm[q]][iAlarm[q] -1]), xycoords='data',xytext=(0.1, 0.95), textcoords='axes fraction', arrowprops=dict(arrowstyle="->",connectionstyle="angle3,angleA=0,angleB=-90"),horizontalalignment='right', verticalalignment='top')
        # plt.show()
        q = q + 1

    print("Clip-to-frame||" , "TotalFrameNumber = ", FrameNumber, "TotalWeldsNumber = ", k)
    plt.plot(d[1])
    plt.show()
    TotalWelds = TotalWelds + k
    FrameNumber = FrameNumber +1

# 29 stringers and 13 frames 299 welds
print(y, b)
print(TotalWelds)
print(aAlarm, len(aAlarm))
print(iAlarm, len(iAlarm))
print(kAlarm, len(kAlarm))