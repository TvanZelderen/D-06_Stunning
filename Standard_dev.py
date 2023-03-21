from load import Data
import numpy as np
<<<<<<< HEAD
=======
import seaborn as sns
import matplotlib as plt
import os.path

>>>>>>> fc8a107418a24a4f56ab9f7122cf7f8fc37b7142

frame_01 = np.array()

for i in range(1,13):
    if len(str(i)) == 1:
        no = '0'+str(i)
    else:
<<<<<<< HEAD
        no = str(i)
    frame_01.append(Data(frame_no='01', stringer_no=no, weld_no='01', type=1))
    frame_01[i].normalize()
    frame_01[i].bar_to_N()
    frame_01[i].plot(axes=ax, displacement=False)
    
=======
        no = str(i+2)
    file_path = './STUNNING Demonstrator USW Data'+ folder + '/Frame_' + str(frame_no) + '/' + '1kHz' + '_' + str(stringer_no)+'_' + str(weld_no) + '.dat'
    if os.path.exists(file_path):
        frame_01.append(Data(frame_no='01', stringer_no=no, weld_no='02', type=1))
        frame_01[i].normalize()
        frame_01[i].bar_to_N()
        frame_01[i].plot(axes=ax, displacement=False)

plt.show()
>>>>>>> fc8a107418a24a4f56ab9f7122cf7f8fc37b7142
