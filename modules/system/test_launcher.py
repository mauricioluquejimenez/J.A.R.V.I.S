from modules.system.launcher import Launcher

if __name__ == "__main__":
    launcher = Launcher()
    
    # Pruebas con nombres exactos, parciales y con pequeñas erratas (búsqueda difusa)
    pruebas = ["dbeaver", "notep", "audaci", "obs", "fooootball manager"]
    
    for test in pruebas:
        print(f"\n==============================")
        print(f"Probando comando: '{test}'")
        print(f"==============================")
        
        # Comprobamos qué apps encuentra get_app
        apps = launcher.get_app(test, cutoff=0.4)
        if apps:
            print(f"Aplicaciones localizadas ({len(apps)}):")
            for app in apps:
                print(f"  -> {app[2]} ({app[1]}): {app[0]}")
        else:
            print("  -> No se encontró ninguna coincidencia.")