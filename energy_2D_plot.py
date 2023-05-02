from load import Data
from total_energy import energy
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.gridspec import GridSpec
import numpy as np
axs = []
fig, axs = plt.subplots(3, 4, subplot_kw=dict(projection="polar"))
axs = np.reshape(axs, -1)
ax_iter = iter(axs)
weld_loc = 1
weld_type = 1
print(axs)
for j in range(0, 12):
    theta = np.array([], float)
    radii = np.array([], float)
    for i in range(0, 31):
        dtheta = np.array([9*i])#np.linspace(9*i-4.5, 9*i+4.5, 1)
        try:
            en = energy(stringer=[i+1], frame = [j+1], type=weld_type, weld=[weld_loc])
            dradii = np.ones(1)*float(en['Energy'])
        except:
            dradii = np.zeros(1)
        theta = np.concatenate((theta, dtheta), axis = 0)
        radii = np.concatenate((radii, dradii), axis = 0)

    print(theta)
    print(radii)
    theta = -theta*np.pi/180
    radii = radii/1000
    
    ax = next(ax_iter)
    #ax.set_ylim([1, max(radii)])

    ax.xaxis.set_ticks(np.arange(0, -189, -18)*np.pi/180)
    ax.set_xticklabels(['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21'])
    ax.yaxis.set_ticks([1, 2, 3, 4])

    ax.bar(theta, radii, bottom = 0.0, width = 9*np.pi/180, label = 'Weld Enegry [kJ]')
    radii[radii == 0] = np.nan
    ax.plot(np.linspace(0, 2*np.pi, 50), np.ones(50)*np.nanmean(radii), color = 'green', linewidth= 0.7 , label = 'Mean Weld Enegry [kJ]')
    

    #ax.legend()
    ax.set_title('Frame '+str(j+1) + '\n Mean: ' + str(np.round(np.nanmean(radii), 1)) + 'kJ' + ' STD: ' +str(np.round(np.nanstd(radii), 2)))
    ax.set_thetamin(4.5)
    ax.set_thetamax(-184.5)
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower right')
fig.suptitle('Weld position: ' + str(weld_loc) +', weld type: ' +str(weld_type))
plt.show()