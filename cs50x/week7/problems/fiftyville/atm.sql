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