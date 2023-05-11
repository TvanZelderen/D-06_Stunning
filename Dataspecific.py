import numpy as np
import matplotlib.pyplot as plt
from load import *
from sklearn.preprocessing import Normalizer, StandardScaler
import seaborn as sns
from Autoencoder import LOF
from collections import defaultdict
import csv
#from shape import get_peaks


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
          if b > 4:
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

# def peaks(total):
#      all_peak =[]
#      for i in total:
#           i.smoothing()
#           peak = get_peaks(i)
#           all_peak += peak
#           if len(all_peak) != 0:
#                roots, values, second_devs = zip(*all_peak)
#      return values, second_devs

#activation
vis = 0
map = 0
local = 0
list_ = 0
power = 1
pressure = 0
displacement = 0
loc_maximum = 0
clustering_list = 1

a = 1

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
# if loc_maximum == 1:
#      total2 = iterate_points(type = 0)
#      X0 = peaks(total2)
#      print(X0)


#Data Normalization
normalized_data0 = standard(X0)
normalized_data1 = standard(X1)
#print(normalized_data0)


abnomal_skin, abnomal_frame, X_0, X_scores_0, X_1, X_scores_1, outlier_indice_0, outlier_indice_1 = LOF(a, X0, X1, total0, total1, normalized_data0, normalized_data1)
radius_0 = (X_scores_0.max() - X_scores_0) / (X_scores_0.max() - X_scores_0.min())
radius_1 = (X_scores_1.max() - X_scores_1) / (X_scores_1.max() - X_scores_1.min())

#ill_list
if list_ == 1:
     list_of_suspicious_skin, list_of_baddy_skin = counter(abnomal_skin, a)
     list_of_suspicious_frame, list_of_baddy_frame = counter( abnomal_frame, a)
     print(list_of_baddy_skin, list_of_baddy_frame, list_of_suspicious_skin, list_of_suspicious_frame)
     with open('list of ill-welding from AI model.csv', mode='w') as file:
          writer = csv.writer(file)
          writer.writerows(list_of_baddy_skin)

#Visualization
if vis == 1:
     fig, (ax0, ax1) = plt.subplots(1, 2)

     ax0.scatter(X_0[:, 0], X_0[:, 1], color="m", s=3.0, label="Data points")
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
     ax1.scatter(X_1[:, 0], X_1[:, 1], color="b", s=3.0, label="Data points")
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
     score_skin_frame = np.abs(score_skin_frame)/(np.abs(score_skin_frame)).max*10.0


     for j in total1:
          score_frame_frame[j.frame_no-1] += radius_1[d]
          score_frame_stringer[j.stringer_no-1] += radius_1[d]
          d+=1

     fig, axs = plt.subplots(2, 2)
     
     axs[0,0].bar(np.linspace(1,12,12),score_skin_frame, color='orange')
     axs[0,0].set_title('Outlier scores of clip-to-skin weldings along the frames')

     # axs[0,1].barh(np.linspace(1,27,27),np.abs(score_skin_stringer)/np.abs(score_skin_stringer).max*10.0, color='orange')
     # axs[0,1].set_title('Outlier scores of clip-to-skin weldings along the stringers')

     # axs[1,0].bar(np.linspace(1,12,12),np.abs(score_frame_frame)/(np.abs(score_frame_frame)).max*10.0, color='blue')
     # axs[1,0].set_title('Outlier scores of clip-to-frame weldings along the frames')

     # axs[1,1].barh(np.linspace(1,29,29),np.abs(score_frame_stringer)/(np.abs(score_frame_stringer)).max*10.0, color='blue')
     # axs[1,1].set_title('Outlier scores of clip-to-frame weldings along the stringers')

     plt.show()

if clustering_list == 1:
     file_list0 = []
     file_list1 = []

     for i in total0:
          file_list0.append([int(i.frame_no), int(i.stringer_no), int(i.weld_no), int(i.type)])

     #print((file_list0), len(radius_0))
     file_list_0 = np.concatenate((np.array(file_list0), np.array(radius_0*10).reshape(-1,1)), axis=1)

     for j in total1:
          file_list1.append([int(j.frame_no), int(j.stringer_no), int(j.weld_no), int(j.type)])

     file_list_1 = np.concatenate((np.array(file_list1), np.array(radius_1*10).reshape(-1,1)), axis=1)
     
     file_list = np.concatenate((file_list_0, file_list_1), axis=0)

     if power == 1:
          str = 'Power'
     if pressure == 1:
          str = 'Pressure'
     if displacement == 1:
          str = 'Displacement'

     with open('Clustering.csv', 'w', newline='') as file:
          writer = csv.writer(file)
          writer.writerows(file_list)
     
