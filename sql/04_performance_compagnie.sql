SELECT
    f.carrier,
    al.name AS compagnia,
    COUNT(*) AS voli,
    ROUND(AVG(f.arr_delay), 2) AS ritardo_medio_arrivo_min,
    ROUND(100.0 * SUM(CASE WHEN f.arr_delay > 15 THEN 1 ELSE 0 END) / COUNT(*), 2) AS perc_voli_in_ritardo
FROM flights f
JOIN airlines al ON al.carrier = f.carrier
WHERE f.arr_delay IS NOT NULL
GROUP BY f.carrier, al.name
ORDER BY ritardo_medio_arrivo_min ASC;