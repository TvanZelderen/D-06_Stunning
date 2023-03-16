from load import Data
from load import plot_ini
import numpy as np
import seaborn as sns
import matplotlib as plt
import os.path



frame_01 = []
ax = plot_ini()
for i in range(12):
    if len(str(i)) == 1:
        no = '0'+str(i+2)
    else:
        no = str(i+2)
    file_path = 
    if os.path.exists(file_path):
        frame_01.append(Data(frame_no='01', stringer_no=no, weld_no='02', type=1))
        frame_01[i].normalize()
        frame_01[i].bar_to_N()
        frame_01[i].plot(axes=ax, displacement=False)

plt.show()
    