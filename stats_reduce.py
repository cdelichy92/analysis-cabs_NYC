#!/usr/bin/env python2.7

from itertools import groupby
from operator import itemgetter
import sys
from datetime import datetime
from math import *

R=3959

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator='\t'):


    header = ["date", "hour", "drivers_onduty", "drivers_occupied", "t_onduty", "t_occupied", "n_pass", "n_trip", "n_mile", "earnings"]
    print ",".join(header)

    data = read_mapper_output(sys.stdin, separator=separator)

    for current_word, group in groupby(data, itemgetter(0)):
        try:

            drivers_onduty=0
            drivers_occupied=0
            t_onduty=0
            t_occupied=0
            n_pass=0
            n_trip=0
            n_mile=0
            earnings=0

            for current_word, count in group:
                # elements = [hack, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings]
                elements=count.rstrip().split(",")
                if (float(elements[1])>0.01666666666):
                    drivers_onduty+=1
                if (float(elements[2])>0.01666666666):
                    drivers_occupied+=1
                t_onduty+=float(elements[1])
                t_occupied+=float(elements[2])
                n_pass+=int(elements[3])
                n_trip+=int(elements[4])
                n_mile+=float(elements[5])
                earnings+=float(elements[6])

            output=current_word.rstrip().split(",")+[drivers_onduty,drivers_occupied,t_onduty,t_occupied,n_pass,n_trip,n_mile,earnings]
            print ",".join([str(x) for x in output])


        except ValueError:
            # count was not a number, so silently discard this item
            pass




if __name__ == "__main__":
    main()
