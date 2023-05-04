print('this is power throng\'s SECOND property')

from load import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import seaborn as sns
sns.set_theme()

with open('powerthrong_0.csv', 'r', newline='') as file:
    data = list(csv.reader(file))
data = np.array(data)
data = data.astype('float64')

ssds = data[:,4].reshape(-1)
tresh = np.mean(ssds) + 1.5*np.std(ssds)
print(tresh)
plt.hist(ssds,bins=30)
plt.show()

pm = data[:,5].reshape(-1)
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

ssd_array = np.empty((12,27,6))
ssd_array[:] = np.nan
for i in range(data.shape[0]):
    ssd_array[int(data[i,0])-1,int(data[i,1])-1,int(data[i,2])-1] = data[i,4]

mean_ssd = np.nanmean(ssd_array, axis=2)

x_plot = []
y_plot = []
ssd_plot = []

for i in range(mean_ssd.shape[0]):
    for j in range(mean_ssd.shape[1]):
        if mean_ssd[i,j] != np.nan:
            x_plot.append(i)
            y_plot.append(j)
            ssd_plot.append(np.log(mean_ssd[i,j]))

plt.scatter(x_plot, y_plot, c=ssd_plot, cmap='coolwarm')
plt.colorbar()
plt.show()

frame_mean_ssd = np.nanmean(mean_ssd, axis=1)
x_plot = range(1,13)
plt.plot(x_plot,frame_mean_ssd)
plt.show()

string_mean_ssd = np.nanmean(mean_ssd, axis=0)
x_plot = range(1,28)
plt.plot(x_plot,string_mean_ssd)
plt.show()

#pm analysis
'''pm_rank = np.arange(1,len(pm)+1)
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