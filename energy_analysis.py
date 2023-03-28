import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from total_energy import energy 


a = energy([1],list(range(2,29)),[1],2)
b= np.mean(a["Energy"])
print("The mean is:", b)

for i in range(2,29):
    c = energy([1],[i],[1],2)
    print(c["Energy"])
    #if c["Energy"] < 0.5*b:
        #print(c)

sns.histplot(a["Energy"])
plt.show()
