import matplotlib.pyplot as plt
import total_energy as en 
import numpy as np
import pandas as pd

energy = en.energy(type=0).to_numpy()
mean = np.mean(energy[:,-1])
mse = np.sqrt((energy[:,-1]-mean)**2)
mse = np.reshape((mse-min(mse))/(max(mse)-min(mse))*10, (-1,1))
energy = np.concatenate((energy, mse), axis=1)
energy = np.delete(energy, -2, axis=1)
plt.hist(energy[:,-1])
data = np.array([[]])
for i in energy:
    data = np.append(data, ["["+str(int(i[0]))+', '+str(int(i[1]))+', '+str(int(i[2]))+', '+str(int(i[3]))+"]", i[4]])
data = np.reshape(data, (-1,2))
data = pd.DataFrame(data)

#data.to_csv('.\energy_score_clip_to_skin.csv', header=False, index=False)
#print(energy)
plt.show()
