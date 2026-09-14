import sqlite3
import subprocess
import platform
import os
from difflib import get_close_matches

class Launcher:
    def __init__(self, db_path="jarvis.db"):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.db_path = os.path.join(base_dir, db_path)

    def get_app(self, command, cutoff=0.5):
        current_os = platform.system().lower()
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()

        query = """
            SELECT path, exec_type, name FROM apps 
            WHERE (LOWER(alias) = LOWER(?) OR LOWER(name) = LOWER(?)
               OR LOWER(alias) LIKE LOWER(?) OR LOWER(name) LIKE LOWER(?)) 
              AND LOWER(os) = ?
            ORDER BY 
                CASE 
                    WHEN LOWER(alias) = LOWER(?) THEN 1
                    WHEN LOWER(name) = LOWER(?) THEN 2
                    WHEN LOWER(name) LIKE LOWER(?) THEN 3
                    ELSE 4 
                END
        """
        
        exact_cmd = command.strip()
        starts_with_cmd = f"{command}%"
        like_cmd = f"%{command}%"
        
        cursor.execute(query, (
            exact_cmd, exact_cmd, like_cmd, like_cmd, current_os, 
            exact_cmd, exact_cmd, starts_with_cmd
        ))
        apps = cursor.fetchall()

        if not apps:
            cursor.execute("SELECT path, exec_type, name, alias FROM apps WHERE LOWER(os) = ?", (current_os,))
            fuzzy_apps = cursor.fetchall()

            dic = {}
            for path, exec_type, name, alias in fuzzy_apps:
                dic[name.lower()] = (path, exec_type, name)
                if alias:
                    dic[alias.lower()] = (path, exec_type, name)

            matches = get_close_matches(exact_cmd.lower(), dic.keys(), n=3, cutoff=cutoff)
            apps = [dic[m] for m in matches]

        con.close()
        return apps

    def run(self, command):
        apps = self.get_app(command)
        current_os = platform.system().lower()

        if not apps:
            return f"No se encontró ninguna aplicación para '{command}' en {current_os}."

        errores = []

        for path, exec_type, name in apps:
            try:
                if current_os == "windows":
                    if exec_type == 'path':
                        working_dir = os.path.dirname(path)
                        subprocess.Popen([path], cwd=working_dir, shell=True)
                    elif exec_type == 'guid':
                        if "\\" in path and not path.startswith("C:"):
                            raise Exception("Formato GUID/ruta no compatible directamente")
                        subprocess.Popen([path], shell=True)
                    elif exec_type == 'uwp':
                        subprocess.Popen(f"explorer.exe shell:AppsFolder\\{path.replace('AppFolder: ', '')}", shell=True)
                    elif exec_type == 'appid':
                        subprocess.Popen(f"explorer.exe shell:AppsFolder\\{path}", shell=True)
                    elif exec_type == 'uri':
                        import webbrowser
                        webbrowser.open(path)
                    else:
                        continue

                elif current_os == 'linux':
                    if exec_type == 'uri':
                        import webbrowser
                        webbrowser.open(path)
                    else:
                        subprocess.Popen([path], shell=True)

                return f"Abriendo {name} ({exec_type})..."
            except Exception as e:
                errores.append(f"{exec_type}: {str(e)}")
                continue
            
        return f"Error al intentar abrir '{command}'. Fallaron todos los métodos registrados: {'; '.join(errores)}"

def run(params):
    app_name = params.get("app", "") if isinstance(params, dict) else str(params)
    return Launcher().run(app_name)
        