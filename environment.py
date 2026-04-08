from models import Action, Observation
from openenv.core.env_server import Environment

class SREIncidentEnv(Environment):
    
    def __init__(
        self, 
        initial_servers=None, 
        initial_telemetry=None, 
        objective="Diagnose incident", 
        alert="No active alerts", 
        root_cause_service="none", 
        required_action="none"
    ):
        super().__init__()
        
        self.initial_servers = initial_servers if initial_servers is not None else []
        self.initial_telemetry = initial_telemetry if initial_telemetry is not None else {"cpu_usage": 0.0, "memory_usage": 0.0, "active_connections": 0}
        
        self.objective = objective
        self.alert = alert
        self.root_cause_service = root_cause_service
        self.required_action = required_action
        
        self.current_step = 0
        self.max_steps = 15
        self.is_resolved = False

    def reset(self):
        self.current_step = 0
        self.is_resolved = False
        # The grader wants reward/done/info even on reset!
        return self.state(reward=0.0, done=False, info={"status": "Environment reset."})

    def state(self, reward=0.0, done=False, info=None):
        if info is None:
            info = {}
        # We now pass the reward, done, and info into the Observation
        return Observation(
            servers=self.initial_servers,
            telemetry=self.initial_telemetry,
            alert=self.alert,
            objective=self.objective,
            reward=reward,
            done=done,
            info=info
        )

    def step(self, action: Action):
        self.current_step += 1
        reward = 0.0
        done = False
        info = {}

        action_str = str(action).lower()
        
        if self.required_action != "none" and self.required_action.lower() in action_str:
            reward = 1.0  
            done = True
            self.is_resolved = True
            info["status"] = "Incident resolved successfully!"
        elif self.current_step >= self.max_steps:
            reward = 0.0
            done = True
            info["status"] = "Max steps reached."
        else:
            reward = 0.0
            done = False
            info["status"] = "Action executed. Issue persists."

        # Create the observation with the updated reward data
        obs = self.state(reward=reward, done=done, info=info)
        
        return obs, reward, done, info
