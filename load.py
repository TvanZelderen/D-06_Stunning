import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_ini(title):
    fig, ax = plt.subplots()
    plt.title(title)
    plt.xlabel('Time [s]')
    return ax

class Data:

    def __init__(self, frame_no, stringer_no, weld_no, type):

        #defining variables
        self.frame_no = frame_no
        self.stringer_no = stringer_no
        self.weld_no = weld_no
        self.type = type # True: clip-to-frame, False: clip-to-skin
        folder = '/Clip-to-Frame weld data' if type==True else '/Clip-to-Skin weld data'
        self.file_path_1kHz = './STUNNING Demonstrator USW Data'+ folder + '/Frame_' + str(frame_no) + '/' + '1kHz' + '_' + str(stringer_no)+'_' + str(weld_no) + '.dat'
        self.frame = pd.read_csv(self.file_path_1kHz, delimiter='\t', skiprows=[0], names=['Time', 'Pressure', 'Displacement'])
        file_path_100Hz = './STUNNING Demonstrator USW Data'+ folder + '/Frame_' + str(frame_no) + '/' + '100Hz' + '_' + str(stringer_no)+'_' + str(weld_no) + '.dat'
        power = pd.read_csv(file_path_100Hz, delimiter='\t', skiprows=[0], names=['Time', 'Power'])
        self.frame = self.frame.join(power.set_index('Time'), on='Time')

    def normalize(self): # normalize time step to start from 0
        time_0 = self.frame.at[0, 'Time']
        self.frame['Time'] = self.frame['Time'].sub(time_0)
        self.frame['Time'] = self.frame['Time'].div(1000)

    def bar_to_N(self): # convert 1 bar = 266.667 N/m^2
        self.frame['Force'] = self.frame['Pressure'].mul(266.667)
        # print(self.frame['Pressure'][0:10])

    def create_array(self): # convert pandas data frame to numpy array
        self.array = self.frame.to_numpy()
        #print(self.array)

    def plot(self, axes, power=True, displacement=True, pressure=True):
        if pressure==True:
            sns.lineplot(data=self.frame, x='Time_step', y='Pressure', ax=axes)
        if displacement==True:
            sns.lineplot(data=self.frame, x='Time_step', y='Displacement', ax=axes)
        # if power==True:
        #     sns.lineplot(data=self.frame, x='Time_step', y='Power', ax=ax)         
    
'''a = Data('01', '02', '02', 1)
a.normalize()
a.bar_to_N()
print(a.frame[0:10])

