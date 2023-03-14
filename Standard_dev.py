from load import Data
import numpy as np

frame_01 = np.array()

for i in range(1,13):
    if len(str(i)) == 1:
        no = '0'+str(i)
    else:
        no = str(i)
    frame_01.append(Data(frame_no='01', stringer_no=no, weld_no='01', type=1))
    frame_01[i].normalize()
    frame_01[i].bar_to_N()
    frame_01[i].plot(axes=ax, displacement=False)
    