import numpy as np
import pandas as pd
from pathlib import Path

# Path to the data directory
for path in Path('STUNNING Demonstrator USW Data').rglob('*.dat'):
    print(path.name)

# Data class
class Data:
    def __init__(self, file_name):
        self
    def print(self)