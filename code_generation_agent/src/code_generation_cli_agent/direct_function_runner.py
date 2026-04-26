from __future__ import annotations
from .agent import Agent
from .new_file_name_so_it_works import AgentConfig, RunResult

from .cli import generate_repo_name, ensure_repo_path, sanitize_name
from pathlib import Path
import os


DEFAULT_MODEL = "devstral-small-2:24b-cloud"
DEFAULT_HOST = "http://localhost:11434"
VERSION = "0.5.0"
project_name = "test1"
model = os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)
host = os.environ.get("OLLAMA_HOST", DEFAULT_HOST)
temperature = float(os.environ.get("OLLAMA_TEMPERATURE", "0.0"))
repo = generate_repo_name(sanitize_name(project_name))
print(f"Repository: {repo}")





module = 'src/main.py'                             #Sets default module path if not provided
print(f"Module: {module}")
repo_path = Path(repo)
if not repo_path.exists():
    repo_path.mkdir(parents=True, exist_ok=True)
ensure_repo_path(repo)

cfg = AgentConfig(
        repo=repo,
        model=model,
        host=host,
        temperature=temperature,
        verbose= False
    )


agent = Agent(cfg)

description = "Create a create a blackjack program using separation of concerns. Use at least 2 files"


agent.create_multiple_files(description, module)
print("ALL DONE!")


