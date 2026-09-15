import re
from difflib import get_close_matches
from modules.core.db import get_connection
from modules.core.models import Request
from pydantic import BaseModel, Field
from typing import Any, Dict

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

        if text in keyword_map:
            return Intent(name=keyword_map[text], confidence=1.0, params={})

        phrase_match = get_close_matches(text, keyword_map.keys(), n=1, cutoff=0.8)
        if phrase_match:
            intent_id = keyword_map[phrase_match[0]]
            if intent_id in ("close_all", "minimize_all"):
                return Intent(name=intent_id, confidence=1.0, params={})

        for i, word in enumerate(words):
            matches = get_close_matches(word, keyword_map.keys(), n=1, cutoff=0.6)
            if matches:
                matched_keyword = matches[0]
                intent_id = keyword_map[matched_keyword]
                
                params = {}

                if intent_id in ("close_all", "minimize_all"):
                    params = {}

                elif intent_id in ("open_app", "close_app", "minimize_app", "maximize_app"):
                    raw_list = " ".join(words[i + 1:]).strip()
                    apps_list = [a.strip() for a in re.split(r'\s+y\s+|\s+e\s+|,', raw_list) if a.strip()]
                    params = {"apps": apps_list} if len(apps_list) > 1 else {"app": raw_list}               

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