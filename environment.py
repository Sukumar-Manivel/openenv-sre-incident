from models import Observation, Action, ServerState, Telemetry
import copy

class SREIncidentEnv:
    def __init__(self, initial_servers: list[ServerState], initial_telemetry: Telemetry, objective: str, alert: str, root_cause_service: str, required_action: str):
        self.initial_servers = initial_servers
        self.initial_telemetry = initial_telemetry
        self.objective = objective
        self.alert = alert
        self.root_cause_service = root_cause_service
        self.required_action = required_action
        self.max_steps = 10
        self.reset()
        
    def reset(self) -> Observation:
        self.servers = copy.deepcopy(self.initial_servers)
        self.telemetry = copy.deepcopy(self.initial_telemetry)
        self.step_count = 0
        self.done = False
        self.has_investigated = False
        self.state_data = {"actions_taken": [], "fixed": False}
        return self._get_obs()

    def _get_obs(self, error=None) -> Observation:
        return Observation(
            servers=self.servers,
            telemetry=self.telemetry,
            active_alert=self.alert if not self.state_data["fixed"] else None,
            last_error=error
        )
        
    def state(self) -> dict:
        return {
            "objective": self.objective,
            "state_data": self.state_data,
            "step_count": self.step_count
        }

    def step(self, action: Action) -> tuple[Observation, float, bool, dict]:
        if self.done:
            return self._get_obs(), 0.0, True, {"msg": "Task completed."}
            
        self.step_count += 1
        self.state_data["actions_taken"].append(action.model_dump())
        reward = 0.0
        error = None
        
        # 1. Reward Incremental Progress (Investigation)
        if action.action_type in ["view_logs", "view_telemetry"]:
            if not self.has_investigated:
                reward += 0.2  # Good habit reward
                self.has_investigated = True
                
        # 2. Handle System Mutations
        elif action.action_type in ["restart_service", "rollback_deployment"]:
            if not self.has_investigated:
                reward -= 0.3  # Reckless penalty! Didn't check logs first.
                
            # Did they target the correct broken server?
            if action.target_service == self.root_cause_service:
                if action.action_type == self.required_action:
                    self.state_data["fixed"] = True
                    for s in self.servers:
                        if s.name == self.root_cause_service:
                            s.status = "Online"
                            s.recent_logs = ["INFO: System recovered and operating normally."]
                    reward += 0.8  # Successfully fixed!
                else:
                    error, reward = f"Action {action.action_type} did not resolve the issue.", -0.1
            else:
                # Catastrophic failure: Messed with the wrong server
                error, reward = f"CRITICAL: Targeted wrong service ({action.target_service}).", -0.5
                self.done = True 
                
        elif action.action_type == "done":
            self.done = True
            
        # Infinite loop protection
        if self.step_count >= self.max_steps:
            self.done = True
            reward -= 1.0 
            
        return self._get_obs(error), reward, self.done, {"state": self.state_data}
