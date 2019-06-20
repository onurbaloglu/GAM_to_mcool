#!/bin/bash

CHROMSIZES=$1
OPREFIX=$2

zcat   \
    | python <(cat <<EOF
from itertools import combinations
import csv
import pandas as pd
import numpy as np
import re
x =[]
with open('$3', 'r' ) as d: ##need to write MCT file address as $3
        keeper = "keeper"
        for row in csv.reader(d ,dialect="excel-tab"):
            if row[0] != keeper:
                keeper = row[0]
                for each in combinations(x,2):
                    t = ':'.join(each)
                    y = t.split(':')
                    if y[0] == y[5]:
                        temp = int(y[4])*int(y[9])
                        print(y[0] , y[1] , y[5] , y[6], str(temp) ,sep='\t')
                x =[]
            if row[0] == keeper:
                x = np.append (x, [row[1]])
          
EOF
)  \
   | cooler cload pairs \
        -c1 1 -p1 2 -c2 3 -p2 4 \
        --zero-based --chunksize 10000000 --field count=5:dtype=float32 \
        $CHROMSIZES:25000 - "${OPREFIX}.cool"
