from environment import SREIncidentEnv
from models import ServerState, Telemetry

def get_easy_task():
    servers = [
        ServerState(name="web_server", status="Offline", recent_logs=["FATAL: OutOfMemoryError in main thread."]),
        ServerState(name="db_server", status="Online", recent_logs=["INFO: DB Connections stable."])
    ]
    telemetry = Telemetry(cpu_usage=15.0, memory_usage=99.9, active_connections=0)
    return SREIncidentEnv(
        initial_servers=servers, initial_telemetry=telemetry,
        objective="The web server is down due to memory issues. Investigate and restore it.",
        alert="CRITICAL: web_server offline", root_cause_service="web_server", required_action="restart_service"
    )

def get_medium_task():
    servers = [
        ServerState(name="web_server", status="Error", recent_logs=["ERROR: SyntaxError at line 42 in auth.py after latest push."]),
        ServerState(name="db_server", status="Online", recent_logs=["INFO: DB Connections stable."])
    ]
    telemetry = Telemetry(cpu_usage=25.0, memory_usage=45.0, active_connections=12)
    return SREIncidentEnv(
        initial_servers=servers, initial_telemetry=telemetry,
        objective="Users cannot login after the recent update. Find the cause and fix it.",
        alert="WARNING: 500 Internal Server Errors spiking on web_server", root_cause_service="web_server", required_action="rollback_deployment"
    )

def get_hard_task():
    servers = [
        ServerState(name="web_server", status="High_Latency", recent_logs=["WARN: DB query timeout after 30000ms. Waiting..."]),
        ServerState(name="db_server", status="Error", recent_logs=["FATAL: Deadlock detected in transaction. Queues full."])
    ]
    telemetry = Telemetry(cpu_usage=95.0, memory_usage=80.0, active_connections=5000)
    return SREIncidentEnv(
        initial_servers=servers, initial_telemetry=telemetry,
        objective="The website is timing out. Identify the true bottleneck and resolve the system outage.",
        alert="CRITICAL: P99 latency > 30s on web_server", root_cause_service="db_server", required_action="restart_service"
    )

class Grader:
    @staticmethod
    def grade(state) -> float:
        is_fixed = False
        if isinstance(state, dict):
            is_fixed = state.get("reward", 0.15) > 0.8 or state.get("state_data", {}).get("fixed", False)
        else:
            is_fixed = getattr(state, "reward", 0.15) > 0.8
            
        # The ultimate safe numbers: 0.85 and 0.15
        return 0.85 if is_fixed else 0.15
