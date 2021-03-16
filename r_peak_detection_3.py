'''
Inspiration from https://www.hindawi.com/journals/jhe/2017/5980541/
'''

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from math import sqrt

'''
DEBUG: Import csv data into dataframe
df=pd.read_csv('./mit-bih-database/MITBIH_Norm16265.csv',header=[0, 1])
print(df.head())

xVal=df[["'sample interval'"]]
yVal=df.iloc[:,1]
interval=0.0078125 # change to t_samp when integrated into main.py

y=yVal[0:1000].to_numpy()
y=y.ravel() # converts ECG data to 1D array, the appropriate format to finding peaks
print(y)
'''

## Mirror negative R peaks if present
# THRESHOLD: for each point, check whether adjacent points within 0.3s (0.3/0.0078125=38 samples) has an amplitude at least 1.5 times smaller.
# If the above returns true, that particular point signifies an R peak, and the whole 0.6s range is mirrored along y=0.
def mirror_ecg(y):
    y_m=np.array([0.000]*len(y))
    to_mirror=False
    y=y.to_numpy()
    for i in range(38,len(y)-38):
        if y[i]<0:
            for j in range(i-38,i+38):
                if abs(y[i])>=abs(1.5*y[j]):
                    to_mirror=True
            if to_mirror==True:
                y_m[i]=abs(y[i])
            to_mirror=False
        else: y_m[i]=y[i]
    y_m = pd.DataFrame(y_m, columns=['y'])
    return y_m

#y_m=mirror_ecg(y)
#print(y)
#print(y_m)

#If mirroring function not used:
#y_m=y

'''
DEBUG: Check that negative peaks are mirrored correctly
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
'''

## Arrays of differences between adjacent data points
def diffs(y):
    d1=[0]*(len(y)-1) # 1st difference, to be normalised by values -1,0, or 1
    d2=[0]*(len(y)-2) # 2nd difference, between normalised 1st differences
    y=y.to_numpy()
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

#peaks=diffs(y)

'''
DEBUG: Check that local peaks are detected correctly
plt.plot(xVal[0:1000],y_m)
plt.plot(peaks,y_m[peaks],"x")
plt.show()
'''

## Average amplitude a and width w of peaks determines the thresholds a_t,w_t in which R peaks are detected
def get_r_peaks(peaks,y_m, w_t, a_t):

    y_m=y_m.to_numpy()

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
# THRESHOLDS for Norm ECGs:
# w must be more than 0.6 times of w_avg
# a must be more than 1.5 times of a_avg
    r_peaks=[]
    for i in range(len(w)):
        if w[i]>w_t*w_avg and y_m[peaks[i]]>a_t*a_avg:
            r_peaks.append(peaks[i])
    '''
    DEBUG: Check that R peaks are detected correctly
    print("Sample numbers of local peaks: "+str(peaks))
    print("Sample numbers of R peaks: "+str(r_peaks))
    plt.plot(xVal[0:1000],y_m)
    plt.plot(r_peaks,y_m[r_peaks],"x")
    plt.show()
    '''
    '''
# Sample numbers of R peaks are converted to time/seconds.
# Time interval between each adjacent sample is found directly below "sample interval" in chosen CSV file
    for i in range(len(r_peaks)):
        r_peaks[i]=r_peaks[i]*interval
    print("Time points of R peaks: "+str(r_peaks))
'''
    return r_peaks

#r_peaks=get_r_peaks(peaks,y_m,interval,0.6,1.5)

def get_rr(r_peaks,t_samp):
## Return array of RR intervals
    rr_intervals=[0]*(len(r_peaks)-1)

    for i in range(len(rr_intervals)):
        rr_intervals[i]=(r_peaks[i+1]-r_peaks[i])*t_samp
    print("RR intervals: "+str(rr_intervals))

    return rr_intervals

#rr_intervals=get_rr(r_peaks,0.0078125)

## Calculate standard deviation of NN intervals (sdnn), root mean square of successive differences (rmssd) and average RR interval (rr_avg), in seconds
def hrv(rr_intervals):
    total=0
    total_diff_sq=0
    total_diff_adj_sq=0

    for j in range(len(rr_intervals)):
        total+=rr_intervals[j]
    rr_avg=total/len(rr_intervals)

    for j in range(len(rr_intervals)):
        total_diff_sq+=(rr_intervals[j]-rr_avg)**2
    sdnn=sqrt(total_diff_sq/(len(rr_intervals)))

    for j in range(len(rr_intervals)-1):
        total_diff_adj_sq+=(rr_intervals[j]-rr_intervals[j+1])**2
    rmssd=sqrt(total_diff_adj_sq/(len(rr_intervals)-1))

    return rr_avg, sdnn, rmssd

#sdnn,rr_avg=hrv(rr_intervals)

#print("SDNN: "+str(sdnn))
#print("Average RR interval: "+str(rr_avg))


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