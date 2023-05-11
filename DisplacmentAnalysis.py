from load import Data
from scipy.integrate import simpson
import pandas as pd
from load import iterate_points
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pylab as py
import csv 

# 29 stringers and 13 frames 299 welds

FrameNumber= 1                                      # Integer that tells which frame number is being considered, starting with frame 1.
TypeFile = False                                     # Boolean that tells the program if it needs to get the data from the clip to skin (False) or clip to 
                                                    #frame (True) data.
index_csv = []                                      # A list where the position of the welds is going to be put.
ListOfMaximumValues =[]                             # A list of the maximum values of all the frames.
TotalNegativeDisplacementAlarmABS = []              # A list which contains hwo big the gap is between when a sonotrodes goes below a treshold and when it
                                                    #goes back to the treshold in absolute time.
TotalNegativeDisplacementAlarmREL = []              # A list which contains how big the gap is between when a sonotrodes goes below a treshold and when it 
                                                    #goes back to the treshold in relative time (on a scale from 0 to 10 relative to the other gaps in the
                                                    #fuselage).

# The program iterates all the calcualtions over each frame.
while FrameNumber != 13: 
    data = iterate_points(frames=[FrameNumber] ,type = TypeFile)

    # Definition of all the variabels and constants
    ImportedData = []                               # A list of all the data .
    WeldNumberWithPositiveDisplacement = []         # A list that stores all the weldsnumbers which have a positive displacement.
    TimaAtPositiveDisplacement = []                 # A list that stores all the timestamps of when the weld start to have a psoitive displacement.
    DisplacementValueOfPositiveDisplacement = []    # A list that stores all the displacements of when the weld start to have a positive displacement.
    ListOfLengthsOfPositiveDisplacement = []        # A List of the list of negatives

    Time = 1                                        # Counter for which time it the code is looking for at a given weld (starts at 1 so it can compare welds
                                                    #with the value before it)
    Weldnumber = 0                                  # Counter for which weld is examined
    LengthOfPositiveDisplacement = 0                # Counter to determine how long it takes for the sonotrode to "go back" to the original displacement. 
    w = 0                                           # Counter that stores the original time when a sonotroes goes up. It is used to determine the size of the
                                                    #gap by remembering the original value and comparing it with the next value.
    
    # Pulls the list of displacement values and generates an index list used for the writing of the CSV file part
    for WeldNumberInData in data:   
        ImportedData.append(WeldNumberInData.frame['Displacement'].dropna().to_numpy())
        index_csv.append(repr([WeldNumberInData.frame_no,WeldNumberInData.stringer_no,WeldNumberInData.weld_no,int(WeldNumberInData.type)]))


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


    # Way to circumvent a bug, need to fix later
    if TypeFile == True :       
        IgnoreLength = 1

    else :
        IgnoreLength = 5000

    # The big for loop that cycles through all the welds and dispalcements to find where the sonotrodes goes up
    for Weld in ImportedData :
        while Time != (len(Weld) - IgnoreLength) and (Time < (len(Weld) - IgnoreLength)) :
            # print(Time, (len(Weld) - IgnoreLength))
            if Weld[Time-1] > Weld[Time] :

                # When a positive displacement is found, the length of this needs to be known to determine if it is
                #noise or an indication of a bad weld. Therefore, the length of this negative displacement needs to
                #be calculated. This is done by having a separate while loop that looks for this length. First the
                #treshold is defined by the counter "Time" and then a second counter is used to go through the 
                #displacements and increment the counter until the displacement is equal to the original threshold
                #Then, everything below a certain value is filtered out as this is probably noise. Finally, the 
                #original loop continues from the last "w" value, so it is continuing from the value that equals or
                # is higher than the threshold. The else statement is there to save the coordinates of the negative
                #displacement for the graphs.

                w = Time   
                print(Weld, len(Weld), w, Time)
                while Weld[Time-1] > Weld[w] :
                    LengthOfPositiveDisplacement = LengthOfPositiveDisplacement + 1
                    w = w + 1
                if LengthOfPositiveDisplacement <= 30:
                    LengthOfPositiveDisplacement = 0 
                else :
                    TimaAtPositiveDisplacement.append(Time) 
                    WeldNumberWithPositiveDisplacement.append(Weldnumber) 
                    DisplacementValueOfPositiveDisplacement.append(Weld[Time])

                Time = w

            Time = Time + 1

        # Appending the list with the lengths of positive displacements to get a list which has all the positive displacement lengths 
        ListOfLengthsOfPositiveDisplacement.append(LengthOfPositiveDisplacement)
        LengthOfPositiveDisplacement = 0 
        Weldnumber = Weldnumber + 1

        Time = 1 

    list(filter(lambda a: a != 0, DisplacementValueOfPositiveDisplacement))      # Don't know what it does, but I did it to circumvent a bug, will fix later
    list(filter(lambda a: a != 0, TimaAtPositiveDisplacement))
    list(filter(lambda a: a != 0, WeldNumberWithPositiveDisplacement))

    # To help the human during the debugging proces and to find ways to improve the code, a graph can be made which points to the welds which have
    #a positive displacement. 
    for (WeldNumber, TimeStamp) in zip(WeldNumberWithPositiveDisplacement, TimaAtPositiveDisplacement) :
        plt.plot(ImportedData[WeldNumber])
        plt.annotate('Positive slope',xy=(TimeStamp -1, ImportedData[WeldNumber][TimeStamp -1]), xycoords='data',xytext=(0.1, 0.95), textcoords='axes fraction', arrowprops=dict(arrowstyle="->",connectionstyle="angle3,angleA=0,angleB=-90"),horizontalalignment='right', verticalalignment='top')
        # plt.show()    


    # Printed tekst used for debugging 
    if TypeFile == True :
        StringTypeOfWeld = "Clip-to-frame||"
    elif TypeFile == False :
        StringTypeOfWeld = "Clip-to-skin||"

    print(StringTypeOfWeld , "TotalFrameNumber = ", FrameNumber, "TotalWeldsNumber = ", Weldnumber)

    plt.plot(ImportedData[1])
    # plt.show()

    FrameNumber = FrameNumber + 1
    TotalNegativeDisplacementAlarmABS.append(ListOfLengthsOfPositiveDisplacement)

# The data is now in a raw state meaning that it now knows the exact length of the time the sonotrodes goes below the threshold. This needs to be 
#recalculated to get the relative length. This is needed to give a "grade" to each weld how "bad" it is. First the program finds the max value
#per frame and then finds the maximum value of all the max frame values.
ListOfMaximumValuesPerFrame = []

for MaximumValuePerFrame in TotalNegativeDisplacementAlarmABS :
    ListOfMaximumValuesPerFrame.append(max(MaximumValuePerFrame))

MaximumValueOfTheTotalNetativeDisplacementAlarm = max(ListOfMaximumValuesPerFrame)
FinalFrameNegtiveDisplacementAlarmList = []

for RawAlarmDataFrameList in TotalNegativeDisplacementAlarmABS :
    for RawAlarmDataWeld in RawAlarmDataFrameList :
        FinalFrameNegtiveDisplacementAlarmList.append((RawAlarmDataWeld / MaximumValueOfTheTotalNetativeDisplacementAlarm) * 10)

    TotalNegativeDisplacementAlarmREL.append(FinalFrameNegtiveDisplacementAlarmList)
    FinalFrameNegtiveDisplacementAlarmList = []


# Everything is now calculated and can be writen in a CSV file, that teh perpuse of the next bit of code.
data = TotalNegativeDisplacementAlarmREL  # Redefining the name of the data 

with open('SuperDuperImportantDisplacementMainFinalVersion87FinalFinalReallyFinalV2.csv', 'w') as file:
    writer = csv.writer(file)

    for frame in data :
        for weld in frame :
            writer.writerow([weld])
           










