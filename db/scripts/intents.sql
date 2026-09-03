CREATE TABLE IF NOT EXISTS intents (
    id TEXT PRIMARY KEY,
    description TEXT NOT NULL
);

INSERT OR IGNORE INTO intents (id, description) VALUES
('open_app', 'Abrir aplicaciones del sistema'),
('get_weather', 'Consultar información del tiempo');