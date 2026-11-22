SELECT
    hour AS ora_programmata,
    COUNT(*) AS voli,
    ROUND(AVG(dep_delay), 2) AS ritardo_medio_partenza_min,
    ROUND(100.0 * SUM(CASE WHEN dep_delay > 15 THEN 1 ELSE 0 END) / COUNT(*), 2) AS perc_partenze_in_ritardo
FROM flights
WHERE dep_delay IS NOT NULL
GROUP BY hour
ORDER BY hour;