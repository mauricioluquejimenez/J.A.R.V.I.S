CREATE TABLE IF NOT EXISTS system_info (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	timestamp TIMESTAMP NOT NULL,
	platform TEXT,
	platform_release TEXT,
	processor TEXT,
	cpu_physical_cores INTEGER,
	cpu_logical_cores INTEGER,
	cpu_used REAL,
	cpu_freq REAL,
	cpu_temps TEXT,
	ram_percent REAL,
	ram_used_gb REAL,
	ram_total_gb REAL,
	disks TEXT,
	gpu TEXT,
	power_plugged BOOLEAN,
	battery_percent REAL
)

drop table system_info;

CREATE TABLE system_info_new (
    request_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    platform TEXT,
    platform_release TEXT,
    processor TEXT,
    cpu_physical_cores INTEGER,
    cpu_logical_cores INTEGER,
    cpu_used REAL,
    cpu_freq REAL,
    cpu_temps TEXT,
    ram_percent REAL,
    ram_used_gb REAL,
    ram_total_gb REAL,
    disks TEXT,
    gpu TEXT,
    power_plugged BOOLEAN,
    battery_percent REAL,
    FOREIGN KEY (request_id) REFERENCES registry(request_id) ON DELETE CASCADE
);

-- 2. Copiar los datos de la tabla antigua a la nueva.
-- NOTA: Si en la tabla antigua tenías registros huérfanos que no estaban en `registry`, 
-- SQLite fallará por la Foreign Key. Asegúrate de mapear un request_id que exista en registry,
-- o limpia los datos antiguos si eran de pruebas previas.
INSERT INTO system_info_new (
    request_id, timestamp, platform, platform_release, processor, 
    cpu_physical_cores, cpu_logical_cores, cpu_used, cpu_freq, cpu_temps, 
    ram_percent, ram_used_gb, ram_total_gb, disks, gpu, power_plugged, battery_percent
)
SELECT 
    -- Si tus registros antiguos no tienen request_id, puedes asignarles temporalmente 
    -- el request_id de alguna petición existente en registry, o borrarlos si son obsoletos.
    -- Ejemplo asumiendo que quieres migrar conservando el orden:
    (SELECT request_id FROM registry LIMIT 1), -- O un ID específico si puedes relacionarlos
    timestamp, platform, platform_release, processor, 
    cpu_physical_cores, cpu_logical_cores, cpu_used, cpu_freq, cpu_temps, 
    ram_percent, ram_used_gb, ram_total_gb, disks, gpu, power_plugged, battery_percent
FROM system_info;

-- 3. Eliminar la tabla antigua
DROP TABLE system_info;

-- 4. Renombrar la nueva tabla con el nombre original
ALTER TABLE system_info_new RENAME TO system_info;

COMMIT;

SELECT request_id, timestamp, cpu_used FROM system_info ORDER BY timestamp DESC LIMIT 3;

PRAGMA table_info(system_info);

INSERT INTO system_info (request_id, timestamp, platform, power_plugged, battery_percent) 
VALUES ('test-1', '2026-03-30 12:00:00', 'Windows', 1, 100.0);

delete from system_info where request_id is null