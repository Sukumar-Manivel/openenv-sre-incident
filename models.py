from pydantic import BaseModel
from typing import List, Dict, Any

# --- Needed for Phase 2 (tasks.py / inference.py) ---
class Telemetry(BaseModel):
    cpu_usage: float
    memory_usage: float
    active_connections: int

class ServerState(BaseModel):
    id: str
    status: str
    telemetry: Telemetry

# --- Needed for Phase 1 (OpenEnv spec) ---
class Action(BaseModel):
    command: str

class Observation(BaseModel):
    servers: List[Any] = []
    telemetry: Dict[str, Any] = {"cpu_usage": 0.0, "memory_usage": 0.0, "active_connections": 0}
    alert: str = "No active alerts"
    objective: str = "Diagnose incident"
    
    reward: float = 0.0
    done: bool = False
    info: Dict[str, Any] = {}
