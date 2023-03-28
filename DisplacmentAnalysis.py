from load import Data
from scipy.integrate import simpson
import pandas as pd
from load import iterate_points
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pylab as py


data = iterate_points(frames=[4])

d = []
kAlarm = []
iAlarm = []
# t = []
# print(data)

for i in data:
    d.append(i.frame['Displacement'].dropna().to_numpy())
    t = (i.frame['Time'].drop(i.frame['Displacement'].isna()*range(len(i.frame['Displacement']))).to_numpy())
    dt = t[1]-t[0]
    

# d = data.frame['Displacement']
# na_rows = d.isna()
# rows_remove = np.where(na_rows)[0]
# d = d.dropna()
# t=data.frame['Time']
# t.drop(rows_remove, axis=0)
# t.reset_index()

# print(len(d))

# print('Displacement: ' + len(d))
# Displacement = pd.DataFrame(Displacement, columns=['Displacement'])
# print(d)

i = 1
k = 0

while k != len(d) :
    while i != len(d[k]) :
        if d[k][i-1] > d[k][i] :
            print("Positive slope Alarm! i = ", i,"k = ", k)
            iAlarm.append(i)
            kAlarm.append(k)
        i = i + 1
    
    k = k + 1
    i = 0

print(k, i)
q = 0
while q != len(kAlarm) :
    plt.plot(d[kAlarm[q]])
    print(len(kAlarm))

    plt.annotate('This point is interesting!', xy=(iAlarm[q], 1), xytext=(0, 1),arrowprops=dict(facecolor='black', shrink=0.05))
    plt.show()
    q = q + 1

 
# Annotate with text + Arrow


# Show the graph
plt.show()

# plt.plot(d[1])
# plt.show()