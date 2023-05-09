import numpy as np
import matplotlib.pyplot as plt
from load import *
from sklearn.preprocessing import Normalizer, StandardScaler
import seaborn as sns
from Autoencoder import LOF
from collections import defaultdict
from shape import *


def Data_Power(total):
    X = pd.DataFrame()
    max_row = 0
    
    for i in range(0, len(total)):
        tmp_col = total[i].frame['Power'].dropna().to_numpy()
        #print(tmp_col, tmp_col.shape[0])
        if tmp_col.shape[0] > max_row:
                max_row = tmp_col.shape[0]

    for i in range(0, len(total)):
        #count = 0
        tmp_col_1 = pd.DataFrame(total[i].frame['Power'].dropna().to_numpy())
        X = pd.concat([X, tmp_col_1], axis=1)
        X.fillna(0, inplace=True)
    return X.T

def Data_Pres(total):
    X = pd.DataFrame()
    max_row = 0
    
    for i in range(0, len(total)):
        tmp_col = total[i].frame['Pressure'].dropna().to_numpy()
        #print(tmp_col, tmp_col.shape[0])
        if tmp_col.shape[0] > max_row:
                max_row = tmp_col.shape[0]

    for i in range(0, len(total)):
        #count = 0
        tmp_col_1 = pd.DataFrame(total[i].frame['Pressure'].dropna().to_numpy())
        X = pd.concat([X, tmp_col_1], axis=1)
        X.fillna(0, inplace=True)
    return X.T

def Data_Disp(total):
    X = pd.DataFrame()
    max_row = 0
    
    for i in range(0, len(total)):
        tmp_col = total[i].frame['Displacement'].dropna().to_numpy()
        #print(tmp_col, tmp_col.shape[0])
        if tmp_col.shape[0] > max_row:
                max_row = tmp_col.shape[0]

    for i in range(0, len(total)):
        #count = 0
        tmp_col_1 = pd.DataFrame(total[i].frame['Displacement'].dropna().to_numpy())
        X = pd.concat([X, tmp_col_1], axis=1)
        X.fillna(0, inplace=True)
    return X.T

def counter(abnomal_skin, b):
     counts = defaultdict(int)
     list_of_suspicious = []
     list_of_baddy = []

     for result in abnomal_skin:
          counts[result] += 1

     for result, count in counts.items():
          if count == b-2 or b-1:
               list_of_suspicious.append(result)
          if count == b:
               list_of_baddy.append(result)
     
     
     return list_of_suspicious, list_of_baddy

def standard(X0):
     scaler_0 = StandardScaler()
     normalized_features_0 = scaler_0.fit_transform(X0)
     scaler0 = Normalizer()
     normalized_features0 = scaler0.fit_transform(normalized_features_0)
     normalized_data0 = pd.DataFrame(normalized_features0, columns = X0.columns)
     return normalized_data0

def peaks():
     for frame in range(1,13):
          for weld in range(1,7):
               all_peaks = []
               try:
                    obj = dt(frame, 20, weld, 1)
               except:
                    continue
               else:
                    if 'Power' not in obj.frame.keys() or len(obj.frame['Power'].dropna())==0:
                         continue
                    else:
                         obj.smoothing()
                         peaks = get_peaks(obj)
                         all_peaks += peaks
          # print(str(i)+str(all_peaks))
               if len(all_peaks)!= 0:
                    roots, values, second_devs = zip(*all_peaks)
     return values

#activation
vis = 0
map = 0
local = 0
list_ = 0
power = 0
pressure = 1
displacement = 0
loc_maximum = 0

'''Data processing'''
if power == 1:
     #clip_to_skin
     total0 = iterate_points(type = 0)
     X0 = Data_Power(total0)
     #clip_to_frame
     total1 = iterate_points(type = 1)
     X1 = Data_Power(total1)
if pressure == 1:
     total0 = iterate_points(type = 0)
     X0 = Data_Power(total0)
     #clip_to_frame
     total1 = iterate_points(type = 1)
     X1 = Data_Power(total1)
if displacement == 1:
     total0 = iterate_points(type = 0)
     X0 = Data_Disp(total0)
     #clip_to_frame
     total1 = iterate_points(type = 1)
     X1 = Data_Disp(total1)
if loc_maximum == 1:
     X0 = peaks()


#Data Normalization
normalized_data0 = standard(X0)
normalized_data1 = standard(X1)
#print(normalized_data0)

a = 3
abnomal_skin, abnomal_frame, X_0, X_scores_0, X_1, X_scores_1, outlier_indice_0, outlier_indice_1 = LOF(a, X0, X1, total0, total1, normalized_data0, normalized_data1)
radius_0 = (X_scores_0.max() - X_scores_0) / (X_scores_0.max() - X_scores_0.min())
radius_1 = (X_scores_1.max() - X_scores_1) / (X_scores_1.max() - X_scores_1.min())

#ill_list
if list_ == 1:
     list_of_suspicious_skin, list_of_baddy_skin = counter(abnomal_skin, a)
     list_of_suspicious_frame, list_of_baddy_frame = counter( abnomal_frame, a)
     print(list_of_baddy_skin, list_of_baddy_frame, list_of_suspicious_skin, list_of_suspicious_frame)


#Visualization
if vis == 1:
     fig, (ax0, ax1) = plt.subplots(1, 2)

     ax0.scatter(X_0[:, 1], X_0[:, 2], color="m", s=3.0, label="Data points")
     # plot circles with radius proportional to the outlier scores

     ax0.scatter(
     X_0[:, 0],
     X_0[:, 1],
     s=1000 * radius_0,
     edgecolors="g",
     facecolors="none",
     label="Outlier scores",
     )
     ax0.legend(loc="upper left")
     ax0.title.set_text("Local Outlier Factor (LOF) for clip-to-skin")
     ax1.scatter(X_1[:, 1], X_1[:, 2], color="b", s=3.0, label="Data points")
     # plot circles with radius proportional to the outlier scores

     ax1.scatter(
     X_1[:, 0],
     X_1[:, 1],
     s=1000 * radius_1,
     edgecolors="c",
     facecolors="none",
     label="Outlier scores",
     )
     ax1.legend(loc="upper left")
     ax1.title.set_text("Local Outlier Factor (LOF) for clip-to-frame")
     plt.show()

#map
if map == 1:
     fig, (ax_0, ax_1) = plt.subplots(1, 2)

     x_plot = []
     y_plot = []

     for i in total0:
          x_plot.append(i.frame_no + ((i.weld_no-1)%3)/10 - 0.10)
          y_plot.append(i.stringer_no + ((i.weld_no-1)//3)/2.5 - 0.20)
     x_plot = np.array(x_plot)
     y_plot = np.array(y_plot)

     #print(x_plot[0:5], y_plot[0:5])

     idx = np.argsort(radius_0)
     sorted_x_plot = x_plot[idx]
     sorted_y_plot = y_plot[idx]
     #ssd_rank = np.arange(1,len(X_scores_0)+1)
     im1 = ax_0.scatter(sorted_x_plot, sorted_y_plot, c=radius_0*10, cmap='Oranges')
     fig.colorbar(im1, ax = ax_0)

     x_plot = []
     y_plot = []

     for i in total1:
          x_plot.append(i.frame_no + ((i.weld_no-1)%3)/10 - 0.10)
          y_plot.append(i.stringer_no + ((i.weld_no-1)//3)/2.5 - 0.20)
     x_plot = np.array(x_plot)
     y_plot = np.array(y_plot)

     idx = np.argsort(radius_1)
     sorted_x_plot = x_plot[idx]
     sorted_y_plot = y_plot[idx]
     #ssd_rank = np.arange(1,len(X_scores_1)+1)
     im2 = ax_1.scatter(sorted_x_plot, sorted_y_plot, c=radius_1*10, cmap='Blues')
     fig.colorbar(im2, ax = ax_1)
     plt.show()

if local == 1:
     score_skin_frame = np.zeros(12)
     score_skin_stringer = np.zeros(27)
     score_frame_frame = np.zeros(12)
     score_frame_stringer = np.zeros(29)
     c = 0
     d = 0

     for i in total0:
          score_skin_frame[i.frame_no-1] += radius_0[c]
          score_skin_stringer[i.stringer_no-1] += radius_0[c]
          c+=1


     for j in total1:
          score_frame_frame[j.frame_no-1] += radius_1[d]
          score_frame_stringer[j.stringer_no-1] += radius_1[d]
          d+=1

     fig, axs = plt.subplots(2, 2)
     
     axs[0,0].bar(np.linspace(0,12,12),np.abs(score_skin_frame))
     axs[0,1].barh(np.linspace(0,27,27),np.abs(score_skin_stringer))
     axs[1,0].bar(np.linspace(0,12,12),np.abs(score_frame_frame))
     axs[1,1].barh(np.linspace(0,29,29),np.abs(score_frame_stringer))

     plt.show()
