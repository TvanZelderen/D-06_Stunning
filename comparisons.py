from load import *

ax = plot_ini('test')    
all_obj = iterate_points(type = 1)
for i in all_obj:
    try:
        i.power_norm()
    except:
        pass
    else:
        i.plot(ax, norm_power=True)
plot_legends()