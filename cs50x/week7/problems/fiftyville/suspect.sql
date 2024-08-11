SELECT
    "name"
FROM people
WHERE
    -- Passengers of the first flight on July 29 out of town
    passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)
    AND phone_number IN (SELECT "caller" FROM phone_calls
                         WHERE
                            "month" = 7
                            AND "day" = 28
                            AND "year" = 2021
                            -- assuming duration is in seconds
                            AND duration < 60)
    AND license_plate IN (SELECT license_plate
                          FROM bakery_security_logs
                          WHERE
                            "month" = 7
                            AND "day" = 28
                            AND "year" = 2021
                            AND "hour" = 10
                            AND "minute" BETWEEN 15 AND 30
                            AND activity = 'exit')
    AND id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
                (SELECT account_number
                 FROM atm_transactions
                 WHERE
                    "month" = 7
                    AND "day" = 28
                    AND "year" = 2021
                    AND LOWER(atm_location) LIKE '%leggett street%'
                    AND transaction_type = 'withdraw'))