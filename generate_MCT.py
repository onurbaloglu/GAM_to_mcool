def generateMCT (input_file , output_sorted , threshold_value):
    import csv
    import fileinput
    import os
    
    with open(input_file) as h:
        row1 = csv.reader(h)
        NPnames = next(row1)
    h.close()
    
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
