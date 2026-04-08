import uvicorn
from openenv.core.env_server import create_app
from environment import SREIncidentEnv
from models import Action, Observation

# Create the official OpenEnv FastAPI server
# We pass the class name directly (SREIncidentEnv) without the ()
app = create_app(SREIncidentEnv, Action, Observation)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
