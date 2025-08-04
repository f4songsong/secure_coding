CREATE TABLE person_auth (
    token TEXT PRIMARY KEY,   
    person_id INTEGER NOT NULL,   
    expires_at DATETIME NOT NULL,   
    is_used INTEGER DEFAULT 0,   
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES person(person_id) ON DELETE CASCADE
);