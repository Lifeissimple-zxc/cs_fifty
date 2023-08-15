SELECT id, name, transcript
FROM interviews
WHERE
    "month" = 7
    AND "day" = 28
    AND "year" = 2021
ORDER BY id ASC
