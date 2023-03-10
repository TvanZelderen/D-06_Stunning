import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set the style
# sns.set_style("darkgrid")

# Create a figure
def data_for_cylinder_along_z(center_x,center_y,radius,length):
    z = np.linspace(0, length, 50)
    theta = np.linspace(0, -np.pi, 50)
    theta_grid, z_grid=np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + center_x
    y_grid = radius*np.sin(theta_grid) + center_y
    return x_grid,y_grid,z_grid

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

Xc,Yc,Zc = data_for_cylinder_along_z(0,0.2,4,6)
ax.plot_surface(Xc, Zc, Yc, alpha=0.5)

plt.show()