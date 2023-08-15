
CREATE TABLE IF NOT EXISTS transaction_types (
    type_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    type_name TEXT NOT NULL
);

INSERT INTO transaction_types(type_name) VALUES ('buy'), ('sell');