CREATE OR REPLACE TABLE `data-with-darshil.uber_data_engineering_yt.tbl_analytics` AS (
SELECT 
f.trip_id,
f.VendorID,
d.tpep_pickup_datetime,
d.tpep_dropoff_datetime,
p.passenger_count,
t.trip_distance,
r.rate_code_name,
pick.pickup_latitude,
pick.pickup_longitude,
drop.dropoff_latitude,
drop.dropoff_longitude,
pay.payment_type_name,
f.fare_amount,
f.extra,
f.mta_tax,
f.tip_amount,
f.tolls_amount,
f.improvement_surcharge,
f.total_amount
FROM 

`data-with-darshil.uber_data_engineering_yt.fact_table` f
JOIN `data-with-darshil.uber_data_engineering_yt.datetime_dim` d  ON f.datetime_id=d.datetime_id
JOIN `data-with-darshil.uber_data_engineering_yt.passenger_count_dim` p  ON p.passenger_count_id=f.passenger_count_id  
JOIN `data-with-darshil.uber_data_engineering_yt.trip_distance_dim` t  ON t.trip_distance_id=f.trip_distance_id  
JOIN `data-with-darshil.uber_data_engineering_yt.rate_code_dim` r ON r.rate_code_id=f.rate_code_id  
JOIN `data-with-darshil.uber_data_engineering_yt.pickup_location_dim` pick ON pick.pickup_location_id=f.pickup_location_id
JOIN `data-with-darshil.uber_data_engineering_yt.dropoff_location_dim` drop ON drop.dropoff_location_id=f.dropoff_location_id
JOIN `data-with-darshil.uber_data_engineering_yt.payment_type_dim` pay ON pay.payment_type_id=f.payment_type_id)
;

-- find top 10 pickup locations based on number of trips
select pickup_location_name, count(1) as total_trips 
from `xenon-timer-455106-t9.yellow_taxi_data.tbl_analytics` 
group by pickup_location_name
order by 2 desc;

-- avg fair amount by hour of the day
select  EXTRACT(HOUR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%S', tpep_pickup_datetime)) as hour_of_day, avg(fare_amount) as avg_fare_amount
from `xenon-timer-455106-t9.yellow_taxi_data.tbl_analytics`  
group by 1
order by 2 asc;
