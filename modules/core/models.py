import uuid
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class Request(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user: Optional[str] = None
    msg: str
    source: str = "cli"
    metadata: Dict[str, Any] = Field(default_factory = dict)

class Response(BaseModel):
    request_id: str
    success: bool
    msg: str
    metadata: Dict[str, Any] = Field(default_factory=dict)