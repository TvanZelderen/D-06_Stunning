from load import *

atotal = iterate_points(type=1, frames=[1], stringers=range(1,11))
for i in atotal:
    ax = plot_ini('test')
    i.smoothing()
    i.plot(ax, power=True ,smooth_power=True)
    plot_legends()