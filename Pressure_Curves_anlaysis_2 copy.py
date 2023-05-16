import matplotlib.pyplot as plt
import numpy as np
from load import Data as dt
from load import iterate_points
import csv
#from Pressure_Curves_analysis import peakvalues 
from math import isnan
import seaborn as sns
sns.set_theme()

"""a = dt('01', '02', '02', 1) #choose (frame_no, stringer_no, weld_no, type)
b = dt('04', '12', '01', 1) #choose (frame_no, stringer_no, weld_no, type)
d=dt(1,2,2,1)"""
#print("hi")
#timea=peakvalues(a)
#timeb=peakvalues(b)
#print(timea)
#print(timeb)

def calculatepeack(data):

    p = data.frame['Pressure'].to_numpy()
    t = data.frame['Time'].to_numpy()
    avg = np.average(p) #average of pressure graphs
    std = np.std(p) #standard deviation of pressure graphs
    n = 1.5

    p_peak = p[np.where(p > (avg+n*std))]
    t_peak = t[np.where(p > (avg+n*std))]
    ti=[]
    po=[]
    i=0
    while i<len(p):
        if isnan(p[i]):
            continue
        elif abs(p[i]-avg)>n*std:
            #print(p[i], t[i])
            ti.append(t[i])
            po.append(p[i])

            
        i=i+1
    
    peaksp=[]
    peakst=[]
    pre=po[0]
    n=0
    j=0
    while j<len(po):
        
        if(abs(po[j]-pre)<0.001):
            n=n+1
        elif(abs(po[j]-pre)>0.001):
            peaksp.append(po[j-1])
            peakst.append(ti[j-int(n/2)])
            pre=po[j]
            n=0
        j=j+1
    """ plt.plot(peakst, peaksp, "o")
    plt.plot(t, p)
    plt.show()"""
    return(peaksp,peakst, avg)

def normalize_peaks(peaksp,peakst, avg):
    #print(peaksp, peakst)
    t0=peakst[0]
    tn=[]
    pn=[]
    i=1
    n=1
    #print(len(peakst))
    while i< len(peakst):
     
        selected_values=peaksp[i-n:i]
       
        """if (peakst[i]-peakst[i-1])<0.5:
            n=n+1"""
        if (peakst[i]-peakst[i-1])>=0.5 or i==len(peakst)-1 and i!=0:
            h=0
            m=0
            loc=0
            repeat =False
            #print(peakst)
            while h<n:
                pressure_dif=abs(peaksp[i-n+h]-avg)
                if(m<pressure_dif):
                    m = pressure_dif
                    loc=i-n+h
                h=h+1
           
            tn.append(peakst[loc])
            pn.append(peaksp[loc])
            #print(tn, pn, peakst[loc], loc, i, n, h)
            """ pn.append(max(selected_values))
            print(selected_values)
            print(max(selected_values))
            tn.append(peakst[i-n+np.argmax(selected_values)])
            print(peakst[i-n+np.argmax(selected_values)])
            print(i-n + np.argmax(selected_values)"""
            n=0
        else:
            n=n+1
            
        i=i+1

        tn_unique = []
        pn_unique = []
        for t, p in zip(tn, pn):
            if t not in tn_unique:
                tn_unique.append(t)
                pn_unique.append(p)

    return tn_unique, pn_unique

def av_freq(tn, pn):
    i=0
    t=[]
    idx = np.argsort(tn)
    tn = np.array(tn)[idx]
    pn = np.array(pn)[idx]

    while i<(len(tn)-1):
        t.append(tn[i+1]-tn[i])
        i=i+1
    ma = max(t)
    mi = min(t)
    
    
    tav=np.average(t)
    pav=np.average(pn)
    return tav, pav, ma, mi

#to activate type 0
objects = iterate_points(type=0)  

#to activate type 1
#objects = iterate_points(type=1,welds=[1,2])
number=[]
i=1
weld_list = []
for obj in objects:
    p = obj.frame['Pressure'].to_numpy()
    t = obj.frame['Time'].to_numpy()
    peaksp,peakst, avg =calculatepeack(obj)
    max_time_freq , max_pressure_freq = normalize_peaks(peaksp,peakst, avg)
    #print(max_time_freq)
    av_time, av_pressure, ma, mi = av_freq(max_time_freq, max_pressure_freq)
    number.append(i)

    weld_location = [obj.frame_no, obj.stringer_no, obj.weld_no, obj.type]
    
    if i==13:
        plt.figure()
        plt.plot(peakst, peaksp, "o")
        plt.plot(max_time_freq, max_pressure_freq, "o")
        print(max_pressure_freq)
        print(max_time_freq)
        plt.plot(t, p)
        plt.xlabel("time")
        plt.ylabel("pressure")
        plt.show()

    weld_list.append([weld_location, ma, mi, av_time, av_pressure])#creates a matrix with the weld location, maximum and minimum time difference and average time
    i=i+1

weld_1=[]
weld_2=[]
weld_3=[]
weld_4=[]
weld_5=[]
weld_6=[]
for weld in weld_list:
    if weld[0][2]==1:
        weld_1.append(weld)
    if weld[0][2]==2:
        weld_2.append(weld)
    if weld[0][2]==3:
        weld_3.append(weld)
    if weld[0][2]==4:
        weld_4.append(weld)
    if weld[0][2]==5:
        weld_5.append(weld)
    if weld[0][2]==6:
        weld_6.append(weld)

averages_pressures_1= [lst[4] for lst in weld_1]
averages_pressures_2= [lst[4] for lst in weld_2]
averages_pressures_3= [lst[4] for lst in weld_3]
averages_pressures_4= [lst[4] for lst in weld_4]
averages_pressures_5= [lst[4] for lst in weld_5]
averages_pressures_6= [lst[4] for lst in weld_6]
print(np.average(averages_pressures_1), np.average(averages_pressures_2), np.average(averages_pressures_3), np.average(averages_pressures_4), np.average( averages_pressures_5), np.average( averages_pressures_6))
print()
averages_maximums_1= [lst[1] for lst in weld_1]
averages_maximums_2= [lst[1] for lst in weld_2]
averages_maximums_3= [lst[1] for lst in weld_3]
averages_maximums_4= [lst[1] for lst in weld_4]
averages_maximums_5= [lst[1] for lst in weld_5]
averages_maximums_6= [lst[1] for lst in weld_6]
print(np.average(averages_maximums_1), np.average( averages_maximums_2), np.average(averages_maximums_3), np.average( averages_maximums_4), np.average( averages_maximums_5), np.average( averages_maximums_6))
print()

averages_minimums_1= [lst[2] for lst in weld_1]
averages_minimums_2= [lst[2] for lst in weld_2]
averages_minimums_3= [lst[2] for lst in weld_3]
averages_minimums_4= [lst[2] for lst in weld_4]
averages_minimums_5= [lst[2] for lst in weld_5]
averages_minimums_6= [lst[2] for lst in weld_6]

print(np.average(averages_minimums_1), np.average( averages_minimums_2), np.average(averages_minimums_3), np.average( averages_minimums_4), np.average( averages_minimums_5), np.average( averages_minimums_6))
print()

averages_average_1= [lst[3] for lst in weld_1]
averages_average_2= [lst[3] for lst in weld_2]
averages_average_3= [lst[3] for lst in weld_3]
averages_average_4= [lst[3] for lst in weld_4]
averages_average_5= [lst[3] for lst in weld_5]
averages_average_6= [lst[3] for lst in weld_6]
print(np.average(averages_minimums_1), np.average( averages_minimums_2), np.average(averages_minimums_3), np.average( averages_minimums_4), np.average( averages_minimums_5), np.average( averages_minimums_6))
print()
def give_punctuation(average):
    avg=np.average(average)
    std=np.std(average)
    value=1
    col_p=0
    color=[]
    for num in range(len(average)):
        if average[num]< avg-value*4/3*std:
            col_p=col_p-2.5
        if average[num]< avg-value*1*std:
            col_p=col_p-2.5
        if average[num]< avg-value*2/3*std:
            col_p=col_p-2.5
        if average[num]< avg-1/3*value*std:
            col_p=col_p-2.5
        if average[num]> avg+1/3*value*std:
            col_p=col_p+2.5
        if average[num]> avg+2/3*value*std:
            col_p=col_p+2.5
        if average[num]> avg+1*value*std:
            col_p=col_p+2.5
        if average[num]> avg+4/3*value*std:
            col_p=col_p+2.5

        color.append([average, col_p])
        col_p=0



color_plot = []
x_plot = []
y_plot = []
for weld in color_time:
    x_plot.append(weld[0][0][0] + ((weld[0][0][2]-1)%3)/10 - 0.10)
    y_plot.append(weld[0][0][1] + ((weld[0][0][2]-1)//3)/2.5 - 0.20)
    color_plot.append(weld[1])
plt.scatter(x_plot, y_plot, c=color_plot, cmap='coolwarm')
plt.colorbar()
plt.show()

color_plot_p = []
x_plot_p = []
y_plot_p = []
for weld in color_pressure:
    x_plot_p.append(weld[0][0][0] + ((weld[0][0][2]-1)%3)/10 - 0.10)
    y_plot_p.append(weld[0][0][1] + ((weld[0][0][2]-1)//3)/2.5 - 0.20)
    color_plot_p.append(weld[1])
plt.scatter(x_plot_p, y_plot_p, c=color_plot_p, cmap='coolwarm')
plt.colorbar()
plt.show()



#for type 0

with open('pressure_time_0.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(color_time)):
        writer.writerow([repr(color_time[i][0][0]),abs(color_time[i][1])])

with open('pressure_0_no_look.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(color_pressure)):
        writer.writerow([repr(color_pressure[i][0][0]),abs(color_pressure[i][1])])  

score_array_time = np.empty((12,27,6))
score_array_time[:] = np.nan

score_array_pressure = np.empty((12,27,6))
score_array_pressure[:] = np.nan
for i in range(len(color_time)):
    score_array_time[color_time[i][0][0][0]-1,color_time[i][0][0][1]-1,color_time[i][0][0][2]-1] = color_time[i][1]

for i in range(len(color_pressure)):
    score_array_pressure[color_pressure[i][0][0][0]-1,color_pressure[i][0][0][1]-1,color_pressure[i][0][0][2]-1] = color_pressure[i][1]

frame_mean_time = np.nanmean(score_array_time, axis=(1,2))
stringer_mean_time = np.nanmean(score_array_time, axis=(0,2))

frame_mean_pressure = np.nanmean(score_array_pressure, axis=(1,2))
stringer_mean_pressure = np.nanmean(score_array_pressure, axis=(0,2))


plt.bar(range(1,13),frame_mean_time)
plt.title("clip to framme mean time")
plt.show()

plt.bar(range(1,28),stringer_mean_time)
plt.title("clip to stringer mean time")
plt.show()

plt.bar(range(1,13),frame_mean_pressure)
plt.title("clip to framme mean pressure")
plt.show()

plt.bar(range(1,28),stringer_mean_pressure)
plt.title("clip to steringer mean pressure")
plt.show()


#for type 1
"""
with open('pressure_time_1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(color_time)):
        writer.writerow([repr(color_time[i][0][0]),abs(color_time[i][1])])

with open('pressure_1_nolook.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(color_pressure)):
        writer.writerow([repr(color_pressure[i][0][0]),abs(color_pressure[i][1])])  

score_array_time = np.empty((12,29,2))
score_array_time[:] = np.nan

score_array_pressure = np.empty((12,29,2))
score_array_pressure[:] = np.nan
for i in range(len(color_time)):
    score_array_time[color_time[i][0][0][0]-1,color_time[i][0][0][1]-1,color_time[i][0][0][2]-1] = color_time[i][1]

for i in range(len(color_pressure)):
    score_array_pressure[color_pressure[i][0][0][0]-1,color_pressure[i][0][0][1]-1,color_pressure[i][0][0][2]-1] = color_pressure[i][1]

frame_mean_time = np.nanmean(score_array_time, axis=(1,2))
stringer_mean_time = np.nanmean(score_array_time, axis=(0,2))

frame_mean_pressure = np.nanmean(score_array_pressure, axis=(1,2))
stringer_mean_pressure = np.nanmean(score_array_pressure, axis=(0,2))


plt.bar(range(1,13),frame_mean_time)
plt.title("clip to framme mean time")
plt.show()

plt.bar(range(1,30),stringer_mean_time)
plt.title("clip to stringer mean time")
plt.show()

plt.bar(range(1,13),frame_mean_pressure)
plt.title("clip to framme mean pressure")
plt.show()

plt.bar(range(1,30),stringer_mean_pressure)
plt.title("clip to steringer mean pressure")
plt.show()

"""
#--------------------------------------------------------------------------------------#

