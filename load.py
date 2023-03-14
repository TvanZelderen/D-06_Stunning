import pandas as pd

class Data:

    def __init__(self, frame_no, stringer_no, weld_no, type):
        self.frame_no = frame_no
        self.stringer_no = stringer_no
        self.weld_no = weld_no
        self.type = type
        self.frame = pd.read_csv('.\Frame_' + str(frame_no) + '\\1kHz_' + str(stringer_no)+'_' + str(weld_no) + '.dat', delimiter='\t', skiprows=[0], header=['Time_step', 'Pressure', 'Displacement'])
