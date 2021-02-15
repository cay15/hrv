"""
Created on Sat Feb 13 19:57:13 2021

@author: Tarane Subramaniam
"""
#Signal was exported as .csv from PhysioBank ATM 
#(https://archive.physionet.org/cgi-bin/atm/ATM)
#Data used: MIT BIH normal sinus rhythm database (record: 16265)
            #ECG1 is MLII lead
            #ECG2 is V5 lead
            #Length of signal: To end (1 minute)
            #Time format: Seconds
            #Data format: Standard
            #Total no.of samples: 7679
            
#I renamed the data file from 'samples.csv' to '16265_secs_toend.csv' to avoid confusion between datasets. Check what you have named your file before running this code.

#OG Sampling interval, T = 0.0078125s
#OG Sampling rate, fs = 1/T = 128 Hz

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#create a table with 3 columns depending on .csv file
column_names = [
    't',
    'ecg1',
    'ecg2',
    ]

#read the .csv file into a dataframe using pandas and skip the first 2 rows
whole_signal = pd.read_csv('16265_secs_toend.csv', sep=',', 
                           names = column_names, skiprows = 2)
#plot ECG 1
plt.figure(0)
plt.plot(whole_signal.t, whole_signal.ecg1)
plt.ylabel("MLII/mV")
plt.xlabel("Time(sec)")
plt.title("Patient 16265 - ECG1 signal from MLII lead")

#plot ECG 2
plt.figure(1)
plt.plot(whole_signal.t, whole_signal.ecg2)
plt.ylabel("V5/mV")
plt.xlabel("Time(sec)")
plt.title("Patient 16265 - ECG2 signal from V5 lead")



#resampling at 1000Hz
f_samp = 1000
time = np.array([i/f_samp for i in range(0, len(whole_signal.ecg1), 1)]) # sampling rate 1000 Hz


#plot resampled ECG 1 and ECG 2
plt.figure(2)
plt.title('Patient 16265 - ECG1 resampled at 1kHz')
plt.plot(time, whole_signal.ecg1)
plt.xlabel('Time (sec)')
plt.ylabel('MLII/mV')

plt.figure(3)
plt.title('Patient 16265 - ECG2 resampled at 1kHz')
plt.plot(time, whole_signal.ecg2)
plt.xlabel('Time (sec)')
plt.ylabel('V5/mV')



#create a new array containing first 1000 samples of ecg1,ecg2 and time
ecg1 = np.array(whole_signal.ecg1[0:(f_samp+1)])
ecg2 = np.array(whole_signal.ecg2[0:(f_samp+1)])
time1 = np.array(time[0:(f_samp+1)])

#create a new array containing first 'f_samp2' samples of ecg1 and ecg2 (original sampling rate)
t_samp2 = whole_signal.t[1]
f_samp2 = int(1/t_samp2)
ecg1_original = np.array(whole_signal.ecg1[0:(f_samp2+1)])
ecg2_original = np.array(whole_signal.ecg2[0:(f_samp2+1)])
time2 = np.array(whole_signal.t[0:(f_samp2+1)])


#plot ECG 1 for both sampling frequencies (only first second)
fig = plt.figure(4)
plt.subplot(1,2,1)
plt.plot(time1, ecg1)
plt.ylabel("MLII/mV")
plt.xlabel("Time(sec)")
plt.title("ECG1 for 1 second (fs = 1kHz)")

plt.subplot(1,2,2)
plt.plot(time2, ecg1_original)
plt.ylabel("MLII/mV")
plt.xlabel("Time(sec)")
plt.title("ECG1 for 1 second (fs = 128Hz)")

fig.tight_layout()
fig.set_size_inches(w=11,h=7)

#plot ECG 2 for both sampling frequencies (only first second)
fig = plt.figure(5)
plt.subplot(1,2,1)
plt.plot(time1, ecg2)
plt.ylabel("V5/mV")
plt.xlabel("Time(sec)")
plt.title("ECG2 for 1 second (fs = 1kHz)")

plt.subplot(1,2,2)
plt.plot(time2, ecg2_original)
plt.ylabel("V5/mV")
plt.xlabel("Time(sec)")
plt.title("ECG2 for 1 second (fs = 128Hz)")

fig.tight_layout()
fig.set_size_inches(w=11,h=7)

#remove mean ECG (useful for noisy ECG)
ecg1_correctmean = ecg1 - np.mean(whole_signal.ecg1)
ecg2_correctmean = ecg2 - np.mean(whole_signal.ecg2)

#plot comparison of ecg1 with offset vs. mean-corrected values
fig = plt.figure(6)
plt.subplot(1, 2, 1)
plt.subplot(1, 2, 1).set_title('Mean offset present (ECG1)')
plt.plot(time1, ecg1)
plt.ylabel("MLII/mV")
plt.xlabel("Time(sec)")
#plt.xlim(0,0.125)

plt.subplot(1, 2, 2)
plt.subplot(1, 2, 2).set_title('Mean-corrected values (ECG1)')
plt.plot(time1, ecg1_correctmean)
plt.ylabel("MLII/mV")
plt.xlabel("Time(sec)")
#plt.xlim(0,0.125)

fig.tight_layout()
fig.set_size_inches(w=11,h=7)

#plot comparison of ecg2 with offset vs. mean-corrected values
fig = plt.figure(7)
plt.subplot(1, 2, 1)
plt.subplot(1, 2, 1).set_title('Mean offset present (ECG2)')
plt.plot(time1, ecg2)
plt.ylabel("V5/mV")
plt.xlabel("Time(sec)")
#plt.xlim(0,0.125)

plt.subplot(1, 2, 2)
plt.subplot(1, 2, 2).set_title('Mean-corrected values (ECG2)')
plt.plot(time1, ecg2_correctmean)
plt.ylabel("V5/mV")
plt.xlabel("Time(sec)")
#plt.xlim(0,0.125)

fig.tight_layout()
fig.set_size_inches(w=11,h=7)
