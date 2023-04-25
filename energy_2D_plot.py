from load import Data
from total_energy import energy
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

theta = np.array([0])
radii = np.array([0])
for i in range(0, 20):
    dtheta = np.linspace(9*i-4.5, 9*i+4.5, 10)
    try:
        dradii = np.ones(10)*float(energy(stringer=[i+1])['Energy'])
    except:
        dradii = np.zeros(10)
    print(dtheta)
    print(dradii)
    theta = np.concatenate(theta, dtheta)
    radii = np.concatenate(radii, dradii)

print(theta)