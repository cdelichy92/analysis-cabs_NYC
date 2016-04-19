# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 17:30:05 2015

@author: Cyprien
"""

import sys
import re

for line in sys.stdin:
    line=line.strip()
    if line[0]=="m":
        print line
        if line=="medallion, hack_license, vendor_id, rate_code, store_and_fwd_flag, pickup_datetime, dropoff_datetime, passenger_count, trip_time_in_secs, trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude":
            index=5
        else:
            index=3
    else:
        groups=line.split(',')
        date=groups[index][:11]
        date = re.sub('[:-]', '', date)
        if date[:8]=='20130101':
            print line