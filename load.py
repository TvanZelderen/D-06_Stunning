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

    def __normalize(self): # normalize time step to start from 0
        time_0 = self.frame.at[0, 'Time']
        self.frame['Time'] = self.frame['Time'].sub(time_0)
        self.frame['Time'] = self.frame['Time'].div(1000)

    def __bar_to_N(self): # convert 1 bar = 266.667 N/m^2
        self.frame['Force'] = self.frame['Pressure'].mul(266.667)
        # print(self.frame['Pressure'][0:10])

    def __init__(self, frame_no, stringer_no, weld_no, type):

        #defining variables
        self.frame_no = frame_no
        if frame_no < 10:
            self.frame_string = '/Frame_'+'0'+str(frame_no)
        else:
            self.frame_string = '/Frame_'+str(frame_no)
        self.stringer_no = stringer_no
        if stringer_no < 10:
            self.stringer_string = '_0'+str(stringer_no)
        else:
            self.stringer_string = '_'+str(stringer_no)
        self.weld_no = weld_no
        if weld_no < 10:
            self.weld_string = '_0'+str(weld_no)
        else:
            self.weld_string = '_'+str(weld_no)
        self.type = type # True: clip-to-frame, False: clip-to-skin
        folder = '/Clip-to-Frame weld data' if type==True else '/Clip-to-Skin weld data'
        try:
            self.file_path_1kHz = './STUNNING Demonstrator USW Data'+ folder + self.frame_string + '/' + '1kHz' + self.stringer_string + self.weld_string + '.dat'
            self.frame = pd.read_csv(self.file_path_1kHz, delimiter='\t', skiprows=[0], names=['Time', 'Pressure', 'Displacement'])
        except FileNotFoundError:
            print(f'File {self.file_path_1kHz} not found.')
        try:
            file_path_100Hz = './STUNNING Demonstrator USW Data'+ folder + self.frame_string + '/' + '100Hz' + self.stringer_string + self.weld_string + '.dat'
            power = pd.read_csv(file_path_100Hz, delimiter='\t', skiprows=[0], names=['Time', 'Power'])
            self.frame = self.frame.join(power.set_index('Time'), on='Time')
        except FileNotFoundError:
            print(f'No power data for {self.file_path_1kHz} found.')

        self.__normalize()
        self.__bar_to_N()

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
            legend.append('')
        if displacement==True:
            sns.lineplot(data=self.frame, x='Time', y='Displacement', ax=axes)
            legend.append(main_label+' Displacement')
            legend.append('')
        if power==True:
            try:
                sns.lineplot(data=self.frame, x='Time', y='Power', ax=axes)
            except:
                print('Power data for '+main_label+' is not available.')
            else:  
                legend.append(main_label+' Power')
                legend.append('')

def plot_legends():
    plt.legend(loc = 2, bbox_to_anchor = (1,1), labels=legend)
    plt.show()

def save_with_legends(filename):
    plt.legend(loc = 2, bbox_to_anchor = (1,1), labels=legend)
    plt.savefig(filename, bbox_inches = 'tight')      

def iterate_points(type = 1, frames='All', stringers='All', welds='All'):
    if frames == 'All':
        frames = range(1,13)
    if stringers == 'All':
        stringers = range(1,30)
    if welds == 'All':
        welds = range(1,7)

    valid_welds = []
    for frame_no in frames:
        if frame_no < 10:
            frame_no = '0'+str(frame_no)
        else:
            frame_no = str(frame_no)
        
        for stringer_no in stringers:
            if stringer_no < 10:
                stringer_no = '0'+str(stringer_no)
            else:
                stringer_no = str(stringer_no)
            
            for weld_no in welds:
                if weld_no < 10:
                    weld_no = '0'+str(weld_no)
                else:
                    weld_no = str(weld_no)
                
                try:
                    new_object = Data(frame_no, stringer_no, weld_no, type)
                except:
                    pass
                else:
                    valid_welds.append(new_object)
    return valid_welds

def test():
    a = Data(1, 2, 2, 1)
    print(a.frame[0:10])

# test()
