from pydantic import BaseModel, Field
from typing import Any, Dict
from difflib import get_close_matches
from modules.core.db import get_connection
from modules.core.models import Request

class Intent(BaseModel):
    name: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    params: Dict[str, Any] = Field(default_factory=dict)

class Parser:
    def parse(self, request: Request) -> Intent:
        text = request.msg.strip().lower()
        words = text.split()
        
        if not words:
            return Intent(name="unknown", confidence=0.0)

        with get_connection() as con:
            cursor = con.cursor()
            cursor.execute("SELECT keyword, intent_id FROM keywords")
            keywords_data = cursor.fetchall()

        keyword_map = {kw: intent_id for kw, intent_id in keywords_data}

        for i, word in enumerate(words):
            matches = get_close_matches(word, keyword_map.keys(), n=1, cutoff=0.6)
            if matches:
                matched_keyword = matches[0]
                intent_id = keyword_map[matched_keyword]
                
                params = {}
                if intent_id == "open_app":
                    app_words = words[i + 1:]
                    params = {"app": " ".join(app_words).strip()}

                elif intent_id == "get_system_info":
                    with get_connection() as con:
                        cursor = con.cursor()
                        cursor.execute("""
                            SELECT keyword, mapped_column 
                            FROM keywords 
                            WHERE intent_id = 'get_system_info' AND mapped_column IS NOT NULL
                        """)
                        mapping_data = cursor.fetchall()
                    
                    requested_metrics = []
                    for kw, col in mapping_data:
                        if kw in text:
                            if col not in requested_metrics:
                                requested_metrics.append(col)
                    
                    if not requested_metrics:
                        with get_connection() as con:
                            cursor = con.cursor()
                            cursor.execute("PRAGMA table_info(system_info)")
                            requested_metrics = [row[1] for row in cursor.fetchall() if row[1] not in ('request_id', 'timestamp')]
                    
                    params = {"metrics": requested_metrics}
                
                return Intent(name=intent_id, confidence=1.0, params=params)

        return Intent(name="unknown", confidence=0.0)