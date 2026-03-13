from math import sqrt
import pandas as pd
import numpy as np

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

# Adding a column to track whether a neighbor has already been used in a cell for each negative weight loop
fullData['used'] = False

# Adding a column to track the negative weight event's distance to all other events
fullData['distance'] = 0.0

# Iterating over every case of negative weight
for i, row in negWeights.iterrows():
    if row['weight'] < 0:

        # Setting pt and y values of each negative event for distance calculation
        ptNeg = row['pt']
        yNeg = row['y']
        cellWeight = row['weight'] # Cell weight prior to adding anything to it
        fullData.at[i, 'used'] = True # Setting current negative event to used so it's not counted in the following loop
        used_events = [i] # Indices of events that are being added to the current cell

        fullData['distance'] = np.sqrt((fullData['pt'] - ptNeg)**2 + 100*(fullData['y'] - yNeg)**2) # Calculating distances to all other events
        sortedDistIndices = fullData['distance'].sort_values().index # Sorting the distances from shortest to largest
        
        for j in sortedDistIndices:
            # Checking to see if event has already been used in different cell
            if not fullData.at[j, 'used']: 
                cellWeight += fullData.at[j, 'weight'] # Adding weight of next nearest event to cell
                fullData.at[j, 'used'] = True # Marking event as used in a cell
                used_events.append(j) # Adding event to current cell

                if cellWeight > 0:
                    break # Getting out of the for loop when cell weight is positive
            
        