'''
Summary of steps taken to extract HRV
1a. Input raw ECG OR 1b. Artificial ECG
2. Pre-processing
3a. R peak detection
3b. RR interval calculations and HRV analysis
'''

# Main file where individual .py files are combined and HRV analysis will be done
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import signal
# The following are .py files we have written which contain the functions used in this code
from artificial_ecg_1b import whole_fakeecg
from filter_ecg_2 import plot_data,filter, denoise
from peak_detection_3 import mirror_ecg, diffs, get_r_peaks, get_rr, hrv

  
    
def decidetype():
    while True: #choice to test simulation using artificial ECG or raw ECG
        d1=input("Do you want to: A) Input a raw .csv ECG file or B)Use an artificial ECG? [A/B]: ")
        if d1 in ['A', 'B']: #keeps asking if the user input isn't A or B
            break
    if d1 == "A": 
        filename = input("Enter your filename (including .csv): ")
        print("Loading", filename + "...")
        ## 1a. Input File
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
            short_ecg1 = np.array(whole_signal.ecg1[0:5*f_samp])
        
        elif d2 == "2": 
            short_ecg1 = np.array(whole_signal.ecg2[0:5*f_samp])
             
        # Split signal into chunks
        #create a new array containing first 1024 (~8 waves) samples of ecg1,ecg2 and time
        
        time = np.array(whole_signal.t[0:5*f_samp])
        chunkLength = len(short_ecg1)
        resampledLength = math.floor(1000*chunkLength/f_samp)

        #resampling signal to 1000Hz using scipy.signal.resample
        #note: this produces a tuple
        resampled_ecg = signal.resample(short_ecg1,resampledLength, t = time)
 
        #convert tuple to dataframe
        ecg1 = np.transpose(resampled_ecg[0])
        time = np.transpose(resampled_ecg[1])

        upsampled_sig = np.stack((time, ecg1), axis = 1)
        upsampled_sig = pd.DataFrame(upsampled_sig, columns = ['t', 'ECG'])

        # Plot resampled ECG
        plot_data(upsampled_sig.t,upsampled_sig.ECG,resampledLength,f_samp,'Resampled ECG')
        
        
        return ecg1, time, f_samp, x
    elif d1 == "B": 
        ## 1b. Artificial ECG (artificial_ecg.py)
        artificial_points, xtime = whole_fakeecg(120)
        sampfreq=1000
        a=np.arange(len(xtime))
        b=pd.DataFrame(data=a, columns=['Samples']) 
        samples=b[['Samples']]
        return artificial_points, xtime, sampfreq, samples


ecg, t, f, x=decidetype()

upsampled_sig = np.stack((t, ecg), axis = 1)
upsampled_sig = pd.DataFrame(upsampled_sig, columns = ['t', 'ecg'])
#
## 2. FILTERING (filter_ecg.py)
# Apply all filters to denoise ECG
filteredSig = denoise(upsampled_sig.ecg,1000,100,0.5,50,2)
plot_data(upsampled_sig.t,filteredSig,5000,f,'Denoised ECG')

# consider: anomalous/atopic beats

## 3a. R PEAK DETECTION (peak_detection.py)
# Mirror negative R peaks if present
mirroredSig=mirror_ecg(filteredSig)
# DEBUG
plot_data(upsampled_sig.t,mirroredSig,5000,f,'Mirrored ECG')

# Find sample numbers where local peaks present
peaks=diffs(mirroredSig)
# DEBUG
plt.plot(x[0:len(mirroredSig)],mirroredSig)
plt.plot(peaks,mirroredSig.iloc[peaks],"x")
plt.title('Local peaks')
plt.show()

## 3b. RR INTERVALS and HRV CALCULATIONS
# edit w_t and a_t based on condition being analysed
r_peaks=get_r_peaks(peaks,mirroredSig,0.6,3)
# DEBUG
plt.plot(x[0:len(mirroredSig)],mirroredSig)
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
