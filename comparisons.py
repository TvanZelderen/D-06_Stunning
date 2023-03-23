from load import *

atotal = iterate_points(type=1)
for i in atotal:
    ax = plot_ini('test')
    i.smoothing()
    i.plot(ax, smooth_power=True)
    plot_legends()