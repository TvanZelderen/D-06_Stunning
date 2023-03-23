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

obj = Data(1,4,2,1)
obj.smoothing()

power = obj.frame['Smooth power'].to_numpy()
time = obj.frame['Time'].to_numpy()
power, time = nan_filter(power,time)
power_1 = np.gradient(power,time)    #first dev
power_2 = np.gradient(power_1,time)  #second dev

roots = root_finder(power_1,time)
plt.plot(time, power_1)
plt.scatter(roots, np.zeros(len(roots)))
plt.show()






