import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from total_energy import energy as tot

a = tot([1],[2, 3],[1],1)
print(a)
sns.histplot(a)
plt.show()
