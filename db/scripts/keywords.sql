CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id TEXT NOT NULL,
    keyword TEXT NOT NULL UNIQUE,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
);

INSERT OR IGNORE INTO keywords (intent_id, keyword) VALUES
('open_app', 'abre'),
('open_app', 'lanza'),
('open_app', 'ejecuta'),
('open_app', 'inicia'),
('get_weather', 'tiempo'),
('get_weather', 'clima'),
('get_weather', 'temperatura')