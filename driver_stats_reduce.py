#!/usr/bin/env python2.7

from itertools import groupby
from operator import itemgetter
import sys
from datetime import datetime, timedelta
from math import *



def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)


def main(separator='\t'):


    header = ["date", "hour", "hack", "t_onduty", "t_occupied", "n_pass", "n_trip", "n_mile", "earnings"]
    print ",".join(header)

    data = read_mapper_output(sys.stdin, separator=separator)

    for current_driver, group in groupby(data, itemgetter(0)):

        try:

            group = sorted(group)

            # Get keys
            hack_license, year = current_driver.rstrip().split(",")           

            # Variables to store data between hours
            current_hour = None
            current_date = None
            previous_dropoff = None
            previous_pickup = None
            output= None
            remaining = [0,0,0,None]

            for current_driver, infos in group:

                # elements = [pickup_datetime,dropoff_datetime,passenger_count,trip_time_in_secs,trip_distance,total_amount]
                elements=infos.rstrip().split(",")

                pickup_date = datetime.strptime(elements[0],"%Y-%m-%d %H:%M:%S")
                dropoff_date = datetime.strptime(elements[1],"%Y-%m-%d %H:%M:%S")
                passenger_count = int(elements[2])
                trip_time_in_secs = float(elements[3])
                trip_distance = float(elements[4])
                total_amount = float(elements[5])

                date_pickup = pickup_date.strftime("%Y-%m-%d")
                hour_pickup = pickup_date.strftime("%H")
                total_seconds_pickup = int(pickup_date.strftime("%M"))*60+int(pickup_date.strftime("%S"))

                # We want to know how much time has passed since last drive: break or not break.
                minutes_since_last_drive = 0.0
                if (previous_dropoff):
                    minutes_since_last_drive = float(abs((pickup_date-previous_dropoff).seconds)) / 60.0


                if (date_pickup==current_date and hour_pickup==current_hour):

                    # New line has same date and hour

                    # For t_onduty
                    if (minutes_since_last_drive < 30.0 and output):
                        # The time between two drives is not a break: we add that to t_onduty
                        output[3]+=(minutes_since_last_drive/60.0)


                else:

                    # New line has new hour

                    # For t_onduty: complete time of previous hour
                    t_onduty_for_previous_hour = 0.0
                    # For t_onduty: complete time of current hour
                    t_onduty_for_current_hour = 0.0

                    if (minutes_since_last_drive < 30.0 and output):

                        # This is not a break: we need to update t_onduty

                        t_onduty_for_previous_hour = max((float(minutes_since_last_drive)-float(pickup_date.strftime("%M")))/60.0,0)

                        if (remaining[0]==0):
                            t_onduty_for_current_hour = (float(pickup_date.strftime("%M")))/60.0
                        else:
                            t_onduty_for_current_hour = (float(minutes_since_last_drive))/60.0

                    # We print output from previous line
                    if output:
                        if (previous_pickup):
                            previous_data_time_plus_one = previous_pickup + timedelta(hours=1)
                            # We add "t_onduty_for_previous_hour" only if the last drive finish at the previous hour. 
                            # For example if we have a drive from 3:30 to 4:50 and then a new one at 5:10, "t_onduty_for_previous_hour" should be added to 4:00, not 3:00
                            if (previous_data_time_plus_one.strftime("%Y-%m-%d")==current_date and previous_data_time_plus_one.strftime("%H")==current_hour):
                                output[3]+=t_onduty_for_previous_hour
                        if output[3]<1.05:
                            print ",".join([str(x) for x in output])

                    current_date=date_pickup 
                    current_hour=hour_pickup

                    if (remaining[0]==0):
                        # We start from fresh
                        output = [current_date, current_hour, hack_license, t_onduty_for_current_hour, 0, 0, 0, 0, 0]

                    else:

                        # We need to take care of remaining time, miles and earnings coming from previous hour
                        the_date = remaining[3]
                        the_date = the_date + timedelta(hours=1)

                        while (remaining[0]>1):

                            # The previous ride last more than 1h: hours in bewteen have to be covered

                            miles_for_hour =  remaining[1] / remaining[0]
                            money_for_hour =  remaining[2] / remaining[0]
            
                            print ",".join([str(x) for x in [the_date.strftime("%Y-%m-%d"),the_date.strftime("%H"),hack_license,1,1,0,0,miles_for_hour,money_for_hour]])
         
                            remaining[0]-=1
                            remaining[1]-=miles_for_hour
                            remaining[2]-=money_for_hour

                            the_date = the_date + timedelta(hours=1)

                        # We are now with a remaining time less than 1h

                        if (the_date.strftime("%Y-%m-%d")==current_date and the_date.strftime("%H")==current_hour):
                            # Remaining time adds up to current hour
                            output = [current_date, current_hour, hack_license, remaining[0]+t_onduty_for_current_hour, remaining[0], 0, 0, remaining[1], remaining[2]]
                        else:
                            # Remaining time is before current hour, so we print and current output starts from scratch
                            # Taking previous example (drive from 3:30 to 4:50 and then a new one at 5:10): we create a 4:00 category and then start from scratch for 5:00
                            if remaining[0]<1.05:
                                print ",".join([str(x) for x in [the_date.strftime("%Y-%m-%d"), the_date.strftime("%H"), hack_license, remaining[0]+t_onduty_for_previous_hour, remaining[0], 0, 0, remaining[1], remaining[2]]])
                            output = [current_date, current_hour, hack_license, t_onduty_for_current_hour, 0, 0, 0, 0, 0]

                # n_pass
                output[5]+=passenger_count
                # n_trip
                output[6]+=1

                if ((total_seconds_pickup+trip_time_in_secs)<3600):

                    # "Within same hour"

                    # t_onduty
                    output[3]+=(trip_time_in_secs/3600)
                    # t_occupied
                    output[4]+=(trip_time_in_secs/3600)
                    
                    #n_mile
                    output[7]+=trip_distance
                    #earnings
                    output[8]+=total_amount

                    remaining = [0,0,0,None]


                else:

                    # "Going over next hour"

                    ratio = float((3600-total_seconds_pickup))/float(trip_time_in_secs)

                    # t_onduty
                    output[3]+=(trip_time_in_secs/3600) * ratio
                    # t_occupied
                    output[4]+=(trip_time_in_secs/3600) * ratio
                    
                    #n_mile
                    output[7]+=trip_distance * ratio
                    #earnings
                    output[8]+=total_amount * ratio

                    remaining = [(trip_time_in_secs/3600)* (1-ratio),trip_distance* (1-ratio),total_amount* (1-ratio),pickup_date] 

                previous_pickup = pickup_date
                previous_dropoff = dropoff_date

            print ",".join([str(x) for x in output])

        except:
            # count was not a number, so silently discard this item
            pass




if __name__ == "__main__":
    main()

