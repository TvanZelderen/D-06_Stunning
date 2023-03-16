from load import *

ax = plot_ini('test')    
a1 = Data('01', '02', '01', 1)
#a2 = Data('02', '02', '01', 1)
a3 = Data('03', '02', '01', 1)
#a4 = Data('04', '02', '01', 1)
a5 = Data('05', '02', '01', 1)
a6 = Data('06', '02', '01', 1)
#a7 = Data('07', '02', '01', 1)
#a8 = Data('08', '02', '01', 1)
#a9 = Data('09', '02', '01', 1)
#a10 = Data('10', '02', '01', 1)
a11= Data('11', '02', '01', 1)
a12= Data('12', '02', '01', 1)
atotal = [a1, a3, a5, a6, a11, a12]
for i in atotal:
    i.normalize()
    i.bar_to_N()
    i.plot(ax, power=True)
    print(i.frame[0:10])
plot_legends()