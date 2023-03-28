from load import Data
from scipy.integrate import simpson
import pandas as pd
from load import iterate_points
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pylab as py


data = iterate_points(frames=[10])

print(data[1])


# energy = []
# for i in data:
#     d = i.frame['Displacement'].dropna().to_numpy()
#     t = i.frame['Time'].drop(i.frame['Displacement'].isna()*range(len(i.frame['Displacement']))).to_numpy()
#     dt = t[1]-t[0]

# d = data.frame['Displacement']
# na_rows = d.isna()
# rows_remove = np.where(na_rows)[0]
# d = d.dropna()
# t=data.frame['Time']
# t.drop(rows_remove, axis=0)
# t.reset_index()

# print('Energy: ' + str(energy))
# df_energy = pd.DataFrame(energy, columns=['energy'])

# i = 1

# while i != len(d) :
#     if d[i-1] > d[i] :
#         print("FFFFF", i)

#     i = i + 1


# plt.plot(d)
# plt.show()
