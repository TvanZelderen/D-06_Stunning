import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sc
import pandas as pd
import load as ld
from math import isnan

all_data = ld.Data(1,7,7,1)
power=all_data.frame["Power"]
time=all_data.frame["Time"]
print(max(power))


def find_break(power, time):
    max=0
    max_loc=0
    t=[]
    p=[]
    ti=[]
    po=[]
    for i in range(len(power)):
        if isnan(power[i]):
            continue
        elif max<=power[i]:
            max=power[i]
            max_loc=i
        elif max > power[i] and ((max-power[i])>max*0.005):
            break_point=i
            t.append(time[i])
            p.append(power[i])
            print('oh no')
            break

        t.append(time[i])
        p.append(power[i])
    
    for i in range(len(power)):
        if isnan(power[i]):
            continue
        else:
            ti.append(time[i])
            po.append(power[i])

    return( max, max_loc, break_point, t, p, ti, po)
k=0

"""
j=0
t=[]
p=[]

while j<=break_point:
"""

max, max_loc, break_point, t, p, ti, po=find_break(power, time)
"""print(max_loc)
print(max)
print(t)
print(p)
print(power)"""

#ax = ld.plot_ini('test')
#all_data.plot(ax, power=True)

plt.plot(ti, po, "r")
plt.plot(t, p, "b")
plt.show()


