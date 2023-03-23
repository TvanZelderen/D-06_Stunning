import matplotlib.pyplot as plt
import numpy as np

from load import Data as dt
from Pressure_Curves_analysis import peakvalues 
from math import isnan

a = dt('01', '02', '02', 1) #choose (frame_no, stringer_no, weld_no, type)
b = dt('08', '03', '01', 1) #choose (frame_no, stringer_no, weld_no, type)

#print("hi")
#timea=peakvalues(a)
#timeb=peakvalues(b)
#print(timea)
#print(timeb)

def calculatepeack(a):

    p = a.frame['Pressure'].to_numpy()
    t = a.frame['Time'].to_numpy()
    avg = np.average(p) #average of pressure graphs
    std = np.std(p) #standard deviation of pressure graphs
    n = 2

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
        if(po[i]==pre):
            n=n+1
        elif(po[i]!=pre):
            peaksp.append(po[i-1])
            peakst.append(ti[i-int(n/2)])
            pre=p[i]
            n=0
        i=i+1
    #plt.plot(t, p)
    #plt.show()
    return(peaksp,peakst)

peaksp,peakst=(calculatepeack(b))
for i in range (len(peaksp)):
    print(peakst[i], peaksp[i])