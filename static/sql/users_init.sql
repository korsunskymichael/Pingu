CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL,
    user_password VARCHAR(50) NOT NULL
);