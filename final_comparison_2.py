import pandas as pd
import matplotlib.pyplot as plt
# Weights and scores for the final comparison of the models
w_ssd = 2
w_dummy1 = 1
w_dummy2 = 1

w_total = 4

amber_list = []
red_list = []

amber_score = 2
max_score = 3

df1=pd.read_csv('ssd.csv', header = None, index_col = 0, names = ['Index','SSD'])
df2=pd.read_csv('dummy1.csv', header = None, index_col = 0, names = ['Index','dummy1'])
df3=pd.read_csv('dummy2.csv', header = None, index_col = 0, names = ['Index','dummy2'])

dftotal=pd.concat([df1, df2, df3], axis= 1)
corr_matrix = dftotal.corr()
print(corr_matrix)

dftotal['Final Score'] = dftotal['SSD']*w_ssd + dftotal['dummy1']*w_dummy1 + dftotal['dummy2']*w_dummy2
dftotal['Final Score'] /= w_total
print(dftotal.to_string)

plt.hist(dftotal['Final Score'], bins=30)
plt.show()