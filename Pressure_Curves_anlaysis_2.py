import matplotlib.pyplot as plt
import numpy as np

from load import Data as dt
#from Pressure_Curves_analysis import peakvalues 
from math import isnan

a = dt('01', '02', '02', 1) #choose (frame_no, stringer_no, weld_no, type)
b = dt('04', '12', '01', 1) #choose (frame_no, stringer_no, weld_no, type)

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
    n = 1

    p_peak = p[np.where(p > (avg+n*std))]
    t_peak = t[np.where(p > (avg+n*std))]
    ti=[]
    po=[]
    i=0
    while i<len(p):
        if isnan(p[i]):
            continue
        elif p[i]-avg>n*std:
            #print(p[i], t[i])
            ti.append(t[i])
            po.append(p[i])
            
        i=i+1
    i=0
    peaksp=[]
    peakst=[]
    pre=po[0]
    n=0
    while i<len(po):
        
        if(abs(po[i]-pre)<0.001):
            n=n+1
        elif(abs(po[i]-pre)>0.001):
            peaksp.append(po[i-1])
            peakst.append(ti[i-int(n/2)])
            pre=po[i]
            n=0
        i=i+1
    """ plt.plot(peakst, peaksp, "o")
    plt.plot(t, p)
    plt.show()"""
    return(peaksp,peakst)

def normalize_peaks(peaksp,peakst):
    print(peaksp, peakst)
    t0=peakst[0]
    tn=[]
    pn=[]
    i=1
    n=1
    print(len(peakst))
    while i< len(peakst):
        print(i)
        selected_values=peaksp[i-n:i]
        print(peakst[i]-peakst[i-1])
        if(peakst[i]-peakst[i-1])<0.5:
            n=n+1
        else:
            
            pn.append(max(selected_values))
            """ print(selected_values)
            print(max(selected_values))"""
            tn.append(peakst[i-n+np.argmax(selected_values)])
            """print(peakst[i-n+np.argmax(selected_values)])"""
            """print(i-n + np.argmax(selected_values))"""
            n=0
            
        i=i+1

    """print("hi")
    print("holllo")
    while i<len(peaksp):
        print("hi")
        selected_values=peaksp[i-n:i]
        print(selected_values, )
        if abs(peakst[i]-t0)<0.06:
            print("hi")
            n=n+1
            print(n)
        elif abs(peakst[i]-t0)<0.06:
            print("hçll")
            pn.append(max(selected_values))
            n=0
            t0=peakst[i]
        i=i+1      
    print(pn)"""
    return pn, tn


p = b.frame['Pressure'].to_numpy()
t = b.frame['Time'].to_numpy()

print("hi")
peaksp,peakst=(calculatepeack(b))
print("hi")
max_pressure_freq , max_time_freq= (normalize_peaks(peaksp,peakst))
print("hi")
#for i in range (len(peaksp)):
#   print(peakst[i], peaksp[i])
plt.plot(peakst, peaksp, "o")
plt.plot(max_time_freq, max_pressure_freq, "o")
plt.plot(t, p)
plt.show()
print("hi")
for i in range(len(max_time_freq)):
    print(max_time_freq[i], max_pressure_freq[i])
print()
print(max_time_freq[1])
print(max_time_freq[0])
print(max_time_freq[1]-max_time_freq[0])