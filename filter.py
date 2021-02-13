import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, iirnotch

df=pd.read_csv('ecgSample.csv',header=[0, 1])
print(df.head())

xVal=df[["'sample interval'"]]
yVal=df[["'ECG1'"]]

def plot_data(xVal,yVal,length):
    plt.figure(0)
    plt.plot(xVal[0:length]/360,yVal[0:length])
    ax=plt.gca()
    ax.axes.yaxis.set_ticks([])
    plt.ylabel("Amplitude")
    plt.title("Unfiltered Signal")
    plt.show()

plot_data(xVal,yVal,4000)

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
plot_data(xVal,filtered_signal,2000)

