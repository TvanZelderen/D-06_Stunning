from load import *

ax = plot_ini('test')    
atotal = iterate_points(type=0, frames=[1],stringers=[1,2])
print(atotal.frame)


#for i in atotal:
#     i.plot(ax, power=True)
#plot_legends()