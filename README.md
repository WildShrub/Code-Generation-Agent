# Code-Generation-Agent
---

## Run the following commands to ensure you have the LLM's needed:
```bash
ollama serve
ollama pull nomic-embed-text
ollama pull devstral-2:123b-cloud
```
---


## If the contents of rag_docs has changed, then run this command from code_generation_cli_agent:
```bash
python rag/build_rag_index.py
```

---

## Run this from the code_generation_agent directory (after you have made a venv and installed the required modules in it and then deactivated it.)
```bash

 python -m src.code_generation_cli_agent.cli "Create a class called bucket with the variables label, has_handle, contents, and amount_filled. Then create a class called Bucket_user with the variables name and current_bucket (which will be of the Bucket type), it will also have a function that pours the contents of the bucket its holding. The bucket that its holding should have its amount_filled variable set to 0.0 when this occurs. Then create an instance of the Bucket_holder class where name is paul, and current_bucket is an instance of the Bucket class called water_pail where label is water pail, has_handle is a boolean set to true, contents is water, and amount_filled=0.25. finally, print the amount filled of water_pail before and after the Bucket_user pours it. Use best coding practices where applicable. Use 3 separate files."

You can swap out the prompt for anything.

 Or run this 

 .\venv\Scripts\python.exe -m src.code_generation_cli_agent.direct_function_runner
```