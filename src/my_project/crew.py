# crew.py
import os
import yaml
from dotenv import load_dotenv
from crewai import Crew, Agent, Task

load_dotenv()

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

BASE_DIR = os.path.dirname(__file__)
CONFIG_DIR = os.path.join(BASE_DIR, "config")

agents_config = load_yaml(os.path.join(CONFIG_DIR, "agents.yaml"))
tasks_config = load_yaml(os.path.join(CONFIG_DIR, "tasks.yaml"))

# Inject .env model defaults if not in YAML
agents_config["summarizer"]["model_name"] = os.environ.get("MODEL_NAME", agents_config["summarizer"].get("model_name", "ollama/phi3"))
agents_config["summarizer"]["model_api"] = os.environ.get("MODEL_API", agents_config["summarizer"].get("model_api", "http://localhost:11434"))


class TherapySummarizer(Crew):
    def __init__(self):
        # Build Agent and Task
        summarizer_agent = Agent(**agents_config["summarizer"])
        summarize_task = Task(**tasks_config["summarize_session"])
        summarize_task.agent = summarizer_agent

        super().__init__(
            agents=[summarizer_agent],
            tasks=[summarize_task],
            verbose=True
        )
