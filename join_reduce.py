#!/usr/bin/env python2.7

from itertools import groupby
from operator import itemgetter
import sys
from datetime import datetime
from math import *


#reader
def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

#discard trips with errors
def correctOutput(output_in):

    output = output_in

    #load pick up and drop off times
    timeDropOff=datetime.strptime(output[6],"%Y-%m-%d %H:%M:%S")
    timePickUp=datetime.strptime(output[1],"%Y-%m-%d %H:%M:%S")

    #recompute trip time in seconds from pick up and drop off times
    output[8] = str(abs((timeDropOff-timePickUp).seconds))

    #if GPS coordinate to 0: discard
    if (float(output[10]) == 0.0 or float(output[11]) == 0.0 or float(output[12]) == 0.0 or float(output[13]) == 0.0):
        None
    #if total earning minus tip negative: discard
    if (float(output[20]) - float(output[18]) < 0):
        None
    #if trip too short or too long or unrealistic speed: discard
    elif (float(output[8]) < 20 or float(output[8]) > 10000 or float(output[9])>40 or float(output[9])/float(output[8])>0.025):
        None
    #if no error, print to file
    else:
        print ",".join(output)


def main(separator='\t'):

    header = ["medallion","pickup_datetime","hack_license","vendor_id","rate_code","store_and_fwd_flag","dropoff_datetime","passenger_count","trip_time_in_secs","trip_distance","pickup_longitude","pickup_latitude","dropoff_longitude","dropoff_latitude","payment_type","fare_amount","surcharge","mta_tax","tip_amount","tolls_amount","total_amount"]
    print ",".join(header)

    data = read_mapper_output(sys.stdin, separator=separator)

    #read rows with the same key
    for key, group in groupby(data, itemgetter(0)):


        try:
            output=key.rstrip().split(",")
            data=None
            fare=None

            #read each row
            for key, value in group:

                elements=value.rstrip().split(",")

                #extract values for both trip and fare
                if len(elements)==12:
                    data=elements
                elif len(elements)==9:
                    fare=elements[2:]

            #if both rows extracted, feed key value to the check function which will output to file if no error
            if (data and fare):
                output = output + data + fare
                correctOutput(output)

        except:
            #exception
            pass




if __name__ == "__main__":
    main()
