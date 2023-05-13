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

# The program iterates all the calcualtions over each frame.
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
    DispalcementDuringPsoitiveDisplacement = []     # A list of how much the sosnotrode goes up during a weld where there is positive displacement
    
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
    for (WeldNumber, TimeStamp) in zip(WeldNumberWithPositiveDisplacement, TimeAtPositiveDisplacement) :
        # print(WeldNumber)
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



# Everything is now calculated and can be writen in a CSV file, that teh perpuse of the next bit of code.


TemporaryListForWritingCSV1 = []
TemporaryListForWritingCSV2 = []
TemporaryListForWritingCSV3 = []
TemporaryListForWritingCSV4 = []
           
# plt.show()
CounterForCSVFile1 = 0
CounterForCSVFile2 = 0

# print(DisplacementAnomalyList)
# print()
# print(TotalNegativeDisplacementAlarmREL)

if TypeFile == True :
    with open('DisplacementVeryHighWeldsClipToFrame.csv', 'w', newline='') as file:
        for frame in DisplacementAnomalyList :
            while CounterForCSVFile1 != len(index_csv) :
                OPPER1 = index_csv[CounterForCSVFile1] + " " +  str(frame)
                TemporaryListForWritingCSV1.append(OPPER1)
                CounterForCSVFile1 = CounterForCSVFile1 + 1

        writer = csv.writer(file)
        while CounterForCSVFile2 != len(TemporaryListForWritingCSV1) :
            writer.writerow([TemporaryListForWritingCSV1[CounterForCSVFile2]])
            CounterForCSVFile2 = CounterForCSVFile2 +1
            
    CounterForCSVFile1 = 0
    CounterForCSVFile2 = 0
    CounterForCSVFile3 = 0


    with open('DisplacementPositiveClipToFrame.csv', 'w', newline='') as file:
        while CounterForCSVFile3 != len(TotalNegativeDisplacementAlarmREL) :
            print(TotalNegativeDisplacementAlarmREL[CounterForCSVFile3])
            while CounterForCSVFile1 != len(index_csv) :
                OPPER2 = (index_csv[CounterForCSVFile1] + " " +  str(TotalNegativeDisplacementAlarmREL[CounterForCSVFile3]))
                print(OPPER2, str(TotalNegativeDisplacementAlarmREL[CounterForCSVFile3]))
                TemporaryListForWritingCSV2.append(OPPER2)
                CounterForCSVFile1 = CounterForCSVFile1 + 1
            CounterForCSVFile3 = CounterForCSVFile3 + 1

        writer = csv.writer(file)
        while CounterForCSVFile2 != len(TemporaryListForWritingCSV2) :
            writer.writerow([TemporaryListForWritingCSV2[CounterForCSVFile2]])
            CounterForCSVFile2 = CounterForCSVFile2 +1




if TypeFile == False :
    with open('DisplacementVeryHighWeldsClipToSkin.csv', 'w', newline='') as file:
        for frame in DisplacementAnomalyList :
            while CounterForCSVFile1 != len(index_csv) :
                OPPER3 = index_csv[CounterForCSVFile1] + " " +  str(frame)
                TemporaryListForWritingCSV3.append(OPPER3)
                CounterForCSVFile1 = CounterForCSVFile1 + 1

        writer = csv.writer(file)
        while CounterForCSVFile2 != len(TemporaryListForWritingCSV3) :
            writer.writerow([TemporaryListForWritingCSV3[CounterForCSVFile2]])
            CounterForCSVFile2 = CounterForCSVFile2 +1
            
    CounterForCSVFile1 = 0
    CounterForCSVFile2 = 0

    with open('DisplacementPositiveClipToSkin.csv', 'w', newline='') as file:
        for frame in TotalNegativeDisplacementAlarmREL :
            while CounterForCSVFile1 != len(index_csv) :
                OPPER4 = index_csv[CounterForCSVFile1] + " " +  str(frame)
                TemporaryListForWritingCSV4.append(OPPER4)
                CounterForCSVFile1 = CounterForCSVFile1 + 1

        writer = csv.writer(file)
        while CounterForCSVFile2 != len(TemporaryListForWritingCSV4) :
            writer.writerow([TemporaryListForWritingCSV4[CounterForCSVFile2]])
            CounterForCSVFile2 = CounterForCSVFile2 +1



#     with open('DisplacementVeryHighWeldsClipToFrame.csv', 'w', newline='') as file:
#         writer = csv.writer(file)
#         for frame in DisplacementAnomalyList :
#             for  IndexForWelds in index_csv :
#                 writer.writerow([IndexForWelds] + [frame] + [BreakCounter])
#                 if BreakCounter >=  len(index_csv) :
                    
#                     file.close()
#                 BreakCounter = BreakCounter + 1
#                 print(len(IndexForWelds), BreakCounter, "very high")
#                 # file.close()


#     with open('DisplacementPositiveClipToFrame.csv', 'w', newline='') as file:
#         writer = csv.writer(file)
#         for frame in TotalNegativeDisplacementAlarmREL :
#             for (weld2, IndexForWelds) in zip (frame, index_csv) :
#                 writer.writerow([IndexForWelds] + [weld2])
#                 if BreakCounter >=  len(index_csv) :
#                     break
#                 BreakCounter = BreakCounter + 1


# BreakCounter = 0
# if TypeFile == False :
#     with open('DisplacementVeryHighWeldsClipToSkin.csv', 'w', newline='') as file:
#         writer = csv.writer(file)
#         for frame in DisplacementAnomalyList :
#             for  IndexForWelds in index_csv :
#                 writer.writerow([IndexForWelds] + [frame])
#                 if BreakCounter >=  len(index_csv) :
#                     break
#                 BreakCounter = BreakCounter + 1
#                 # print(BreakCounter, "very high")


#     BreakCounter = 0
#     with open('DisplacementPositiveClipToSkin.csv', 'w', newline='') as file:
#         writer = csv.writer(file)
#         for frame in TotalNegativeDisplacementAlarmREL :
#             # print(len(frame), )
#             for (weld2, IndexForWelds) in zip (frame, index_csv) :
#                 writer.writerow([IndexForWelds] + [weld2])
#                 if BreakCounter >=  len(index_csv) :
#                     break
#                 BreakCounter = BreakCounter + 1
 



# for (WeldNumber, TimeStamp) in zip(WeldNumberWithPositiveDisplacement, TimeAtPositiveDisplacement) :

#! things to do, differentioate between kind of dips. So dips in the beginning are fine but late roen are bad. 
#! Beter noise reduction. 
# Combine the CVS files beter write. 
#! Try to calcualte the "area" of the dips (so dept times width fo the dip).
#  and that dtermines the score fo the dispalcment. 
# AMke a index files 
# and try to get teh smae as the rest of the peopels csv files
# Make Wei Wei List