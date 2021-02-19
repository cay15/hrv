'''
Inspiration from https://www.hindawi.com/journals/jhe/2017/5980541/
'''

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from math import sqrt


df=pd.read_csv('./mit-bih-database/arrythmia_100.csv',header=[0, 1])
print(df.head())

xVal=df[["'sample interval'"]]
yVal=df[["'MLII'"]]

y=yVal[0:1000].to_numpy()
y=y.ravel() # converts ECG data to 1D array, the appropriate format to finding peaks
#print(y)

## Mirror negative R peaks if present
# THRESHOLD: for each point, check whether adjacent points within 0.3s (0.3/0.0078125=38 samples) has an amplitude at least 1.5 times smaller.
# If the above returns true, that particular point signifies an R peak, and the whole 0.6s range is mirrored along y=0.
def mirror_ecg(y):
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
    return y_m

y_m=mirror_ecg(y)
#print(y)
#print(y_m)


# DEBUG: Check that negative peaks are mirrored correctly
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

## Arrays of differences between adjacent data points
def diffs(y):
    d1=[0]*(len(y)-1) # 1st difference, to be normalised by values -1,0, or 1
    d2=[0]*(len(y)-2) # 2nd difference, between normalised 1st differences
    for i in range(len(d1)):
        d1[i]=y[i+1]-y[i]
        if d1[i]>0:
            d1[i]=1
        elif d1[i]==0:
            d1[i]=0
        else: d1[i]=-1

## Find local peaks
# THRESHOLD: If a 2nd difference=-2, the next sample is an R peak.
    peaks=[]
    for i in range(len(d2)):
        d2[i]=d1[i+1]-d1[i]
        if d2[i]==-2:
            peaks.append(i+1)
    return peaks

peaks=diffs(y)

# DEBUG: Check that local peaks are detected correctly
plt.plot(xVal[0:1000],y_m)
plt.plot(peaks,y_m[peaks],"x")
plt.show()

## Average amplitude a and width w of peaks determines the threshold in which R peaks are detected
def get_rr(peaks,y_m):
    w=[0]*(len(peaks)-1)
    w_tot=0
    a_tot=0
    for i in range(len(w)):
        w[i]=peaks[i+1]-peaks[i]
        w_tot+=w[i]
    for i in peaks:
        a_tot+=y_m[i]

    w_avg=w_tot/len(w)
    a_avg=a_tot/len(peaks)
    
    # DEBUG: Check that totals and averages of a and w are correct
    print("w_tot: "+str(w_tot))
    print("a_tot: "+str(a_tot))
    print("w_avg: "+str(w_avg))
    print("a_avg: "+str(a_avg))

## Generate array of sample numbers where R peaks are present
# THRESHOLDS:
# w must be more than 0.6 times of w_avg
# a must be more than 1.5 times of a_avg
    r_peaks=[]
    for i in range(len(w)):
        if w[i]>0.6*w_avg and y_m[peaks[i]]>1.5*a_avg:
            r_peaks.append(peaks[i])

# DEBUG: Check that R peaks are detected correctly
    print("Sample numbers of local peaks: "+str(peaks))
    print("Sample numbers of R peaks: "+str(r_peaks))
    plt.plot(xVal[0:1000],y_m)
    plt.plot(r_peaks,y_m[r_peaks],"x")
    plt.show()

# Sample numbers of R peaks are converted to time/seconds.
# Time interval between each adjacent sample is 0.0078125s
    for i in range(len(r_peaks)):
        r_peaks[i]=r_peaks[i]*0.0078125
    print("Time points of R peaks: "+str(r_peaks))

## Return array of RR intervals
    rr_intervals=[0]*(len(r_peaks)-1)

    for i in range(len(rr_intervals)):
        rr_intervals[i]=r_peaks[i+1]-r_peaks[i]
    print("RR intervals: "+str(rr_intervals))

    return rr_intervals

rr_intervals=get_rr(peaks,y_m)

## Calculate standard deviation of NN intervals (sdnn) and average RR interval (rr_avg), in seconds
def hrv(rr_intervals):
    total=0
    total_sq=0
    for j in range(len(rr_intervals)):
        total+=rr_intervals[j]
        total_sq+=(rr_intervals[j]**2)
    sdnn=sqrt(total_sq/len(rr_intervals))
    rr_avg=total/len(rr_intervals)
    return sdnn,rr_avg

sdnn,rr_avg=hrv(rr_intervals)

print("SDNN: "+str(sdnn))
print("Average RR interval: "+str(rr_avg))

'''
Debugging - ensuring peak detection works through the use of find_peaks function

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