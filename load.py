import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_ini(title):
    sns.set_theme()
    fig, ax = plt.subplots()
    plt.title(title)
    plt.xlabel('Time [s]')

    global legend
    legend = []
    return ax 

class Data:

    def __init__(self, frame_no, stringer_no, weld_no, data_type):

        #defining variables
        self.frame_no = frame_no
        if frame_no >= 10:
            frame_name = '/Frame_' + str(frame_no)
        else:
            frame_name = '/Frame_0' + str(frame_no)
        self.stringer_no = stringer_no
        if stringer_no >= 10:
            stringer_name = '_' + str(stringer_no)
        else:
            stringer_name = '_0' + str(stringer_no)
        self.weld_no = weld_no
        if weld_no >= 10:
            weld_name = '_' + str(weld_no)
        else:
            weld_name = '_0' + str(weld_no)
        self.folder = '/Clip-to-Frame weld data' if data_type == True else '/Clip-to-Skin weld data'
        try:
            self.file_path_1kHz = './STUNNING Demonstrator USW Data'+ self.folder + frame_name + '/' + '1kHz' + stringer_name + weld_name + '.dat'
            self.frame = pd.read_csv(self.file_path_1kHz, delimiter='\t', skiprows=[0], names=['Time', 'Pressure', 'Displacement'])
        except FileNotFoundError:
            print('No 1kHz data available')
        try:
            file_path_100Hz = './STUNNING Demonstrator USW Data'+ self.folder + frame_name + '/' + '100Hz' + stringer_name + weld_name + '.dat'
            power = pd.read_csv(file_path_100Hz, delimiter='\t', skiprows=[0], names=['Time', 'Power'])
            self.frame = self.frame.join(power.set_index('Time'), on='Time')
        except FileNotFoundError:
            print('No power data available')

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

    def plot(self, axes, power=False, displacement=False, force=False):
        if self.type == True:
            loc = 'Frame'
        else:
            loc = 'Skin'
        main_label = loc+'_'+str(self.frame_no)+'_'+str(self.stringer_no)+'_'+str(self.weld_no)

        if force==True:
            sns.lineplot(data=self.frame, x='Time', y='Force', ax=axes)
            legend.append(main_label+' Force')
        if displacement==True:
            sns.lineplot(data=self.frame, x='Time', y='Displacement', ax=axes)
            legend.append(main_label+' Displacement')
        if power==True:
            sns.lineplot(data=self.frame, x='Time', y='Power', ax=axes)
            legend.append(main_label+' Power')

def plot_legends():
    plt.legend( loc='upper left', labels=legend)
    plt.show()

def save_with_legends(filename):
    plt.legend( loc='upper left', labels=legend)
    plt.savefig(filename)      

def test():
    a = Data(2, 2, 2, 1)
    a.normalize()
    a.bar_to_N()
    print(a.frame)
