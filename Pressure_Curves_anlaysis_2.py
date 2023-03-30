import matplotlib.pyplot as plt
import numpy as np

from load import Data as dt
from load import iterate_points
#from Pressure_Curves_analysis import peakvalues 
from math import isnan

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
            while h<n:
                pressure_dif=abs(peaksp[i-n+h]-avg)
                if(m<pressure_dif):
                    m = pressure_dif
                    loc=i-n+h
                h=h+1
            tn.append(peakst[loc])
            pn.append(peaksp[loc])
            print(tn, pn, peakst[loc], loc, i, n, h)
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
    
    return tn, pn

def av_freq(tn, pn):
    i=0
    t=[]
    while i<(len(tn)-1):
        t.append(tn[i+1]-tn[i])
        i=i+1
    m = max(t)

    
    
    tav=np.average(t)
    pav=np.average(pn)
    return tav, pav, m


objects = iterate_points(type=1, stringers= [2])
print(objects)
number=[]
i=1
for obj in objects:
    p = obj.frame['Pressure'].to_numpy()
    t = obj.frame['Time'].to_numpy()
    peaksp,peakst, avg =calculatepeack(obj)
    max_time_freq , max_pressure_freq = normalize_peaks(peaksp,peakst, avg)
    print(max_time_freq)
    av_time, av_pressure, m = av_freq(max_time_freq, max_pressure_freq)
    number.append(i)
    print(m, av_time)
    plt.figure()
    plt.plot(peakst, peaksp, "o")
    plt.plot(max_time_freq, max_pressure_freq, "o")
    plt.plot(t, p)
    plt.xlabel("time")
    plt.ylabel("pressure")
    plt.show()
    i=i+1

"""plt.figure()
plt.subplot(111)
plt.plot(number, av_time)
plt.xlabel("frames")
plt.ylabel("average time")
plt.show()"""


p = a.frame['Pressure'].to_numpy()
t = a.frame['Time'].to_numpy()
peaksp, peakst, avg=calculatepeack(a)
max_time_freq, max_pressure_freq=normalize_peaks(peaksp, peakst, avg)
#for i in range (len(peaksp)):
#   print(peakst[i], peaksp[i])
"""plt.plot(peakst, peaksp, "o")
plt.plot(max_time_freq, max_pressure_freq, "o")
plt.plot(t, p)
plt.show()"""
#print("hi")
for i in range(len(max_time_freq)):
    print(max_time_freq[i], max_pressure_freq[i])
print()
print(max_time_freq[1])
print(max_time_freq[0])
print(av_freq(max_time_freq, max_pressure_freq))