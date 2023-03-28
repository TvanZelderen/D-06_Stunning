import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from total_energy import energy

a = energy([1],[2, 3, 5, 4, 7],[1],1)
print(a)
sns.histplot(a['Energy'])
plt.show()
