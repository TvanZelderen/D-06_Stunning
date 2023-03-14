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

    def normalize(self):
        time_0 = self.frame.at[0, 'Time_step']
        self.frame['Time_step'] = self.frame['Time_step'].sub(time_0)
        self.frame['Time_step'] = self.frame['Time_step'].div(1000)
        # print(self.frame['Time_step'][0:10])

    def bar_to_N(self):
        self.frame['Pressure'] = self.frame['Pressure'].mul(266.667)
        print(self.frame['Pressure'][0:10])

a = Data('01', '02', '01', 1)
a.normalize()
a.bar_to_N()

