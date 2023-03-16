from load import Data as dt

a = dt('01', '02', '02', 1)
a.normalize()
a.create_array()
a.bar_to_N()
print(a.array())