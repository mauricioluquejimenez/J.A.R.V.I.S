from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from modules.core.db import get_connection
from modules.core.models import Request

class Intent(BaseModel):
    name: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    params: Dict[str, Any] = Field(default_factory=dict)

class Parser:
    def parse(self, request: Request) -> Intent:
        text = request.msg.strip().lower()

        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute("SELECT keyword, intent_id FROM keywords")
            keywords = cursor.fetchall()

        for keyword, intent_id in keywords:
            if keyword in text:
                params = {}

                if intent_id == "open_app":
                    app = text.replace(keyword, "").strip()
                    params = {"app": app}

                return Intent(name=intent_id, confidence=1.0, params=params)

        return Intent(name="unknown", confidence=0.0)

if __name__ == "__main__":
    parser = Parser()
    req = Request(msg="Abre Spotify")
    intent = parser.parse(req)
    print(f"Intención detectada: {intent.name} | Parámetros: {intent.params}")
