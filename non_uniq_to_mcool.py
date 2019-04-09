#!/usr/bin/env python

import numpy as np
import pandas as pd
from itertools import combinations
import fileinput
import os
import sys
import os.path

for i in range (1,5):
    file_name = input ("enter the file location and name of the csv file:\n")
    if os.path.isfile(file_name):
        print ('your file name is: %s' %file_name)
        break
    else :
        print ("folder not found!! enter the folder name of the csv file again:\n  ")
        if i == 4:
            print('iteration exceeded!!! ')
            
for i in range (1,5):  
    size = input('enter the chrom size file name -.../...size-:\n')
    if os.path.isfile(file_name):
        print ('your size file name is: %s' %size)
        break
    else :
        print ("folder not found!! enter the chrom size file again:\n  ")
        if i == 4:
            print('iteration exceeded!!! ')
            
limit = int(input('enter the filtering limit:\n'))
print ("enter the name for the output file:\n")
out_name = str(input())

os.system("rm %s_pair.txt" %out_name)
cvrtbl = pd.read_csv("%s" %(file_name))  ##location of the segregation file .csv format
cvrtbl2 = pd.read_csv("%s" %(file_name) , header= None , low_memory=False)
cvrtbl2 = cvrtbl2.drop ([2], axis = 1) ##remove stop column

q = len (cvrtbl2.columns) ##column length
p = len (cvrtbl)          ##row length
myx =open("%s_pair.txt" %out_name , "a")

for i in range (3,q+1):
    g = cvrtbl.iloc[:,[0,1,i]]
    g.columns.values[2] = "X"
    h = g.loc[g.X >=21]   
    p = len(h)
    for j in range (0,p):
            for k in range (j,p):
                if h.iloc[j,0] == h.iloc[k,0]:
                    myx.write (h.iloc[j,0])
                    myx.write ("\t")
                    myx.write (str(h.iloc[j,1]))
                    myx.write ("\t")
                    myx.write (h.iloc[k,0])
                    myx.write ("\t")
                    myx.write (str(h.iloc[k,1]))
                    myx.write ("\t")
                    myx.write (str(h.iloc[j,2] * h.iloc[k,2]))
                    myx.write ("\n")
                else :
                    break


myx.close()


os.system("cooler cload pairs -c1 1 -p1 2 -c2 3 -p2 4 --zero-based --chunksize 10000000 --field count=5:dtype=float32 %s:50000 %s_pair.txt %s.cool" %(size, out_name,out_name))
os.system("cooler balance --cis-only %s.cool" %out_name)
os.system("cooler zoomify --balance %s.cool -o %s.mcool" %(out_name,out_name) )
