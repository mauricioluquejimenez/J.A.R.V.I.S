CREATE TABLE IF NOT EXISTS intents (
    id TEXT PRIMARY KEY,
    description TEXT NOT NULL
);

INSERT OR IGNORE INTO intents (id, description) VALUES
('open_app', 'Abrir aplicaciones del sistema'),
('get_weather', 'Consultar información del tiempo');

DROP TABLE IF EXISTS intents;

CREATE TABLE intents (
    id TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    handler_module TEXT NOT NULL,   -- Ej: 'modules.system.system_info' o 'modules.system.launcher'
    handler_function TEXT NOT NULL  -- Ej: 'write_to_db' o 'run'
);

INSERT INTO intents (id, description, handler_module, handler_function) VALUES 
('get_system_status', 'Consultar y registrar telemetría del equipo', 'modules.system.system_info', 'write_to_db'),
('open_app', 'Abrir aplicaciones del sistema', 'modules.system.launcher', 'run');

DELETE FROM intents WHERE id = 'get_system_status';

-- 2. Asegurar que get_system_info está configurada con su módulo y función
INSERT OR REPLACE INTO intents (id, description, handler_module, handler_function) 
VALUES ('get_system_info', 'Consultar telemetría y estado del sistema', 'modules.system.system_info', 'write_to_db');

-- 1. Crear una tabla temporal con la nueva estructura sin description
CREATE TABLE intents_new (
    id TEXT PRIMARY KEY,
    handler_module TEXT NOT NULL,
    handler_function TEXT NOT NULL
);

-- 2. Copiar los datos existentes omitiendo la columna description
INSERT INTO intents_new (id, handler_module, handler_function)
SELECT id, handler_module, handler_function FROM intents;

-- 3. Eliminar la tabla antigua
DROP TABLE intents;

-- 4. Renombrar la nueva tabla al nombre original
ALTER TABLE intents_new RENAME TO intents;

UPDATE intents SET handler_function = 'write_to_db' WHERE id = 'get_system_info';

SELECT id, handler_module, handler_function FROM intents WHERE id LIKE '%system%';

INSERT OR IGNORE INTO intents (id, handler_module, handler_function) VALUES
('close_app', 'modules.system.window_manager', 'close_app'),
('close_all', 'modules.system.window_manager', 'close_all'),
('minimize_app', 'modules.system.window_manager', 'minimize_app'),
('minimize_all', 'modules.system.window_manager', 'minimize_all');

-- 1. Actualizar open_app para apuntar a app_manager y a la función open_app
UPDATE intents 
SET handler_module = 'modules.system.app_manager',
    handler_function = 'open_app'
WHERE id = 'open_app';

-- 2. Asegurar que close_app apunte a app_manager y la función close_app
INSERT OR REPLACE INTO intents (id, handler_module, handler_function) 
VALUES ('close_app', 'modules.system.app_manager', 'close_app');

-- 3. Asegurar las intenciones de escritorio en window_manager
INSERT OR REPLACE INTO intents (id, handler_module, handler_function) VALUES
('close_all', 'modules.system.window_manager', 'close_all'),
('minimize_app', 'modules.system.window_manager', 'minimize_app'),
('minimize_all', 'modules.system.window_manager', 'minimize_all');

-- 1. Registrar la nueva intención en la tabla intents
INSERT OR IGNORE INTO intents (id, handler_module, handler_function) 
VALUES ('maximize_app', 'modules.system.window_manager', 'maximize_app');



