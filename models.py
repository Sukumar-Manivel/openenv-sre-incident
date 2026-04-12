from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# --- Needed for Phase 2 (tasks.py / inference.py) ---
class Telemetry(BaseModel):
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    active_connections: int = 0
    
    class Config:
        extra = "allow"  # Prevents crashes from unexpected fields

class ServerState(BaseModel):
    id: str = ""
    name: str = ""
    status: str = ""
    recent_logs: List[str] = []
    telemetry: Optional[Telemetry] = None
    
    class Config:
        extra = "allow"  # Prevents crashes from unexpected fields

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
    
    class Config:
        extra = "allow"
