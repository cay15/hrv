import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, iirnotch, butter

df=pd.read_csv('ecgSample.csv',header=[0, 1])
print(df.head())

xVal=df[["'sample interval'"]]
yVal=df[["'ECG1'"]]

def plot_data(xVal,yVal,length):
    plt.figure()
    plt.plot(xVal[0:length]/360,yVal[0:length])
    ax=plt.gca()
    ax.axes.yaxis.set_ticks([])
    plt.ylabel("Amplitude")
    plt.title("ECG Signal")
    plt.show()

plot_data(xVal,yVal,1000)

def remove_baseline_drift(data,sample_rate,cutoff=0.05):
    b, a = iirnotch(cutoff, Q=0.005, fs=sample_rate)    # get coefficients for notch filter
    signal = data.to_numpy()    # convert column in dataframe to a numpy array
    signal = signal.T
    filtered_data = filtfilt(b, a, signal)    # applies notch filter forward and backward to a signal
    filtered_data = filtered_data.T
    filtered_df = pd.DataFrame(filtered_data, columns=['y'])
    print(filtered_df)
    return filtered_df

filtered_signal = remove_baseline_drift(yVal,100.0,0.05)
plot_data(xVal,filtered_signal,1000)

def highpass(cutoff=0.05,order=2):
    b, a = butter(order, cutoff, btype='high', analog=False)
    return b, a

def lowpass(cutoff,order=2):
    b, a = butter(order, cutoff, btype='low', analog=False)
    return b, a

def filter(data, sample_rate, cutoff, order=2, filtertype='lowpass'):
    if filtertype.lower() == 'lowpass':
        b, a = lowpass(cutoff, order=order)
    elif filtertype.lower() == 'highpass':
        b, a = highpass(cutoff, order=order)
    elif filtertype.lower() == 'notch':
        b, a = iirnotch(cutoff, Q=0.005, fs=sample_rate)
    else:
        raise ValueError('filtertype: %s is unknown, available are: \ lowpass, highpass, and notch' % filtertype)

    signal = data.to_numpy()  # convert column in dataframe to a numpy array
    signal = signal.T         # transpose numpy array into row vector

    filtered_data = filtfilt(b, a, signal)  # applies notch filter forward and backward to a signal

    # convert numpy array back to dataframe for plotting
    filtered_data = filtered_data.T
    filtered_df = pd.DataFrame(filtered_data, columns=['y'])
    return filtered_df

filtered_signal2 = filter(yVal,100,0.05,2,'highpass')
plot_data(xVal,filtered_signal2,1000)

#filtered_signal3 = filter(yVal,100,2,2,'lowpass')
#plot_data(xVal,filtered_signal3,1000)

filtered_signal4 = filter(yVal,100,0.05,2,'notch')
plot_data(xVal,filtered_signal4,1000)