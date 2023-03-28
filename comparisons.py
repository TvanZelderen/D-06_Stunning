from load import *
ax = plot_ini('test')    
i = Data(2,2,2,1)
i.smoothing()
i.plot(ax, smooth_power=True)
plot_legends()