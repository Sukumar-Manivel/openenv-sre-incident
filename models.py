from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# --- Needed for Phase 2 (tasks.py / inference.py) ---
class Telemetry(BaseModel):
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    active_connections: int = 0
    
    class Config:
        extra = "allow"

class ServerState(BaseModel):
    id: str = ""
    name: str = ""
    status: str = ""
    recent_logs: List[str] = []
    telemetry: Optional[Telemetry] = None
    
    class Config:
        extra = "allow"

# --- Needed for Phase 1 (OpenEnv spec) ---
class Action(BaseModel):
    command: str

class Observation(BaseModel):
    # Changed these to 'Any' so they accept objects, dicts, or lists without crashing!
    servers: Any = []
    telemetry: Any = {}
    alert: Any = "No active alerts"
    objective: Any = "Diagnose incident"
    
    # Required OpenEnv tracking fields
    reward: float = 0.0
    done: bool = False
    info: Dict[str, Any] = {}
    
    class Config:
        extra = "allow"
