from load import *
sns.set_theme()

# i = Data(1,2,1,1)

# lblist = ['Clip-to-skin pressure outlier score map',
#           'Clip-to-frame pressure outlier score map',
#           'Clip-to-skin power outlier score map',
#           'Clip-to-frame power outlier score map',
#           'Zero derivative points, stringer 6',
#           'Zero derivative points, stringer 7']

# for label in lblist:
#     ax = plot_ini(label)
#     i.plot(ax, displacement = True)
#     plt.savefig('C:\\Users\\SID-DRW\\Desktop\\New folder\\'+label+'.png')

# all_obj = iterate_points(type = 0)
# for i in all_obj:
#     try:
#         i.plot(ax, displacement = True)
#     except:
#         pass
# plt.xlabel('Time [s]')
# plt.ylabel('Displacement [mm]')
# plt.show()

ax = plot_ini('Clip-to-frame displacement curves')
all_obj = iterate_points(type = 1)
for i in all_obj:
    try:
        i.plot(ax, displacement = True)
    except:
        pass

plt.xlabel('Time [s]')
plt.ylim([-1,20])
plt.ylabel('Displacement [mm]')
plt.show()
