# OpenEnv: SRE Incident Management

This is a complete, real-world Reinforcement Learning environment built for the OpenEnv Hackathon. It simulates a Site Reliability Engineering (SRE) scenario where an AI agent must diagnose and resolve server incidents across different difficulty levels.

## Environment Description
The environment simulates a microservices architecture (`web_server` and `db_server`). The agent receives telemetry data and logs, and must identify root causes (like Memory Leaks, Deadlocks, or Syntax Errors) and take appropriate corrective actions without breaking healthy services.

## Observation Space
The agent receives a strict JSON state matching the `Observation` Pydantic model:
* **servers**: List of server states (Online, Offline, Error, High_Latency) and recent logs.
* **telemetry**: Current CPU usage, memory usage, and active connections.
* **active_alert**: Any active P99 latency or downtime alerts.
* **last_error**: Feedback if the agent made an invalid move.

## Action Space
The agent must output a strict JSON matching the `Action` Pydantic model:
* **action_type**: `"view_logs" | "view_telemetry" | "restart_service" | "rollback_deployment" | "done"`
* **target_service**: The name of the service to target (e.g., `"web_server"`, `"db_server"`).

## Setup & Execution Instructions
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Export the required environment variables:
   ```bash
   export API_BASE_URL="https://router.huggingface.co/v1/"
   export MODEL_NAME="Qwen/Qwen2.5-7B-Instruct"
   export HF_TOKEN="your_huggingface_token"
4. Run the evaluation script:
   python inference.py
