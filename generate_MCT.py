def generateMCT (input_file , output_sorted , threshold_value):
    """
This code is for generating Multiple Contact Table from segregation or coverage tables which are generated by 
GAMtools process_nps tool. MCT is then used to generate cool files. Segregation files do not need to any modifications.
For using coverage table : Gamtool process_nps produce ".table" file and coverage table 1st row is written in one column 
so need to be seperated like segregation file (names not to be specific as original NPs but each column need to 
have different first row)

After reading segregation/coverage file for data; MCT is created. Segr/cov file is read for each NP. 
NPs are located at columns that is each column in segr/cov table is belong to an NP. 
Each row is for chromosome location with chromosome start and stop coordinates.
this binned location is taken and convert to MCT format --we use ':' instead of '\t' for size and 
next MCT to cool code--. Each row in MCT file has a format like "4DNFI11KCHDF.rmdup.bam	chr1:12050000:chr1:12075000:1". 
That is "NP name  chr_name:start:chr_name:stop". Finally MCT file is sorted by NP_names.
    """
    """
input_file: segregation or coverage file from gamtool process_nps. Need to be tab seperated .csv file
output_sorted: name of the output file which is sorted according to NPs.
threshold_value: Minimum value for difference of bin locations for generating MCT file.
    """
    
    import csv
    import fileinput
    import os
    
    with open(input_file) as h:
        row1 = csv.reader(h)
        NPnames = next(row1)
    h.close()
    
    #create empty table for MCT and read from segr/cov & generate sorted MCT table
    f =open(output_sorted , "a")
    with open(input_file, 'r' ) as d:
        reader = csv.reader(d)
        next(d)
        for row in reader:
            for i in range (3, len(NPnames)):
                if int(row[i]) >= threshold_value:
                    f.write (NPnames[i] + "\t" + row[0] + ":" + row[1] + ":" + row[0] + ":" + row[2] + ":" + row[i] + "\n")
    f.close()
    os.system("sort %s -o %s" %(output_sorted,output_sorted))
return
