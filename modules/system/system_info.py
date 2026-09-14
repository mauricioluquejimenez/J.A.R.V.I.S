import datetime
import platform
import psutil
import sqlite3
from modules.core.db import get_connection

try:
    import cpuinfo
except ImportError:
    cpuinfo = None

try:
    import GPUtil
except ImportError:
    GPUtil = None

class SystemInfo:
    @staticmethod
    def get_system_info() -> dict:
        cpu_name = "Unknown"
        if cpuinfo:
            info = cpuinfo.get_cpu_info()
            cpu_name = info.get('brand_raw', platform.processor())
        else:
            cpu_name = platform.processor()

        cpu_freq = psutil.cpu_freq()
        battery = psutil.sensors_battery()
        disks = []
        gpu_info = []

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "used_gb": round(usage.used / (1024**3), 2),
                    "total_gb": round(usage.total / (1024**3), 2),
                    "percent": usage.percent
                })
            except PermissionError: continue

        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    gpu_info.append({
                        "name": gpu.name,
                        "driver": getattr(gpu, 'driver', 'Desconocido'),
                        "load": round(gpu.load * 100, 1),
                        "temperature": gpu.temperature,
                        "mem_used": gpu.memoryUsed,
                        "mem_total": gpu.memoryTotal
                    })
            except Exception: pass

        cpu_temps = {}
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if entries:
                        cpu_temps[name] = entries[0].current

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "timestamp": timestamp,
            "platform": platform.system(),
            "platform_release": platform.release(),
            "processor": cpu_name,
            "cpu_physical_cores": psutil.cpu_count(logical=False),
            "cpu_logical_cores": psutil.cpu_count(logical=True),
            "cpu_used": psutil.cpu_percent(interval=0.5),
            "cpu_freq": round(cpu_freq.current, 2) if cpu_freq else None,
            "cpu_temps": str(cpu_temps),
            "ram_percent": psutil.virtual_memory().percent,
            "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "disks": str(disks),
            "gpu": str(gpu_info),
            "power_plugged": battery.power_plugged if battery else True,
            "battery_percent": battery.percent if battery else 100
        }

    @staticmethod
    def write_to_db(request_id: str = None, existing_con=None):
        data = SystemInfo.get_system_info()

        if existing_con:
            cursor = existing_con.cursor()

            values = (
                request_id,
                data["timestamp"], data["platform"], data["platform_release"], data["processor"],
                data["cpu_physical_cores"], data["cpu_logical_cores"], data["cpu_used"],
                data["cpu_freq"], data["cpu_temps"], data["ram_percent"], data["ram_used_gb"],
                data["ram_total_gb"], data["disks"], data["gpu"], 
                1 if data["power_plugged"] else 0, data["battery_percent"]
            )

            cursor.execute("""
                INSERT INTO system_info (
                    request_id, timestamp, platform, platform_release, processor, 
                    cpu_physical_cores, cpu_logical_cores, cpu_used, 
                    cpu_freq, cpu_temps, ram_percent, ram_used_gb, 
                    ram_total_gb, disks, gpu, power_plugged, battery_percent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, values)
            existing_con.commit()
            return "[INFO] Datos del sistema guardados correctamente en la base de datos."
        else:
            con = sqlite3.connect("jarvis.db")
            cursor = con.cursor()
            
            values = (
                request_id,
                data["timestamp"], data["platform"], data["platform_release"], data["processor"],
                data["cpu_physical_cores"], data["cpu_logical_cores"], data["cpu_used"],
                data["cpu_freq"], data["cpu_temps"], data["ram_percent"], data["ram_used_gb"],
                data["ram_total_gb"], data["disks"], data["gpu"], 
                1 if data["power_plugged"] else 0, data["battery_percent"]
            )

            cursor.execute("""
                INSERT INTO system_info (
                    request_id, timestamp, platform, platform_release, processor, 
                    cpu_physical_cores, cpu_logical_cores, cpu_used, 
                    cpu_freq, cpu_temps, ram_percent, ram_used_gb, 
                    ram_total_gb, disks, gpu, power_plugged, battery_percent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, values)
            
            con.commit()
            con.close()
            
            return "[INFO] Datos del sistema guardados correctamente en la base de datos."  

def write_to_db(params=None, request_id=None):
    # Aseguramos que se pasa el request_id correctamente a la clase
    SystemInfo.write_to_db(request_id=request_id)

    metrics = params.get("metrics", []) if isinstance(params, dict) else []
    if not metrics:
        return "[INFO] Datos del sistema guardados correctamente en la base de datos."

    with get_connection() as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        
        cursor.execute("PRAGMA table_info(system_info)")
        allowed_cols = {row[1] for row in cursor.fetchall()}
        
        safe_metrics = [m for m in metrics if m in allowed_cols]
        if not safe_metrics:
            return "[INFO] Datos del sistema guardados correctamente en la base de datos."

        cursor.execute(f"SELECT {', '.join(safe_metrics)} FROM system_info ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()

    if not row:
        return "No hay registros del sistema disponibles."

    results = [f"{key.replace('_', ' ').capitalize()}: {row[key]}" for key in safe_metrics]
    return " | ".join(results)