import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sns
import logging

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
        self.frame_string = '/Frame_'+str(frame_no).zfill(2)
        self.stringer_no = stringer_no
        self.stringer_string = '_'+str(stringer_no).zfill(2)
        self.weld_no = weld_no
        self.weld_string = '_'+str(weld_no).zfill(2)
        self.type = type # True: clip-to-frame, False: clip-to-skin
        folder = '/Clip-to-Frame weld data' if type==True else '/Clip-to-Skin weld data'
        try:
            self.file_path_1kHz = './STUNNING Demonstrator USW Data'+ folder + self.frame_string + '/' + '1kHz' + self.stringer_string + self.weld_string + '.dat'
            self.frame = pd.read_csv(self.file_path_1kHz, delimiter='\t', skiprows=[0], names=['Time', 'Pressure', 'Displacement'])
        except FileNotFoundError:
            logging.info(f'No data for {self.file_path_1kHz} found.')
        try:
            self.file_path_100Hz = './STUNNING Demonstrator USW Data'+ folder + self.frame_string + '/' + '100Hz' + self.stringer_string + self.weld_string + '.dat'
            power = pd.read_csv(self.file_path_100Hz, delimiter='\t', skiprows=[0], names=['Time', 'Power'])
            self.frame = self.frame.join(power.set_index('Time'), on='Time')
        except FileNotFoundError:
            logging.info(f'No data for {self.file_path_100Hz} found.')

        self.__normalize()
        self.__bar_to_N()

    def create_array(self): # convert pandas data frame to numpy array
        self.array = self.frame.to_numpy()
        #print(self.array)

    def smoothing(self, window=12, order=3):
        power_frame = self.frame['Power'].dropna()
        power_frame = power_frame[:-1]
        power_data = power_frame.to_numpy()
        window = min(window, len(power_data))
        if len(power_data) == 0:
            return None
        smooth_power = sp.signal.savgol_filter(power_data, window_length=window, polyorder=order)
        power_frame = power_frame.to_frame(name='Power')
        power_frame['Smooth power'] = smooth_power.tolist()
        self.frame = self.frame.join(power_frame['Smooth power'])
    
    def plot(self, axes, power=False, displacement=False, force=False, smooth_power = False, norm_power = False):
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
        if smooth_power==True:
            try:
                sns.lineplot(data=self.frame, x='Time', y='Smooth power', ax=axes)
            except:
                print('Smooth power data for '+main_label+' is not available.')
            else:  
                legend.append(main_label+' Smooth power')
                legend.append('')
        if norm_power==True:
            try:
                sns.lineplot(data=self.frame, x='Normalized time', y='Normalized power', ax=axes)
            except:
                print('Normalized power data for '+main_label+' is not available.')
            else:  
                legend.append(main_label+' Normalized power')
                legend.append('')

    def power_norm(self):
        power = self.frame['Power'].dropna()
        idx = power.index[-1]

        average_power = avg_power(self)
        self.frame['Normalized power'] = self.frame['Power'].div(average_power)
        self.frame['Normalized power'][idx] = np.nan

        total_time = tot_time(self)
        self.frame['Normalized time'] = self.frame['Time'].div(total_time)

    #def __del__(self):
    #    print('Destructor called, kill me too please.')

def plot_legends():
    plt.legend(loc = 2, bbox_to_anchor = (1,1), labels=legend)
    plt.show()

def save_with_legends(filename):
    plt.legend(loc = 2, bbox_to_anchor = (1,1), labels=legend)
    plt.savefig(filename, bbox_inches = 'tight')      

def energy(frame:list = [1], stringer:list = [2, 3], weld:list = [1], type:int = 1):
    from scipy.integrate import simpson

    data = iterate_points(frames=frame, stringers=stringer, welds =weld, type=type)
    energy = []
    for i in data:
        try: 
            p = i.frame['Power'].dropna().to_numpy()
            t = i.frame['Time'].drop(i.frame['Power'].isna()*range(len(i.frame['Power']))).to_numpy()
            energy.append([i.frame_no, i.stringer_no, i.weld_no, i.type, simpson(p, t)])
        except:
            energy.append([i.frame_no, i.stringer_no, i.weld_no, i.type, 0])
    #print('Energy: ' + str(energy))
    df_energy = pd.DataFrame(energy, columns=['Frame', 'Stringer', 'Weld', 'Type', 'Energy'])
    return df_energy

def iterate_points(type = 1, frames='All', stringers='All', welds='All'):
    if frames == 'All':
        frames = range(1,13)
    if stringers == 'All':
        stringers = range(1,30)
    if welds == 'All':
        welds = range(1,7)
    if type == 'All':
        types = range(0,2)
    else:
        types = [type]

    valid_welds = []
    for type in types:
        for frame_no in frames:
            for stringer_no in stringers:
                for weld_no in welds:
                    try:
                        new_object = Data(frame_no, stringer_no, weld_no, type)
                        new_object.frame
                    except:
                        pass
                    else:
                        valid_welds.append(new_object)
    return valid_welds

def nan_filter(var, time):
    from math import isnan

    time_fil = []
    var_fil = []
    for i in range(len(var)):
        if isnan(var[i]):
            continue
        else:
            time_fil.append(time[i])
            var_fil.append(var[i])
    
    return var_fil, time_fil

def test():
    ax = plot_ini('Normalized')
    obj = Data(1,2,2,1)
    obj.power_norm()
    obj.plot(ax, norm_power = True)
    plot_legends()

def tot_time(obj):
    power = obj.frame['Power'].dropna()
    idx = power.index[-2]
    time = obj.frame['Time'][idx]
    return time

def avg_power(obj):
    energy_df = energy(frame=[obj.frame_no], stringer=[obj.stringer_no], weld=[obj.weld_no], type= obj.type)
    power = energy_df['Energy'][0]/tot_time(obj)
    return power

if __name__ == '__main__': 
	test()


