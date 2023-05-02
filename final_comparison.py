import pandas as pd

# Weights for the final comparison of the models
w_displacement = 1
w_pressure = 1
w_power = 2


# Suspect welds in displacement
suspectwelds = [1223, 1423, 2335]

# Open the csv with pandas and create a dataframe
df = pd.read_csv('final_comparison.csv', header=0, names=['Weld', 'Displacement', 'Pressure', 'Power'])

# Find the if the suspect welds are in the dataframe
for weld in suspectwelds:
    # Index in the dataframe
    index = df.index[(df['Weld'] == weld)]
    print(index)
    # If the index is not empty write to second column w_displacement
    if not index.empty:
        df.iloc[index[0], 1] = w_displacement
        print(df.iloc[index[0], 1])

                     