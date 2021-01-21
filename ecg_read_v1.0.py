## LINKS

# 1. data obtained from https://www.kaggle.com/shymammoth/mitbih-normal-sinus-rhythm-database

# 2. code adapted from https://www.kaggle.com/khatri007/detection-of-congestive-heart-failure-using-ecg/notebook

# 3. documentation of wfdb functions: https://wfdb.readthedocs.io/en/latest/processing.html

# 4. possible method to finding RR intervals: https://pdf.sciencedirectassets.com/282073/1-s2.0-S2212017312X00057/1-s2.0-S2212017312004227/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEM3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDZD7gXzfItUde0x57lb8e4hwCFAO4w07Jef7pswHyzYgIhAPKV7jG%2BkRUO91gyOLA6IL1a8Z334sZSBtt2QbkMnNJpKr0DCKb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQAxoMMDU5MDAzNTQ2ODY1Igz0iHUKtivD5Eqt8CgqkQNNR83CSrDmJnkRL%2Bmpm8zWC5KDid%2Fm03rw0LC9F7nwsOLwzVJKAJ1kQVOBdFEuu58Gvw6QLzyxAX7zaKheOqKgvTEMNf8kKvy5Z3LC2ZMvjbxqWI6JAvqsY%2BGCOy3DzhcX9J391naSscSJAsgJRMU2ivnS%2BvMEw2K53Mnv%2BKIMmjMCZLnfvo4VQygwIRrOOLAKCXZsrZWCW2b9mqd%2BLLuSgNdMNLseIiUgZkSsrabh0PpHmQunSTI3iVUkgJcLCo6vXTLI5GFIcHxEhCrsMfljTLnYHdZWWrlViC%2FJmTlZpgiwswGiKLf0ZSG%2Flei1zJuo4JEkXmJzP%2FFTo3%2BClpntKiC2DhFn5jy3fT5xVyoeGKfy3gbwS34WTnxx%2BBwhznZYY8izGTGEqrDeomddhabbSwrN%2B0xRNAVw2navCZhESyiGY7F8Ajw7C3y3I%2BWulYu%2B%2BsuDqSodKXCPXpEl%2FmJktpXV0CiPUhWFNLvht7aBPElToIfUFk7cwNLvuXAerxiRgJ5JfD0fkmlKwGBe%2Fq4oWTC99KWABjrqAVe5SN1EBJqXQuWyIW6tSiYK51CRCiQBITrv75HVU4C0CkCqPHcuZr7S1NdUmjRKx802t%2FTHWVb2XHOFS7qqK9x9oacGu%2F7ecFOR38U6dRK9maJDJBZ8EbM2hISfJ4X50lpFufQizsPziAHrIzLGXcRbDzyF4tQ1fjWp7IQ5kHUdOGYteBHBWJmSyUlsYol0iyS1imAEWIx2IAtLpmVmIfTM6HfzQzFRBJMXwvhSFO1UUn2ItpMk9pKs3kYG9dQuixF6cKSAWk47rFEq2syutLL8AnqTeQRfbSdDGw7WCEtEBhlnQOQhzGNGcQ%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210121T143647Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTY2AUKZGHX%2F20210121%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=18ccb250a527c28184e779aeee224a7574bcd2159ba0b0d925d569a832fe9779&hash=8bd242e681dd25e592a6bb93d64eea4f1eb050ca36274ba92a88f94a50032ea2&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S2212017312004227&tid=spdf-d0b5c27d-09ab-455b-9b9c-ea45902949e1&sid=db26d9d5598691480088b9f6501e8b47adf6gxrqb&type=client


# BEFORE RUNNING CODE(!)

# Enter the following on terminal to import relevant packages:
# pip3 install wfdb
# pip3 install keras

# Download the database through link 1 (top),
# Unzip the download to get a folder called "mit-bih-normal-sinus-rhythm-database-1.0.0". It should contain lots of files including some ending with .dat
# Keep a note of the file path where you saved the folder in your local computer i.e. "[file paths]/mit-bih-normal-sinus-rhythm-database-1.0.0"

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