from load import Data
from scipy.integrate import simpson
import pandas as pd
from load import iterate_points
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


data = iterate_points(frames=[10])
energy = []
for i in data:
    i.normalize()
    i.bar_to_N()
    p = i.frame['Power'].dropna().to_numpy()
    t = i.frame['Time'].drop(i.frame['Power'].isna()*range(len(i.frame['Power']))).to_numpy()
    #dt = t[1]-t[0]
    energy.append(simpson(p, t))
print('Energy: ' + str(energy))
df_energy = pd.DataFrame(energy, columns=['energy'])
#plt.scatter(np.ones(len(energy)), energy)
sns.histplot(df_energy, x = 'energy', binwidth=150)
plt.show()
'''a = Data('01', '02', '02', 0)
a.normalize()
a.bar_to_N()
print(a.frame)
p = a.frame['Power'].dropna().to_numpy()
t = a.frame['Time'].drop(a.frame['Power'].isna()*range(len(a.frame['Power']))).to_numpy()
dt = t[1]-t[0]'''
#print(len(p))
#print(len(t))
#print(dt)

print(energy)