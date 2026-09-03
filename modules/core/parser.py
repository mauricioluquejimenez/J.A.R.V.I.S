from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from modules.core.models import Request

class Intent(BaseModel):
    name: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    params: Dict[str, Any] = Field(default_factory=dict)

class Parser:
    def parse(self, request: Request):
        text = request.msg.strip().lower()

        if "abrir" in text or "abre" in text:
            app = text.replace("abrir", "").replace("abre", "").strip()
            return Intent(name="open_app", params={"app":app})

        elif "tiempo" in text or "clima" in text:
            return Intent(name="get_weather")

        return Intent(name="unknown", confidence=0.0)

if __name__ == "__main__":
    parser = Parser()
    req = Request(msg="Abre Spotify")
    intent = parser.parse(req)
    print(f"Intención detectada: {intent.name} | Parámetros: {intent.params}")
