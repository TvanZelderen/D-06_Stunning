import numpy as np
import pandas as pd
from pathlib import Path

# Path to the data directory
list = []
for path in Path('STUNNING Demonstrator USW Data').rglob('*.dat'):
    list.append(path.name)
print(len(list)/2)

# # Data class
# class Data:
#     def __init__(self, file_name):
#         self
#     def print(self)