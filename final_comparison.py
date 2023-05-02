# Weights for the final comparison of the models
w_displacement = 1
w_pressure = 1
w_power = 2

amber_list = []
red_list = []

amber_score = 2
max_score = 3

# Example lists
suspectwelds = [[1,2,2,3], [1,4,2,3], [2,3,3,5]]
suspectwelds_2 = [[1,1,2,3], [1,4,3,6], [2,1,1,1]]
suspectwelds_3 = [[1,1,1,1], [1,4,3,6], [2,1,1,1]]

# Distribute this code to the other teams
'''
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
'''

# Pull the welds from text files into a dictionary
final_weld_comparison = {}
with open('suspectwelds_position.txt', 'r') as f_displacement:
    for line in f_displacement.readlines():
        final_weld_comparison[str(line.strip("\n"))] = w_displacement
    print(f'Wrote displacement welds to dict')
with open('suspectwelds_pressure.txt', 'r') as f_pressure:
    for line in f_pressure.readlines():
        # print(line)
        # If weld already exists, add to value
        try:
            final_weld_comparison[str(line.strip("\n"))] += w_pressure
            # print(f'Wrote existing pressure welds to dict')
        except KeyError: 
            # If weld does not exist, create new key
            final_weld_comparison[str(line.strip("\n"))] = w_pressure
            # print(f'Wrote new pressure welds to dict')
    print(f'Wrote pressure welds to dict')
with open('suspectwelds_power.txt', 'r') as f_power:
    for line in f_power.readlines():
        # print(line)
        # If weld already exists, add to value
        try:
            final_weld_comparison[str(line.strip("\n"))] += w_power
            # print(f'Wrote existing power welds to dict')
        except KeyError:
            # If weld does not exist, create new key
            final_weld_comparison[str(line.strip("\n"))] = w_power
            # print(f'Wrote new power welds to dict')
    print(f'Wrote power welds to dict')
# print(final_weld_comparison)

for key in final_weld_comparison:
    if final_weld_comparison[key] >= amber_score:
        amber_list.append(key)
    elif final_weld_comparison[key] >= max_score:
        red_list.append(key)

# print(f'Amber list: {amber_list}')
# print(f'Red list: {red_list}')

def main():
    with open('suspectedwelds.txt', 'w') as f:
        print(f'Opened {f.name} for writing')
        f.write(f'Amber list: with a score of higher than {amber_score}\n')
        for i in amber_list:
            f.write(str(i)+'\n')
        f.write(f'Red list: with a score of higher than {max_score}\n')
        for i in red_list:
            f.write(str(i)+'\n')

main()

# TODO check formatting of Wei Wei's output. Go through all the files and check if they are formatted correctly.
