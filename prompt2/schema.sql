CREATE TABLE IF NOT EXISTS code_files (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    filename        TEXT        NOT NULL,
    rel_path        TEXT        NOT NULL,
    abs_path        TEXT        NOT NULL UNIQUE,
    extension       TEXT,
    language        TEXT,
    author          TEXT,
    tags            TEXT,
    date_added      TEXT        NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    last_modified   TEXT,
    file_size_bytes INTEGER,
    checksum_sha256 TEXT,
    content         TEXT        NOT NULL
);

CREATE TABLE IF NOT EXISTS file_attributes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id     INTEGER NOT NULL REFERENCES code_files(id) ON DELETE CASCADE,
    attr_key    TEXT    NOT NULL,
    attr_value  TEXT,
    UNIQUE(file_id, attr_key)
);

CREATE INDEX IF NOT EXISTS idx_code_files_rel_path ON code_files(rel_path);
CREATE INDEX IF NOT EXISTS idx_code_files_language ON code_files(language);
CREATE INDEX IF NOT EXISTS idx_code_files_checksum ON code_files(checksum_sha256);
CREATE INDEX IF NOT EXISTS idx_file_attributes_key ON file_attributes(attr_key);

