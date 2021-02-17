import pylab
import scipy.signal as signal
import numpy
import math
import random

def plotecg(x, ecg):
    pylab.plot(x/1000, ecg)
    pylab.xlabel('Time /s')
    pylab.ylabel('Amplitude')
    pylab.title('Heart ECG Template')
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
    
    i=0
    rest_array=numpy.random.randint(45, 70, size=(num_heart_beats))
    whole_ecg=[]
    while i<num_heart_beats:                            
        zero_array=numpy.zeros(rest_array[i], dtype=float)
        pqrst=numpy.concatenate([qrs, zero_array])
        newpqrst=signal.resample(pqrst, 1000)
        for x in newpqrst:
            whole_ecg.append(x)
        n=[0, 5, 10, 15, 20, 25, 30]
        b=numpy.random.choice(n)
        whole_ecg=whole_ecg[:len(whole_ecg)-b]
        i+=1
    
    whole_ecg=signal.resample(whole_ecg, 1000*num_heart_beats)
    """
    code i used previously and am not sure whether i might have to use again
    #samples_rest = 63 #must be 9/10 of the signal so =9*samples qrs
    #zero_array = numpy.zeros(samples_rest, dtype=float)#creates the rest section
    #pqrst_full = numpy.concatenate([qrs,zero_array]) #combines the rest section and qrs
    
    #newpqrst=signal.resample(pqrst_full, 1000)
    #xnew=numpy.linspace(0, 1, 1000, endpoint=False)

    #ecg_template = numpy.tile(newpqrst , num_heart_beats)#puts all the beats together
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

def fakeecg(samples)  #samples is time in seconds of fake ecg  
    ecg, x=fakeecg(samples)

    mainsecg=addnoise(ecg, samples, 50, 0.25) #adds mains noise of 50Hz
    basedriftecg=addnoise(mainsecg, samples, 0.3, 0.1) #adds baseline drift of 0.3Hz
    smallerdrift=addnoise(basedriftecg, samples, 0.01, 0.2) #adds lower frequency baseline drift of 0.01Hz
    noisedecg=randomnoise(basedriftecg)
    offset=addoffset(noisedecg, 0.5)

    plotecg(x, offset)
    return offset, x

fakeecg(60)