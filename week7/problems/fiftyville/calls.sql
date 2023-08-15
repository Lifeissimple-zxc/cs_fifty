SELECT
    id, caller, receiver, duration
FROM phone_calls
WHERE
    "month" = 7
    AND "day" = 28
    AND "year" = 2021
    -- assuming duration is in seconds
    AND duration < 60