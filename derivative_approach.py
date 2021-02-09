import pandas as pd

#df = pd.read_table("mit-bih-normal-sinus-rhythm-database-1.0.0/16265.dat",sep='delimiter',encoding='latin-1',engine='python')
#print(df)
#df1=df.head()
#print(df1)

df=pd.DataFrame(columns=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
a = [0 for x in range(35192816)]
#a_t = [0 for x in range(16)]
count=0

file = open("mit-bih-normal-sinus-rhythm-database-1.0.0/16265.dat", "rb")

byte = file.read(1)
#byte=int.from_bytes(byte, "little")
while byte: #byte=false at end of file
    print(byte)
    for i in range(len(a)):
        a[i]=byte
        #a_t[i]=str(type(byte))
        byte = file.read(1)
        #byte=int.from_bytes(byte,'little')
        #df.loc[count]=a
    #print("line "+str(count)+" aka "+str(hex(count)))
    #print(a_t)
    count+=1
df=a
file.close()
print(df)

pd.DataFrame(a).to_excel("16265_a.xlsx")