from load import *

sns.set_theme()
fig, axs = plt.subplots(1,2, sharey=True)

all_obj = iterate_points(type = 0)
for i in all_obj:
    try:
        i.plot(axs[0], displacement = True)
    except:
        pass

all_obj = iterate_points(type = 1)
for i in all_obj:
    try:
        i.plot(axs[1], displacement = True)
    except:
        pass

axs[0].set_xlabel('Time [s]')
axs[1].set_xlabel('Time [s]')
axs[0].set_ylabel('Displacement [mm]')
plt.show()
