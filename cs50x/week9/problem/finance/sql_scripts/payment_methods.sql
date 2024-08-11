
CREATE TABLE IF NOT EXISTS payment_methods (
    payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    payment_method_key TEXT NOT NULL,
    paymment_method_name TEXT NOT NULL
);

INSERT INTO payment_methods(payment_method_key, paymment_method_name)
VALUES
    ('card', 'Bank Card'),
    ('apple_pay', 'Apple Pay'),
    ('bank_transfer', 'Bank Transfer'),
    ('ideal', 'IDEAL')
    ('account_balance', 'Account Balance')
;