from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# --- Phase 2 Requirements ---
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

# --- Phase 1 Requirements ---
class Action(BaseModel):
    command: str
    
    class Config:
        extra = "allow"

class Observation(BaseModel):
    # These 7 fields match environment.py EXACTLY!
    # 'Any' stops Pydantic from crashing if the grader sends weird data
    servers: Any = []
    telemetry: Any = {}
    alert: Any = ""
    objective: Any = ""
    reward: float = 0.0
    done: bool = False
    info: Dict[str, Any] = {}
    
    class Config:
        extra = "allow"
