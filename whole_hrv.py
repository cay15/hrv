# Main file where individual .py files are combined and HRV analysis will be done
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import signal
# The following are .py files we have written which contain the functions used in this code
from artificial_ecg_1b import whole_fakeecg
from filter_ecg_2 import plot_data,filter, denoise
from r_peak_detection_3 import mirror_ecg, diffs, get_r_peaks, get_rr, hrv
from input_real_ecg_1a import input_ecg
  
    
def decidetype():
    while True: #choice to test simulation using artificial ECG or raw ECG
        d1=input("Do you want to: A) Input a raw .csv ECG file or B)Use an artificial ECG? [A/B]: ")
        if d1 in ['A', 'B']: #keeps asking if the user input isn't A or B
            break
    if d1 == "A":
        ## 1. a) Input ECG
        ecg1, time, f_samp, resampledLength=input_ecg()
        # Plot resampled ECG
        plot_data(time,ecg1,resampledLength,f_samp,'Resampled ECG')
        return ecg1, time, f_samp
    elif d1 == "B": 
        ## 1. b) Create Artificial ECG
        artificial_points, xtime = whole_fakeecg(60)
        sampfreq=1000
        a=np.arange(len(xtime))
        b=pd.DataFrame(data=a, columns=['Samples']) 
        return artificial_points, xtime, sampfreq


ecg, t, f_samp=decidetype()
f=1000
x=np.arange(len(t))
upsampled_sig = np.stack((t, ecg), axis = 1)
upsampled_sig = pd.DataFrame(upsampled_sig, columns = ['t', 'ecg'])
plot_data(upsampled_sig.t,upsampled_sig.ecg, len(upsampled_sig.t),f_samp,'Inputted ECG')

#
## 2. FILTERING
# Apply all filters to denoise ECG
filteredSig = denoise(upsampled_sig.ecg,1000,100,0.5,50,2)
plot_data(upsampled_sig.t,filteredSig, len(upsampled_sig.t),f_samp,'Denoised ECG')

# consider: anomalous/atopic beats

## 3. R PEAK DETECTION
# Mirror negative R peaks if present
mirroredSig=mirror_ecg(filteredSig)
#mirroredSig=filteredSig
# DEBUG
plot_data(upsampled_sig.t,mirroredSig,5000,f_samp,'Mirrored ECG')

# Find sample numbers where local peaks present
peaks=diffs(mirroredSig)

rtime=np.zeros(len(mirroredSig))
amps=mirroredSig['y'].values.tolist()
for i in peaks:
    rtime[i]=amps[i]
# DEBUG
rtime= rtime[rtime != 0]
newpeaks = [z / 1000 for z in peaks]

plt.plot(x/1000,mirroredSig)
plt.plot(newpeaks,rtime,"x")
plt.title('Local Peaks', fontsize=20)
plt.ylabel('Amplitude (mV)', fontsize=18)
plt.xlabel('Time (seconds)', fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.show()


## 4. RR INTERVALS
# edit w_t and a_t based on condition being analysed
r_peaks=get_r_peaks(peaks,mirroredSig,0.6,4)

rrtime=np.zeros(len(mirroredSig))
amps=mirroredSig['y'].values.tolist()
for i in r_peaks:
    rrtime[i]=amps[i]
# DEBUG
rrtime= rrtime[rrtime != 0]
newrpeaks = [w / 1000 for w in r_peaks]
# DEBUG
plt.plot(x/1000,mirroredSig)
plt.plot(newrpeaks,rrtime,"x")
plt.title('R Peaks', fontsize=20)
plt.ylabel('Amplitude (mV)', fontsize=18)
plt.xlabel('Time (seconds)', fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.show()

print("t: "+str(t))
rr_intervals=get_rr(r_peaks,1/f)
del(r_peaks[0])
for i in range(len(r_peaks)):
    r_peaks[i]*= 1/f
print("r peaks: "+str(r_peaks))
plt.plot(r_peaks,rr_intervals)
plt.title('Time Series of RR intervals', fontsize=20)
plt.ylabel('RR Interval (seconds)', fontsize=18)
plt.xlabel('Time (seconds)', fontsize=18)
plt.ylim(ymin=0)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.show()

# calculate average RR interval, SDNN, RMSSD
rr_avg, sdnn, rmssd=hrv(rr_intervals)
print("avg: "+str(rr_avg))
print("SDNN: "+str(sdnn))
print("RMSSD: "+str(rmssd))


## consider: frequency domain conversion
