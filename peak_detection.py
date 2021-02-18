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
y=y.ravel() # converts ECG data to 1D array, the appropriate format to finding peaks
#print(y)

# Mirror negative R peaks if present
# Condition: for each point, check whether adjacent points within 0.3s (0.3/0.0078125=38 samples) has an amplitude at least 1.5 times smaller.
# If the above returns true, that particular point signifies an R peak, and the whole 0.6s range is mirrored along y=0.
y_m=np.array([0.000]*len(y))
to_mirror=False
for i in range(38,len(y)-38):
    if y[i]<0:
        for j in range(i-38,i+38):
            if abs(y[i])>=abs(1.5*y[j]):
                to_mirror=True
        if to_mirror==True:
            y_m[i]=abs(y[i])
        to_mirror=False

    else: y_m[i]=y[i]
#print(y)
#print(y_m)

plt.figure(0)
plt.subplot(2, 1, 1)
plt.plot(xVal[0:1000],y)
plt.ylabel("MLII /mV")
plt.title("Original ECG")

plt.subplot(2, 1, 2)
plt.plot(xVal[0:1000],y_m)
plt.xlabel("Time /s")
plt.ylabel("MLII /mV")
plt.title("ECG with mirrored peaks")
plt.show()

# Arrays of differences between adjacent data points
d1=[0]*(len(y)-1) # 1st difference, to be normalised by 1/0/-1 later
d2=[0]*(len(y)-2) # 2nd difference, between normalised 1st differences
for i in range(len(d1)):
    d1[i]=y[i+1]-y[i]
    if d1[i]>0:
        d1[i]=1
    elif d1[i]==0:
        d1[i]=0
    else: d1[i]=-1

sample=[]
for i in range(len(d2)):
    d2[i]=d1[i+1]-d1[i]
    if d2[i]==-2:
        sample.append(i+1)
'''
plt.plot(xVal[0:1000],y_m)
plt.plot(sample,y_m[sample],"x")
plt.show()
'''
# Average amplitude and width of peaks determines the threshold in which R peaks are detected
w=[0]*(len(sample)-1)
w_tot=0
a_tot=0
for i in range(len(w)):
    w[i]=sample[i+1]-sample[i]
    w_tot+=w[i]
for i in sample:
    a_tot+=y_m[i]

w_avg=w_tot/len(w)
a_avg=a_tot/len(sample)
print("w_tot: "+str(w_tot))
print("a_tot: "+str(a_tot))
print("w_avg: "+str(w_avg))
print("a_avg: "+str(a_avg))
print(len(w))
print(len(y_m))
print(len(sample))

r_peaks=[]
for i in range(len(w)):
        if w[i]>0.6*w_avg and y_m[sample[i]]>1.5*a_avg:
            #print("dis: "+str(sample[i]))
            r_peaks.append(sample[i])

print(r_peaks)
print(sample)
plt.plot(xVal[0:1000],y_m)
plt.plot(r_peaks,y_m[r_peaks],"x")
plt.show()

'''
Debugging - ensuring peak detection works

The maximal possible time window of one QRS wave is taken to be 150ms
The sample interval is 0.0078125s
Therefore, the minimal distance between peaks (in terms of samples) should be the quotient of these values: 19
However, this detects 2-3 extra samples (in between each RR interval) as peaks. 
Currently the distance is taken to be 19*2.5=48, but this still detects a false first peak (which is not an R peak)
Taking a threshold height (y value) of 0.1 rectifies this problem, though the distance variable may be better to use in ECGs with more irregularities

# Plot ECG with peaks indicated
peaks, _ = find_peaks(y,height=None, distance=48) #distance=48
plt.plot(xVal[0:1000],y)
plt.plot(peaks, y[peaks],"x")
#plt.plot(np.zeros_like(y), "--", color="gray") # y axis at 0
plt.show()

peaks=peaks*0.0078125 # Convert from sample number to time in seconds
print("Peaks:")
print(peaks)
'''
'''
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
'''