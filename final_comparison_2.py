import pandas as pd
import matplotlib.pyplot as plt
# Weights and scores for the final comparison of the models
w_disp_heavy = 10
w_energy = 4
w_power = 4
w_pressure_time = 1
w_pressure_filter = 2
w_pressure_peak = 1
w_displ = 1

w_total = 24

#amber_list = []
#red_list = []
suspicious_list = []

#amber_score = 2
#max_score = 3
cutoff_score = 12

df1=pd.read_csv('disp_heavy.csv', header = None, index_col = 0, names = ['Index','disp_heavy'])
df2=pd.read_csv('energy.csv', header = None, index_col = 0, names = ['Index','energy'])
df3=pd.read_csv('power.csv', header = None, index_col = 0, names = ['Index','power'])
df4=pd.read_csv('pressure_time.csv', header = None, index_col = 0, names = ['Index','pressure_time'])
df5=pd.read_csv('pressure_filter.csv', header = None, index_col = 0, names = ['Index','pressure_filter'])
df6=pd.read_csv('pressure_peak.csv', header = None, index_col = 0, names = ['Index','pressure_peak'])
df7=pd.read_csv('displ.csv', header = None, index_col = 0, names = ['Index','displacement'])

dftotal=pd.concat([df1, df2, df3], axis= 1)
corr_matrix = dftotal.corr()
print(corr_matrix)

dftotal['Final Score'] = dftotal['disp_heavy']*w_disp_heavy + dftotal['power']*w_power + dftotal['energy']*w_energy + dftotal['pressure_time']*w_pressure_time + dftotal['pressure_filter']*w_pressure_filter + dftotal['pressure_peak']*w_pressure_peak + dftotal['displacement']*w_displ
dftotal['Final Score'] /= w_total
print(dftotal.to_string)

plt.hist(dftotal['Final Score'], bins=30)
plt.show()