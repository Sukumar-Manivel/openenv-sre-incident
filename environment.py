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
        # Initialize the base Environment class to get close() and reset_async()
        super().__init__()
        
        # Safety fallbacks so the server doesn't crash when OpenEnv boots up
        self.initial_servers = initial_servers if initial_servers is not None else []
        self.initial_telemetry = initial_telemetry if initial_telemetry is not None else {"cpu_usage": 0.0, "memory_usage": 0.0, "active_connections": 0}
        
        self.objective = objective
        self.alert = alert
        self.root_cause_service = root_cause_service
        self.required_action = required_action
        
        # State tracking variables
        self.current_step = 0
        self.max_steps = 15
        self.is_resolved = False

    def reset(self):
        """
        Resets the environment for a new task.
        The Hackathon grader automatically calls this.
        """
        self.current_step = 0
        self.is_resolved = False
        return self.state()

    def state(self):
        """
        Returns the current state.
        IMPORTANT: Make sure these arguments (servers, telemetry, etc.) 
        match exactly what you defined in models.py!
        """
        return Observation(
            servers=self.initial_servers,
            telemetry=self.initial_telemetry,
            alert=self.alert,
            objective=self.objective
        )

    def step(self, action: Action):
        """
        Takes an action and returns (Observation, reward, done, info).
        """
        self.current_step += 1
        reward = 0.0
        done = False
        info = {}

        # Convert the action to a string to easily check if it matches the required fix
        action_str = str(action).lower()
        
        # Basic Grader Logic:
        # If the action contains the required action word, they solved it!
        if self.required_action != "none" and self.required_action.lower() in action_str:
            reward = 1.0  # Perfect score for this task
            done = True
            self.is_resolved = True
            info["status"] = "Incident resolved successfully!"
            
        # If they took too many steps, end the task with 0 reward
        elif self.current_step >= self.max_steps:
            reward = 0.0
            done = True
            info["status"] = "Max steps reached. Incident not resolved."
            
        else:
            # Task continues
            reward = 0.0
            done = False
            info["status"] = "Action executed. Issue persists."

        return self.state(), reward, done, info
