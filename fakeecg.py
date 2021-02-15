import pylab
import scipy.signal as signal
import numpy
import math

def fakeecg(nosamples):
    #"Daubechies" wavelet approximates to pqrst
    qrs = signal.wavelets.daub(4) #gives it in 7 sample values
    # Add the gap after the pqrst when the heart is resting. 
    samples_rest = 63 #must be 9/10 of the signal so =9*samples qrs
    zero_array = numpy.zeros(samples_rest, dtype=float)#creates the rest section
    pqrst_full = numpy.concatenate([qrs,zero_array]) #combines the rest section and qrs

    # Simulated Beats per minute rate
    bpm = 60 #for a reasonably healthy person, can be changed
    bps = bpm / 60
    
    capture_length = nosamples #time in seconds of ecg 

    num_heart_beats =int(capture_length * bps)

    ecg_template = numpy.tile(pqrst_full , num_heart_beats)#puts all the beats together
    
    samplingrate=len(qrs)+samples_rest
    return ecg_template, samplingrate

def randomnoise(ecg):
    randomnoise = numpy.random.normal(0, 0.01, len(ecg))
    noisyecg = randomnoise + ecg
    return noisyecg

def addmains(ecg):
    t=numpy.arange(0, (len(ecg)/70), 1/70)
    f=50
    mains=numpy.sin(2*(math.pi)*f*t)
    mains=mains/10
    mainsecg=ecg+mains
    return mainsecg

def plotecg(ecg):
    pylab.plot(ecg)
    pylab.xlabel('Sample number')
    pylab.ylabel('Amplitude')
    pylab.title('Heart ECG Template')
    pylab.show()


samples=200  #time in seconds of fake ecg  
x, y=fakeecg(samples)               
mainsecg=addmains(x)
noisedecg=randomnoise(mainsecg)
plotecg(x[100:1000])
plotecg(mainsecg[100:1000])
plotecg(noisedecg[100:1000])

