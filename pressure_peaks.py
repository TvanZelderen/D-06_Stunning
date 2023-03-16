from load import Data as dt
import numpy as np
import matplotlib.pyplot as plt

a = dt('01', '02', '02', 1)
a.normalize()
a.create_array()
a.bar_to_N()
p = a.frame['Pressure'].to_numpy()
t = a.frame['Time'].to_numpy()
avg = np.average(p)
std = np.std(p)
n = 2

p_peak = p[np.where(p > (avg+n*std))]
t_peak = t[np.where(p > (avg+n*std))]

plt.scatter(t_peak, p_peak)
print("The peak values are:", np.unique(p_peak))
print("The number of peak values are:", len(np.unique(p_peak)))
plt.plot(t, p)
plt.show()

