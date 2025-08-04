CREATE TABLE like (
    like_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    record_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (person_id, record_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id) ON DELETE CASCADE,
    FOREIGN KEY (record_id) REFERENCES record(record_id) ON DELETE CASCADE
);
