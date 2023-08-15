SELECT
    id,
    activity,
    license_plate,
    hour,minute
FROM bakery_security_logs
WHERE
    "month" = 7
    AND "day" = 28
    AND "year" = 2021
    AND "hour" = 10
    AND "minute" BETWEEN 15 AND 30
    AND activity = 'exit'
ORDER BY id
