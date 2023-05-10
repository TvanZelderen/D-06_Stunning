from load import Data as dt
import numpy as np
import matplotlib.pyplot as plt
from load import *
import random
from scipy.signal import savgol_filter
from sklearn.linear_model import LinearRegression

a = dt('09', '07', '06', 0) #choose (frame_no, stringer_no, weld_no, type) for pressure graphs

def peakvalues2(a): #pressure graph, with its corresponding upper and lower peak values and number of upper and lower peak values
    a.create_array()

    p = a.frame['Pressure'].to_numpy()
    t = a.frame['Time'].to_numpy()
    avg = np.average(p) #average of pressure graphs
    std = np.std(p) #standard deviation of pressure graphs
    n = 2

    p_peak_high = p[np.where(p > (avg+n*std))]
    t_peak_high = t[np.where(p > (avg+n*std))]

    p_peak_low = p[np.where(p < (avg-n*std))]
    t_peak_low = t[np.where(p < (avg-n*std))]

    p_peak_merged = np.concatenate((p_peak_high, p_peak_low))
    t_peak_merged = np.concatenate((t_peak_high, t_peak_low))

    Np_peak_merged = len(np.unique(p_peak_merged)) #number of peaks in merged pressure graph
    Vp_peak_merged = np.unique(p_peak_merged) #array of peak values for merged pressure


    plt.scatter(t_peak_merged, p_peak_merged)
    print("The merged peak values are:", Vp_peak_merged)
    print("The number of merged peak values are:", Np_peak_merged)

    plt.plot(t, p)
    plt.show()


def boxplots2(): #boxplots of upper and lower pressure graph peaks
    atotal = iterate_points(type=0, frames='All', stringers='All', welds='All')  # choose type, frames, stringers, welds
    diffl = []

    for i in atotal:
        p = i.frame['Pressure'].to_numpy()
        t = i.frame['Time'].to_numpy()
        avg = np.average(p)  # average of pressure graphs
        std = np.std(p)  # standard deviation of pressure graphs
        n = 2

        p_peak_high = p[np.where(p > (avg + n * std))]
        p_peak_high_max = np.max(p_peak_high)
        p_peak_low = p[np.where(p < (avg - n * std))]
        p_peak_low_min = np.min(p_peak_low)
        diff = np.abs(p_peak_high_max - p_peak_low_min)
        diffl.append(avg)
        i.avg = avg

    # Calculate boxplot and extract outliers
    box = plt.boxplot([np.unique(diffl)])
    outliers = box["fliers"][0].get_data()[1]

    # Find combinations corresponding to outliers
    outliers_list = []
    for i, outlier in enumerate(outliers):
        for point in atotal:
            if point.avg == outlier:
                outlier_combination = {
                    'type': point.type,
                    'frame': point.frame_no,
                    'stringer': point.stringer_no,
                    'weld': point.weld_no
                }
                outliers_list.append((outlier_combination, outlier))
    plt.show()
    print(outliers_list)

def test():
    atotal = iterate_points(type= 0, frames='All', stringers='All', welds='All')
    outliers_list = [] 
    x_plot = []
    y_plot = []
    stdmed = []
    scores = []
    dot_alpha = 1

    jitter_amount = 0.2

    for i in atotal:
        p = i.frame['Pressure'].to_numpy()
        t = i.frame['Time'].to_numpy()
        window_size = 1000
        poly_order = 0

        p_smooth = savgol_filter(p, window_size, poly_order)
        aveg = np.average(p_smooth)

        
        #Calculate residuals
        residuals = np.abs(p_smooth - aveg)
        # Calculate the standard deviation of the residuals # ROOT MEAN SQUARE ERROR
        std_deviation = np.sqrt((np.sum((residuals)**2))/(len(p_smooth)))
        #std_deviation = (np.std(residuals))
        stdmed.append(std_deviation)

      #  plt.plot(t, p, label='Original Data')
       # plt.plot(t, p_smooth, label='Smoothed Data')
       # plt.axhline(y=aveg, color='red', linestyle='--', label='Average')
       # plt.xlabel('Time')
       # plt.ylabel('Pressure')
       # plt.title('Smoothed Pressure Graph with Linear Regression')
        #plt.legend()
        #plt.show()

        outliers_list.append({
            'type': i.type,
            'frame': i.frame_no,
            'stringer': i.stringer_no,
            'weld': i.weld_no
        })        
        
    min_var = min(stdmed)
    max_var = max(stdmed)

    log_min_var = np.sqrt(1.0*(min_var))
    log_max_var = np.sqrt(1.0*(max_var))

    for var in stdmed:
        log_var = np.sqrt(1.0*(var))
        score = 10 * (log_var - log_min_var) / (log_max_var - log_min_var)
        scores.append(score)

    for i, item in enumerate(outliers_list):
        item['score'] = scores[i]


    for i in atotal:
        x_jittered = i.frame_no + random.uniform(-jitter_amount, jitter_amount)
        x_plot.append(x_jittered)
        y_plot.append(i.stringer_no)

    plt.scatter(x_plot, y_plot, facecolor='gray', c=scores, cmap='coolwarm', vmax = 10)
    plt.colorbar()
    plt.xlabel("Frame number")
    plt.ylabel("Stringer number")
    plt.grid(True, linestyle='-', linewidth=0.5, zorder = 0)
    plt.show()

    outlists = [    np.array([        item['frame'],
            item['stringer'],
            item['weld'],
            item['type']
        ])
        for item in outliers_list
    ]
    for arr, score in zip(outlists, scores):
        print(arr.tolist(), score)




def boxplots222(): 
    atotal = iterate_points(type= 0, frames='All', stringers='All', welds='All')
    outliers_list = [] 
    variances = []
    x_plot = []
    y_plot = []
    scores = []
    dot_alpha = 1

    jitter_amount = 0.2

    for i in atotal:
        p = i.frame['Pressure'].to_numpy()
        avg = np.average(p)
        std = np.std(p)
        n = 2

        p_peak_high = p[np.where(p > (avg+n*std))]
        p_peak_low = p[np.where(p < (avg-n*std))]
        p_peak_merged = np.concatenate((p_peak_high, p_peak_low))
        Vp_peak_merged = np.unique(p_peak_merged)
        Np_peak_merged = len(np.unique(p_peak_merged))
        VAR = np.sqrt((np.sum((Vp_peak_merged-avg)**2))/(Np_peak_merged))
        variances.append(VAR)
        outliers_list.append({
            'type': i.type,
            'frame': i.frame_no,
            'stringer': i.stringer_no,
            'weld': i.weld_no
        })        
        
    min_var = min(variances)
    max_var = max(variances)

    log_min_var = (min_var)
    log_max_var = (max_var)

    for var in variances:
        log_var = (var)
        score = 10 * (log_var - log_min_var) / (log_max_var - log_min_var)
        scores.append(score)

    for i, item in enumerate(outliers_list):
        item['score'] = scores[i]


    for i in atotal:
        x_jittered = i.frame_no + random.uniform(-jitter_amount, jitter_amount)
        x_plot.append(x_jittered)
        y_plot.append(i.stringer_no)

    plt.scatter(x_plot, y_plot, facecolor='gray', c=scores, cmap='coolwarm', alpha=dot_alpha, vmax = 6)
    plt.colorbar()
    plt.xlabel("Frame number")
    plt.ylabel("Stringer number")
    plt.grid(True, linestyle='-', linewidth=0.5, zorder = 0)
    plt.show()

    outlists = [    np.array([        item['frame'],
            item['stringer'],
            item['weld'],
            item['type']
        ])
        for item in outliers_list
    ]
    
    
    #with open('suspectwelds_pressure.txt', 'w') as f:
      #  print(f'Opened {f.name} for writing')
      #  for arr, score in zip(outlists, scores):
      #      print(arr.tolist(), score)
      #      f.write(str(arr.tolist()) + ' ' + str(score) + '\n')


#boxplots2()  #boxplots of upper pressure peaks
#peakvalues2(a) #plots of pressure peaks with upper and lower maximum values
boxplots222() #boxplots of upper and lower pressure peaks
#test()