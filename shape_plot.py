print('this is power throng\'s SECOND property')

from load import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import seaborn as sns
sns.set_theme()
from numpy.random import random
from sklearn.linear_model import LinearRegression as LiRe


# with open('powerthrong_0.csv', 'r', newline='') as file:
#     data0 = list(csv.reader(file))
# data0 = np.array(data0)
# data0 = data0.astype('float64')
# data = data0
# s = 27
# w = 6

with open('powerthrong_1.csv', 'r', newline='') as file:
    data1 = list(csv.reader(file))
data1 = np.array(data1)
data1 = data1.astype('float64')
data = data1
s = 29
w = 2

# data = np.vstack([data0,data1])

log_ssds = np.log(data[:,4].reshape(-1))
max_log = np.max(log_ssds)
min_log = np.min(log_ssds)
print(max_log, min_log)
scaled_log = 10*((log_ssds-min_log)/(max_log-min_log))
plt.hist(scaled_log,bins=30)
plt.show()

index = data[:,0:4]
index = index.astype(int)
index_csv = []
for i in range(index.shape[0]):
    index_csv.append(repr(list(index[i,:])))

# with open('ssd.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for i in range(index.shape[0]):
#         writer.writerow([index_csv[i],scaled_log[i]])

# with open('dummy1.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for i in range(index.shape[0]):
#         writer.writerow([index_csv[i],10*random()])

# with open('dummy2.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for i in range(index.shape[0]):
#         writer.writerow([index_csv[i],10*random()])

# data = data[data[:,2]==1.0]

ssds = data[:,4].reshape(-1)
# pm = data[:,5].reshape(-1)
frame_no = data[:,0].reshape(-1)
stringer_no = data[:,1].reshape(-1)
weld_no = data[:,2].reshape(-1)

x_plot = frame_no + ((weld_no-1)%3)/10 - 0.10
y_plot = stringer_no + ((weld_no-1)//3)/2.5 - 0.20

idx = np.argsort(ssds)
sorted_x_plot = x_plot[idx]
sorted_y_plot = y_plot[idx]

#ssd analysis
ssd_rank = np.arange(1,len(ssds)+1)
plt.scatter(sorted_x_plot, sorted_y_plot, c=ssd_rank, cmap='coolwarm')
plt.colorbar()
plt.show()

# plots by type
if w==6:
    fig, axs = plt.subplots(2,3, sharex=True, sharey=True)
elif w==2:
    fig, axs = plt.subplots(1,2, sharex=True, sharey=True)
for i in range(0,w):
    data_i = data[data[:,2]==i+1]
    ssds = np.log(data_i[:,4].reshape(-1))
    frame_no = data_i[:,0].reshape(-1)
    stringer_no = data_i[:,1].reshape(-1)
    if w==6:
        axs[i//3,i%3].scatter(frame_no, stringer_no, c=ssds, cmap='coolwarm', clim=(-1.5, 4))
        axs[i//3,i%3].set_title('Weld '+str(i+1))
    elif w==2:
        axs[i].scatter(frame_no, stringer_no, c=ssds, cmap='coolwarm', clim=(-2.5, 4))
        axs[i].set_title('Weld '+str(i+1))
    # axs[i//3,i%3].colorbar()
#fig.colorbar(plt.cm.ScalarMappable(cmap='coolwarm'), ax=axs[:,:])
if w==6:
    mappable = axs[0,0].collections[0]
    fig.colorbar(mappable=mappable, ax=axs[:,:])
elif w==2:
    mappable = axs[0].collections[0]
    fig.colorbar(mappable=mappable, ax=axs[:])
fig.suptitle('Log of SSDs per frame (horizontal axis) and stringer (vertical axis)')
plt.show()


ssd_array = np.empty((12,s,w))
ssd_array[:] = np.nan
for i in range(data.shape[0]):
    ssd_array[int(data[i,0])-1,int(data[i,1])-1,int(data[i,2])-1] = data[i,4]

frame_range = range(1,13)
stringer_range = range(1,s+1)
fig, axs = plt.subplots(2)
for weld in range(1,w+1):
    ssd_i = ssd_array[:,:,weld-1]
    lin_ssd = ssd_i.reshape(-1)
    print('Weld ',weld,': mean ',np.nanmean(lin_ssd),' and std ',np.nanstd(lin_ssd), sep='')

    frame_mean_ssd = np.nanmean(ssd_i, axis=1)
    axs[0].plot(frame_range,frame_mean_ssd)

    string_mean_ssd = np.nanmean(ssd_i, axis=0)
    axs[1].plot(stringer_range,string_mean_ssd)
fig.suptitle('Average SSD per weld by...')
axs[0].set_title('...frame')
axs[1].set_title('...stringer')
axs[0].legend(['Weld '+str(i) for i in range(1,w+1)])
axs[1].legend(['Weld '+str(i) for i in range(1,w+1)])
plt.show()

slope_array = np.empty(ssd_array.shape)
slope_array[:] = np.nan
slope = []
x_slope = []
y_slope = []
for i in range(ssd_array.shape[0]):
    for j in range(ssd_array.shape[1]):
        X = np.array(range(1,w+1)).reshape(-1, 1)
        y = ssd_array[i,j,:]
        y,X = nan_filter(y,X)
        if len(y)>1:
            reg = LiRe().fit(X,y)
            slope_array[i,j] = reg.coef_[0]
            slope.append(reg.coef_[0])
            x_slope.append(i)
            y_slope.append(j)
plt.scatter(x_slope, y_slope, c=slope, cmap='coolwarm', clim =(-5,5))
plt.title('Average increase of SSD between weld spots per location')
plt.colorbar()
plt.show()

frame_mean_slope = np.nanmean(slope_array, axis=1)
x_plot = range(1,13)
plt.plot(x_plot,frame_mean_slope)
plt.show()

string_mean_slope = np.nanmean(slope_array, axis=0)
x_plot = range(1,s+1)
plt.plot(x_plot,string_mean_slope)
plt.show()

x_plot = []
y_plot = []
ssd_plot = []
mean_ssd = np.nanmean(ssd_array, axis=2)

for i in range(mean_ssd.shape[0]):
    for j in range(mean_ssd.shape[1]):
        if mean_ssd[i,j] != np.nan:
            x_plot.append(i)
            y_plot.append(j)
            ssd_plot.append(np.log(mean_ssd[i,j]))

plt.scatter(x_plot, y_plot, c=ssd_plot, cmap='coolwarm')
plt.colorbar()
plt.show()

frame_mean_ssd = np.nanmean(ssd_array, axis=(1,2))
x_plot = range(1,13)
plt.plot(x_plot,frame_mean_ssd)
plt.show()

string_mean_ssd = np.nanmean(ssd_array, axis=(0,2))
x_plot = range(1,s+1)
plt.plot(x_plot,string_mean_ssd)
plt.show()

'''#pm analysis
pm_rank = np.arange(1,len(pm)+1)
plt.scatter(sorted_x_plot, sorted_y_plot, c=pm_rank, cmap='coolwarm')
plt.colorbar()
plt.show()

pm_array = np.empty((12,27,6))
pm_array[:] = np.nan
for i in range(data.shape[0]):
    pm_array[int(data[i,0])-1,int(data[i,1])-1,int(data[i,2])-1] = data[i,5]

mean_pm = np.nanmean(pm_array, axis=2)

x_plot = []
y_plot = []
pm_plot = []

for i in range(mean_pm.shape[0]):
    for j in range(mean_pm.shape[1]):
        if mean_pm[i,j] != np.nan:
            x_plot.append(i)
            y_plot.append(j)
            pm_plot.append(mean_pm[i,j])

plt.scatter(x_plot, y_plot, c=pm_plot, cmap='coolwarm')
plt.colorbar()
plt.show()

frame_mean_pm = np.nanmean(mean_pm, axis=1)
x_plot = range(1,13)
plt.plot(x_plot,frame_mean_pm)
plt.show()

string_mean_pm = np.nanmean(mean_pm, axis=0)
x_plot = range(1,28)
plt.plot(x_plot,string_mean_pm)
plt.show()'''

# good_ones = [i for i in all_obj if i.diff<9 and i.peak_m>0.53]
# ax = plot_ini('test') 
# for i in good_ones:
#     i.plot(ax, norm_power=True)
# plt.plot(x_axis, y_mean, linewidth=3, color='black')
# plot_legends()

# diff_list = [obj.diff for obj in all_obj]

# ranked_obj = sorted(all_obj, key=lambda x: x.diff)
# ranked_diff = sorted(diff_list)

# for i in range(0,10):
#     print(all_obj[i].main_label + ': Rank ' + str(rank(all_obj[i])) + ' out of ' + str(len(all_obj)))


# plt.hist(diff_list,bins=30)
# plt.show()

# total = iterate_points(type=1)
# all_peaks = []
# for obj in total:
#     if 'Power' not in obj.frame.keys() or len(obj.frame['Power'].dropna())==0:
#         continue
#     else:
#         obj.smoothing()
#         peaks = get_peaks(obj, time_norm=True, power_norm=True, first_only=True)
#         all_peaks += peaks

# all_peaks = [x for x in all_peaks if x[2]<0]
# roots, values, second_devs = zip(*all_peaks)
# plt.scatter(roots, values)
# plt.show()