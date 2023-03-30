# print("\U0001F601 \U0001F410")
print('this is power throng\'s property')


from load import *
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
sns.set_theme()

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

def mean_curve(obj_list):
    x_axis = np.arange(0,1.005,0.005)
    all_y = []
    for obj in obj_list:
        obj.power_norm()

        power = obj.frame['Normalized power'].to_numpy()    
        time = obj.frame['Normalized time'].to_numpy()
        power, time = nan_filter(power,time)

        y_interp = np.interp(x_axis,time,power)
        all_y.append(y_interp)
    all_y = np.array(all_y)
    y_mean = np.mean(all_y, axis=0)

    return x_axis, y_mean

def square_diff(x_axis, y_mean, obj):
    obj.power_norm()

    power = obj.frame['Normalized power'].to_numpy()    
    time = obj.frame['Normalized time'].to_numpy()
    power, time = nan_filter(power,time)

    loc_diff = (y_mean - np.interp(x_axis,time,power))**2
    obj.diff = sum(loc_diff)
    return obj.diff

def rank(obj):
    index = ranked_diff.index(obj.diff)
    ranking = index+1
    return ranking


if __name__ == '__main__':

    ax = plot_ini('test')    
    all_obj = iterate_points(type = 1)
    for i in all_obj:
        try:
            i.power_norm()
        except:
            all_obj.remove(i)
        # else:
        #     i.plot(ax, norm_power=True)
    
    x_axis, y_mean = mean_curve(all_obj)
    #plt.plot(x_axis, y_mean, linewidth=3, color='black')
    #plot_legends()

    for i in all_obj:
        square_diff(x_axis, y_mean, i)
        if i.diff < 0:
            i.plot(ax, norm_power=True)
    #plt.plot(x_axis, y_mean, linewidth=3, color='black')
   # plot_legends()

    diff_list = [obj.diff for obj in all_obj]

    ranked_obj = sorted(all_obj, key=lambda x: x.diff)
    ranked_diff = sorted(diff_list)

    for i in range(0,10):
        print(all_obj[i].main_label + ': Rank ' + str(rank(all_obj[i])) + ' out of ' + str(len(all_obj)))


    # plt.hist(diff_list,bins=30)
    # plt.show()

    # total = iterate_points(type=1)
    # all_peaks = []
    # for obj in total:
    #     if 'Power' not in obj.frame.keys() or len(obj.frame['Power'].dropna())==0:
    #         continue
    #     else:
    #         obj.smoothing()
    #         peaks = get_peaks(obj, time_norm=True, power_norm=True)
    #         all_peaks += peaks

    # all_peaks = [x for x in all_peaks if x[2]<0]
    # roots, values, second_devs = zip(*all_peaks)
    # plt.scatter(roots, values)
    # plt.show()
