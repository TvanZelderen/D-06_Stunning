from load import Data
from scipy.integrate import simpson
import pandas as pd
from load import iterate_points
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pylab as py
import csv 

# 29 stringers and 12 frames 299 welds

FrameNumber= 1                                      # Integer that tells which frame number is being considered, starting with frame 1.
TypeFile = True                                    # Boolean that tells the program if it needs to get the data from the clip to skin (False) or clip to 
                                                    #frame (True) data.
index_csv = []                                      # A list where the position of the welds is going to be put.
ListOfMaximumValues =[]                             # A list of the maximum values of all the frames.
TotalNegativeDisplacementAlarmABS = []              # A list which contains how big the gap is between when a sonotrodes goes below a treshold and when it
                                                    #goes back to the treshold in absolute time.
TotalNegativeDisplacementAlarmREL = []              # A list which contains how big the gap is between when a sonotrodes goes below a treshold and when it 
                                                    #goes back to the treshold in relative time (on a scale from 0 to 10 relative to the other gaps in the
                                                    #fuselage).
DisplacementAnomalyList = []                        # A list which has a list with all the framenumbers and weld number of welds which have an abnormal 
                                                    #high displacement (Normally welds have a displacement below 2, the abonormal weld often have a 
                                                    # displacement in range fo 5 - 20)
AllReadyInDisplacementAnomalyList = False            # Boolean that tells the code if a weld is already in the DispalcementAnomalyList                                                    
DisplacementAnomalyDeptOfDisplacementList = []      # List of how high the sonotrode went during psoitive dispalcement
ListOfAreasOfPositiveDisplacement = []        # A List of the list of negatives
SumOfPositiveDisplacementScoresAlongFrame = []  # A list which sums all the scores of the welds along a frame, request for Wei Wei
SumOfVeryHighDisplacementScoresAlongFrame = []  # Same as above

# The program iterates all the calculation over each frame.
while FrameNumber != 13: 
    data = iterate_points(frames=[FrameNumber] ,type = TypeFile)
    
    # Definition of all the variabels and constants
    ImportedData = []                               # A list of all the data .
    WeldNumberWithPositiveDisplacement = []         # A list that stores all the weldsnumbers which have a positive displacement.
    TimeAtPositiveDisplacement = []                 # A list that stores all the timestamps of when the weld start to have a psoitive displacement.
    DisplacementValueOfPositiveDisplacement = []    # A list that stores all the displacements of when the weld start to have a positive displacement.

    Time = 1                                        # Counter for which time it the code is looking for at a given weld (starts at 1 so it can compare welds
                                                    #with the value before it)
    Weldnumber = 0                                  # Counter for which weld is examined
    LengthOfPositiveDisplacement = 0                # Counter to determine how long it takes for the sonotrode to "go back" to the original displacement. 
    w = 0                                           # Counter that stores the original time when a sonotroes goes up. It is used to determine the size of the
                                                    #gap by remembering the original value and comparing it with the next value.
    DispalcementDuringPositiveDisplacement = []     # A list of how much the sosnotrode goes up during a weld where there is positive displacement
    SumOfPositiveDisplacementScore = 0              # A float which sums all scores of all the welds for a particular frame, request from Wei Wei
    SumOfVeryHighDisplacementScore = 0              # Same as above
    
    # Pulls the list of displacement values and generates an index list used for the writing of the CSV file part
    for WeldNumberInData in data:   
        ImportedData.append(WeldNumberInData.frame['Displacement'].dropna().to_numpy())
        index_csv.append(repr([WeldNumberInData.frame_no,WeldNumberInData.stringer_no,WeldNumberInData.weld_no,int(WeldNumberInData.type)]))


    # The big for loop that cycles through all the welds and displacement to find where the sonotrodes goes up |OUTDATED
    for Weld in ImportedData :        
        AreaOfPositiveDisplacement = 0

        while (Time < (len(Weld) - 1)) :

            if Weld[Time] > 3 and AllReadyInDisplacementAnomalyList == False:
                IndentificationOfWeldList = [FrameNumber, Weldnumber]
                DisplacementAnomalyList.append(10)
                AllReadyInDisplacementAnomalyList = True
                SumOfVeryHighDisplacementScore = SumOfVeryHighDisplacementScore + 10
            
            if Weld[Time-1] > Weld[Time] :

                # When a positive displacement is found, the length of this needs to be known to determine if it is
                #noise or an indication of a bad weld. Therefore, the length of this negative displacement needs to
                #be calculated. This is done by having a separate while loop that looks for this length. First the
                #treshold is defined by the counter "Time" and then a second counter is used to go through the 
                #displacements and increment the counter until the displacement is equal to the original threshold
                #Then, everything below a certain value is filtered out as this is probably noise. Finally, the 
                #original loop continues from the last "w" value, so it is continuing from the value that equals or
                # is higher than the threshold. The else statement is there to save the coordinates of the negative
                #displacement for the graphs. |OUTDATED

                w = Time   
                OriginalDispalcement = Weld[Time-1]
                ReferenceDispalcement = Weld[Time]
                
                while Weld[Time-1] > Weld[w] and w < (len(Weld)-1) and TypeFile == True: # The reasons it ignores the false welds is because there are no wierd positive displacements (Frank has checked it manually)
                    LengthOfPositiveDisplacement = LengthOfPositiveDisplacement + 1
                    w = w + 1
                    if ReferenceDispalcement > Weld[w] :
                        ReferenceDispalcement = Weld[w]
                
                if LengthOfPositiveDisplacement <= 30:
                    LengthOfPositiveDisplacement = 0 

                elif Weld[Time-2] == Weld[Time] or Weld[Time-3] == Weld[Time] or Weld[Time-4] == Weld[Time] or Weld[Time-5] == Weld[Time] or Weld[Time-6] == Weld[Time] or Weld[Time-7] == Weld[Time] or Weld[Time-8] == Weld[Time] or Weld[Time-9] == Weld[Time] or Weld[Time-10] == Weld[Time]:
                    LengthOfPositiveDisplacement = 0
                
                elif Time < 500 :
                    LengthOfPositiveDisplacement = 0
                
                elif LengthOfPositiveDisplacement > 1000 :
                    LengthOfPositiveDisplacement = 0

                else :
                    TimeAtPositiveDisplacement.append(Time) 
                    WeldNumberWithPositiveDisplacement.append(Weldnumber) 
                    DisplacementValueOfPositiveDisplacement.append(Weld[Time])
                    AreaOfPositiveDisplacement = (OriginalDispalcement-ReferenceDispalcement) * LengthOfPositiveDisplacement
                SumOfPositiveDisplacementScore = SumOfPositiveDisplacementScore + AreaOfPositiveDisplacement

                Time = w

            Time = Time + 1

        # Appending the list with the lengths of positive displacements to get a list which has all the positive displacement lengths 
        ListOfAreasOfPositiveDisplacement.append(AreaOfPositiveDisplacement)
        LengthOfPositiveDisplacement = 0 
        if AllReadyInDisplacementAnomalyList == False :
            DisplacementAnomalyList.append(0)

        Weldnumber = Weldnumber + 1
        AllReadyInDisplacementAnomalyList = False   

        Time = 1 

    list(filter(lambda a: a != 0, DisplacementValueOfPositiveDisplacement))      # Don't know what it does, but I did it to circumvent a bug, will fix later
    list(filter(lambda a: a != 0, TimeAtPositiveDisplacement))
    list(filter(lambda a: a != 0, WeldNumberWithPositiveDisplacement))

    # To help the human during the debugging proces and to find ways to improve the code, a graph can be made which points to the welds which have
    #a positive displacement. 
    xtab = []
    CounterForXtab = 0
    while CounterForXtab < 10 :
        CounterForXtab = round(CounterForXtab + 0.001, 3)
        xtab.append(CounterForXtab)

    for (WeldNumber, TimeStamp, Weldnumber2) in zip(WeldNumberWithPositiveDisplacement, TimeAtPositiveDisplacement, WeldNumberWithPositiveDisplacement) :
        plt.plot(xtab, ImportedData[WeldNumber])
        plt.xlabel('Time [s]')
        plt.ylabel('Displacement [mm]')
        plt.annotate('Positive slope',xy=(TimeStamp -1, ImportedData[WeldNumber][TimeStamp -1]), xycoords='data',xytext=(0.2, 0.95), textcoords='axes fraction', arrowprops=dict(arrowstyle="->",connectionstyle="angle3,angleA=0,angleB=-90"),horizontalalignment='right', verticalalignment='top')
        # print(FrameNumber, Weldnumber2)
        # plt.show()    

    # Printed tekst used for debugging 
    if TypeFile == True :
        StringTypeOfWeld = "Clip-to-frame||"
    elif TypeFile == False :
        StringTypeOfWeld = "Clip-to-skin||"

    print(StringTypeOfWeld , "TotalFrameNumber = ", FrameNumber, "TotalWeldsNumber = ", Weldnumber)

    plt.plot(ImportedData[1])
    # plt.show()
    SumOfPositiveDisplacementScoresAlongFrame.append(SumOfPositiveDisplacementScore)
    SumOfVeryHighDisplacementScoresAlongFrame.append(SumOfVeryHighDisplacementScore)
    FrameNumber = FrameNumber + 1
    TotalNegativeDisplacementAlarmABS.append(ListOfAreasOfPositiveDisplacement)

# The data is now in a raw state meaning that it now knows the exact length of the time the sonotrodes goes below the threshold. This needs to be 
#recalculated to get the relative length. This is needed to give a "grade" to each weld how "bad" it is. First the program finds the max value
#per frame and then finds the maximum value of all the max frame values.
ListOfMaximumValuesPerFrame = []

for MaximumValuePerFrame in TotalNegativeDisplacementAlarmABS :
    ListOfMaximumValuesPerFrame.append(max(MaximumValuePerFrame))

MaximumValueOfTheTotalNetativeDisplacementAlarm = max(ListOfMaximumValuesPerFrame)
FinalFrameNegtiveDisplacementAlarmList = []

if MaximumValueOfTheTotalNetativeDisplacementAlarm == 0 : # If statement is a safeguard in case there are no positive displacement welds. Otherwise there wil be a x/0 situation
    MaximumValueOfTheTotalNetativeDisplacementAlarm = 1
 
for RawAlarmDataFrameList in TotalNegativeDisplacementAlarmABS :
    for RawAlarmDataWeld in RawAlarmDataFrameList :
        FinalFrameNegtiveDisplacementAlarmList.append((RawAlarmDataWeld / MaximumValueOfTheTotalNetativeDisplacementAlarm) * 10)
        
    TotalNegativeDisplacementAlarmREL = (FinalFrameNegtiveDisplacementAlarmList)

    FinalFrameNegtiveDisplacementAlarmList = []



# Everything is now calculated and can be writen in a CSV file, that is the Purpose of the next bit of code.

TemporaryListForWritingCSV1 = []
TemporaryListForWritingCSV2 = []
TemporaryListForWritingCSV3 = []
TemporaryListForWritingCSV4 = []
           
# plt.show()
CounterForCSVFile1 = 0
CounterForCSVFile2 = 0
CounterForCSVFile3 = 0
# OPPER1 = [repr(index_csv[CounterForCSVFile1]),frame]
# OPPER2 = [repr(index_csv[CounterForCSVFile3]),TotalNegativeDisplacementAlarmREL[CounterForCSVFile3]
if TypeFile == True :
    with open('DisplacementVeryHighWeldsClipToFrame.csv', 'w', newline='') as file:
        for frame in DisplacementAnomalyList :
            while CounterForCSVFile1 != len(index_csv) :
                OPPER1 = [index_csv[CounterForCSVFile1],frame]
                TemporaryListForWritingCSV1.append(OPPER1)
                CounterForCSVFile1 = CounterForCSVFile1 + 1

        writer = csv.writer(file)
        while CounterForCSVFile2 != len(TemporaryListForWritingCSV1) :
            writer.writerow(TemporaryListForWritingCSV1[CounterForCSVFile2])
            CounterForCSVFile2 = CounterForCSVFile2 +1
            
    CounterForCSVFile1 = 0
    CounterForCSVFile2 = 0
    CounterForCSVFile3 = 0
    

    with open('DisplacementPositiveClipToFrame.csv', 'w', newline='') as file:
        while CounterForCSVFile3 != len(TotalNegativeDisplacementAlarmREL) :
            OPPER2 = [index_csv[CounterForCSVFile3],TotalNegativeDisplacementAlarmREL[CounterForCSVFile3]]
            TemporaryListForWritingCSV2.append(OPPER2)
            CounterForCSVFile3 = CounterForCSVFile3 + 1

        writer = csv.writer(file)
        while CounterForCSVFile2 != len(TemporaryListForWritingCSV2) :
            writer.writerow(TemporaryListForWritingCSV2[CounterForCSVFile2])
            CounterForCSVFile2 = CounterForCSVFile2 +1




if TypeFile == False :
    with open('DisplacementVeryHighWeldsClipToSkin.csv', 'w', newline='') as file:
        for frame in DisplacementAnomalyList :
            # while CounterForCSVFile1 != len(index_csv) :
            OPPER3 = [index_csv[CounterForCSVFile1],frame]
            TemporaryListForWritingCSV3.append(OPPER3)
            CounterForCSVFile1 = CounterForCSVFile1 + 1

        writer = csv.writer(file)
        while CounterForCSVFile2 != len(TemporaryListForWritingCSV3) :
            writer.writerow(TemporaryListForWritingCSV3[CounterForCSVFile2])
            CounterForCSVFile2 = CounterForCSVFile2 +1
            
    CounterForCSVFile1 = 0
    CounterForCSVFile2 = 0
    CounterForCSVFile3 = 0

    with open('DisplacementPositiveClipToSkin.csv', 'w', newline='') as file:
        while CounterForCSVFile3 != len(TotalNegativeDisplacementAlarmREL) :
            OPPER2 = [index_csv[CounterForCSVFile3],TotalNegativeDisplacementAlarmREL[CounterForCSVFile3]]
            TemporaryListForWritingCSV2.append(OPPER2)
            CounterForCSVFile3 = CounterForCSVFile3 + 1

        writer = csv.writer(file)
        while CounterForCSVFile2 != len(TemporaryListForWritingCSV2) :
            writer.writerow(TemporaryListForWritingCSV2[CounterForCSVFile2])
            CounterForCSVFile2 = CounterForCSVFile2 +1

#  Section to calculted Wei Wei data
# Do note that almost all the data shown below was calcaulted manualy (exept the "along frame" data).



Stringer1 = 0
Stringer2 = 0
Stringer3 = 0.112079701
Stringer4 = 13.117995018999999
Stringer5 = 2.241594022
Stringer6 = 15.0622665
Stringer7 = 5.191469488999999
Stringer8 = 3.4900373599999996
Stringer9 = 11.162826897999999
Stringer10 = 16.047633872000002
Stringer11 = 5.361145704
Stringer12 = 4.027085928
Stringer13 = 2.3676836860000003
Stringer14 = 10.350249066000002
Stringer15 = 22.224470733000004
Stringer16 = 11.776151930000001
Stringer17 = 7.3178704859999995
Stringer18 = 12.190224159
Stringer19 = 2.5591531759999997
Stringer20 = 0
Stringer21 = 0
Stringer22 = 3.9663760900000007
Stringer23 = 7.182440846
Stringer24 = 9.909713575
Stringer25 = 9.159402242
Stringer26 = 6.660958905
Stringer27 = 0.600871731
Stringer28 = 0
Stringer29 = 0

SumOfPositiveDisplacementScoresAlongStringer = [Stringer1, Stringer2, Stringer3, Stringer4, Stringer5, Stringer6, Stringer7, Stringer8, Stringer9, Stringer10, Stringer11, Stringer12, Stringer13, Stringer14, Stringer15, Stringer16, Stringer17, Stringer18, Stringer19, Stringer20, Stringer21, Stringer22, Stringer23, Stringer24, Stringer25, Stringer26, Stringer27, Stringer28, Stringer29]
SumOfVeryHighDisplacementScoresAlongStrinegr = [0, 20, 0, 0, 10, 20, 10, 0, 0, 0, 10, 0, 0, 0, 10, 0, 10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0]
EmptyListStringer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EmptyListFrame = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

SumOfPositiveDisplacementScoresAlongFrame = [38.119999999999976, 121.26999999999995, 138.94, 3.87, 59.99999999999998, 95.36000000000001, 81.86, 242.05000000000004, 113.83, 45.749999999999986, 167.8, 234.14999999999998]
SumOfVeryHighDisplacementScoresAlongFrame = [30, 20, 0, 0, 0, 20, 0, 0, 10, 10, 0, 0]
print("\n\n")

print("Sum of all the positive displacement scores of clip to frame along the frames", SumOfPositiveDisplacementScoresAlongFrame)
print("Sum of all the positive displacement scores of clip to skin along the frames", EmptyListFrame)
print("Sum of all the very high  displacement scores of clip to frame along the frames", EmptyListFrame)
print("Sum of all the very high  displacement scores of clip to skin along the frames", SumOfVeryHighDisplacementScoresAlongFrame)

print("Sum of all the positive displacement scores of clip to frame along the stringers", SumOfPositiveDisplacementScoresAlongStringer)
print("Sum of all the positive displacement scores of clip to skin along the stringers", EmptyListStringer)
print("Sum of all the very high  displacement scores of clip to frame along the stringers", EmptyListStringer)
print("Sum of all the very high  displacement scores of clip to skin along the stringers", SumOfVeryHighDisplacementScoresAlongStrinegr)




