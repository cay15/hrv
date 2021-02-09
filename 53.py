import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

#Code for data downloaded through physionet atm function in csv format

name=input("Please enter the file name: ")
f=open(name)
df=pd.read_csv(f, header=[0, 1])
print(df.head())

xpoints=df[["'Elapsed time'"]]
ypoints=df[["'ECG1'"]]
zpoints=df[["'ECG2'"]]

plt.figure(0)
plt.subplot(2, 1, 1)
plt.plot(xpoints, ypoints)
ax=plt.gca()
#ax.axes.yaxis.set_ticks([]) 
plt.ylabel("MLII /mV")
plt.title("ECG Larger Sample Time")

plt.subplot(2, 1, 2)
plt.plot(xpoints, zpoints)
plt.xlabel("Time/s")
ax=plt.gca()
#ax.axes.yaxis.set_ticks([])
plt.ylabel("V5 /mV")
plt.show()

plt.figure(1)
plt.subplot(2,1,1)
plt.plot(xpoints[0:1000], ypoints[0:1000])
ax=plt.gca()
#ax.axes.yaxis.set_ticks([])
plt.ylabel("MLII / mV")
plt.title("ECG Smaller Sample Time")

plt.subplot(2, 1, 2)
plt.plot(xpoints[0:1000], zpoints[0:1000])
plt.xlabel("Time/s")
ax=plt.gca()
#ax.axes.yaxis.set_ticks([])
plt.ylabel("V5 /mV")
plt.show()

#find the time when the smallest maximum peak is reached
#scan through the sample to see at what number sample that value occurs
#check whether it has occurred within 0.8 of a second so 0.8*360 samples, if it has exclude it no duplicates 
