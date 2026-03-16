## GSoC Pre-Selection Task: Negative Weight Mitigation with Cell Resampling 

### Results
![Histogram for $\rho_T$](ptHistogram.png) 

Fig. 1: Histogram for $\rho_T$

![Histogram for $\rho_T$](yHistogram.png) 

Fig. 2: Histogram for $y$

### Structure
This is my implementation of the Cell Resampling Method. Overall structure of the code is as follows, with more comments in the script:

1. Read both datasets into dataframes.
2. Apply the Born Transform to all $\rho_T$ and $y$ values in the virtual_events dataset with the formula:
   - $\rho_T = \rho_{T, real} + z_{gluon}$ 
   - $y = y_{real}$
3. Merge both the (modified) virtual and real events into one dataframe.
4. Looping through each negative weight event and calculating its distance to all other events, building its cell, and using cell resampling to adjust all weights within that cell.
5. Using the original and new (all positive) weights to generate the two required histograms

### Computational Complexity
I have limited experience programming, so my best attempt at determining the computational complexity of the code is $O(N^2logN)$, based on a $for$ ( $O(N)$ ) loop containing another $for$ loop with a sorting algorithm ( $O(NlogN)$ ) in it.

### Discussion Question
Looking at $\rho_T$ and $y$ in the data, it's easy to see $\rho_T$ is in general 1 to 2 orders of magnitude larger than $y$. Calculating distance without a scaling factor would mean the larger $\rho_T$ would dominate the metric, distance would just mean the closest $\rho_T$ value. I consider the following to be a fair estimate:

<center>

$SF = \left(\frac{\sum_{i=1}^{N} |\rho_{T,i}|}{\sum_{i=1}^{N} |y_i|}\right)^2 =$ ~ $736$

</center>

Infinite events would mean that for each negative weight event the distance to the nearest events approaches $0$ and a scaling factor becomes irrelevant.
