from load import Data
from scipy.integrate import simpson
import pandas as pd
from load import iterate_points
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pylab as py
import csv 

TotalNegativeDisplacementAlarm = []
FrameNumber= 1                                      # The frame number that is beaing considered, starting with frame 1.
TypeFile = True                                     # Tells the program if it needs to choose between clip to skin (False) or clip to frame (True)
index_csv = []                      
ListOfMaximumValues =[]                             # List of the maximum values of all the frames.
TotalNegativeDisplacementAlarmList1 = []            
TotalNegativeDisplacementAlarmList2 = []


while FrameNumber != 13: 
    data = iterate_points(frames=[FrameNumber] ,type = TypeFile)

    d = []           # all data 
    kAlarm = []      # A variabel that I only use to find which graphs have positive displacement for the annotated graph, it gives the weld position
    iAlarm = []      # A variabel that I only use to find which graphs have positive displacement for the annotated graph, it goves the frame position
    aAlarm = []      # If the program finds there is a positive displacement, it stores the value of this positive dispalcment in here for further analaysis
    uAlarm = []      # List of u values (see u)
    wAlarm = []      # List of the list of negatives

    for i in data:
        d.append(i.frame['Displacement'].dropna().to_numpy())
        index_csv.append(repr([i.frame_no,i.stringer_no,i.weld_no,int(i.type)]))

    i = 1  # Counter for which weld it is looking in a given "k" frame
    k = 0  # Counter for which frame it
    q = 0  # Counter used in the annotated graph while loop to tell which frame I am using
    u = 0  # How long it takes for the sonotrode to "go back" to the original displacement. 
    w = 0  # Counter that stores the original time when a sonotroes goes up. It is used to determine the size of the gap by remembering the original value and comparing it with the next value.
    
    # while k != len(d) :
    #         while i != (len(d[k])) :
    #             if d[k][i] >= 3 :
    #                 print("Very big graph!", " k = ", k, "Value is = ", d[k][i]) 
    #                 k2Alarm.append(k) 
    #                 a2Alarm.append(d[k][i])
    #                 b = b +1

    #             i = i + 1
            
    #         k = k + 1
    #         i = 1



    if TypeFile == True :       # Way to circumvent a bug, need to fix later
        IgnoreLength = 1

    else :
        IgnoreLength = 1000
  
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

                    if u <= 5 :
                        u = 0 

            i = i + 1

        wAlarm.append(u)
        u = 0 
        k = k + 1
        i = 1

    list(filter(lambda a: a != 0, aAlarm))
    list(filter(lambda a: a != 0, iAlarm))
    list(filter(lambda a: a != 0, kAlarm))

    while q != len(kAlarm) :
        plt.plot(d[kAlarm[q]])
        plt.annotate('Positive slope',xy=(iAlarm[q] -1, d[kAlarm[q]][iAlarm[q] -1]), xycoords='data',xytext=(0.1, 0.95), textcoords='axes fraction', arrowprops=dict(arrowstyle="->",connectionstyle="angle3,angleA=0,angleB=-90"),horizontalalignment='right', verticalalignment='top')
        # plt.show()
        q = q + 1

    print("Clip-to-frame||" , "TotalFrameNumber = ", FrameNumber, "TotalWeldsNumber = ", k)
    plt.plot(d[1])
    # plt.show()
    FrameNumber = FrameNumber +1
    TotalNegativeDisplacementAlarm.append(wAlarm)

x = 0
while x != len(TotalNegativeDisplacementAlarm) :
    ListOfMaximumValues.append(max(TotalNegativeDisplacementAlarm[x]))
    x = x + 1

MaximumMaximum = max(ListOfMaximumValues)
 
First = 0 
Second = 0

while First != len(TotalNegativeDisplacementAlarm) :
    while Second != len(TotalNegativeDisplacementAlarm[First]) :
        Finalvalue = (TotalNegativeDisplacementAlarm[First][Second] / MaximumMaximum)*10
        TotalNegativeDisplacementAlarmList1.append(Finalvalue)
        Second  = Second + 1

    Second = 0
    TotalNegativeDisplacementAlarmList2.append(TotalNegativeDisplacementAlarmList1)
    TotalNegativeDisplacementAlarmList1 = []
    First = First + 1    
    

# 29 stringers and 13 frames 299 welds

data = TotalNegativeDisplacementAlarmList2

with open('SuperDuperImportantDisplacementMainFinalVersion87FinalFinalReallyFinalV2.csv', 'w') as file:
     writer = csv.writer(file)


with open('SuperDuperImportantDisplacementMainFinalVersion87FinalFinalReallyFinalV2.csv', 'w') as file:
    writer = csv.writer(file)

    for frame in data :
        for weld in frame :
            writer.writerow([weld])
           










