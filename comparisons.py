from load import *

ax = plot_ini('test')    
i = Data(1,2,2,1)
print(i.frame)
i.plot(ax, force=True)
plot_legends()