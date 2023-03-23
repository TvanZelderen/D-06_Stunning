from load import Data
from scipy.integrate import simpson
import pandas as pd
from load import iterate_points
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pylab as py

def total_energy(frame:list = [1], stringer:list = [1], weld:list = [1], type:int = 1):
    data = iterate_points(frames=frame, stringers=stringer, welds =weld, type=type)
    energy = []
    for i in data:
        p = i.frame['Power'].dropna().to_numpy()
        t = i.frame['Time'].drop(i.frame['Power'].isna()*range(len(i.frame['Power']))).to_numpy()
        dt = t[1]-t[0]
        print(len(t))
        print(len(p))
        energy.append(simpson(p, t))
    print('Energy: ' + str(energy))
    df_energy = pd.DataFrame(energy, columns=['energy'])
    #plt.scatter(np.ones(len(energy)), energy)
    sns.histplot(df_energy, x = 'energy')
    plt.show()
total_energy()
#print(len(p))
#print(len(t))
#print(dt)

print(energy)