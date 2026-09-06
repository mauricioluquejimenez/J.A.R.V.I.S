import sqlite3
import os

def limpiar_guids_inteligente(db_path="jarvis.db"):
    if not os.path.exists(db_path):
        current = os.getcwd()
        for _ in range(3):
            test_path = os.path.join(current, db_path)
            if os.path.exists(test_path):
                db_path = test_path
                break
            current = os.path.dirname(current)

    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    # Mostramos todos los registros de tipo guid actuales
    cursor.execute("SELECT id, name, path FROM apps WHERE exec_type = 'guid'")
    guids = cursor.fetchall()
    
    print(f"--- Encontrados {len(guids)} registros de tipo 'guid' ---")
    for app_id, name, path in guids:
        print(f"[{app_id}] {name} -> {path}")

    # Borrado automático de GUIDs que contengan rutas de ejecutables físicos con formato mixto
    cursor.execute("""
        DELETE FROM apps 
        WHERE exec_type = 'guid' 
        AND (path LIKE '%.exe%' OR path LIKE '%\\%')
    """)
    
    con.commit()
    print(f"\nSe han eliminado {cursor.rowcount} registros 'guid' con rutas mixtas o ejecutables.")
    con.close()

if __name__ == "__main__":
    limpiar_guids_inteligente()