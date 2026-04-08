from pydantic import BaseModel
from typing import List, Optional, Literal

class Telemetry(BaseModel):
    cpu_usage: float
    memory_usage: float
    active_connections: int

class ServerState(BaseModel):
    name: str
    status: Literal["Online", "Offline", "Error", "High_Latency"]
    recent_logs: List[str]

class Observation(BaseModel):
    servers: List[ServerState]
    telemetry: Telemetry
    active_alert: Optional[str] = None
    last_error: Optional[str] = None

class Action(BaseModel):
    action_type: Literal["view_logs", "view_telemetry", "restart_service", "rollback_deployment", "done"]
    target_service: Optional[str] = None

class Reward(BaseModel):
    value: float
    reason: str
