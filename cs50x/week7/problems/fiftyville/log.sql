-- Keep a log of any SQL queries you execute as you solve the mystery.
-- This query was used to pull descriptions of the crime scenes of the day in question
WITH
crime_descs AS (
SELECT
    id, "description"
FROM crime_scene_reports
WHERE
    "month" = 7
    AND "day" = 28
    AND "year" = 2021
    AND street = 'Humphrey Street'
),

/*
| 295 | - id of our crime scene
Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
This tells about the time of when the event happend. We also know there were interviews, makes sense to check interviews table?
*/
-- This is the query to pull inteviews for the day in question
interviews AS
SELECT id, name, transcript
FROM interviews
WHERE
    "month" = 7
    AND "day" = 28
    AND "year" = 2021
ORDER BY id ASC;
/*
| 158 | Jose    | “Ah,” said he, “I forgot that I had not seen you for some weeks. It is a little souvenir from the King of Bohemia in return for my assistance in the case of the Irene Adler papers.”                                                                                                                               |
| 159 | Eugene  | “I suppose,” said Holmes, “that when Mr. Windibank came back from France he was very annoyed at your having gone to the ball.”                                                                                                                                                                                      |
| 160 | Barbara | “You had my note?” he asked with a deep harsh voice and a strongly marked German accent. “I told you that I would call.” He looked from one to the other of us, as if uncertain which to address.                                                                                                                   |
| 161 | Ruth    | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
| 162 | Eugene  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
| 163 | Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
| 191 | Lily    | Our neighboring courthouse has a very annoying rooster that crows loudly at 6am every day. My sons Robert and Patrick took the rooster to a city far, far away, so it may never bother us again. My sons have successfully arrived in Paris.

Ruth: we can look at security logs near the time when the event happened (10:15 am crime time +- 10 min) to find cars that left the place
Eugene: thief took out money on legget street 28 July in the morning
Raymond: thief made a call, less than a minute, planned to leave the town next day first flight. thief's collocutor must have purchased the ticket
*/
-- This query is to pull data from bakery security logs
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
/* These are the crime-like licence plates
+-----+----------+---------------+------+--------+
| id  | activity | license_plate | hour | minute |
+-----+----------+---------------+------+--------+
| 260 | exit     | 5P2BI95       | 10   | 16     |
| 261 | exit     | 94KL13X       | 10   | 18     |
| 262 | exit     | 6P58WS2       | 10   | 18     |
| 263 | exit     | 4328GD8       | 10   | 19     |
| 264 | exit     | G412CB7       | 10   | 20     |
| 265 | exit     | L93JTIZ       | 10   | 21     |
| 266 | exit     | 322W7JE       | 10   | 23     |
| 267 | exit     | 0NTHK55       | 10   | 23     |
+-----+----------+---------------+------+--------+
*/
-- With this query we check who took out money on legget street 28 July in the morning (before 10:15 am)
SELECT
    id,
    account_number,
    transaction_type,
    amount
FROM atm_transactions
WHERE
    "month" = 7
    AND "day" = 28
    AND "year" = 2021
    AND LOWER(atm_location) LIKE '%leggett street%'
    AND transaction_type = 'withdraw'
ORDER BY id ASC
/*
Amoung these should be criminals bank account
+-----+----------------+------------------+--------+
| id  | account_number | transaction_type | amount |
+-----+----------------+------------------+--------+
| 246 | 28500762       | withdraw         | 48     |
| 264 | 28296815       | withdraw         | 20     |
| 266 | 76054385       | withdraw         | 60     |
| 267 | 49610011       | withdraw         | 50     |
| 269 | 16153065       | withdraw         | 80     |
| 288 | 25506511       | withdraw         | 20     |
| 313 | 81061156       | withdraw         | 30     |
| 336 | 26013199       | withdraw         | 35     |
+-----+----------------+------------------+--------+
*/
-- With this query we try to identify who had a call less than a minute on July 28 after the time of the crime 10:15
SELECT
    id, caller, receiver, duration
FROM phone_calls
WHERE
    "month" = 7
    AND "day" = 28
    AND "year" = 2021
    -- assuming duration is in seconds
    AND duration < 60
/*
Here we have potential numbers of the criminal and her / his partner
+-----+----------------+----------------+----------+
| id  |     caller     |    receiver    | duration |
+-----+----------------+----------------+----------+
| 221 | (130) 555-0289 | (996) 555-8899 | 51       |
| 224 | (499) 555-9472 | (892) 555-8872 | 36       |
| 233 | (367) 555-5533 | (375) 555-8161 | 45       |
| 251 | (499) 555-9472 | (717) 555-1342 | 50       |
| 254 | (286) 555-6063 | (676) 555-6554 | 43       |
| 255 | (770) 555-1861 | (725) 555-3243 | 49       |
| 261 | (031) 555-6622 | (910) 555-3251 | 38       |
| 279 | (826) 555-1652 | (066) 555-9701 | 55       |
| 281 | (338) 555-6650 | (704) 555-2131 | 54       |
+-----+----------------+----------------+----------+
*/
-- With this query we try to shortlist the flight that the criminal might have used, should be the first flight out of fiftyville on July 29 2021
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
/*
Flight's id in 36
+----+-------+-----+------+--------+-------------+---------------+
| id | month | day | hour | minute | origin_city |   dest_city   |
+----+-------+-----+------+--------+-------------+---------------+
| 36 | 7     | 29  | 8    | 20     | Fiftyville  | New York City |
+----+-------+-----+------+--------+-------------+---------------+
*/
-- With this SQL I am trying to see the passengers of this flight
SELECT * FROM passengers WHERE flight_id = 36;
/*
+-----------+-----------------+------+
| flight_id | passport_number | seat |
+-----------+-----------------+------+
| 36        | 7214083635      | 2A   |
| 36        | 1695452385      | 3B   |
| 36        | 5773159633      | 4A   |
| 36        | 1540955065      | 5C   |
| 36        | 8294398571      | 6C   |
| 36        | 1988161715      | 6D   |
| 36        | 9878712108      | 7A   |
| 36        | 8496433585      | 7B   |
+-----------+-----------------+------+
*/
-- With this query I am trying to create a list of suspects based on my findings above
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
/*
This returns
+-------+
| name  |
+-------+
| Bruce |
+-------+
*/
-- With bruce as our suspect, we can slightly revamp calls query to understand who helped him buy tickets
SELECT
    id, caller, receiver, duration, callers.name AS caller_name, receivers.name AS receiver_name
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