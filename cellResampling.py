from math import sqrt
from numpy import full
import pandas as pd

# Reading both csv files into dataframes
real = pd.read_csv("real_events.csv")
virt = pd.read_csv("virtual_events.csv")

# Applying Born Projection -->
# pt = ptreal = zgluon
# y = yreal
real['pt'] = real['pt_real'] + real['z_gluon']
real['y'] = real['y_real']

# Extracting new real events and combining with virtual ones
newReal = real[['pt', 'y', 'weight']]
virt = virt[['pt', 'y', 'weight']]
fullData = pd.concat([virt, newReal], ignore_index=True)

# All cases of negative weight
negWeights = fullData[fullData['weight'] < 0]

# Adding a column to track whether a neighbor has already been used in a cell
fullData['used'] = False

# Iterating over every case of negative weight
for i, row in negWeights.iterrows():
    w = row['weight']

# Function for calculating distance to neighbors
def dist(pti, ptj, yi, yj):
    d = sqrt((pti - ptj)**2 + 100*(yi - yj)**2)
    return d
print(fullData)