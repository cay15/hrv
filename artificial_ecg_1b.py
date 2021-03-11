import pylab
import scipy.signal as signal
import numpy
import math
import random
import pandas as pd
import matplotlib.pyplot as plt
from filter_ecg_2 import plot_data,filter, denoise
from peak_detection_3 import mirror_ecg, diffs, get_r_peaks, get_rr, hrv
from input_ecg_1a import input_ecg

def plotecg(x, ecg, title):
    pylab.plot(x/1000, ecg)
    pylab.xlabel('Time /s')
    pylab.ylabel('Amplitude')
    pylab.title(title)
    pylab.show()
    
def fakeecg(nosamples):
    
    # Simulated Beats per minute rate
    bpm = 60 #for a reasonably healthy person, can be changed
    bps = bpm / 60
    
    capture_length = nosamples #time in seconds of ecg 

    num_heart_beats =int(capture_length*bps)
    
    #"Daubechies" wavelet approximates to pqrst
    qrs = signal.wavelets.daub(4) #gives it in 7 sample values
    # Add the gap after the pqrst when the heart is resting.
    #plot daubechies
    
    i=0
    rest_array=numpy.random.randint(50, 60, size=(num_heart_beats))


    whole_ecg=[]
    while i<num_heart_beats:                            
        zero_array=numpy.zeros(rest_array[i], dtype=float)
        pqrst=numpy.concatenate([qrs, zero_array])
        pqrst=pqrst*random.uniform(1.05, 0.95)
        for x in pqrst:
            whole_ecg.append(x)
        n=[0, 5, 10, 15, 20, 25, 30]
        b=numpy.random.choice(n)
        whole_ecg=whole_ecg[:len(whole_ecg)-b]
        i+=1

    whole_ecg=signal.resample(whole_ecg, 1000*num_heart_beats)


    """
    code i used previously and am not sure whether i might have to use again
    samples_rest = 63 #must be 9/10 of the signal so =9*samples qrs
    zero_array = numpy.zeros(samples_rest, dtype=float)#creates the rest section
    pqrst_full = numpy.concatenate([qrs,zero_array]) #combines the rest section and qrs
    
    newpqrst=signal.resample(pqrst_full, 1000)
    xnew=numpy.linspace(0, 1, 1000, endpoint=False)

    ecg_template = numpy.tile(newpqrst , num_heart_beats)#puts all the beats together
    """
    xarray=numpy.linspace(0, len(whole_ecg), num=len(whole_ecg))
    return whole_ecg, xarray

def randomnoise(ecg):
    randomnoise = numpy.random.normal(0, 0.1, len(ecg))
    noisyecg = randomnoise + ecg
    return noisyecg

def addnoise(ecg, samples, f, amp):  #f is noise frequency (hertz) 
    
    fs = 1000 #Sampling frequency
    dt = 1/fs #seconds per sample  
     
    t=numpy.arange(0, samples, dt)
    mains=numpy.sin(2*(math.pi)*f*t)
    sinwave=amp*mains
    noised=ecg+sinwave
    return noised

def addoffset(ecg, amp):
    delta=amp*random.random()
    offset_ecg = [x+delta for x in ecg]
    return offset_ecg

def whole_fakeecg(samples):  #samples is time in seconds of fake ecg
    ecg, x=fakeecg(samples)
    
    mainsecg=addnoise(ecg, samples, 50, 0.8) #adds mains noise of 50Hz
    
    basedriftecg=addnoise(mainsecg, samples, 0.3, 0.7) #adds baseline drift of 0.3Hz
    
    noisedecg=randomnoise(basedriftecg)
   
    highfreqnoise=addnoise(noisedecg, samples, 200, 0.7) #adds high frequency noise of 200Hz
    
    return highfreqnoise, x
