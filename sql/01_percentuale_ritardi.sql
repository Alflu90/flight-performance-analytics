SELECT
    COUNT(*) AS voli_totali,
    SUM(CASE WHEN arr_delay > 15 THEN 1 ELSE 0 END) AS voli_in_ritardo,
    ROUND(100.0 * SUM(CASE WHEN arr_delay > 15 THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentuale_ritardo
FROM flights
WHERE arr_delay IS NOT NULL;