#this is power throng's property
print("\U0001F601")

from load import *
import numpy as np
import matplotlib.pyplot as plt

def root_finder(var, time):
    root_loc=[]
    for i in range(1,len(var)):
        if var[i]*var[i-1]<0:
            slope = (var[i]-var[i-1])/(time[i]-time[i-1])
            new_root = -var[i-1]/slope + time[i-1]
            root_loc.append(new_root)
        elif var[i] == 0:
            root_loc.append(time[i])
    
    return root_loc

peaks_valleys = []
total = iterate_points(type=1)
print(total)
for obj in total:
    obj.smoothing()

    power = obj.frame['Smooth power'].to_numpy()
    time = obj.frame['Time'].to_numpy()
    power, time = nan_filter(power,time)
    power_1 = np.gradient(power,time)    #first dev
    power_2 = np.gradient(power_1,time)  #second dev

    roots = root_finder(power_1,time)
    for t in roots:
        value = np.interp(t, time, power)
        second_dev = np.interp(t, time, power_2)
        peaks_valleys.append((t,value,second_dev))

roots, values, second_devs = zip(*peaks_valleys)
plt.scatter(roots, values)
plt.show()






