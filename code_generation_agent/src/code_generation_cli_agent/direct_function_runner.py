from __future__ import annotations
from .agent import Agent
from .new_file_name_so_it_works import AgentConfig, RunResult

from .cli import generate_repo_name, ensure_repo_path, sanitize_name
from pathlib import Path
import os

from .rag.rag import get_context
from langchain_ollama import ChatOllama

DEFAULT_MODEL = "devstral-small-2:24b-cloud"
DEFAULT_HOST = "http://localhost:11434"
VERSION = "0.5.0"
project_name = "test1"
model = os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)
host = os.environ.get("OLLAMA_HOST", DEFAULT_HOST)
temperature = float(os.environ.get("OLLAMA_TEMPERATURE", "0.0"))
repo = generate_repo_name(sanitize_name(project_name))
print(f"Repository: {repo}")

#all for testing
llm_model = os.environ.get("OLLAMA_MODEL", "devstral-small-2:24b-cloud")
llm_temp = float(os.environ.get("OLLAMA_TEMPERATURE", "0.0"))
llm = ChatOllama(model=llm_model, temperature=llm_temp)

print("\n\nTesting rag...")
print("cwd: ", os.getcwd())
test_prompt = "Is the color of the food in green eggs and ham steve's favorite color?"
print("prompt: ", test_prompt)
context = get_context(test_prompt)
new_prompt = f"""

        Retrieved context:
        {context}

        Task:
        {test_prompt}
        """
    #can probably just return the new prompt here to be used on the real thing
resp = llm.invoke(new_prompt)
answer = resp.content if isinstance(resp.content, str) else str(resp.content)
print("\n\nAnswer:", answer)
if len(answer) == 0:
    print("\n\nResponse not given\n\n")





module = 'src/'                             #Sets default module path if not provided
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


