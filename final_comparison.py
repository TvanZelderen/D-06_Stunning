import pandas as pd

# Weights for the final comparison of the models
w_displacement = 1
w_pressure = 1
w_power = 2


# Suspect welds in displacement
suspectwelds = [[1,2,2,3], [1,4,2,3], [2,3,3,5]]
suspectwelds_2 = [[1,1,2,3], [1,4,3,6], [2,1,1,1]]
suspectwelds_3 = [[1,1,1,1]]

# Open the csv with pandas and create a dataframe
df = pd.read_csv('final_comparison.csv', header=0, names=['Weld', 'Displacement', 'Pressure', 'Power'])

# Write suspect position welds to a txt file
with open('suspectwelds_position.txt', 'w') as f:
    print(f'Opened {f.name} for writing')
    for i in suspectwelds:
        f.write(str(i)+'\n')

# Write suspect pressure welds to a txt file
with open('suspectwelds_pressure.txt', 'w') as f:
    print(f'Opened {f.name} for writing')
    for i in suspectwelds_2:
        f.write(str(i)+'\n')

# Write suspect power welds to a txt file
with open('suspectwelds_power.txt', 'w') as f:
    print(f'Opened {f.name} for writing')
    for i in suspectwelds_3:
        f.write(str(i)+'\n')

# Pull the welds from text files into a dictionary
final_weld_comparison = {}
with open('suspectwelds_position.txt', 'r') as f:
    for line in f.readlines():
        final_weld_comparison[str(line)] = w_displacement
with open('suspectwelds_pressure.txt', 'r') as f:
    for line in f.readlines():
        final_weld_comparison[str(line)] = w_pressure
with open('suspectwelds_power.txt', 'r') as f:
    for line in f.readlines():
        final_weld_comparison[str(line)] = w_power
print(final_weld_comparison)