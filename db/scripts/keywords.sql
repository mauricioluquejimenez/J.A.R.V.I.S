CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id TEXT NOT NULL,
    keyword TEXT NOT NULL UNIQUE,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
);

BEGIN TRANSACTION;

CREATE TABLE keywords_new (
    intent_id TEXT NOT NULL,
    keyword TEXT NOT NULL,
    mapped_column TEXT,
    PRIMARY KEY (intent_id, keyword, mapped_column)
);

DROP TABLE IF EXISTS keywords;
ALTER TABLE keywords_new RENAME TO keywords;

COMMIT;

-- 1. Limpiamos todas las keywords actuales para reinsertarlas de forma estructurada
DELETE FROM keywords;

-- 2. Inserción de intenciones para abrir aplicaciones
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('open_app', 'abrir', NULL);
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('open_app', 'lanza', NULL);
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('open_app', 'ejecuta', NULL);
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('open_app', 'iniciar', NULL);

-- 3. Inserción de intenciones de información del sistema con sus columnas mapeadas correspondientes

-- Estado / General (muestra plataforma y release)
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'estado', 'platform');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'estado', 'platform_release');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'sistema', 'platform');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'sistema', 'platform_release');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'operativo', 'platform');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'operativo', 'platform_release');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'rendimiento', 'cpu_used');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'rendimiento', 'ram_percent');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'recursos', 'cpu_used');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'recursos', 'ram_percent');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'cpu', 'cpu_physical_cores');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'cpu', 'cpu_logical_cores');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'cpu', 'cpu_used');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'cpu', 'cpu_freq');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'cpu', 'cpu_temps');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'memoria', 'ram_percent');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'memoria', 'ram_used_gb');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'memoria', 'ram_total_gb');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'batería', 'power_plugged');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'batería', 'battery_percent');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'temperatura', 'cpu_temps');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'telemetría', 'cpu_used');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'telemetría', 'ram_percent');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'hardware', 'processor');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'hardware', 'cpu_physical_cores');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'procesador', 'processor');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'procesador', 'cpu_physical_cores');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'procesador', 'cpu_logical_cores');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'grafica', 'gpu');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'gpu', 'gpu');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'espacio', 'disks');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'disco', 'disks');
INSERT INTO keywords (intent_id, keyword, mapped_column) VALUES ('get_system_info', 'discos', 'disks');

UPDATE keywords SET mapped_column = NULL WHERE keyword IN ('estado', 'sistema', 'rendimiento', 'recursos', 'telemetría');

DELETE FROM keywords 
WHERE intent_id IN ('close_app', 'minimize_app', 'minimize_all', 'close_all');

INSERT OR IGNORE INTO keywords (intent_id, keyword, mapped_column) VALUES
('close_app', 'cerrar', NULL),
('close_app', 'terminar', NULL),
('close_app', 'matar', NULL),
('close_app', 'apagar', NULL),

('close_all', 'cerrar todo', NULL),
('close_all', 'cerrar todas', NULL),
('close_all', 'despejar escritorio', NULL),
('close_all', 'limpiar escritorio', NULL),

('minimize_app', 'minimizar', NULL),
('minimize_app', 'ocultar', NULL),

('minimize_all', 'minimizar todo', NULL),
('minimize_all', 'minimizar todas', NULL),
('minimize_all', 'ocultar todo', NULL);

INSERT OR REPLACE INTO keywords (intent_id, keyword, mapped_column) VALUES 
('maximize_app', 'maximiza', NULL),
('maximize_app', 'maximizar', NULL),
('maximize_app', 'agranda', NULL),
('maximize_app', 'agrandar', NULL);