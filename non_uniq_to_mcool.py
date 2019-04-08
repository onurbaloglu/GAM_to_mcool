#!/usr/bin/env python

import numpy as np
import pandas as pd
from itertools import combinations
import fileinput
import os
import sys


os.system("rm /../../n/scratch2/onur/APRIL/week1/coverage_cis_only.txt")
cvrtbl = pd.read_csv("/../../n/scratch2/onur/APRIL/week1/coveragetable.csv")  ##location of the segregation file .csv format
cvrtbl2 = pd.read_csv("/../../n/scratch2/onur/APRIL/week1/coveragetable.csv" , header= None , low_memory=False)
cvrtbl2 = cvrtbl2.drop ([2], axis = 1) ##remove stop column

q = len (cvrtbl2.columns) ##column length
p = len (cvrtbl)          ##row length
myx =open("/../../n/scratch2/onur/APRIL/week1/coverage_cis_only" , "a")

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


os.system("cooler cload pairs -c1 1 -p1 2 -c2 3 -p2 4 --zero-based --chunksize 10000000 --field count=5:dtype=float32 mm10.size:25000 /../../n/scratch2/onur/APRIL/week1/coverage_cis_only.txt /../../n/scratch2/onur/APRIL/week1/17542_overage_cis_only.cool")
os.system("cp /../../n/scratch2/onur/APRIL/week1/overage_cis_only.cool /../../n/scratch2/onur/APRIL/week1/unbalanced/")
os.system("cooler balance --cis-only /../../n/scratch2/onur/APRIL/week1/overage_cis_only.cool")
os.system("cooler zoomify --balance /../../n/scratch2/onur/APRIL/week1/overage_cis_only.cool -o /../../n/scratch2/onur/APRIL/week1/overage_cis_only.mcool")
