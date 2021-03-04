import wfdb
from wfdb import processing
import os
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
#matplotlib inline
import scipy
import shutil
from IPython.display import display 
import keras
from keras import optimizers, losses, activations, models
from keras.layers import Dense, Input, Dropout, Convolution1D, MaxPool1D, GlobalMaxPool1D, GlobalAveragePooling1D, concatenate, MaxPool2D
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D


## GRAPH PLOTTING

# Display 1 record and its dictionary (from:100 - to:2100)
# for both variables record and ann, edit the file path to fit yours and follow it with the .dat file you want to plot e.g. the file I chose here is called "16265"
record = wfdb.rdrecord('/Users/choiwan/Desktop/MMGP/mit-bih-normal-sinus-rhythm-database-1.0.0/16265', sampfrom=100, sampto=7900)
ann = wfdb.rdann('/Users/choiwan/Desktop/MMGP/mit-bih-normal-sinus-rhythm-database-1.0.0/16265', 'dat', sampfrom=100, sampto=7900)
wfdb.plot_wfdb(record, ann)
display(record.__dict__)


## NEXT STEPS
# find R peaks and find RR intervals from that. links 3 and 4 may help


## DEBUGGING
#checks files are present
#import os
#for dirname, _, filenames in os.walk('/Users/choiwan/Desktop/MMGP/mit-bih-normal-sinus-rhythm-database-1.0.0'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))

# directory for dataset
#dir = '/Users/choiwan/Desktop/MMGP/mit-bih-normal-sinus-rhythm-database-1.0.0/'
#df1 = list()

# all the annotations from dataset
#for i in os.listdir(dir):
#    if i.endswith(".atr"):
#        df1.append(i)        

#df = pd.DataFrame(df1)
#df_1 = pd.read_csv("/Users/choiwan/Desktop/MMGP/mit-bih-normal-sinus-rhythm-database-1.0.0/RECORDS", header=None)
#df_1.head()
#print(df_1)
