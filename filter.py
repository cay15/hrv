import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import filtfilt, iirnotch, butter, wiener

#df=pd.read_csv('ecgSample.csv',header=[0, 1])
#print(df.head())

def plot_data(xVal,yVal,length,fs,Title='ECG Signal',xlabel='Time/s',ylabel='Amplitude'):
    plt.figure()
    plt.plot(xVal[0:length]/fs,yVal[0:length])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(Title)
    plt.show()

def highpass(sampling_rate,cutoff=0.05,order=2):

    '''
    scipy.signal.butter(N, Wn, btype='high', analog=False, output='ba', fs=None)
    Function to create a digital High Pass Filter because data is regularly sampled

    :param sampling_rate: the sampling frequency (fs) of the ECG

    :param cutoff: the frequencies below the cutoff will be removed, the default is set to 0.05Hz
    For digital filters, Wn are in the same units as fs. Wn is normalised between 0 and 1, where 1 is the Nyquist frequency

    :param order: the order N of the filter, the default is set to 2

    btype='high' specifies that this is a high pass filter

    :return: Numerator (b) and denominator (a) polynomials of the IIR high pass filter
    '''

    nyquist_freq = 0.5 * sampling_rate  # nyquist frequency (folding point) is the max freq that can be reconstructed given the sampling rate
    normalCutoff = cutoff / nyquist_freq    # normalise cutoff frequency
    b, a = butter(order, normalCutoff, btype='high', analog=False)
    return b, a

def lowpass(sampling_rate,cutoff=150,order=2):

    '''
    scipy.signal.butter(N, Wn, btype='low', analog=False, output='ba', fs=None)
    Function to create a digital Low Pass Filter because data is regularly sampled

    :param sampling_rate: the sampling frequency (fs) of the ECG

    :param cutoff: the frequencies above the cutoff will be removed
    For digital filters, Wn are in the same units as fs. Wn is normalised between 0 and 1, where 1 is the Nyquist frequency

    :param order: the order N of the filter, the default is set to 2

    btype='low' specifies that this is a low pass filter

    :return: Numerator (b) and denominator (a) polynomials of the IIR high pass filter
    '''

    nyquist_freq = 0.5 * sampling_rate  # Nyquist frequency is the max freq that can be reconstructed given the sampling rate
    normalCutoff = cutoff / nyquist_freq    # normalise cutoff frequency
    b, a = butter(order, normalCutoff, btype='low', analog=False)
    return b, a


def filter(data, sampling_rate, cutoff, order=2, filtertype='lowpass'):

    '''
    This function calculates the coefficients of the filter specified by filtertype, cutoff and order.
    The input signal is converted to a numpy array then filtered using filtfilt and the filter coefficients found.
    The filtered signal is converted back to df and returned.

    The notch filter is a band-stop filter which removes a narrow frequency band around the specified cutoff frequency.
    scipy.signal.iirnotch(w0, Q, fs=2.0)
    w0: frequency to be removed
    Q: quality factor (Q = w0/bandwidth), the greater the value of Q, the narrower the notch

    :param data: the ECG signal to be filtered as a df
    :param sampling_rate: the sampling frequency (fs) of the ECG
    :param cutoff: the critical frequency of the filter to be made
    :param order: the order N of the filter to be made
    :param filtertype: 'lowpass','highpass' and 'notch'
    :return: filtered signal
    '''

    signal = data.to_numpy()  # convert column in dataframe to a numpy array
    signal = signal.T  # transpose numpy array into row vector

    if filtertype.lower() == 'lowpass':
        b, a = lowpass(sampling_rate, cutoff, order=order)
    elif filtertype.lower() == 'highpass':
        b, a = highpass(sampling_rate, cutoff, order=order)
    elif filtertype.lower() == 'notch':
        w0 = cutoff/ (sampling_rate/2)  # normalised cutoff is cutoff frequency divided by nyquist frequency
        Q = 30    # Q = w0/bandwidth where bandwidth=2
        b, a = iirnotch(w0, Q, sampling_rate)
    elif filtertype.lower() == 'wiener':
        filtered_data = wiener(signal)
    else:
        raise ValueError('filtertype: %s is unknown, available are: \ lowpass, highpass, and notch' % filtertype)

    if filtertype.lower() != 'wiener':
        filtered_data = filtfilt(b, a, signal)  # applies filter forward and backward to a signal

    # convert numpy array back to dataframe for plotting
    filtered_data = filtered_data.T
    filtered_df = pd.DataFrame(filtered_data, columns=['y'])
    return filtered_df

def denoise(data, sampling_rate, cutoffLow, cutoffHigh, cutoff, order=2):
    b, a = lowpass(sampling_rate, cutoffLow, order=order)
    c, d = highpass(sampling_rate, cutoffHigh, order=order)
    w0 = cutoff / (sampling_rate / 2)  # normalised cutoff is cutoff frequency divided by nyquist frequency
    Q = 30  # Q = w0/bandwidth where bandwidth=2
    e, f = iirnotch(w0, Q, sampling_rate)

    signal = data.to_numpy()  # convert column in dataframe to a numpy array
    signal = signal.T  # transpose numpy array into row vector

    filtered_data = filtfilt(b, a, signal)  # applies lowpass filter forward and backward to a signal
    filtered_data = filtfilt(c,d,filtered_data) # apply highpass filter
    filtered_data = filtfilt(e,f,filtered_data) # apply notch filter

    # convert numpy array back to dataframe for plotting
    filtered_data = filtered_data.T
    filtered_df = pd.DataFrame(filtered_data, columns=['y'])
    return filtered_df
