import numpy as np
import matplotlib.pyplot as plt
from load import *
from sklearn.preprocessing import Normalizer, StandardScaler
import seaborn as sns
from Autoencoder import LOF
import collections
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

def numb(total0):
     count = defaultdict(int)
     count1 = defaultdict(int)
     num0_frame = []
     num0_stringer = []

     for i in total0:
          count[i.frame_no] += 1
     count = collections.OrderedDict(sorted(count.items()))
     for i, count in count.items():
          num0_frame.append(count)
          
     
     for i in total0:
          count1[i.stringer_no] += 1
     count1 = collections.OrderedDict(sorted(count1.items()))
     for i, count1 in count1.items():
          num0_stringer.append(count1)

     return num0_frame, num0_stringer

def scale(list1):
     list1 = np.abs(np.array(list1))
     list2 = (list1-list1.min())/(list1.max()-list1.min())*10 

     return list2

#activation
vis = 0
map = 1
local = 0
list_ = 0
power = 1
pressure = 0
displacement = 0
clustering_list = 0

a = 5

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
     im1 = ax_0.scatter(sorted_x_plot, sorted_y_plot, c=radius_0*10, cmap='coolwarm')
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
     im2 = ax_1.scatter(sorted_x_plot, sorted_y_plot, c=radius_1*10, cmap='coolwarm')
     fig.colorbar(im2, ax = ax_1)
     plt.show()

if local == 1:
     score_skin_frame = np.zeros(12)
     score_skin_stringer = np.zeros(27)
     score_frame_frame = np.zeros(12)
     score_frame_stringer = np.zeros(29)
     c = 0
     d = 0

     num_0_frame, num_0_stringer = numb(total0)
     num_1_frame, num_1_stringer = numb(total1)
     num_1_stringer = [1, 14, 4, 21, 14, 20, 19, 5, 8, 7, 10, 16, 13, 16, 19, 20, 15, 14, 6, 1, 1, 6, 11, 13, 14, 6, 6, 1, 2]
     if displacement == 1:
          dis_1_frame = [38.119999999999976, 121.26999999999995, 138.94, 3.87, 59.99999999999998, 95.36000000000001, 81.86, 242.05000000000004, 113.83, 45.749999999999986, 167.8, 234.14999999999998]
          dis_1_frame = scale(dis_1_frame)
          dis_1_stringer = [0, 0, 0.112079701, 13.117995018999999, 2.241594022, 15.0622665, 5.191469488999999, 3.4900373599999996, 11.162826897999999, 16.047633872000002, 5.361145704, 4.027085928, 2.3676836860000003, 10.350249066000002, 22.224470733000004, 11.776151930000001, 7.3178704859999995, 12.190224159, 2.5591531759999997, 0, 0, 3.9663760900000007, 7.182440846, 9.909713575, 9.159402242, 6.660958905, 0.600871731, 0, 0]
          dis_1_stringer = scale(dis_1_stringer)
          dis_0_frame = [30, 20, 0, 0, 0, 20, 0, 0, 10, 10, 0, 0]
          dis_0_frame = scale(dis_0_frame)
          dis_0_stringer = [0, 20, 0, 0, 10, 20, 10, 0, 0, 0, 10, 0, 0, 0, 10, 0, 10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0]
          dis_0_stringer = scale(dis_0_stringer)

     if pressure == 1:
          pres_0_frame = [ 1.94444444, -7.15217391, -7.00549451, -0.75342466,  4.21511628,  4.34027778, -4.0625, -0.9375, 7.61538462, 5.23076923,  4.24657534, -2.4695122 ]
          pres_0_frame = scale(pres_0_frame)
          pres_1_frame = [-1.11111111,  1.35714286,  3.4,        -0.41666667,  0.90909091, -2.03703704, 0.15625,    -0.35714286,  0.69444444,  0.625,      -2.1,        -1.07142857]
          pres_1_Frame = scale(pres_1_frame)
          pres_0_stringer = [ 1.59090909,  2.5,         1.84782609, -0.15625,    -1.75531915,  0.92592593, -1.25,        1.19047619,  2.1875,      0.,          0.875,       0.39772727, -0.32258065,  0.78431373,  0.88235294,  0.43650794, -0.16393443, -0.37234043,
     -1.640625 ,  -0.20833333, -1.66666667, -1.09756098, -6.60714286, -2.,
     0. ,        -7.5    ,    -7.5    ,   ]
          pres_0_stringer = scale(pres_0_stringer)
          pres_1_stringer = [        0,  0.96153846,  1.25,       -1.18421053, -0.35714286, -1.125,
     0.97222222,  1.875 ,      2.1875,      1.07142857, -2.25 ,      -0.46875,
     -0.41666667 ,-3.75 ,       1.44736842 ,-1.625     ,  1.33333333 ,-0.625,
     3.75   ,            0,         0,  5. ,         1.13636364 , 0.76923077,
     0.38461538 ,-0.83333333 ,-0.83333333 ,       0,  1.25      ]
          pres_1_stringer = scale(pres_1_stringer)

     for i in total0:
          score_skin_frame[i.frame_no-1] += radius_0[c]
          score_skin_stringer[i.stringer_no-1] += radius_0[c]
          c+=1
     #score_skin_frame = np.abs(score_skin_frame)/(np.abs(score_skin_frame)).max*10.0
     score_skin_frame = score_skin_frame/num_0_frame
     score_skin_frame = score_skin_frame/max(score_skin_frame)*10
     score_skin_stringer = score_skin_stringer/num_0_stringer
     score_skin_stringer = score_skin_stringer/max(score_skin_stringer)*10

     for j in total1:
          score_frame_frame[j.frame_no-1] += radius_1[d]
          score_frame_stringer[j.stringer_no-1] += radius_1[d]
          d+=1
     score_frame_frame = score_frame_frame/num_1_frame
     score_frame_frame = score_frame_frame/max(score_frame_frame)*10
     score_frame_stringer = score_frame_stringer/num_1_stringer
     score_frame_stringer = score_frame_stringer/max(score_frame_stringer)*10

     fig, axs = plt.subplots(2, 2)
     
     axs[0,0].plot(np.linspace(1,12,12),np.abs(score_skin_frame), color='orange', label='Clustering')
     if displacement == 1:
          axs[0,0].plot(np.linspace(1,12,12),dis_0_frame, color='green', label='Displacement')
     if pressure == 1:
          axs[0,0].plot(np.linspace(1,12,12),pres_0_frame, color='blue', label='Pressure')
     axs[0,0].set_title('Outlier scores of clip-to-skin weldings along the frames')
     axs[0,0].set_xlabel('frames')
     axs[0,0].set_ylabel('scores')
     axs[0,0].legend(loc="upper right")

     axs[0,1].plot(np.linspace(1,27,27),np.abs(score_skin_stringer), color='orange', label='Clustering')
     if displacement == 1:
          axs[0,1].plot(np.linspace(1,27,27),dis_0_stringer, color='green', label='Displacement')
     if pressure == 1:
          axs[0,1].plot(np.linspace(1,27,27),pres_0_stringer, color='blue', label='Pressure')
     axs[0,1].set_title('Outlier scores of clip-to-skin weldings along the stringers')
     axs[0,1].set_xlabel('frames')
     axs[0,1].set_ylabel('scores')
     axs[0,1].legend(loc="upper right")

     axs[1,0].plot(np.linspace(1,12,12),np.abs(score_frame_frame), color='orange', label='Clustering')
     if displacement == 1:
          axs[1,0].plot(np.linspace(1,12,12),dis_1_frame, color='green', label='Displacement')
     if pressure == 1:
          axs[1,0].plot(np.linspace(1,12,12),pres_1_frame, color='blue', label='Pressure')
     axs[1,0].set_title('Outlier scores of clip-to-frame weldings along the frames')
     axs[1,0].set_xlabel('stringers')
     axs[1,0].set_ylabel('scores')
     axs[1,0].legend(loc="upper right")

     axs[1,1].plot(np.linspace(1,29,29),np.abs(score_frame_stringer), color='orange', label='Clustering')
     if displacement == 1:
          axs[1,1].plot(np.linspace(1,29,29),dis_1_stringer, color='green', label='Displacement')
     if pressure == 1:
          axs[1,1].plot(np.linspace(1,29,29),pres_1_stringer, color='blue', label='Pressure')
     axs[1,1].set_title('Outlier scores of clip-to-frame weldings along the stringers')
     axs[1,1].set_xlabel('stringers')
     axs[1,1].set_ylabel('scores')
     axs[1,1].legend(loc="upper right")

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
          stri = 'Power'
     if pressure == 1:
          stri = 'Pressure'
     if displacement == 1:
          stri = 'Displacement'

     title = 'Clustering' + stri + '.csv'

     with open('Clustering.csv', 'w', newline='') as file:
          writer = csv.writer(file)
          writer.writerows(file_list)
     
