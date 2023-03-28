from load import *
from shape import *
ax = plot_ini('test')    
atotal = iterate_points(type=1)
for i in atotal:
    i.plot(ax, displacement=True)
plot_legends()