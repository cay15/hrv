import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

name=input("Please enter the file name: ")
print("Hello "+name)
f=open(name)
df=pd.read_csv(f)

print(df.head())

xpoints=df[["'sample #'"]]
ypoints=df[["'MLII'"]]
zpoints=df[["'V5'"]]

df['Val_Diff']=df["'MLII'"] - df["'V5'"]
apoints=df[['Val_Diff']]

plt.figure(0)
plt.subplot(2, 1, 1)
plt.plot(xpoints/360, ypoints)
ax=plt.gca()
ax.axes.yaxis.set_ticks([]) 
plt.ylabel("MLII")
plt.title("ECG Larger Sample Time")

plt.subplot(2, 1, 2)
plt.plot(xpoints/360, zpoints)
plt.xlabel("Time/s")
ax=plt.gca()
ax.axes.yaxis.set_ticks([])
plt.ylabel("V5")
plt.show()

plt.figure(1)
plt.subplot(2,1,1)
plt.plot(xpoints[0:4000]/360, ypoints[0:4000])
ax=plt.gca()
ax.axes.yaxis.set_ticks([])
plt.ylabel("MLII")
plt.title("ECG Smaller Sample Time")

plt.subplot(2, 1, 2)
plt.plot(xpoints[0:4000]/360, zpoints[0:4000])
plt.xlabel("Time/s")
ax=plt.gca()
ax.axes.yaxis.set_ticks([])
plt.ylabel("V5")
plt.show()

#i=0
#while i<4000-1:
#	if (ypoints[i])==1180:
#		print(xpoints[i]/360)
#	i=i+1

#find the time when the smallest maximum peak is reached
#scan through the sample to see at what number sample that value occurs
#check whether it has occurred within 0.8 of a second so 0.8*360 samples, if it has exclude it no duplicates 
