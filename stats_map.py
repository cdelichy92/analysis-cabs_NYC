#!/usr/bin/env python2.7

import sys


# input comes from STDIN (standard input)
for line in sys.stdin:
    if (line[0] == 'd'):
        continue

    line = line.strip()
    elems = line.split(",")

    key = [elems[0], elems[1]]
    value = elems[2:]

    print(",".join(key) + '\t' + ",".join(value))
