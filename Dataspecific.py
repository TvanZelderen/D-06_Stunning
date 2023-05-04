import numpy as np
import matplotlib.pyplot as plt
from load import *
from sklearn.preprocessing import Normalizer, StandardScaler
import seaborn as sns
from Autoencoder import LOF
from collections import defaultdict


def Data(total):
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

'''Data processing'''
#clip_to_skin
total0 = iterate_points(type = 0)
X0 = Data(total0)
#clip_to_frame
total1 = iterate_points(type = 1)
X1 = Data(total1)
#print(X1)

     #Data Normalization
scaler_0 = StandardScaler()
scaler_1 = StandardScaler()
normalized_features_0 = scaler_0.fit_transform(X0)
normalized_features_1 = scaler_1.fit_transform(X1)
scaler0 = Normalizer()
scaler1 = Normalizer()
normalized_features0 = scaler0.fit_transform(normalized_features_0)
normalized_data0 = pd.DataFrame(normalized_features0, columns = X0.columns)
normalized_features1 = scaler1.fit_transform(normalized_features_1)
normalized_data1 = pd.DataFrame(normalized_features1, columns = X1.columns)
#print(normalized_data0)

a = 5
abnomal_skin, abnomal_frame, X_0, X_scores_0, X_1, X_scores_1, outlier_indice_0, outlier_indice_1 = LOF(a, X0, X1, total0, total1, normalized_data0, normalized_data1)

'''List of ill-welding'''
list_of_suspicious_skin, list_of_baddy_skin = counter(abnomal_skin, a)
list_of_suspicious_frame, list_of_baddy_frame = counter( abnomal_frame, a)
print(list_of_baddy_skin, list_of_baddy_frame, list_of_suspicious_skin, list_of_suspicious_frame)


'''Visualization'''

fig, (ax0, ax1) = plt.subplots(1, 2)

ax0.scatter(X_0[:, 0], X_0[:, 1], color="m", s=3.0, label="Data points")
# plot circles with radius proportional to the outlier scores
radius_0 = (X_scores_0.max() - X_scores_0) / (X_scores_0.max() - X_scores_0.min())
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
radius_1 = (X_scores_1.max() - X_scores_1) / (X_scores_1.max() - X_scores_1.min())
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

'''Map'''
fig, (ax_0, ax_1) = plt.subplots(1, 2)

x_plot = []
y_plot = []

for i in total0:
     x_plot.append(i.frame_no + ((i.weld_no-1)%3)/10 - 0.10)
     y_plot.append(i.stringer_no + ((i.weld_no-1)//3)/2.5 - 0.20)
x_plot = np.array(x_plot)
y_plot = np.array(y_plot)

idx = np.argsort(radius_0)
sorted_x_plot = x_plot[idx]
sorted_y_plot = y_plot[idx]
ssd_rank = np.arange(1,len(X_scores_0)+1)
im1 = ax_0.scatter(sorted_x_plot, sorted_y_plot, c=radius_0, cmap='Oranges')
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
ssd_rank = np.arange(1,len(X_scores_1)+1)
im2 = ax_1.scatter(sorted_x_plot, sorted_y_plot, c=radius_1, cmap='Blues')
fig.colorbar(im2, ax = ax_1)
plt.show()



