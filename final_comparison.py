import csv

# Weights for the final comparison of the models
w_displacement = 1
w_pressure = 1
w_power = 2


# Suspect welds in displacement
suspectwelds = [[1,2,2,3], [1,4,2,3], [2,3,3,5]]

# Write the data to CSV file
def write_to_csv(suspectwelds, data_type='displacement'):
    with open('final_comparison.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Weldnumber', 'Displacement', 'Pressure', 'Power'])
        for weld in suspectwelds:
            clip_type = weld[0]
            frame = weld[1]
            stringer = weld[2]
            weld = weld[3]
            if data_type == 'displacement':
                writer.writerow([weld, 1, 0, 0])
            elif data_type == 'pressure':
                writer.writerow([weld, 0, 1, 0])
            elif data_type == 'power':
                writer.writerow([weld, 0, 0, 1])

write_to_csv(suspectwelds)