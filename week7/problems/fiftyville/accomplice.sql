SELECT
    phone_calls.id,
    caller,
    receiver,
    duration,
    callers.name AS caller_name,
    receivers.name AS receiver_name
FROM phone_calls
INNER JOIN people AS callers
    ON caller = callers.phone_number
INNER JOIN people AS receivers
    ON receiver = receivers.phone_number
WHERE
    "month" = 7
    AND "day" = 28
    AND "year" = 2021
    -- assuming duration is in seconds
    AND duration < 60
    AND callers.name = 'Bruce';
/*
This gives us Robin as accomplice
+-----+----------------+----------------+----------+-------------+---------------+
| id  |     caller     |    receiver    | duration | caller_name | receiver_name |
+-----+----------------+----------------+----------+-------------+---------------+
| 233 | (367) 555-5533 | (375) 555-8161 | 45       | Bruce       | Robin         |
+-----+----------------+----------------+----------+-------------+---------------+
*/