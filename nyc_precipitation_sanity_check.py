#!/usr/bin/env python2.7

import sys
i=0

dic = {}

# input comes from STDIN (standard input)
for line in sys.stdin:
    if (line[0] == 'S'):
        continue

    line = line.strip()
    elems = line.split(",")

    precip = int(elems[3])
    hour = elems[2][9:]

    if (precip>2):

        if hour in dic:
            dic[hour] +=1
        else:
            dic[hour] = 1
        i=i+1

print 'Total points:',i
print dic
    
