from load import Data
from scipy.integrate import simpson
import pandas as pd

a = Data('01', '02', '02', 0)
a.normalize()
a.bar_to_N()
print(a.frame)
p = a.frame['Power'].dropna().to_numpy()
t = a.frame['Time'].drop(a.frame['Power'].isna()*range(len(a.frame['Power']))).to_numpy()
dt = t[1]-t[0]
#print(len(p))
#print(len(t))
#print(dt)
energy = simpson(p, t)
print(energy)