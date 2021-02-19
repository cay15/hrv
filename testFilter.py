# Main file where individual .py files are combined and HRV analysis will be done
import pandas as pd
from filter import plot_data,filter
from fakeecg import whole_fakeecg

'''
# Create noisy ecg
artificial_ecg, xtime=whole_fakeecg(120)

## artificial ecg is in numpy array format but filter functions take in ecg as dataframe
## So need to convert numpy array to dataframe
xVal = pd.DataFrame(xtime, columns=['x'])
artificial_ecg = pd.DataFrame(artificial_ecg, columns=['y'])
plot_data(xVal,artificial_ecg,10000,'Original Signal') # plot first 2.5s of original artificial ecg


# Baseline drift removal (high-pass filter)
filtered_signal = filter(artificial_ecg,1000,0.5,2,'highpass')   # removes baseline drift
plot_data(xVal,filtered_signal,10000,'Highpass Filtered')

# Mains noise removal (notch filter)
filtered_signal = filter(filtered_signal,1000,50,2,'notch')   # removes 50Hz mains noise (49-51Hz)
plot_data(xVal,filtered_signal,10000,'Notch Filtered')

# High-frequency noise removal (low-pass filter)
filtered_signal = filter(filtered_signal,1000,100,2,'lowpass')    # removes components above 150Hz
plot_data(xVal,filtered_signal,10000,'Lowpass Filtered')


# Import ECG (.csv), get fs
column_names = [    #create a table with 3 columns depending on .csv file
    't',
    'ecg1',
    'ecg2',
    ]
'''

#read the .csv file into a dataframe using pandas and skip the first 2 rows
whole_signal = pd.read_csv('MITBIH_Noise118e00.csv', sep=',',
                           names = column_names, skiprows = 2)
xVal = whole_signal.t
yVal = whole_signal.ecg1