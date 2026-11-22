# Misure e colonne DAX

Misure sulla tabella `fact_flights` (soglia di ritardo: 15 minuti).

```dax
Voli totali = COUNTROWS(fact_flights)
Voli con partenza registrata = COUNT(fact_flights[dep_delay])
Partenze in ritardo = CALCULATE(COUNTROWS(fact_flights), fact_flights[dep_delay] > 15)
Perc partenze in ritardo = DIVIDE([Partenze in ritardo], [Voli con partenza registrata])
Ritardo medio partenza = AVERAGE(fact_flights[dep_delay])
Ritardo mediano partenza = MEDIAN(fact_flights[dep_delay])
Voli con arrivo registrato = COUNT(fact_flights[arr_delay])
Perc arrivi in ritardo = DIVIDE(CALCULATE(COUNTROWS(fact_flights), fact_flights[arr_delay] > 15), [Voli con arrivo registrato])
```

Destinazioni (usano la relazione inattiva `fact_flights[dest]` → `dim_airports[airport_code]`):

```dax
Ritardo medio arrivo destinazione = CALCULATE(AVERAGE(fact_flights[arr_delay]), USERELATIONSHIP(fact_flights[dest], dim_airports[airport_code]))
Voli con arrivo per destinazione = CALCULATE(COUNT(fact_flights[arr_delay]), USERELATIONSHIP(fact_flights[dest], dim_airports[airport_code]))
Ritardo medio destinazione (min 1000 voli) = IF([Voli con arrivo per destinazione] >= 1000, [Ritardo medio arrivo destinazione])
```

Colonne calcolate e tabella calendario:

```dax
Pioggia = IF(ISBLANK(fact_flights[precip]), "Dato non disponibile", IF(fact_flights[precip] > 0, "Pioggia", "No pioggia"))
Fascia oraria = SWITCH(TRUE(), fact_flights[sched_hour] <= 11, "Mattina (5-11)", fact_flights[sched_hour] <= 16, "Pomeriggio (12-16)", "Sera (17-23)")
Classe visibilita = SWITCH(TRUE(), ISBLANK(fact_flights[visib]), "n.d.", fact_flights[visib] <= 1, "0-1 mi", fact_flights[visib] <= 3, "1-3 mi", fact_flights[visib] <= 6, "3-6 mi", "6-10 mi")
Calendario = CALENDAR(DATE(2013, 1, 1), DATE(2013, 12, 31))
```