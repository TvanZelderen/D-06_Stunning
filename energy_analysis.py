import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from total_energy import total_energy as tot

a = tot([1],[2],[1],1)
plt.hist(a)
plt.show
