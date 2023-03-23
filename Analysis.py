import numpy as np
import matplotlib.pyplot as plt
from load import Data

a = Data('01', '02', '02', 1)
a.create_array()

b = Data('01', '02', '01', 1)
b.create_array()

ax = plot_ini(title='power curve')
a.plot(axes=ax, power=True)
b.plot(axes=ax, power=True)
plt.show()

#print(a.frame.iloc[:,1].mean())
