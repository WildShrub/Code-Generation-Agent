from __future__ import annotations
from .agent import Agent
from .new_file_name_so_it_works import AgentConfig, RunResult

from .cli import generate_repo_name, ensure_repo_path, sanitize_name
from pathlib import Path
import os

from .rag.rag import get_context
from langchain_ollama import ChatOllama

DEFAULT_MODEL = "devstral-small-2:24b-cloud"   #"gemma4:e2b" #
DEFAULT_HOST = "http://localhost:11434"
VERSION = "0.5.0"


def test_rag() ->None:
    llm_model = os.environ.get("OLLAMA_MODEL", "gemma4:e2b")
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



project_name = "rag_test1"
model = os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)
host = os.environ.get("OLLAMA_HOST", DEFAULT_HOST)
temperature = float(os.environ.get("OLLAMA_TEMPERATURE", "0.0"))
repo = generate_repo_name(sanitize_name(project_name))
print(f"Repository: {repo}")


print("current directory: ", Path(__file__).parent.resolve())
print("current file: ", Path(__file__).resolve())
print("cwd: ", os.getcwd())

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
hard_test_prompt = "Create a class called bucket with the variables label, has_handle, contents, and amount_filled. Then create a class called Bucket_user with the variables name and current_bucket (which will be of the Bucket type), it will also have a function that pours the contents of the bucket its holding. The bucket that its holding should have its amount_filled variable set to 0.0 when this occurs. Then create an instance of the Bucket_holder class where name is paul, and current_bucket is an instance of the Bucket class called water_pail where label is water pail, has_handle is a boolean set to true, contents is water, and amount_filled=0.25. finally, print the amount filled of water_pail before and after the Bucket_user pours it. Use best coding practices where applicable. Use 3 separate files."
#description = "Create a create a blackjack program using separation of concerns. Use at least 2 files"


agent.create_multiple_files(desc=hard_test_prompt, module_path=module)
print("ALL DONE!")


