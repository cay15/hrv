import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import signal
from filter_ecg_2 import plot_data

def input_ecg():
    filename = input("Enter your filename (including .csv): ")
    print("Loading", filename + "...")
    filepath = '../mit-bih-database/'+filename
    ## 1a. Input File
    #Import ECG (.csv)
    #create a table with 3 columns depending on .csv file
    column_names = [    #create a table with 3 columns depending on .csv file
        't',
        'ecg1',
        'ecg2',
        ]

    #read the .csv file into a dataframe using pandas and skip the first 2 rows
    whole_signal = pd.read_csv(filepath, sep=',',
                       names = column_names, skiprows = 2)

    #read the file header and access the sampling rate
    df=pd.read_csv(filepath, header=[0, 1]) #takes in the csv and tells the program that the first two lines are header
    header=df.columns #makes a list of header titles
    samplinginterval=header[0][1] #records the sampling interval but has sec on end
    numerical_sampleinterval=samplinginterval.replace(" sec", "") #removes sec so the interval is just a number
    numerical_sampleinterval=numerical_sampleinterval.replace("'", "") #removes "'" so str can be converted into float
    t_samp = float(numerical_sampleinterval)
    x=df[["'sample interval'"]]

    #get the sampling frequency of original signal
    f_samp = int(1/t_samp)
    # Plot the original signal
    plot_data(whole_signal.t, whole_signal.ecg1, 5*f_samp, f_samp, "Original ECG")
    
        
    while True: #choice to test simulation using artificial ECG or raw ECG
        d2=input("Do you want to: 1) Input ECG data for 1st lead in the file or 2) The 2nd lead? [1/2]: ")
        if d2 in ['1', '2']: #keeps asking if the user input isn't 1 or 2
             break
    if d2 == "1": 
        ecgchosen=whole_signal.ecg1
        
    elif d2 == "2": 
        ecgchosen=whole_signal.ecg2
             
    time = whole_signal.t
    Length = len(ecgchosen)
    resampledLength = math.floor(1000*Length/f_samp)

    #resampling signal to 1000Hz using scipy.signal.resample
    #note: this produces a tuple
    resampled_ecg = signal.resample(ecgchosen,resampledLength, t = time)
 
    #convert tuple to dataframe
    ecg1 = np.transpose(resampled_ecg[0])
    time = np.transpose(resampled_ecg[1])

    upsampled_sig = np.stack((time, ecg1), axis = 1)
    upsampled_sig = pd.DataFrame(upsampled_sig, columns = ['t', 'ECG'])

    return filename, ecg1, upsampled_sig.t, f_samp, resampledLength