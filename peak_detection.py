import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from math import sqrt

df=pd.read_csv('ecgSample.csv',header=[0, 1])
print(df.head())

xVal=df[["'sample interval'"]]
yVal=df[["'ECG1'"]]

y=yVal[0:1000].to_numpy()
y=y.ravel() # converts ECG data to 1D array, the appropriate format for find_peaks
#print(y)p

'''
The maximal possible time window of one QRS wave is taken to be 150ms
The sample interval is 0.0078125s
Therefore, the minimal distance between peaks (in terms of samples) should be the quotient of these values: 19
However, this detects 2-3 extra samples (in between each RR interval) as peaks. 
Currently the distance is taken to be 19*2.5=48, but this still detects a false first peak (which is not an R peak)
Taking a threshold height (y value) of 0.1 rectifies this problem, though the distance variable may be better to use in ECGs with more irregularities
'''

# Plot ECG with peaks indicated
peaks, _ = find_peaks(y,height=None, distance=48) #distance=48
plt.plot(xVal[0:1000],y)
plt.plot(peaks, y[peaks],"x")
#plt.plot(np.zeros_like(y), "--", color="gray") # y axis at 0
plt.show()

peaks=peaks*0.0078125 # Convert from sample number to time in seconds
print("Peaks:")
print(peaks)

# Return array of RR intervals
rr_intervals=[0]*(len(peaks)-1)

for i in range(len(rr_intervals)):
    rr_intervals[i]=peaks[i+1]-peaks[i]
print("RR intervals:")
print(rr_intervals)

total=0
total_sq=0
for j in range(len(rr_intervals)):
    total+=rr_intervals[j]
    total_sq+=(rr_intervals[j]*rr_intervals[i])
SDNN=sqrt(total_sq/len(rr_intervals))
avg=total/len(rr_intervals)
print("SDNN: ")
print(SDNN)
print("Average RR interval:")
print(avg)