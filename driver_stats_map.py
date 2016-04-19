#!/usr/bin/env python2.7

import sys
from datetime import datetime


# input comes from STDIN (standard input)
for line in sys.stdin:
    if (line[0] == 'm'):
        continue

    line = line.strip()
    elems = line.split(",")

    # elems = ["medallion","pickup_datetime","hack_license","vendor_id","rate_code","store_and_fwd_flag","dropoff_datetime","passenger_count","trip_time_in_secs","trip_distance","pickup_longitude","pickup_latitude","dropoff_longitude","dropoff_latitude","payment_type","fare_amount","surcharge","mta_tax","tip_amount","tolls_amount","total_amount"]

    pickup_datetime = elems[1]
    hack_license = elems[2]
    dropoff_datetime = elems[6]
    passenger_count = elems[7]
    trip_time_in_secs = elems[8]
    trip_distance = elems[9]
    amount = str(float(elems[20]) - float(elems[18]))

    date = datetime.strptime(pickup_datetime,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    year = datetime.strptime(pickup_datetime,"%Y-%m-%d %H:%M:%S").strftime("%Y")

    key = [hack_license, year]
    value = [pickup_datetime,dropoff_datetime,passenger_count,trip_time_in_secs,trip_distance,amount]
  
    print(",".join(key) + '\t' + ",".join(value))
