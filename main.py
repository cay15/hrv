# Main file where individual .py files are combined and HRV analysis will be done
import pandas as pd
from filter import plot_data,filter

## 1. INPUT RAW ECG

# Import ECG (.csv), get fs
column_names = [    #create a table with 3 columns depending on .csv file
    't',
    'ecg1',
    'ecg2',
    ]

#read the .csv file into a dataframe using pandas and skip the first 2 rows
whole_signal = pd.read_csv('arrhythmiaECGsample.csv', sep=',',
                           names = column_names, skiprows = 2)
xVal = whole_signal.t
yVal = whole_signal.ecg1

# Split signal into chunks

# Interpolate

# Resample

# Output: 'feather'/'pickle' format?


## 2. PRE-PROCESSING
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


## 3. R PEAK DETECTION

## 4. RR INTERVALS

## consider: frequency domain conversion