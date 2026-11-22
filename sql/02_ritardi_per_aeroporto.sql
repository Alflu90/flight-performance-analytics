-- Ritardo alla partenza per aeroporto di origine
SELECT
    f.origin,
    a.name AS aeroporto,
    COUNT(*) AS voli,
    ROUND(AVG(f.dep_delay), 2) AS ritardo_medio_partenza_min
FROM flights f
JOIN airports a ON a.faa = f.origin
WHERE f.dep_delay IS NOT NULL
GROUP BY f.origin, a.name
ORDER BY ritardo_medio_partenza_min DESC;