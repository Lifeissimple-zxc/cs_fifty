-- Transactions table needs indexes the most bc it will have many rows
CREATE INDEX IF NOT EXISTS idx_transaction_ts
ON transactions (transaction_ts);

CREATE INDEX IF NOT EXISTS idx_transaction_user
ON transactions (user_id);

CREATE UNIQUE INDEX IF NOT EXISTS idx_transaction_id
ON transactions (transaction_id);

-- For users, we only keep 1 idx for user ids
CREATE UNIQUE INDEX IF NOT EXISTS idx_user_id
ON users (id);
