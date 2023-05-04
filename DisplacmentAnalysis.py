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
TypeFile = True
index_csv = []

while FrameNumber != 13: 
    data = iterate_points(frames=[FrameNumber] ,type = TypeFile)

    d = []           #
    kAlarm = []      #
    iAlarm = []      #
    aAlarm = []      #
    k2Alarm = []     #
    i2Alarm = []     #
    a2Alarm = []     #
    Delete = []      #
    uAlarm = []      # length of the neagtive
    wAlarm = []      # List of the list of negatoves

    for i in data:
        d.append(i.frame['Displacement'].dropna().to_numpy())
        index_csv.append(repr([i.frame_no,i.stringer_no,i.weld_no,int(i.type)]))

    i = 1
    k = 0
    b = 0
    y = 0
    
    while k != len(d) :
            while i != (len(d[k])) :
                if d[k][i] >= 5 :
                    # print("Very big graph!", " k = ", k) 
                    k2Alarm.append(k) 
                    a2Alarm.append(d[k][i])
                    b = b +1

                i = i + 1
            
            k = k + 1
            i = 1

    i = 1
    k = 0
    b = 0
    y = 0

    if TypeFile == True :
        IgnoreLength = 1

    else :
        IgnoreLength = 6000

    u = 0
    v = 0

    if d[k][i-1] > d[k][i] :
        w = i 
        while d[k][i] > d[k][w] :
            u = u + 1
            w = w + 1

        uAlarm.append(u)
        u = 0

    while k != len(d) :
        while i != (len(d[k]) - IgnoreLength) :
            if d[k][i-1] > d[k][i]   :
                iAlarm.append(i) 
                kAlarm.append(k) 
                aAlarm.append(d[k][i])

                if d[k][i-1] > d[k][i] :
                    w = i 

                    while d[k][i-1] > d[k][w] :
                        u = u + 1
                        w = w + 1

                    uAlarm.append(k)
                    uAlarm.append(i)
                    uAlarm.append(u)
                    wAlarm.append(uAlarm)
                    uAlarm = []
                    u = 0

                b = b +1

            i = i + 1
        
        k = k + 1
        i = 1

    y = 0

    print("What the numbers mean", i, b, k)
    while y != len(aAlarm) :
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
    list(filter(lambda a: a != 0, k2Alarm))

    q = 0
    while q != len(kAlarm) :
        plt.plot(d[kAlarm[q]])
        plt.annotate('Positive slope',xy=(iAlarm[q] -1, d[kAlarm[q]][iAlarm[q] -1]), xycoords='data',xytext=(0.1, 0.95), textcoords='axes fraction', arrowprops=dict(arrowstyle="->",connectionstyle="angle3,angleA=0,angleB=-90"),horizontalalignment='right', verticalalignment='top')
        # plt.show()
        q = q + 1

    print("Clip-to-frame||" , "TotalFrameNumber = ", FrameNumber, "TotalWeldsNumber = ", k)
    plt.plot(d[1])
    # plt.show()
    TotalWelds = TotalWelds + k
    FrameNumber = FrameNumber +1

# 29 stringers and 13 frames 299 welds
print(uAlarm)
print(wAlarm)
