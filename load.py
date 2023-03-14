import pandas as pd

class Data:

    def __init__(self, frame_no, stringer_no, weld_no, type):
        self.frame_no = frame_no
        self.stringer_no = stringer_no
        self.weld_no = weld_no
        self.type = type
        folder = '/Clip-to-Frame weld data' if type==True else '/Clip-to-Skin weld data'
        self.file_path = './STUNNING Demonstrator USW Data'+ folder + '/Frame_' + str(frame_no) + '/1kHz_' + str(stringer_no)+'_' + str(weld_no) + '.dat'
        self.frame = pd.read_csv(self.file_path, delimiter='\t', skiprows=[0], names=['Time_step', 'Pressure', 'Displacement'])

