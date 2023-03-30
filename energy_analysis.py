import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from load import energy 

#Calculate the total energy of a weld on all stringers
a = energy([1],list(range(0,29)),[2],1)

#Calculate the mean of the energies
mean = np.mean(a["Energy"])

#Iterate over all the stringers to find energies less than a specified fraction of the mean
for i in range(0,29):
    b = energy([1],[i],[2],2)
    #print(b["Energy"])
    if b["Energy"].to_numpy() < 0.5*mean:
        print(b)

#Print the mean and plot the histogram of the energies 
print("The mean is:", mean)
sns.histplot(a["Energy"])
plt.show()
