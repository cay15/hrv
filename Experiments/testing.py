import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import signal
from artificial_ecg_1b import randomnoise, addnoise, addoffset
from artificial_ecg_1b import whole_fakeecg
from filter_ecg_2 import plot_data,filter, denoise
from peak_detection_3 import mirror_ecg, diffs, get_r_peaks, get_rr, hrv
from input_ecg_1a import input_ecg

#adding noise to normal sinus rhythm
ecg1, t, f_samp, resampledLength=input_ecg()
plot_data(t,ecg1,resampledLength,f_samp,'Resampled ECG')

def addsomenoise(ecg1, time, f_samp, resampledLength):
    tottime=resampledLength/1000
    mains=addnoise(ecg1, tottime, 50, 1)
    basedrift=addnoise(mains, tottime, 0.3, 0.5)
    highfreqnoise=addnoise(basedrift, tottime, 200, 0.4)
    randnoise=randomnoise(highfreqnoise)

    plot_data(time,mains,resampledLength,f_samp,'Mains')
    plot_data(time,basedrift,resampledLength,f_samp,'Basedrift')
    plot_data(time,highfreqnoise,resampledLength,f_samp,'High Freq')
    plot_data(time,randnoise,resampledLength,f_samp,'Random Noise')
    return randnoise

ecg=addsomenoise(ecg1, t, f_samp, resampledLength)
f=1000
x=np.arange(len(t))
upsampled_sig = np.stack((t, ecg), axis = 1)
upsampled_sig = pd.DataFrame(upsampled_sig, columns = ['t', 'ecg'])
plot_data(upsampled_sig.t,upsampled_sig.ecg, len(upsampled_sig.t),f_samp,'Normal ECG')

#
## 2. FILTERING
# Apply all filters to denoise ECG
filteredSig = denoise(upsampled_sig.ecg,1000,100,0.5,50,2)
plot_data(upsampled_sig.t,filteredSig, len(upsampled_sig.t),f_samp,'Denoised ECG')

# consider: anomalous/atopic beats

## 3. R PEAK DETECTION
# Mirror negative R peaks if present
mirroredSig=mirror_ecg(filteredSig)
# DEBUG
plot_data(upsampled_sig.t,mirroredSig,5000,f_samp,'Mirrored ECG')

# Find sample numbers where local peaks present
peaks=diffs(mirroredSig)
# DEBUG
plt.plot(x,mirroredSig)
plt.plot(peaks,mirroredSig.iloc[peaks],"x")
plt.title('Local peaks')
plt.show()

## 4. RR INTERVALS
# edit w_t and a_t based on condition being analysed
r_peaks=get_r_peaks(peaks,mirroredSig,0.6,3)
# DEBUG
plt.plot(x,mirroredSig)
plt.plot(r_peaks,mirroredSig.iloc[r_peaks],"x")
plt.title('R peaks')
plt.show()

print("t: "+str(t))
rr_intervals=get_rr(r_peaks,1/f)
del(r_peaks[0])
for i in range(len(r_peaks)):
    r_peaks[i]*= 1/f
print("r peaks: "+str(r_peaks))
plt.plot(r_peaks,rr_intervals,"x")
plt.title('Distribution of RR intervals')
plt.show()

# calculate SDNN and average RR interval
sdnn,rr_avg=hrv(rr_intervals)
print("SDNN: "+str(sdnn))
print("avg: "+str(rr_avg))

