import numpy as np
import matplotlib.pyplot as plt
from load import Data

a = Data('01', '02', '02', 1)
a.normalize()
a.bar_to_N()
a.create_array()

print(a.frame.iloc[:,1].mean())

