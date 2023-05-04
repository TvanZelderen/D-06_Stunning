from scipy.integrate import simpson
import pandas as pd
from load import iterate_points
import matplotlib.pyplot as plt
import seaborn as sns


def energy(frame:list = range(13), stringer:list = range(31), weld:list = range(7), type:int = range(2)):
    data = iterate_points(frames=frame, stringers=stringer, welds =weld, type=type)
    energy = []
    for i in data:
        try: 
            p = i.frame['Power'].dropna().to_numpy()
            t = i.frame['Time'].drop(i.frame['Power'].isna()*range(len(i.frame['Power']))).to_numpy()
            energy.append([i.frame_no, i.stringer_no, i.weld_no, i.type, simpson(p, t)])
        except:
            energy.append([i.frame_no, i.stringer_no, i.weld_no, i.type, 0])
    #print('Energy: ' + str(energy))
    if len(energy) == 0:
        energy.append([0, 0, 0, 0, 0])
    df_energy = pd.DataFrame(energy, columns=['Frame', 'Stringer', 'Weld', 'Type', 'Energy'])
    return df_energy
#plt.scatter(np.ones(len(energy)), energy)

#sns.histplot(energy(frame = [1], stringer=[2, 3, 4, 5, 6, 7]), x = 'Energy')
#plt.show()