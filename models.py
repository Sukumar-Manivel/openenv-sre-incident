from pydantic import BaseModel
from typing import List, Dict, Any

class Action(BaseModel):
    """
    Defines the action the agent can take.
    The grader will pass a command string here to try and fix the incident.
    """
    command: str

class Observation(BaseModel):
    """
    Defines the state of the environment at any given time.
    Includes the required reward, done, and info fields for the OpenEnv grader.
    """
    servers: List[Any] = []
    telemetry: Dict[str, Any] = {"cpu_usage": 0.0, "memory_usage": 0.0, "active_connections": 0}
    alert: str = "No active alerts"
    objective: str = "Diagnose incident"
    
    # Required by OpenEnv grader during the reset() check
    reward: float = 0.0
    done: bool = False
    info: Dict[str, Any] = {}
