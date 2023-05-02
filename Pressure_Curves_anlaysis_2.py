import matplotlib.pyplot as plt
import numpy as np
from load import Data as dt
from load import iterate_points
#from Pressure_Curves_analysis import peakvalues 
from math import isnan
import seaborn as sns
sns.set_theme()

a = dt('01', '02', '02', 1) #choose (frame_no, stringer_no, weld_no, type)
b = dt('04', '12', '01', 1) #choose (frame_no, stringer_no, weld_no, type)
d=dt(1,2,2,1)
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


objects = iterate_points(type=1)
print(len(objects))
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
    print(ma, mi, av_time)

    weld_location = [obj.frame_no, obj.stringer_no, obj.weld_no, obj.type]
    
    """if i==13:
        plt.figure()
        plt.plot(peakst, peaksp, "o")
        plt.plot(max_time_freq, max_pressure_freq, "o")
        print(max_pressure_freq)
        print(max_time_freq)
        plt.plot(t, p)
        plt.xlabel("time")
        plt.ylabel("pressure")
        plt.show()"""

    weld_list.append([weld_location, ma, mi, av_time])#creates a matrix with the weld location, maximum and minimum time difference and average time
    i=i+1

averages_averages = [lst[3] for lst in weld_list]
total_average_avarage = np.average(averages_averages)
averages_minimums = [lst[2] for lst in weld_list]
total_average_minimums = np.average(averages_minimums)
averages_maximums = [lst[1] for lst in weld_list]
total_average_maximumx = np.average(averages_maximums)
std_avarges=np.std(averages_averages)
std_minimums=np.std(averages_minimums)
std_maximums=np.std(averages_maximums)

value=0.5
bad_weld_avg_avg=[]
bad_weld_avg_max=[]
bad_weld_avg_min=[]
col=0
color=[]
for num in range(len(averages_averages)):
    
    if averages_averages[num]> total_average_avarage+value*std_avarges:
        bad_weld_avg_avg.append(weld_list[num][0])
        col=col+1

    if averages_minimums[num]< total_average_minimums+value*std_minimums:
        bad_weld_avg_min.append(weld_list[num][0])
        col=col+1

    if averages_maximums[num]> total_average_maximumx+value*std_maximums:
        bad_weld_avg_max.append(weld_list[num][0])
        col=col+1
    color.append([weld_list[num], col])
    
    col=0
#print(bad_weld_avg_avg)
print(color)
print(color[0])
print(color[0][1])


color_plot = []
x_plot = []
y_plot = []
for weld in color:
    x_plot.append(weld[0][0][0] + ((weld[0][0][2]-1)%3)/10 - 0.10)
    y_plot.append(weld[0][0][1] + ((weld[0][0][2]-1)//3)/2.5 - 0.20)
    color_plot.append(weld[1])
plt.scatter(x_plot, y_plot, c=color_plot, cmap='coolwarm')
plt.colorbar()
plt.show()

for weld in bad_weld_avg_avg:
    x_plot.append(weld[0][0] + ((weld[0][2]-1)%3)/10 - 0.10)
    y_plot.append(weld[0][1] + ((weld[0][2]-1)//3)/2.5 - 0.20)
    color_plot.append(weld[1])
plt.scatter(x_plot, y_plot, c=color_plot, cmap='coolwarm')
plt.colorbar()
plt.show()

