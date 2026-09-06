import sqlite3
import os

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()
cursor.execute("SELECT id, name, path FROM apps WHERE exec_type = 'path'")
rows = cursor.fetchall()

inexistentes = 0
for app_id, name, path in rows:
    if not os.path.exists(path):
        print(f"[NO EXISTE] ID {app_id} - {name}: {path}")
        inexistentes += 1

print(f"\nVerificación terminada. Rutas no encontradas en disco: {inexistentes}")
con.close()