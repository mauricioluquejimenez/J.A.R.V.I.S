CREATE TABLE IF NOT EXISTS registry (
    request_id TEXT PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    request_msg TEXT NOT NULL,
    response_msg TEXT NOT NULL
);

DROP TABLE registry
delete from registry

-- Si recreas la tabla o añades la columna:
ALTER TABLE registry ADD COLUMN success BOOLEAN;

BEGIN TRANSACTION;

-- 1. Crear la nueva tabla con el orden deseado
CREATE TABLE registry_new (
    request_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    request_msg TEXT,
    intent TEXT,
    params TEXT,
    response_msg TEXT,
    success BOOLEAN
);

-- 2. Copiar los datos existentes mapeándolos en el nuevo orden
INSERT INTO registry_new (request_id, timestamp, request_msg, response_msg, success)
SELECT request_id, timestamp, request_msg, response_msg, success
FROM registry;

-- 3. Eliminar la tabla antigua
DROP TABLE registry;

-- 4. Renombrar la nueva tabla con el nombre original
ALTER TABLE registry_new RENAME TO registry;

COMMIT;

select intent from registry