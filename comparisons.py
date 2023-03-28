from load import *

ax = plot_ini('test')    
atotal = iterate_points(type='All')
for i in atotal:
    i.plot(ax, displacement=True)
plot_legends()