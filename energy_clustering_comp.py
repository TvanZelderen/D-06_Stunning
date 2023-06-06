from total_energy import energy as en
import numpy as np
import matplotlib.pyplot as plt

energy = en(type=1).to_numpy()
print(energy)
mean = np.mean(energy[:,-1])
mse = np.sqrt((energy[:,-1]-mean)**2)
mse = np.reshape((mse-min(mse))/(max(mse)-min(mse))*10, (-1,1))
energy = np.concatenate((energy, mse), axis=1)
energy = np.delete(energy, -2, axis=1)
print(energy)
avg = []
for i in range(1, 13):
    avg.append(np.mean(energy[:,4], where = (energy[:,0] == i)))
print(avg)

plt.plot(range(1,13), avg)
plt.xlabel('Frames')
plt.ylabel('Score')
plt.title('Outlier score of clip-to-skin welding along the stringers')
plt.savefig('clip-to-skin_alongframes.jpg')
plt.show()
