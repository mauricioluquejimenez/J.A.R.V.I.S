from modules.core.models import Request, Response
from modules.core.parser import Parser
from modules.core.state import State

class Orchestrator:
    def __init__(self):
        self.parser = Parser()
        self.state = State.IDLE

    def process_request(self, request: Request) -> Response:
        self.state = State.PROCESSING

        try:
            intent = self.parser.parse(request)
            if intent.name == "open_app":
                app = intent.params.get("app", "desconocida")
                msg = f"Abriendo {app}..."
                success = True

            elif intent.name == "get_weather":
                msg = "Mostrando el tiempo..."
                success = True
            
            else:
                msg = "No he entendido la orden, ¿me la repites?"
                success = False

            self.state = State.IDLE

            return Response(request_id=request.id, success=success, msg=msg, metadata={"intent_detected": intent.name, "params": intent.params})

        except Exception as e:
            self.state = State.ERROR
            return Response(request_id=request.id, success=False, msg="Error interno procesando la solicitud")

if __name__ == "__main__":
    orchestrator = Orchestrator()
    
    # Prueba 1: Comando abrir
    req1 = Request(msg="Abre Spotify")
    res1 = orchestrator.process_request(req1)
    print(f"[{res1.success}] Res: {res1.msg} (Req ID: {res1.request_id})")

    req2 = Request(msg="Muéstrame el tiempo")
    res2 = orchestrator.process_request(req2)
    print(f"[{res2.success}] Res: {res2.msg} (Req ID: {res2.request_id})")

    # Prueba 2: Comando no reconocido
    req3 = Request(msg="Hazme un café")
    res3 = orchestrator.process_request(req3)
    print(f"[{res3.success}] Res: {res3.msg} (Req ID: {res3.request_id})")