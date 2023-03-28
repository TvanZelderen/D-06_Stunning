import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from total_energy import energy 

a = energy([1],[2, 3, 4, 5],[1],1)
print(a)
sns.histplot(a["Energy"])
plt.show()
