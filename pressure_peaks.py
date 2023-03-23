from load import Data as dt
import numpy as np
import matplotlib.pyplot as plt

a = dt(1, 2, 2, 1)
a.create_array()
p = a.frame['Pressure'].to_numpy()
t = a.frame['Time'].to_numpy()
avg = np.average(p) #average of pressure graphs
std = np.std(p) #standard deviation of pressure graphs
n = 2

p_peak = p[np.where(p > (avg+n*std))]
t_peak = t[np.where(p > (avg+n*std))]

Np_peak = len(np.unique(p_peak)) #number of peaks in pressure graph
Vp_peak = np.unique(p_peak) #array of peaks in pressure graph

plt.scatter(t_peak, p_peak)
print("The peak values are:", Vp_peak)
print("The number of peak values are:", Np_peak)
plt.plot(t, p)
plt.show()
