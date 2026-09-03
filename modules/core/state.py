from enum import Enum

class State(str, Enum):
    IDLE = "idle"
    WAITING = "waiting"
    PROCESSING = "processing"
    ERROR = "error"