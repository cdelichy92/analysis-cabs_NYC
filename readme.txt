Authors:
Cyprien de Lichy, Louis Eugene, Guillaume Rostaing

==========================================================================

List of files included:

- singledayjan.py
- join_map.py
- join_reduce.py
- driver_stats_map.py
- driver_stats_reduce.py
- stats_map.py
- stats_reduce.py
- step6.R
- step7.R
- nyc_precipitation_sanity_check.py

==========================================================================

-- File: singledayjan.py --

Python script that pulls out all the trip information for a single day.
In this case, 01/01/2013. The date of the day can be changed according to user’s needs.

-- File: join_map.py --

Our dataset is segmented into two parts: one that contains trip origination and destination details, and a second that contains fare information. This Python script is the map element of the join on those two datasets. The key is [medallion, pickup_datetime] and the value the remaining data. Each key appears twice in the output, once associated with information originating from the trip dataset, once from the fare datasets. Each row consists in a key value pair.

-- File: join_reduce.py --

Python script that reduces the output from join_map.py. Each pair of equal keys is joined (or merged) and the corresponding values are combined. Each row of the output consists in a key value pair, but this time the value is the information from both the trip and fare datasets. Trips with incorrect values are discarded. The errors we consider are: one of the GPS coordinates at 0, negative total earning after removing the tip, too short or too long trips (20 <= t <= 10000 seconds), trips of more than 40 miles, trips with an average speed of more than 0.025 miles per second.

-- File: driver_stats_map.py --

The output of our previous scripts contains the following information for each trip:
["medallion","pickup_datetime","hack_license","vendor_id","rate_code","store_and_fwd_flag","dropoff_datetime","passenger_count","trip_time_in_secs","trip_distance","pickup_longitude","pickup_latitude","dropoff_longitude","dropoff_latitude","payment_type","fare_amount","surcharge","mta_tax","tip_amount","tolls_amount","total_amount »].
The goal of this step is to compute a variety of statistics regarding supply, demand, and earnings, as described below:
-t_onduty: the total amount of time (in units of hours) that the driver is on-duty during the hour
-t_occupied: the total amount of time with passengers in the cab during the hour.
-n_pass: the total number of passengers picked up during the hour.
-n_trip: the total number of trips started during the hour.
-n_mile: the total number of miles traveled with passengers in the hour. 
-earnings: the total amount of money the driver earned in that hour (without tips).
Our Python script maps with the key [hack_license, year].

-- File: driver_stats_reduce.py --

Python script that reduces the output from driver_stats_map.py. To compute our statistics (t_onduty,t_occupied,n_pass,n_trip,n_mile,earnings as seen before), we group by driver for one year. n_pass and n_trip are straightforward. t_onduty,t_occupied,n_mile,earnings are on a trip base on the raw data but we need them on a hour base. To split those numbers, we assume the driver traveled at a constant speed for the duration of the trip. For t_onduty, we consider that a driver is off duty if a cab is unoccupied for at least 30 minutes.

-- File: stats_map.py --

The goal of this third MapReduce is to aggregate the quantities computed in previous step by date and hour. The schema of the output is thus:
[date, hour, drivers_onduty, drivers_occupied, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings]
where drivers_onduty is the number of drivers who were on duty for at least one minute during the hour, and drivers_occupied is the number of drivers who were occupied for at least one minute during the hour. 
Our Python script maps with the key [date, hour].

-- File: stats_reduce.py --

Python script that reduces the output from stats_map.py. t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings are the sums of the analogous ones in the previous step.

-- File: step6.R --

R script to join the output data from EMR (output of step 5) and the NYC precipitation data. The join is performed on the date and hour. A left join needs to be done because the precipitation data only contains the date, hour and precipitation values when it has rained, there is no entry in the precipitation data when it was not raining.

-- File: step7.R --

R script to perform the analysis using dplyr (for the data explroation and analysis) and ggplot (for the plots).

We performed 2 group by operations:
- First, we grouped by rain/no rain and by the hour of the day, then we used the summarise command in dplyr to plot some interesting statistics vs the hour of the day when it was raining and not raining. The results of the summarise operation are in the x dataframe.
- Then, we grouped by rain/no rain only (we aggregate the hours), we have less granularity and we can compute some more general statistics about the data, these interesting values are in the y dataframe.

-- File: nyc_precipitation_sanity_check.py --

Python script that checks how many datapoint are above a threshold in nyc_precipitation.csv. The goal is to analyse the statistical significance of our results for rain / no rain (estimate the variance of results based on number of datapoints).

==========================================================================
Date of Last Update: October 27, 2015 