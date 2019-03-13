#!/usr/bin/env python

import numpy as np
import pandas as pd
from itertools import combinations
import fileinput
import os
import sys

##FIRST DELETE TEMP FILES TO AVOID CONFLICT
os.system("rm /../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/temp1.csv")
os.system("rm /../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/temp2.txt")
os.system("rm /../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/pairfile.txt")

#HERE READ THE SEGREGATION FILE AND DROP STOP CODON
cvrtbl = pd.read_csv("segr1mb_chr19_mm9.csv")  ##location of the segregation file .csv format **make auto
#for header
cvrtbl2 = pd.read_csv("segr1mb_chr19_mm9.csv" , header= None , low_memory=False) **make auto



colendcol = cvrtbl.iloc[[0],[0,1,2]]
colendcol.columns.values[2] = "X"
cvrtbl2 = cvrtbl2.drop ([2], axis = 1) ##remove stop column

q = len (cvrtbl2.columns) ##column length
p = len (cvrtbl)          ##row length

##NOW I HAVE CVR TABLE WITHOUT STOP CODON AND ROW AND COLUMN LENGTHS
##chrom + start = chrom_start column

for i in range (0,p+1):
    a = cvrtbl2.iloc[i,0] 
    b = cvrtbl2.iloc[i,1] 
    #print (a)
    #print(b)
    c = a+':'+b
    t =cvrtbl2
    t.iloc[[i],[1]] = c
#print (t)

mycvr = pd.DataFrame(t)
mycvr.to_csv('/../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/temp1.csv' , index=False, header=False) ##here change this to not writing to a file

NPnames = mycvr.iloc [[0],2:q]


##NOW I HAVE TEMP1 FILE contains like chr1:10000 columns

mid = pd.read_csv("/../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/temp1.csv")

colendcol = mid.iloc[[0],[0,1,2]]
colendcol.columns.values[2] = "X"

## read col by col and take the 1 values name all row its header name

f = colendcol
for i in range (2,q):
     g = mid.iloc[:,[0,1,i]]
     z =cvrtbl2.iloc[0,i]
        
#change variable column (2 and 3) names as X and Y.
     g.columns.values[2] = "X"

#eliminate all lines with zeros for column X and take rest
     h = g.loc[g.X ==1]
     h.iloc[:,[0]] = z 
     df2 = pd.DataFrame (h)
     df1 = pd.DataFrame (f)
       
     result = pd.concat([df1,df2])
     f = result
    
cvrtospr = result.loc[result.X ==1]

  
myx =open("/../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/temp2.txt" , "a") ## SPRITE like file 
l = len (cvrtospr)

for i in range (0,l-1):
    if cvrtospr.iloc[i+1,0] == cvrtospr.iloc[i,0]:
        myx.write (cvrtospr.iloc[i,1])
        myx.write ("\t")
    else :
        myx.write (cvrtospr.iloc[i,1])
        myx.write ("\t")
        myx.write("\n")

myx.write(cvrtospr.iloc[l-1,1])
myx.close()

##MOW I HAVE temp2.txt FILE. NEXT STEP IS CONVERT THIS FILE TO PAIR FILE.

os.system("/../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/rm temp1.csv")

##then we convert SPRITE to PAIR file to make it ready to cool

myx =open("/../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/pairfile.txt" , "a")  ##PAIR FILE
filepath = "/../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/temp2.txt"  
with open(filepath) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       coords = [coord for coord in line.strip().split("\t")] 
       pairs = (combinations(coords, 2))
       line = fp.readline()
       score = 1.0 #/ len(coords)

       for a, b in pairs:
            a = a.replace(':', "\t")
            b = b.replace(':', "\t")
            myx.write(a)
            myx.write ("\t")
            myx.write(b)
            myx.write ("\t")
            myx.write("%.7f" %score)
            myx.write ("\n")

       cnt += 1

myx.close()

##converting the results to mcool
os.system("rm /../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/temp2.txt")
os.system("cooler cload pairs -c1 1 -p1 2 -c2 3 -p2 4 --zero-based --chunksize 10000000 --field count=5:dtype=float32 chrmm9.size:1000000 /../../n/scratch2/onur/MARCH/GEO1mbmm9/MARCH7/temp/pairfile.txt segr1mb_chr19_mm9.cool")
os.system("cooler balance 1mb_mm9_woSc.cool")
os.system("cooler zoomify --balance 1mb_mm9_woSc.cool")

