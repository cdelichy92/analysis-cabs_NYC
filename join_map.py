#!/usr/bin/env python2.7

import sys

#define lengths
len_fare = 11
len_data = 14

# input comes from STDIN (standard input)
for line in sys.stdin:
    if (line[0] == 'm'):
        continue

    line = line.strip()
    elems = line.split(",")

    #if line from fare data
    if (len(elems) == len_fare):
        #create key
        key = [elems[0], elems[3]]

        #create value
        value = [elems[1], elems[2]]
        for i in range(4,len_fare):
            value.append(elems[i])

    #if line from trip data
    if (len(elems) == len_data):
        #create key
        key = [elems[0], elems[5]]

        #create value
        value = [elems[1], elems[2],elems[3], elems[4]]
        for i in range(6,len_data):
            value.append(elems[i])

    #print output key (cvs) value (csv) in a tsv file
    print(",".join(key) + '\t' + ",".join(value))
