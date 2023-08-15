SELECT
    flights.id, "month", "day", "hour", "minute", origin_airports.city AS origin_city, dest_airports.city AS dest_city
FROM flights
INNER JOIN airports AS origin_airports
    ON flights.origin_airport_id = origin_airports.id
INNER JOIN airports AS dest_airports
    ON flights.destination_airport_id = dest_airports.id
WHERE
    "month" = 7
    AND "day" > 28
    AND "year" = 2021
    AND origin_airports.city = 'Fiftyville'
    AND dest_airports.city <> 'Fiftyville'
ORDER BY "day" ASC, "hour" ASC, "minute" ASC
LIMIT 1