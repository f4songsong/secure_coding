CREATE TABLE detail (
    detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    block_type TEXT NOT NULL,           
    detail TEXT NOT NULL,             
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    started_at DATETIME,
    ended_at DATETIME,
    time_at INTEGER,
    FOREIGN KEY (record_id) REFERENCES record(record_id) ON DELETE CASCADE
);

