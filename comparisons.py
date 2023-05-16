from load import *

ax = plot_ini('All displacement data (for clip-to-skin)')    
all_obj = iterate_points(type = 0)
for i in all_obj:
    try:
        i.plot(ax, displacement = True)
    except:
        pass
plt.show()
