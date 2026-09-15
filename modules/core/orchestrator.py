import datetime
import importlib
from modules.core.db import get_connection
from modules.core.models import Request, Response
from modules.core.parser import Parser
from modules.core.state import State
from modules.system.app_manager import AppManager
from modules.system.system_info import SystemInfo

class Orchestrator:
    def __init__(self):
        self.parser = Parser()
        self.state = State.IDLE

    def process_request(self, request: Request) -> Response:
        self.state = State.PROCESSING
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            intent = self.parser.parse(request)
            
            if intent.name == "unknown":
                self.state = State.IDLE
                response_msg = "No he entendido la orden, ¿me la repites?"
                self.registry(request.id, current_time, request.msg, response_msg, success=False, intent=intent.name, params=intent.params)
                return Response(
                    request_id=request.id,
                    success=False,
                    msg=response_msg,
                    metadata={"intent_detected": intent.name, "params": intent.params}
                )

            with get_connection() as con:
                cursor = con.cursor()
                cursor.execute(
                    "SELECT handler_module, handler_function FROM intents WHERE id = ?", 
                    (intent.name,)
                )
                row = cursor.fetchone()

            if not row:
                self.state = State.IDLE
                response_msg = f"No hay un manejador registrado para la intención: {intent.name}"
                self.registry(request.id, current_time, request.msg, response_msg, success=False, intent=intent.name, params=intent.params)
                return Response(
                    request_id=request.id,
                    success=False,
                    msg=response_msg,
                    metadata={"intent_detected": intent.name, "params": intent.params}
                )
                
            handler_module, handler_function = row
                
            module = importlib.import_module(handler_module)
            function = getattr(module, handler_function)

            self.registry(request.id, current_time, request.msg, "Procesando...", success=True, intent=intent.name, params=intent.params)
            
            try:
                result = function(intent.params, request_id=request.id)
            except TypeError:
                result = function(intent.params)

            self.state = State.IDLE
            response_msg = str(result)
            self.registry(request.id, current_time, request.msg, response_msg, success=True, intent=intent.name, params=intent.params)

            return Response(
                request_id=request.id, 
                success=True, 
                msg=response_msg, 
                metadata={"intent_detected": intent.name, "params": intent.params}
            )

        except Exception as e:
            self.state = State.ERROR
            error_msg = f"Error interno: {str(e)}"
            intent_name = getattr(intent, 'name', 'unknown') if 'intent' in locals() else 'unknown'
            intent_params = getattr(intent, 'params', {}) if 'intent' in locals() else {}
            
            self.registry(
                req_id=request.id, 
                timestamp=current_time, 
                req_msg=request.msg, 
                res_msg=error_msg, 
                success=False, 
                intent=intent_name, 
                params=intent_params
            )
            return Response(request_id=request.id, success=False, msg=error_msg)

    def registry(self, req_id: str, timestamp: str, req_msg: str, res_msg: str, success: bool, intent: str = None, params: dict = None):
        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute("""
                INSERT INTO registry (request_id, timestamp, request_msg, response_msg, success, intent, params)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(request_id) DO UPDATE SET
                    timestamp = excluded.timestamp,
                    request_msg = excluded.request_msg,
                    response_msg = excluded.response_msg,
                    success = excluded.success,
                    intent = excluded.intent,
                    params = excluded.params
            """, (
                req_id, 
                timestamp, 
                req_msg, 
                res_msg, 
                1 if success else 0, 
                intent, 
                str(params) if params else None
            ))
            con.commit()   

if __name__ == "__main__":
    orchestrator = Orchestrator()
    print("Bienvenido, señor. J.A.R.V.I.S. inicializado y a la espera...")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("Hasta pronto, señor...")
                break
                
            req = Request(msg=user_input)
            res = orchestrator.process_request(req)
            print(f"[{res.success}] Res: {res.msg} (Req ID: {res.request_id})")
            
        except KeyboardInterrupt:
            print("\nSistema interrumpido por el usuario.")
            break