import numpy as np
import matplotlib.pyplot as plt
from load import Data, plot_ini 

a = Data('01', '02', '02', 1)
a.normalize()
a.bar_to_N()
a.create_array()

ax = plot_ini(title='yy')
a.plot(axes=ax, displacement=False)
plt.show()

#print(a.frame.iloc[:,1].mean())

