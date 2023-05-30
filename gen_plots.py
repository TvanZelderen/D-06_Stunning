from load import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import ListedColormap
import csv
import seaborn as sns
sns.set_theme()


cmap = get_cmap('coolwarm')
cmin=0.3
cmax=1
newcolors = cmap(np.linspace(cmin, cmax, 256))
newcmp = ListedColormap(newcolors)

#structure = [filename, type(0/1), title, data label]
file_list = [['DisplacementPositiveClipToFrame.csv',1,'Score [-]'],
             ['DisplacementPositiveClipToSkin.csv',0,'Score [-]'],
             ['DisplacementVeryHighWeldsClipToFrame.csv',1,'Score [-]'],
             ['DisplacementVeryHighWeldsClipToSkin.csv',0,'Score [-]']]

for file_idx in file_list:
    with open(file_idx[0], 'r', newline='') as file:
        data = list(csv.reader(file))

    for row in data:
        row[0] = row[0].replace('[','').replace(']','').replace(',','')
        row[0] = row[0].split(' ')
        row[:] = row[0]+[row[1]]
    data = np.array(data)
    data = data.astype('float64')

    if file_idx[1] == 1:
        data = data[data[:,2]<=2]

    frame_no = data[:,0].reshape(-1)
    stringer_no = data[:,1].reshape(-1)
    weld_no = data[:,2].reshape(-1)
    data_plot = data[:,4].reshape(-1)

    x_plot = frame_no + ((weld_no-1)%3)/10 - 0.10
    y_plot = stringer_no + ((weld_no-1)//3)/2.5 - 0.20

    if file_idx[1] == 0:
        s = 27
        w = 6
        x_plot = frame_no + ((weld_no-1)%3)/6 - 1/6
        y_plot = stringer_no + ((weld_no-1)//3)/2.5 - 0.20
    elif file_idx[1] == 1:
        s = 29
        w = 2
        x_plot = frame_no + weld_no/6 - 1/4
        y_plot = stringer_no
    else:
        print('Invalid type (not 0/1)')
        break

    plt.scatter(x_plot, y_plot, c=data_plot, cmap=newcmp, s=10, clim=(0,10))
    cbar= plt.colorbar()
    cbar.set_label(file_idx[2], rotation=90)
    plt.xlabel('Frame number [-]')
    plt.ylabel('Stringer number [-]')

    plt.show()
