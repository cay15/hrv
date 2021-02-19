# Main file where individual .py files are combined and HRV analysis will be done
import pandas as pd
from filter import plot_data,filter
from fakeecg import whole_fakeecg

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

# Split signal into chunks
#create a new array containing first 'f_samp' samples of ecg1,ecg2 and time
ecg1 = np.array(whole_signal.ecg1[0:(f_samp+1)])
ecg2 = np.array(whole_signal.ecg2[0:(f_samp+1)])
time = np.array(whole_signal.t[0:(f_samp+1)])

# Interpolate
#combine each new ecg array with new time array into a dataframe for upsampling
split_signal = np.stack((time, ecg1,ecg2), axis = 1)
#convert split_signal into a DataFrame with column headers
split_signal = pd.DataFrame(split_signal, columns=column_names)

#set the time column as datetime index for upsampling
split_signal['t'] = pd.to_datetime(split_signal['t'], unit='s')
upsampled = split_signal.set_index('t').resample('1ms').mean()  #sampling rate 1000Hz

# Interpolate to fill in missing values in upsampled dataframe
interpolated = upsampled.interpolate(method='spline', order=2) #can also use method = 'cubic'

xVal = interpolated.ecg1
yVal = interpolated.ecg1

# Resample

# Output: 'feather'/'pickle' format?

## 2. CREATION OF ARTIFICIAL ECG

artificial_ecg, xtime = whole_fakeecg(120)

## 3. PRE-PROCESSING

plot_data(xVal,yVal,1000,'Original Signal') # plot original signal from ecgSample

# Baseline offset removal

# Baseline drift removal (high-pass filter)
filtered_signal = filter(yVal,128,0.5,2,'highpass')   # removes baseline drift
plot_data(xVal,filtered_signal,1000,'Highpass Filtered')

# Mains noise removal (notch filter)
filtered_signal = filter(filtered_signal,128,50,2,'notch')   # removes 50Hz mains noise (49-51Hz)
plot_data(xVal,filtered_signal,1000,'Notch Filtered')

# High-frequency noise removal (low-pass filter)
filtered_signal = filter(filtered_signal,128,100,2,'lowpass')    # removes components above 150Hz
plot_data(xVal,filtered_signal,1000,'Lowpass Filtered')

# consider: anomalous/atopic beats


## 4. R PEAK DETECTION

## 5. RR INTERVALS

## consider: frequency domain conversion