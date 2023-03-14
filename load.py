import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_ini():
    fig, ax = plt.subplots()
    return ax

class Data:

    def __init__(self, frame_no, stringer_no, weld_no, type, sample_rate=1000):

        #defining variables
        self.frame_no = frame_no
        self.stringer_no = stringer_no
        self.weld_no = weld_no
        self.type = type # True: clip-to-frame, False: clip-to-skin

        if sample_rate == 1000:
            self.sample_rate = '1kHz' # 1kHz
        else:
            self.sample_rate = '100Hz' # 100Hz
        folder = '/Clip-to-Frame weld data' if type==True else '/Clip-to-Skin weld data'
        self.file_path = './STUNNING Demonstrator USW Data'+ folder + '/Frame_' + str(frame_no) + '/' + self.sample_rate + '_' + str(stringer_no)+'_' + str(weld_no) + '.dat'
        self.frame = pd.read_csv(self.file_path, delimiter='\t', skiprows=[0], names=['Time_step', 'Pressure', 'Displacement'])
        sns.set_theme(style='darkgrid')

    def normalize(self): # normalize time step to start from 0
        time_0 = self.frame.at[0, 'Time_step']
        self.frame['Time_step'] = self.frame['Time_step'].sub(time_0)
        self.frame['Time_step'] = self.frame['Time_step'].div(1000)
        if self.sample_rate == '100Hz':
            self.frame['Time_step'] = self.frame['Time_step'].div(0.1)
        # print(self.frame['Time_step'][0:10])

    def bar_to_N(self): # convert 1 bar = 266.667 N/m^2
        self.frame['Pressure'] = self.frame['Pressure'].mul(266.667)
        # print(self.frame['Pressure'][0:10])

    def create_array(self): # convert pandas data frame to numpy array
        self.array = self.frame.to_numpy()
        #print(self.array)

    def plot(self, axes, power=True, displacement=True, pressure=True):
        if pressure==True:
            sns.lineplot(data=self.frame, x='Time_step [ms]', y='Pressure [Bar]', ax=axes)
        if displacement==True:
            sns.lineplot(data=self.frame, x='Time_step [ms]', y='Displacement [mm]', ax=axes)
        # if power==True:
        #     sns.lineplot(data=self.frame, x='Time_step', y='Power', ax=ax)         
    
a = Data('01', '02', '02', 1)
a.normalize()
a.bar_to_N()
a.create_array()

b = Data('01', '02', '01', 1)
b.normalize()
b.bar_to_N()

ax = plot_ini()
a.plot(axes=ax, displacement=False)
b.plot(axes=ax, displacement=False)
plt.show()



