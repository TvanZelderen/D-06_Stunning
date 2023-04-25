from load import Data
from total_energy import energy
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.gridspec import GridSpec
import numpy as np
axs = []
fig, axs = plt.subplots(2, 6, subplot_kw=dict(projection="polar"))
axs = np.reshape(axs, -1)
ax_iter = iter(axs)
print(axs)
for j in range(0, 12):
    theta = np.array([], float)
    radii = np.array([], float)
    for i in range(0, 21):
        dtheta = np.array([9*i])#np.linspace(9*i-4.5, 9*i+4.5, 1)
        try:
            en = energy(stringer=[i+1], frame = [j+1], type=1)
            dradii = np.ones(1)*float(en['Energy'])
        except:
            dradii = np.zeros(1)
        theta = np.concatenate((theta, dtheta), axis = 0)
        radii = np.concatenate((radii, dradii), axis = 0)


    theta = -theta*np.pi/180
    radii = radii/1000
    print(theta)
    print(radii)
    ax = next(ax_iter)
    ax.bar(theta, radii, bottom = 0.0, width = 9*np.pi/180)
    radii[radii == 0] = np.nan
    ax.plot(np.linspace(0, 2*np.pi, 50), np.ones(50)*np.nanmean(radii), color = 'red')
    #ax.xaxis.set_ticks(range(0, 360, 9))
    ax.yaxis.set_ticks(range(1,4, 1))
    ax.set_title('Frame '+str(j+1))
plt.show()