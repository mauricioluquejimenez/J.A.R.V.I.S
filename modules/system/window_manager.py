import psutil
import subprocess
import sys

try:
    import pygetwindow as gw
except ImportError:
    gw = None

class WindowManager:
    def minimize_app(self, params: dict) -> str:
        app = params.get("app", "").strip().lower() if isinstance(params, dict) else str(params).strip().lower()
        if not app:
            return "No se ha encontrado ninguna aplicación para minimizar."

        if not gw:
            return "Módulo 'pygetwindow' no disponible."

        windows = [w for w in gw.getWindowsWithTitle('') if w.title.strip()]
        matches = [w for w in windows if app in w.title.lower()]

        if matches:
            matches[0].minimize()
            return f"Proceso '{matches[0].title}' minimzado."

        return f"Proceso '{app}' no encontrado."

    def minimize_all(self, params: dict = None) -> str:
        if sys.platform.startswith("win"):
            import ctypes
            ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0x44, 0, 0x0002, 0)
            ctypes.windll.user32.keybd_event(0x5B, 0, 0x0002, 0)
            return "Escritorio despejado."

        return "Opción no soportada para este sistema operativo."

    def maximize_app(self, params: dict) -> str:
        app = params.get("app", "").strip().lower() if isinstance(params, dict) else str(params).strip().lower()
        if not app:
            return "No se ha encontrado ninguna aplicación para maximizar."

        if not gw:
            "Módulo 'pygetwindow' no disponible."

        windows = [w for w in gw.getWindowsWithTitle('') if w.title.strip()]
        matches = [w for w in windows if app in w.title.lower()]

        if matches:
            win = matches[0]
            if win.isMinimized:
                win.restore()
            win.maximize()
            win.activate()
            return f"Proceso '{win.title}' maximizado."

        return f"Proceso '{app}' no encontrado."

    def close_all(self, params: dict = None) -> str:
        if not gw:
            return "Módulo 'pygetwindow' no disponible."

        IGNORED_TITLES = ["Program Manager", "Start", "Barra de tareas", ""]

        windows = gw.getWindowsWithTitle('')
        count = 0
        for w in windows:
            title = w.title.strip()
            if title and w.visible and title not in IGNORED_TITLES:
                try:
                    w.close()
                    count += 1
                except Exception:
                    continue

        return f"Se han enviado órdenes de cierre a {count} ventanas activas."

wm = WindowManager()

def minimize_app(params: dict = None, **kwargs) ->  str:
    if isinstance(params, dict) and "apps" in params:
        res = [wm.minimize_app(app) for app in params["apps"]]
        return " | ".join(res)

    return wm.minimize_app(params)

def minimize_all(params: dict = None, **kwargs) -> str:
    return wm.minimize_all(params)

def maximize_app(params: dict = None, **kwargs) -> str:
    if isinstance(params, dict) and "apps" in params:
        res = [wm.maximize_app(app) for app in params["apps"]]
        return " | ".join(res)
        
    return wm.maximize_app(params)

def close_all(params: dict = None, **kwargs) -> str:
    return wm.close_all(params)