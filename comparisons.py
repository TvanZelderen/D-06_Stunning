from load import *

ax = plot_ini('test')    
atotal = iterate_points(type=0)
print(len(atotal))
# for i in atotal:
#     i.plot(ax, power=True)
# plot_legends()