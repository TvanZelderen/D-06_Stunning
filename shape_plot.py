print('this is power throng\'s SECOND property')

# x_plot = np.array(x_plot)
# y_plot = np.array(y_plot)

# idx = np.argsort(ssds)
# sorted_x_plot = x_plot[idx]
# sorted_y_plot = y_plot[idx]
# ssd_rank = np.arange(1,len(ssds)+1)
# plt.scatter(sorted_x_plot, sorted_y_plot, c=ssd_rank, cmap='coolwarm')
# plt.colorbar()
# plt.show()

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