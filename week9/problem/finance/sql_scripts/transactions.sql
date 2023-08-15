
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    transaction_ts INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    transaction_type INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares REAL NOT NULL,
    total_price REAL NOT NULL,
    -- FKEYS
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (transaction_type) REFERENCES transaction_types(type_id),
);

-- Alterations
ALTER TABLE transactions ADD COLUMN payment_method_id INTEGER;

ALTER TABLE transactions
ADD CONSTRAINT fk_transaction_payment
FOREIGN KEY (payment_method_id) REFERENCES payment_methods(payment_method_id);
