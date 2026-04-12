from environment import SREIncidentEnv
from models import ServerState, Telemetry

def get_easy_task():
    servers = [ServerState(name="web_server", status="Offline", recent_logs=["FATAL: OutOfMemoryError"])]
    telemetry = Telemetry(cpu_usage=15.0, memory_usage=99.9, active_connections=0)
    return SREIncidentEnv(initial_servers=servers, initial_telemetry=telemetry, objective="Restore web server.", required_action="restart_service")

def get_medium_task():
    servers = [ServerState(name="web_server", status="Error", recent_logs=["ERROR: SyntaxError in auth.py"])]
    telemetry = Telemetry(cpu_usage=25.0, memory_usage=45.0, active_connections=12)
    return SREIncidentEnv(initial_servers=servers, initial_telemetry=telemetry, objective="Fix login.", required_action="rollback_deployment")

def get_hard_task():
    servers = [ServerState(name="web_server", status="High_Latency", recent_logs=["WARN: DB timeout"])]
    telemetry = Telemetry(cpu_usage=95.0, memory_usage=80.0, active_connections=5000)
    return SREIncidentEnv(initial_servers=servers, initial_telemetry=telemetry, objective="Resolve outage.", required_action="restart_service")

class SREGrader:
    def __call__(self, state) -> float:
        return 0.5
        
    def grade(self, state) -> float:
        return 0.5
        except Exception:
            return 0.15
