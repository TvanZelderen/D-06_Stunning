from load import Data
from scipy.integrate import simpson
import pandas as pd
from load import iterate_points
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.api as sm
import pylab as py
'''data = np.array([])
for stringer_no in range(7):
    try:
        data = np.append(data, (Data(stringer_no, 1, 1, 1)))
    except:
        print('nope')
print(data)
energy = []
for i in data:
    #p = i.frame['Force'].dropna().to_numpy()
    #t = i.frame['Time'].drop(i.frame['Pressure'].isna()*range(len(i.frame['Force']))).to_numpy()
    #dt = t[1]-t[0]
    print(i.frame)
    p = i.frame['Force'].to_numpy()
    t = i.frame['Time'].to_numpy()
    print(i.frame['Force'])
    print(i.frame['Time'])
    print(len(t))
    print(len(p))
    energy.append(simpson(p, t))
print('Energy: ' + str(energy))
df_energy = pd.DataFrame(energy, columns=['energy'])'''


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
#plt.scatter(np.ones(len(energy)), energy)
data = Data(2, 2,2,1)
P = data.frame['Power'].dropna().to_numpy()
t = data.frame['Time'].drop(data.frame['Power'].isna()*range(len(data.frame['Power']))).to_numpy()
plt.plot(t, P)
print(data.frame)

#sns.histplot(df_energy, x = 'energy')
plt.show()

print(energy)