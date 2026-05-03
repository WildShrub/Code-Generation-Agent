# Code-Generation-Agent
---

## Run the following commands to ensure you have the LLM's needed:
```bash
ollama serve
ollama pull nomic-embed-text
ollama pull gemma4:e2b
```
---


## If the contents of rag_docs has changed, then run this command from code_generation_cli_agent:
```bash
python rag/build_rag_index.py
```

---

## Run this from the code_generation_agent directory (after you have made a venv and installed the required modules in it and then deactivated it.)
```bash
.\venv\Scripts\python.exe -m src.code_generation_cli_agent.direct_function_runner
```