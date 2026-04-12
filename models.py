from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ServerState(BaseModel):
    name: str = "unknown"
    status: str = "unknown"
    recent_logs: List[str] = Field(default_factory=list)

class Telemetry(BaseModel):
    cpu_usage: float = 0.5
    memory_usage: float = 0.5
    active_connections: int = 0

class Observation(BaseModel):
    servers: List[ServerState] = Field(default_factory=list)
    telemetry: Telemetry = Field(default_factory=Telemetry)
    alert: str = "none"
    objective: str = "none"
    # STRICT ENFORCEMENT: Default is 0.15. Must be > 0.0 and < 1.0
    reward: float = Field(default=0.15, gt=0.0, lt=1.0) 
    done: bool = False
    info: Dict[str, Any] = Field(default_factory=dict)

class Action(BaseModel):
    action_type: str = "done"
    target_service: Optional[str] = "none"
    reasoning: Optional[str] = "none"
