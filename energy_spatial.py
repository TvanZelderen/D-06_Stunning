from load import Data
from total_energy import energy
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import seaborn as sns
import pandas as pd

sns.set_theme()

frame = energy(type=1).to_numpy()[:,-1]
skin = energy(type=0, weld=[1, 2]).to_numpy()[:,-1]
stringer_skin = energy(type=0, weld=[3, 4, 5, 6]).to_numpy()[:,-1]

labels = ['Clip-to-frame', 'Clip-to-skin', 'Clip-to-stringer-to-skin']
'''sns.boxplot(
    data=[frame, skin, stringer_skin],
    #labels = labels,
    showmeans=True,
    orient='h',
    x="Energy [kJ]", y="Weld Position"
)'''
plt.boxplot([frame, skin, stringer_skin], labels=labels)
plt.show()