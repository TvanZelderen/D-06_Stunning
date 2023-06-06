from load import Data as dt
import numpy as np
import matplotlib.pyplot as plt
from load import *
import random
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
sns.set_theme()

a = dt('5', '23', '2', 1) #choose (frame_no, stringer_no, weld_no, type) for pressure graphs

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

def filter():
    atotal = iterate_points(type= 0, frames='All', stringers='All', welds='All')
    outliers_list = [] 
    x_plot = []
    y_plot = []
    stdmed = []
    scores = []
    dot_alpha = 1
    def sine_function(x, A, B, C, D):
        return A * np.sin(B * x + C) + D

    jitter_amount = 0.2

    for i in atotal:
        p = i.frame['Pressure'].to_numpy()
        t = i.frame['Time'].to_numpy()
        window_size = 1000
        poly_order = 0

        p_smooth = savgol_filter(p, window_size, poly_order)
        aveg = np.average(p_smooth)

        ##### TYPE 0 ####

        # Calculate residuals
        residuals = np.abs(p_smooth - aveg)
        # Calculate the standard deviation of the residuals # ROOT MEAN SQUARE ERROR
        std_deviation = np.sqrt((np.sum((residuals)**2))/(len(p_smooth)))
        stdmed.append(std_deviation)

        ##### TYPE 1 ####

        # amplitude = 0.6
        # frequency = 3
        # phase = 0
        # mean_value = aveg

        # initial_guess = [amplitude, frequency, phase, mean_value]
        # optimized_params, _ = curve_fit(sine_function, t, p_smooth, p0=initial_guess)
        # p_fitted = sine_function(t, *optimized_params)
        # residuals = np.abs(p_smooth - p_fitted)
        # std_deviation = np.sqrt((np.sum((residuals)**2))/(len(p_smooth)))
        # stdmed.append(std_deviation)

        # plt.plot(t, p, label='Original Data')
        # plt.plot(t, p_smooth, label='Smoothed Data')
        # plt.plot(t, p_fitted, label='Fitted Sine Curve')
        # plt.axhline(y=aveg, color='red', linestyle='--', label='Average')
        # plt.xlabel('Time')
        # plt.ylabel('Pressure')
        # plt.title('Smoothed Pressure Graph with Sine Curve Fit')
        # plt.legend()
        # plt.show()

        # plt.plot(t, p, label='Original Data')
        # plt.plot(t, p_smooth, label='Smoothed Data')
        # plt.axhline(y=aveg, color='red', linestyle='--', label='Average')
        # plt.xlabel('Time')
        # plt.ylabel('Pressure')
        # plt.title('Smoothed Pressure Graph with Linear Regression')
        # plt.legend()
        # plt.show()

        outliers_list.append({
            'type': i.type,
            'frame': i.frame_no,
            'stringer': i.stringer_no,
            'weld': i.weld_no
        })     

    max_var = max(stdmed)
    min_var = min(stdmed)

    scores = []
    for var in stdmed:
        score = 10.0 * (var - min_var) / (max_var - min_var)
        scores.append(score)


    for i, item in enumerate(outliers_list):
        item['score'] = scores[i]        




    for i in atotal:
        #x_jittered = i.frame_no + random.uniform(-jitter_amount, jitter_amount)

        #for type 0
        x_plot.append(i.frame_no + ((i.weld_no-1)%3)/6 - 1/6)
        y_plot.append(i.stringer_no + ((i.weld_no-1)//3)/2.5 - 0.20)

        # #for type 1
        # x_plot.append(i.frame_no + i.weld_no/5 - 3/10)
        # y_plot.append(i.stringer_no)
    
    #for type 0
    plt.scatter(x_plot, y_plot, c=scores, cmap='coolwarm', s=10, clim=(0,7))
    # #for type 1
    # plt.scatter(x_plot, y_plot, c=scores, cmap='coolwarm', s=15, clim=(0,10))

    cbar = plt.colorbar()
    cbar.set_label('Score [-]', rotation=90)
    plt.xlabel('Frame number [-]')
    plt.ylabel('Stringer number [-]')
    plt.show()

    outlists = [
        np.array([
            item['frame'],
            item['stringer'],
            item['weld'],
            item['type']
        ])
        for item in outliers_list
    ]

    for arr, score in zip(outlists, scores):
        arr_str = ', '.join(str(x) for x in arr.tolist())
        print(f"[{arr_str}], {score}")

    average_score = np.average(scores)
    print(f"Average Score: {average_score}")

    # with open('Pressure_Scores_Clip_to_skin_PEAKS222.txt', 'w') as f:
    #     print(f'Opened {f.name} for writing')
    #     for arr, score in zip(outlists, scores):
    #         arr_str = ', '.join(str(x) for x in arr.tolist())
    #         f.write(f'"[{arr_str}]",{score}\n')


def boxplots222(): 
    atotal = iterate_points(type= 1, frames='All', stringers='All', welds=[1,2])
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
        
    max_var = max(variances)
    min_var = min(variances)

    scores = []
    for var in variances:
        score = 10.0 * (var - min_var) / (max_var - min_var)
        scores.append(score)


    for i, item in enumerate(outliers_list):
        item['score'] = scores[i]


    for i in atotal:
        #x_jittered = i.frame_no + random.uniform(-jitter_amount, jitter_amount)

        # #for type 0
        # x_plot.append(i.frame_no + ((i.weld_no-1)%3)/6 - 1/6)
        # y_plot.append(i.stringer_no + ((i.weld_no-1)//3)/2.5 - 0.20)

        #for type 1
        x_plot.append(i.frame_no + i.weld_no/5 - 3/10)
        y_plot.append(i.stringer_no)
    
    # #for type 0
    # plt.scatter(x_plot, y_plot, c=scores, cmap='coolwarm', s=10, clim=(0,5))
    #for type 1
    plt.scatter(x_plot, y_plot, c=scores, cmap='coolwarm', s=15, clim=(0,10))

    cbar = plt.colorbar()
    cbar.set_label('Score [-]', rotation=90)
    plt.xlabel('Frame number [-]')
    plt.ylabel('Stringer number [-]')
    plt.show()

    outlists = [
        np.array([
            item['frame'],
            item['stringer'],
            item['weld'],
            item['type']
        ])
        for item in outliers_list
    ]

    for arr, score in zip(outlists, scores):
        arr_str = ', '.join(str(x) for x in arr.tolist())
        print(f"[{arr_str}], {score}")

    average_score = np.average(scores)
    print(f"Average Score: {average_score}")

    with open('Pressure_Scores_Clip_to_skin_PEAKS222.txt', 'w') as f:
        print(f'Opened {f.name} for writing')
        for arr, score in zip(outlists, scores):
            arr_str = ', '.join(str(x) for x in arr.tolist())
            f.write(f'"[{arr_str}]",{score}\n')








#boxplots2()  #boxplots of upper pressure peaks
#peakvalues2(a) #plots of pressure peaks with upper and lower maximum values
boxplots222() #boxplots of upper and lower pressure peaks
#filter()