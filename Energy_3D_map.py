import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from total_energy import total_energy as tot

# Set the style
# sns.set_style("darkgrid")

# Create a figure
def data_for_cylinder_along_z(center_x,center_y,radius,length):
    y = np.linspace(0, length, 50)
    theta = np.linspace(0, -np.pi, 50)
    theta_grid, y_grid=np.meshgrid(theta, y)
    x_grid = radius*np.cos(theta_grid) + center_x
    z_grid = radius*np.sin(theta_grid) + radius
    return x_grid,y_grid,z_grid

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d(-5, 5)
ax.set_ylim3d(0, 10)
ax.set_zlim3d(0, 10)

number_of_frames = 12
fuselage_length = 10
fuselage_radius = 4
side_offset = 0.25
number_of_stringers = 20

Xc,Yc,Zc = data_for_cylinder_along_z(0,4,fuselage_radius,fuselage_length)
ax.plot_surface(Xc, Yc, Zc, alpha=0.5) # Plot a the fuselage surface with half transparency.
for i in range(number_of_frames): # Plot the frame lines
    theta = np.linspace(0, -np.pi, 50)
    x = fuselage_radius*np.cos(theta) + 0
    z = fuselage_radius*np.sin(theta) + fuselage_radius
    y = np.linspace(side_offset + fuselage_length/number_of_frames*i, side_offset + fuselage_length/number_of_frames*i, 50)
    ax.plot(x, y, z, color='k', alpha=0.8) # actually plot, k = black, alpha = transparency

for i in range(number_of_stringers): # Plot the stringer lines
    theta = np.linspace(-np.pi*(10/180)-np.pi*(1-10/180)/number_of_stringers*i,-np.pi*(10/180)-np.pi*(1-10/180)/number_of_stringers*i, 50)
    x = fuselage_radius*np.cos(theta) + 0
    z = fuselage_radius*np.sin(theta) + fuselage_radius
    y = np.linspace(0, fuselage_length, 50)
    ax.plot(x, y, z, color='k', alpha=0.8) # actually plot, k = black, alpha = transparency

positions = [[1,1], [4,5]] # [stringer, frame]
for position in positions:
    theta = -np.pi*(10/180)-np.pi*(1-10/180)/number_of_stringers*position[0]
    x = fuselage_radius*np.cos(theta) + 0
    z = fuselage_radius*np.sin(theta) + fuselage_radius
    y = side_offset + fuselage_length/number_of_frames*position[1]
    ax.scatter(x, y, z, color='r', marker='o', s=100) # Plot a point at the origin

for frame in range(1):
    for stringer in range(1):
        theta_mean = -np.pi/number_of_stringers*stringer
        dtheta = np.pi/(2*number_of_stringers)
        theta = np.linspace(theta_mean - dtheta , theta_mean + dtheta, 50)
        print(theta)
        x = fuselage_radius*np.cos(theta) + 0
        z = fuselage_radius*np.sin(theta) + fuselage_radius
        y = np.array([1]*len(x))
        ax.plot(x, y, z, color='red')
        #E = tot([frame], [stringer])['Energy'].to_numpy()
        #print(E)
plt.show()