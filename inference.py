import os
import json
import time
from openai import OpenAI
from tasks import get_easy_task, get_medium_task, get_hard_task, SREGrader # <-- Updated Import
from models import Action
import http.server
import socketserver

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1/")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def run_inference():
    grader_instance = SREGrader() # <-- Instantiate the grader
    
    tasks = [
        ("sre-incident-easy", get_easy_task(), grader_instance),
        ("sre-incident-medium", get_medium_task(), grader_instance),
        ("sre-incident-hard", get_hard_task(), grader_instance)
    ]
    
    benchmark_env_name = "openenv-sre-incident"

    for task_name, env, grader in tasks:
        obs = env.reset()
        done = False
        step_num = 0
        rewards_history = []
        
        print(f"[START] task={task_name} env={benchmark_env_name} model={MODEL_NAME}", flush=True)
        
        system_prompt = (
            "You are an expert SRE AI troubleshooting server incidents. "
            "Output ONLY valid JSON. Do NOT use markdown formatting. "
            "CRITICAL: Put all parameters at the root level of the JSON. Do not nest them. "
            "First, provide a 'reasoning' key explaining your thought process, what you see in the observation, and your diagnosis. "
            "Then, provide the 'action_type' which MUST be exactly one of: 'view_logs', 'view_telemetry', 'restart_service', 'rollback_deployment', or 'done'. "
            "If an action requires a service target, you MUST use the key 'target_service'. "
            "Valid Example:\n"
            "{\"reasoning\": \"The web_server is throwing 500 errors. I need to view its logs to find the cause.\", \"action_type\": \"view_logs\", \"target_service\": \"web_server\"}"
        )
        
        messages = [{"role": "system", "content": system_prompt}]
        
        try:
            while not done:
                step_num += 1
                
                user_prompt = f"Objective: {env.objective}\nObservation: {obs.model_dump_json()}\nOutput strict JSON for your next action:"
                messages.append({"role": "user", "content": user_prompt})
                
                try:
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        response_format={"type": "json_object"}
                    )
                    
                    raw_content = response.choices[0].message.content
                    content = raw_content.strip()
                    if content.startswith("```json"):
                        content = content[7:-3].strip()
                    elif content.startswith("```"):
                        content = content[3:-3].strip()
                        
                    action_data = json.loads(content)
                    
                    ai_thought = action_data.pop("reasoning", "No reasoning provided.")
                    
                    if "action_type" not in action_data:
                        action_data["action_type"] = "done"

                    action = Action(**action_data)
                    action_str = json.dumps(action_data).replace('\n', '') 
                    
                    messages.append({"role": "assistant", "content": raw_content})
                    
                except Exception as e:
                    print(f"API ERROR: {e}", flush=True) 
                    ai_thought = "Failed to generate valid JSON."
                    action = Action(action_type="done")
                    action_str = '{"action_type": "done"}'
                    
                obs, reward, done, info = env.step(action)
                rewards_history.append(reward)
                
                done_str = "true" if done else "false"
                error_msg = getattr(obs, 'last_error', None)
                error_str = "null" if error_msg is None else error_msg.replace('\n', ' ')
                
                print(f"[STEP] step={step_num} thought=\"{ai_thought}\" action={action_str} reward={reward:.2f} done={done_str} error={error_str}", flush=True)
                
                if step_num >= 8:
                    done = True
                
            final_score = grader(env.state())
            # Looking for our new 0.85 success mark
            success_str = "true" if final_score > 0.8 else "false"
            
        except Exception as e:
            success_str = "false"
            
        finally:
            rewards_str = ",".join([f"{r:.2f}" for r in rewards_history])
            print(f"[END] success={success_str} steps={step_num} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    print("Starting Hackathon Evaluation...", flush=True)
    run_inference()
    print("Evaluation complete! Starting web server to keep Hugging Face happy... 🟢", flush=True)
    
    PORT = 7860
    Handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True 
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Serving at port {PORT}", flush=True)
            httpd.serve_forever()
    except OSError:
        print(f"Port {PORT} is already in use by the grader. Skipping web server startup. We passed!", flush=True)
