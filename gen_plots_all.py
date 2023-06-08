from load import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import ListedColormap
import csv
import seaborn as sns
sns.set_theme()


cmap = get_cmap('coolwarm')
cmin=0
cmax=1
newcolors = cmap(np.linspace(cmin, cmax, 256))
newcmp = ListedColormap(newcolors)

#structure = [filename, type(0/1), title, data label]
file_list = ['final_0.csv','final_1.csv']
data = []

for file_idx in file_list:
    with open('csvs\\'+file_idx, 'r', newline='') as file:
        data += list(csv.reader(file))

for row in data:
    row[0] = row[0].replace('[','').replace(']','').replace(',','')
    row[0] = row[0].split(' ')
    row[:] = row[0]+[row[1]]
data = np.array(data)
data = data.astype('float64')

data = data[np.logical_or(data[:,2]<=2,data[:,3]==0)]

frame_no = data[:,0].reshape(-1)
stringer_no = data[:,1].reshape(-1)
weld_no = data[:,2].reshape(-1)
type_no = data[:,3].reshape(-1)
data_plot = data[:,4].reshape(-1)

spot_no = 6*type_no + weld_no

x_plot = frame_no + ((spot_no-1)%4)/6 - 1/4
y_plot = stringer_no + ((spot_no-1)//4)/2.5 - 0.20
plt.scatter(x_plot, y_plot, c=data_plot, cmap=newcmp, s=10, clim=(0,3.5))

cbar= plt.colorbar()
cbar.set_label('Score [-]', rotation=90)
plt.xlabel('Frame number [-]')
plt.ylabel('Stringer number [-]')

plt.show()
