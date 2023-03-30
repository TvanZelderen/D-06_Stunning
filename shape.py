#this is power throng's property
# print("\U0001F601")

from load import *
import numpy as np
import matplotlib.pyplot as plt

def root_finder(var, time):
    root_loc=[]
    for i in range(1,len(var)):
        if var[i]*var[i-1]<0:
            slope = (var[i]-var[i-1])/(time[i]-time[i-1])
            new_root = -var[i-1]/slope + time[i-1]
            root_loc.append(new_root)
        elif var[i] == 0:
            root_loc.append(time[i])
    
    return root_loc

def get_peaks(obj, power_norm=False, time_norm=False):
    peaks_valleys = []
    
    power = obj.frame['Smooth power'].to_numpy()    
    time = obj.frame['Time'].to_numpy()
    power, time = nan_filter(power,time)
    power_1 = np.gradient(power,time)    #first dev
    power_2 = np.gradient(power_1,time)  #second dev

    roots = root_finder(power_1,time)
    for t in roots:
        value = np.interp(t, time, power)
        second_dev = np.interp(t, time, power_2)
        if power_norm == True:
            avg_p = avg_power(obj)
            value /= avg_p
            second_dev /= avg_p
        if time_norm == True:
            tot_t = tot_time(obj)
            t /= tot_t
            second_dev *= tot_t
        peaks_valleys.append((t,value,second_dev))
    return peaks_valleys

if __name__ == '__main__': 
	main()
        
def main():
    i = Data(1,2,2,1)

    total = iterate_points(type=1)
    all_peaks = []
    for obj in total:
        if 'Power' not in obj.frame.keys() or len(obj.frame['Power'].dropna())==0:
            continue
        else:
            obj.smoothing()
            peaks = get_peaks(obj, time_norm=True, power_norm=True)
            all_peaks += peaks

    all_peaks = [x for x in all_peaks if x[2]<0]
    roots, values, second_devs = zip(*all_peaks)
    plt.scatter(roots, values)
    plt.show()






