#same code just not sampled

# Main file where individual .py files are combined and HRV analysis will be done
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import signal
# The following are .py files we have written which contain the functions used in this code
from artificial_ecg import whole_fakeecg
from filter_ecg import plot_data,filter, denoise
from peak_detection import mirror_ecg, diffs, get_r_peaks, get_rr, hrv

  
    
def decidetype():
    while True: #choice to test simulation using artificial ECG or raw ECG
        d1=input("Do you want to: A) Input a raw .csv ECG file or B)Use an artificial ECG? [A/B]: ")
        if d1 in ['A', 'B']: #keeps asking if the user input isn't A or B
            break
    if d1 == "A": 
        filename = input("Enter your filename (including .csv): ")
        print("Loading", filename + "...")
        ## 1. Input File
        #Import ECG (.csv)
        #create a table with 3 columns depending on .csv file
        column_names = [    #create a table with 3 columns depending on .csv file
            't',
            'ecg1',
            'ecg2',
            ]

        #read the .csv file into a dataframe using pandas and skip the first 2 rows
        whole_signal = pd.read_csv(filename, sep=',',
                           names = column_names, skiprows = 2)

        #read the file header and access the sampling rate
        df=pd.read_csv(filename, header=[0, 1]) #takes in the csv and tells the program that the first two lines are header
        header=df.columns #makes a list of header titles
        samplinginterval=header[0][1] #records the sampling interval but has sec on end
        numerical_sampleinterval=samplinginterval.replace(" sec", "") #removes sec so the interval is just a number
        numerical_sampleinterval=numerical_sampleinterval.replace("'", "") #removes "'" so str can be converted into float
        t_samp = float(numerical_sampleinterval)
        x=df[["'sample interval'"]]

        #get the sampling frequency of original signal
        f_samp = int(1/t_samp)
        # Plot the original signal
        plot_data(whole_signal.t, whole_signal.ecg1, 5*f_samp, f_samp, "ECG 1")
    
        
        while True: #choice to test simulation using artificial ECG or raw ECG
            d2=input("Do you want to: 1) Input ECG data for 1st lead in the file or 2) The 2nd lead? [1/2]: ")
            if d2 in ['1', '2']: #keeps asking if the user input isn't 1 or 2
                break
        if d2 == "1": 
            ecgchosen=whole_signal.ecg1
        
        elif d2 == "2": 
            ecgchosen=whole_signal.ecg2
             
        time = whole_signal.t
        Length = len(ecgchosen)
        resampledLength = math.floor(1000*Length/f_samp)

        #resampling signal to 1000Hz using scipy.signal.resample
        #note: this produces a tuple
        resampled_ecg = signal.resample(ecgchosen,resampledLength, t = time)
 
        #convert tuple to dataframe
        ecg1 = np.transpose(resampled_ecg[0])
        time = np.transpose(resampled_ecg[1])

        upsampled_sig = np.stack((time, ecg1), axis = 1)
        upsampled_sig = pd.DataFrame(upsampled_sig, columns = ['t', 'ECG'])

        # Plot resampled ECG
        plot_data(upsampled_sig.t,upsampled_sig.ECG,resampledLength,f_samp,'Resampled ECG')
        
        
        return ecg1, upsampled_sig.t, f_samp
    elif d1 == "B": 
        ## 2. Artificial ECG
        artificial_points, xtime = whole_fakeecg(120)
        sampfreq=1000
        a=np.arange(len(xtime))
        b=pd.DataFrame(data=a, columns=['Samples']) 
        samples=b[['Samples']]
        return artificial_points, xtime, sampfreq


ecg, t, f_samp=decidetype()
f=1000
x=np.arange(len(t))
upsampled_sig = np.stack((t, ecg), axis = 1)
upsampled_sig = pd.DataFrame(upsampled_sig, columns = ['t', 'ecg'])
plot_data(upsampled_sig.t,upsampled_sig.ecg, len(upsampled_sig.t),f_samp,'Normal ECG')

#
## 3. FILTERING
# Apply all filters to denoise ECG
filteredSig = denoise(upsampled_sig.ecg,1000,100,0.5,50,2)
plot_data(upsampled_sig.t,filteredSig, len(upsampled_sig.t),f_samp,'Denoised ECG')

# consider: anomalous/atopic beats

## 4. R PEAK DETECTION
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

## 5. RR INTERVALS
# edit w_t and a_t based on condition being analysed
r_peaks=get_r_peaks(peaks,mirroredSig,0.6,3)
# DEBUG
plt.plot(x,mirroredSig)
plt.plot(r_peaks,mirroredSig.iloc[r_peaks],"x")
plt.title('R peaks')
plt.show()

print("t: "+str(t))
rr_intervals=get_rr(r_peaks,1/f)
plt.scatter(rr_intervals,np.zeros_like(rr_intervals))
plt.title('Distribution of RR intervals')
plt.show()

# calculate SDNN and average RR interval
sdnn,rr_avg=hrv(rr_intervals)
print("SDNN: "+str(sdnn))
print("avg: "+str(rr_avg))

## consider: frequency domain conversion
