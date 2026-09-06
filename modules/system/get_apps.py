import os
from pathlib import Path

def escanear_y_guardar_todas_las_apps(output_filename="apps.txt"):
    directorios_a_escanear = [
        Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")),
        Path(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")),
        Path(os.environ.get("LOCALAPPDATA", "")),
        Path(os.environ.get("APPDATA", ""))
    ]
    
    palabras_excluidas = ["uninstall", "update", "installer", "helper", "crash", "service", "setup"]
    aplicaciones_encontradas = []

    for base_path in directorios_a_escanear:
        if not base_path.exists():
            continue
        
        try:
            for item in base_path.iterdir():
                if item.is_dir():
                    try:
                        # Buscar todos los .exe recursivamente o en primer nivel
                        todos_los_exe = list(item.glob("*.exe")) + list(item.glob("*/*.exe"))
                        
                        # Filtrar ejecutables excluyendo los que contengan palabras prohibidas
                        exes_validos = [
                            e for e in todos_los_exe 
                            if not any(exc in e.name.lower() for exc in palabras_excluidas)
                        ]
                        
                        if exes_validos:
                            app_name = item.name
                            # Intentar buscar un .exe que coincida con el nombre de la carpeta
                            exe_path = next((e for e in exes_validos if e.stem.lower() in app_name.lower()), exes_validos[0])
                            aplicaciones_encontradas.append((app_name, str(exe_path)))
                    except PermissionError:
                        continue
        except PermissionError:
            continue

    output_path = Path(output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"{'DisplayName':<45} | {'Path'}\n")
        f.write("-" * 110 + "\n")
        for name, path in sorted(set(aplicaciones_encontradas)):
            f.write(f"{name:<45} | {path}\n")

    print(f"Exportación limpia completada en: '{output_path.resolve()}'")

if __name__ == "__main__":
    escanear_y_guardar_todas_las_apps()