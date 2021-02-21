# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:09:27 2021

@author: Tarane Subramaniam
"""

# Main file where individual .py files are combined and HRV analysis will be done
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

## 1. INPUT RAW ECG (in no. of samples)

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

#read the file header and access the sampling rate
df=pd.read_csv(filename, header=[0, 1]) #takes in the csv and tells the program that the first two lines are header
header=df.columns #makes a list of header titles
samplinginterval=header[0][1] #records the sampling interval but has sec on end
numerical_sampleinterval=samplinginterval.replace(" sec", "") #removes sec so the interval is just a number
numerical_sampleinterval=numerical_sampleinterval.replace("'", "") #removes "'" so str can be converted into float
t_samp = float(numerical_sampleinterval)



#no_of_samples =df[["'sample interval'"]] #gives sample no
#whole_ecg1 =df[["'ECG1'"]] #gives first ecg
#whole_ecg2 =df[["'ECG2'"]] #gives second ecg


#get the sampling frequency of original signal
f_samp = int(1/t_samp)


#plot ECG 1
plt.figure(0)
plt.plot(whole_signal.t, whole_signal.ecg1)
plt.ylabel("MLII/mV")
plt.xlabel("No. of samples")
plt.title("Original ECG1 signal from MLII lead (" + str(int(f_samp)) + "Hz)")

#plot ECG 2
plt.figure(1)
plt.plot(whole_signal.t, whole_signal.ecg2)
plt.ylabel("V5/mV")
plt.xlabel("No. of samples")
plt.title("Original ECG2 signal from V5 lead (" + str(int(f_samp)) + "Hz)")


# Split signal into chunks
#create a new array containing first 'f_samp' samples of ecg1,ecg2 and time
short_ecg1 = np.array(whole_signal.ecg1[0:(f_samp+1)])
short_ecg2 = np.array(whole_signal.ecg2[0:(f_samp+1)])
time = np.array(whole_signal.t[0:(f_samp+1)])

#plot only first 'f_samp' samples
plt.figure(2)
plt.plot(time, short_ecg1,'.-')
plt.ylabel("MLII/mV")
plt.xlabel("No. of samples")
plt.title("ECG1 for 1 second (" + str(int(f_samp)) + "Hz)")

plt.figure(3)
plt.plot(time,short_ecg2,'.-')
plt.ylabel("V5/mV")
plt.xlabel("No. of samples")
plt.title("ECG2 for 1 second (" + str(int(f_samp)) + "Hz)")

#resampling signal using scipy.signal.resample
#note: this produces a tuple
resampled_ecg1 = signal.resample(short_ecg1,1000, t = time)
resampled_ecg2 = signal.resample(short_ecg2,1000, t = time)



#plot resampled signal
plt.figure(4)
plt.plot(resampled_ecg1[1], resampled_ecg1[0] ,'.-')
plt.ylabel('MLII/mV')
plt.xlabel('No. of samples')
plt.title('Resampled ECG1 for 1 second (1kHz)')

plt.figure(5)
plt.plot(resampled_ecg2[1], resampled_ecg2[0], '.-')
plt.ylabel('V5/mV')
plt.xlabel('No. of samples')
plt.title('Resampled ECG2 for 1 second (1kHz)')

#plot original vs. resampled signal for comparison
plt.figure(6)
plt.plot(time, short_ecg1, 'go-', resampled_ecg1[1], resampled_ecg1[0] ,'.-')
plt.legend(['Original signal ('+str(int(f_samp))+ 'Hz)', 'Resampled signal (1kHz)'])
plt.ylabel('MLII/mV')
plt.xlabel('Time(sec)')
plt.title('ECG1 for 1 second (Original vs. Resampled)')

plt.figure(7)
plt.plot(time, short_ecg2, 'go-', resampled_ecg2[1], resampled_ecg2[0], '.-')
plt.legend(['Original signal ('+str(int(f_samp))+ 'Hz)', 'Resampled signal (1kHz)'])
plt.ylabel('V5/mV')
plt.xlabel('Time(sec)')
plt.title('ECG2 for 1 second (Original vs. Resampled)')


'''
#alternative method to resample Time Series Data
#combine each new ecg array with new time array into a dataframe for upsampling
split_signal = np.stack((time, ecg1,ecg2), axis = 1)
#convert split_signal into a DataFrame with column headers
split_signal = pd.DataFrame(split_signal, columns=column_names)


split_signal['t'] = pd.to_datetime(split_signal['t'], unit='s')
upsampled = split_signal.set_index('t').resample('1ms').mean()  #sampling rate 1000Hz

# Interpolate
interpolated = upsampled.interpolate(method='spline', order=2)

#create a new time axis
upsampled_time = np.array([i/1000 for i in range(0, len(upsampled.ecg1), 1)])
names = ['t']
upsampled_time = pd.DataFrame(upsampled_time, columns = names)

#combine the upsampled_time dataframe with interpolated ecgs dataframe
#upsampled_sig = pd.concat([upsampled_time,interpolated.ecg1, interpolated.ecg2], axis = 1)


plt.figure(6)
plt.plot(upsampled_time, interpolated.ecg1, '.-')
plt.title("ECG1 for 1 second (1kHz)")
plt.xlabel("Time(sec)")
plt.ylabel("MLII/mV")

plt.figure(7)
plt.plot(upsampled_time, interpolated.ecg2,'.-')
plt.title("ECG2 for 1 second (1kHz)")
plt.xlabel("Time(sec)")
plt.ylabel("V5/mV")

'''

#convert tuple to dataframe
ecg1 = np.transpose(resampled_ecg1[0])
time = np.transpose(resampled_ecg1[1])
ecg2 = np.transpose(resampled_ecg2[0])

upsampled_sig = np.stack((time, ecg1, ecg2), axis = 1)
upsampled_sig = pd.DataFrame(upsampled_sig, columns = column_names)


# Output: 'feather'/'pickle' format?
