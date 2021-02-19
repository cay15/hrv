"""
Created on Wed Feb 17 22:09:27 2021

@author: Tarane Subramaniam
"""

####UPSAMPLING ECG TO 1kHz####

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

## 1. INPUT RAW ECG

#ask user for input
filename = input("Enter your filename (including .csv): ")
print("Loading", filename + "...")

# Import ECG (.csv)
#create a table with 3 columns depending on .csv file
column_names = [   
    't',
    'ecg1',
    'ecg2',
    ]

#read the .csv file into a dataframe using pandas and skip the first 2 rows
whole_signal = pd.read_csv(filename, sep=',',
                           names = column_names, skiprows = 2)



#get the sampling frequency of original signal
t_samp = whole_signal.t[1]
f_samp = int(1/t_samp)

#plot ECG 1
plt.figure(0)
plt.plot(whole_signal.t, whole_signal.ecg1)
plt.ylabel("MLII/mV")
plt.xlabel("Time(sec)")
plt.title("Original ECG1 signal from MLII lead (" + str(int(f_samp)) + "Hz)")

#plot ECG 2
plt.figure(1)
plt.plot(whole_signal.t, whole_signal.ecg2)
plt.ylabel("V5/mV")
plt.xlabel("Time(sec)")
plt.title("Original ECG2 signal from V5 lead (" + str(int(f_samp)) + "Hz)")


# Split signal into chunks
#create a new array containing first 'f_samp' samples of ecg1,ecg2 and time
ecg1 = np.array(whole_signal.ecg1[0:(f_samp+1)])
ecg2 = np.array(whole_signal.ecg2[0:(f_samp+1)])
time = np.array(whole_signal.t[0:(f_samp+1)])

#plot only first 'f_samp' samples of ecg1
plt.figure(2)
plt.plot(time, ecg1,'.-')
plt.ylabel("MLII/mV")
plt.xlabel("Time(sec)")
plt.title("ECG1 for 1 second (" + str(int(f_samp)) + "Hz)")

#plot only first 'f_samp' samples of ecg2
plt.figure(3)
plt.plot(time,ecg2,'.-')
plt.ylabel("V5/mV")
plt.xlabel("Time(sec)")
plt.title("ECG2 for 1 second (" + str(int(f_samp)) + "Hz)")

'''
#alternative method for resampling signal using scipy.signal.resample
resampled_ecg1 = signal.resample(ecg1,1000)
resampled_ecg2 = signal.resample(ecg2,1000)
resampled_time = signal.resample(time, 1000)


plt.figure(4)
plt.plot(time, ecg1, 'go-', resampled_time, resampled_ecg1, '.-')
plt.legend(['Original signal ('+str(int(f_samp))+ ')', 'Resampled signal (1kHz)'])
plt.ylabel('MLII/mV')
plt.xlabel('Time(sec)')
plt.title('ECG1 for 1 second (Original vs. Resampled)')

plt.figure(5)
plt.plot(time, ecg2, 'go-', resampled_time, resampled_ecg2, '.-')
plt.legend(['Original signal ('+str(int(f_samp))+ ')', 'Resampled signal (1kHz)'])
plt.ylabel('V5/mV')
plt.xlabel('Time(sec)')
plt.title('ECG2 for 1 second (Original vs. Resampled)')
'''


#combine each new ecg array with new time array into a dataframe for upsampling
split_signal = np.stack((time, ecg1,ecg2), axis = 1)
#convert split_signal into a DataFrame with column headers
split_signal = pd.DataFrame(split_signal, columns=column_names)

#set the time column as datetime index for upsampling
split_signal['t'] = pd.to_datetime(split_signal['t'], unit='s')
upsampled = split_signal.set_index('t').resample('1ms').mean()  #sampling rate 1000Hz

# Interpolate to fill in missing values in upsampled dataframe
interpolated = upsampled.interpolate(method='spline', order=2) #can also use method = 'cubic'


plt.figure(6)
plt.plot(interpolated.ecg1, '.-')
plt.title("ECG1 for 1 second (1kHz)")
plt.xlabel("Time(sec)")
plt.ylabel("MLII/mV")

plt.figure(7)
plt.plot(interpolated.ecg2,'.-')
plt.title("ECG2 for 1 second (1kHz)")
plt.xlabel("Time(sec)")
plt.ylabel("V5/mV")

#how to reset time column from datetime index to seconds for plotting purposes and rest of signal processing?

# Output: 'feather'/'pickle' format?
