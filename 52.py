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
plt.plot(xpoints/360, ypoints-1000)
plt.ylabel("Voltage Set 1")

plt.subplot(2, 1, 2)
plt.plot(xpoints/360, zpoints-1000)
plt.xlabel("Time/s")
plt.ylabel("Voltage Set 2")
plt.show()

plt.figure(1)
plt.subplot(2,1,1)
plt.plot(xpoints[0:4000]/360, ypoints[0:4000]-1000)
plt.ylabel("Voltage Set 1")

plt.subplot(2, 1, 2)
plt.plot(xpoints[0:4000]/360, zpoints[0:4000]-1000)
plt.xlabel("Time/s")
plt.ylabel("Voltage Set 2")
plt.show()

i=0
while i<4000-1:
	if (ypoints[i]-1000)==180:
		print(xpoints[i]/360)
	i=i+1
	
		
