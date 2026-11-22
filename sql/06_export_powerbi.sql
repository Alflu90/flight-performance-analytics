-- name: fact_flights
SELECT
    printf('%04d-%02d-%02d', f.year, f.month, f.day) AS flight_date,
    f.hour AS sched_hour,
    f.origin,
    f.dest,
    f.carrier,
    f.flight,
    f.tailnum,
    f.dep_delay,
    f.arr_delay,
    f.distance,
    f.air_time,
    w.temp,
    w.wind_speed,
    w.precip,
    w.visib
FROM flights f
LEFT JOIN weather w
    ON w.origin = f.origin
   AND w.year = f.year
   AND w.month = f.month
   AND w.day = f.day
   AND w.hour = f.hour;

-- name: dim_airlines
SELECT carrier, name AS carrier_name
FROM airlines;

-- name: dim_airports
SELECT faa AS airport_code, name AS airport_name, lat, lon
FROM airports
WHERE faa IN (SELECT origin FROM flights UNION SELECT dest FROM flights);