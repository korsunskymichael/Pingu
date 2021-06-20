CREATE TABLE IF NOT EXISTS messages(
    message_id INTEGER PRIMARY KEY,
    message_sender VARCHAR(50) NOT NULL,
    message_receiver VARCHAR(50) NOT NULL,
    message_subject VARCHAR(50),
    message VARCHAR(250),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_message DEFAULT 0
);









