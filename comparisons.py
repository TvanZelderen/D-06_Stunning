from load import *

ax = plot_ini('')    
all_obj = iterate_points(type = 1)
for i in all_obj:
    try:
        i.plot(ax, displacement = True)
    except:
        pass
plt.xlabel('Time [s]')
plt.ylabel('Displacement [mm]')
plt.show()
