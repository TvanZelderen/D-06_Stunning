import numpy as np
import pandas as pd
from pathlib import Path

# Path to the data directory
file_list = []
list_1khz = []
list_100hz = []
for path in Path('STUNNING Demonstrator USW Data').rglob('*.dat'):
    file_list.append(path.name)

for fname in file_list:
    
    if fname.startswith('1kHz'):
        name = fname.strip('1kHz')
        name = name.strip('.dat')
        list_1khz.append(name)
    elif fname.startswith('100Hz'):
        name = fname.strip('100Hz')
        name = name.strip('.dat')
        list_100hz.append(name)

one = set(list_1khz) - set(list_100hz)
two = set(list_100hz) - set(list_1khz)
three = set(list_1khz) & set(list_100hz)
print(three, len(three))

if __name__ == '__main__':
    pass
