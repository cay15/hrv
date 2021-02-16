import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, iirnotch, butter

#df=pd.read_csv('ecgSample.csv',header=[0, 1])
#print(df.head())

#create a table with 3 columns depending on .csv file
column_names = [
    't',
    'ecg1',
    'ecg2',
    ]

#read the .csv file into a dataframe using pandas and skip the first 2 rows
whole_signal = pd.read_csv('ecgSample.csv', sep=',',
                           names = column_names, skiprows = 2)
xVal = whole_signal.t
yVal = whole_signal.ecg1
#xVal=df[["'sample interval'"]]
#yVal=df[["'ECG1'"]]

def plot_data(xVal,yVal,length,Title='ECG Signal'):
    plt.figure()
    plt.plot(xVal[0:length]/360,yVal[0:length])
    ax=plt.gca()
    ax.axes.yaxis.set_ticks([])
    plt.ylabel("Amplitude")
    plt.title(Title)
    plt.show()

plot_data(xVal,yVal,1000,'Original Signal')

def highpass(sampling_rate,cutoff=0.05,order=2):
    nyquist_freq = 0.5 * sampling_rate
    normalCutoff = cutoff / nyquist_freq
    b, a = butter(order, normalCutoff, btype='high', analog=False)
    return b, a

def lowpass(sampling_rate,cutoff=150,order=2):
    nyquist_freq = 0.5 * sampling_rate
    normalCutoff = cutoff / nyquist_freq
    b, a = butter(order, normalCutoff, btype='low', analog=False)
    return b, a

def filter(data, sampling_rate, cutoff, order=2, filtertype='lowpass'):
    if filtertype.lower() == 'lowpass':
        b, a = lowpass(sampling_rate, cutoff, order=order)
    elif filtertype.lower() == 'highpass':
        b, a = highpass(sampling_rate, cutoff, order=order)
    elif filtertype.lower() == 'notch':
        b, a = iirnotch(cutoff, Q=0.005, fs=sampling_rate)
    else:
        raise ValueError('filtertype: %s is unknown, available are: \ lowpass, highpass, and notch' % filtertype)

    signal = data.to_numpy()  # convert column in dataframe to a numpy array
    signal = signal.T         # transpose numpy array into row vector

    filtered_data = filtfilt(b, a, signal)  # applies notch filter forward and backward to a signal

    # convert numpy array back to dataframe for plotting
    filtered_data = filtered_data.T
    filtered_df = pd.DataFrame(filtered_data, columns=['y'])
    return filtered_df



filtered_signal2 = filter(yVal,1000,0.5,2,'highpass')
plot_data(xVal,filtered_signal2,1000,'Highpass Filtered')

filtered_signal3 = filter(yVal,1000,3,2,'lowpass')
plot_data(xVal,filtered_signal3,1000,'Lowpass Filtered')

filtered_signal4 = filter(yVal,1000,0.05,2,'notch')
plot_data(xVal,filtered_signal4,1000,'Notch Filtered')

filtered_signal5 = filter(yVal,1000,150,2,'lowpass')
plot_data(xVal,filtered_signal5,1000,'Lowpass Filtered')