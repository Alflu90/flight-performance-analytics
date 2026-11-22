SELECT
    f.dest,
    COALESCE(a.name, f.dest) AS aeroporto,
    COUNT(*) AS voli,
    ROUND(AVG(f.arr_delay), 2) AS ritardo_medio_arrivo_min
FROM flights f
LEFT JOIN airports a ON a.faa = f.dest
WHERE f.arr_delay IS NOT NULL
GROUP BY f.dest, a.name
HAVING COUNT(*) >= 1000
ORDER BY ritardo_medio_arrivo_min DESC
LIMIT 10;