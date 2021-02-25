# Main file where individual .py files are combined and HRV analysis will be done
import pandas as pd
from fakeecg import whole_fakeecg
from scipy import signal
from filter import plot_data,filter, denoise
import numpy as np
import math

## 1. INPUT RAW ECG

#ask user for input
filename = input("Enter your filename (including .csv): ")
print("Loading", filename + "...")

# Import ECG (.csv)
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

#get the sampling frequency of original signal
f_samp = int(1/t_samp)

# Plot the original signal
plot_data(whole_signal.t,whole_signal.ecg1,5*f_samp,f_samp,"ECG 1")

# Split signal into chunks
#create a new array containing first 1024 (~8 waves) samples of ecg1,ecg2 and time
short_ecg1 = np.array(whole_signal.ecg1[0:5*f_samp])
short_ecg2 = np.array(whole_signal.ecg2[0:5*f_samp])
time = np.array(whole_signal.t[0:5*f_samp])
chunkLength = len(short_ecg1)
resampledLength = math.floor(1000*chunkLength/f_samp)
print(chunkLength)

#resampling signal to 1000Hz using scipy.signal.resample
#note: this produces a tuple
resampled_ecg1 = signal.resample(short_ecg1,resampledLength, t = time)
resampled_ecg2 = signal.resample(short_ecg2,resampledLength, t = time)

#convert tuple to dataframe
ecg1 = np.transpose(resampled_ecg1[0])
time = np.transpose(resampled_ecg1[1])
ecg2 = np.transpose(resampled_ecg2[0])

upsampled_sig = np.stack((time, ecg1, ecg2), axis = 1)
upsampled_sig = pd.DataFrame(upsampled_sig, columns = column_names)

# Plot resampled ECG
plot_data(upsampled_sig.t,upsampled_sig.ecg1,resampledLength,f_samp,'Resampled ECG')


# Output: 'feather'/'pickle' format?

## 2. CREATION OF ARTIFICIAL ECG

artificial_ecg, xtime = whole_fakeecg(120)

## 3. PRE-PROCESSING

# Apply all filters to denoise ECG
filteredSig = denoise(upsampled_sig.ecg1,1000,100,0.5,50,2)
plot_data(upsampled_sig.t,filteredSig,5000,f_samp,'Denoised ECG')

# consider: anomalous/atopic beats


## 4. R PEAK DETECTION

## 5. RR INTERVALS

## consider: frequency domain conversion