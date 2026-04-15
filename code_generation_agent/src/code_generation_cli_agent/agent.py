from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from .llm import OllamaLLM
from .prompt_manager import PromptManager
from .tools import Tools
from .types import AgentConfig, RunResult
from .utils import strip_code_fences

class Agent:
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg
        self.repo = Path(cfg.repo).resolve()
        self.tools = Tools(self.repo)
        self.prompt_manager = PromptManager()
        
        # Default prompt variants
        self.planning_variant = 'default'
        self.code_gen_variant = 'default'
        self.readme_gen_variant = 'default'
        self.multi_file_gen_variant = 'default'

    def _log(self, message: Any) -> None:
        if self.cfg.verbose:
            print(message)

    def _llm(self) -> OllamaLLM:
        return OllamaLLM(
            model=self.cfg.model,
            host=self.cfg.host,
            temperature=self.cfg.temperature,
        )

    def _call_llm(self, prompt: str) -> str:
        return self._llm().generate(prompt)

    def _multi_step_chain(self) -> Callable[[str], str]:
        try:
            from langchain_core.runnables import RunnableLambda
        except Exception:
            return self._call_llm

        return RunnableLambda(self._call_llm).invoke

    def create_program(self, desc: str, module_path: str) -> RunResult:
        """Create a program.
        
        Steps:
        1) produce a plan
        2) draft code
        3) draft readme (if readme-focused variant)
        3) write both to disk 
        """
        run = self._multi_step_chain()

        # Plan
        p1 = self.prompt_manager.get_prompt(
            'planning',
            self.planning_variant,
            desc=desc,
            module_path=module_path
        )
        self._log(p1)
        plan = run(p1).strip()
        if not plan:
            return RunResult(False, "Model returned empty plan.")

        # Draft code
        p2 = self.prompt_manager.get_prompt(
            'code_generation',
            self.code_gen_variant,
            desc=desc,
            module_path=module_path,
            plan=plan
        )
        self._log(p2)
        draft_code_raw = run(p2)
        self._log(draft_code_raw)
        draft_code = strip_code_fences(draft_code_raw)
        if not draft_code.strip():
            return RunResult(False, "Model returned empty module draft.")

        #Draft the readme
        p3 = self.prompt_manager.get_prompt(
            'readme_generation',
            self.readme_gen_variant,
            desc=desc,
            module_path=module_path,
            plan=plan
        )
        self._log(p3)
        draft_readme_raw = run(p3)
        self._log(draft_readme_raw)
        draft_readme = strip_code_fences(draft_readme_raw)
        if not draft_readme.strip():
            return RunResult(False, "Model returned empty readme draft.")

        final_code = draft_code.rstrip() + "\n"
        self.tools.write(module_path, final_code)
        readme_path = "README.md"
        self.tools.write(readme_path, draft_readme)
        return RunResult(True, f"Wrote module: {module_path}, readme: {readme_path}")
    

    def create_multiple_files(self, desc: str, module_path: str) -> RunResult:
        """Create a program.
        
        Steps:
        1) Planning Agent: produce a plan
        2) Code Generation Agent: draft code
        3) Test Generation Agent: draft tests 
        4) write all to disk 
        5) Self-Review Agent: run tests
            5.1) potentially give revision instructions
            5.2) repeat
        6) 
        """
        run = self._multi_step_chain()
        # Plan
        p1 = self.prompt_manager.get_prompt(    #modify prompt manager to get a different prompt
            'planning',
            self.planning_variant,
            desc=desc,
            module_path=module_path
        )
        self._log(p1)
        plan = run(p1).strip()
        if not plan:
            return RunResult(False, "Model returned empty plan.")
        
        end_of_file_name_list = plan.find("$")
        
        
        unparsed_file_plan_list = plan.split("$$$$")
        file_name_list = unparsed_file_plan_list.pop(0).split("-")
        
        for i in range(len(unparsed_file_plan_list)):
            
            file_name = file_name_list[i]
            unparsed_file_plan = unparsed_file_plan_list[i].split("$$$")   #separates file description from function stuff
            file_description = unparsed_file_plan.pop(0)
            functions_plans_string = unparsed_file_plan[0]              #should be the only thing in that list

            """
            
            """
            # Draft code
            p2 = self.prompt_manager.get_prompt(        
                'multi_file_generation',
                self.multi_file_gen_variant,
                desc=desc,
                module_path=(module_path + file_name),
                plan=plan
            )
            self._log(p2)
            draft_code_raw = run(p2)
            self._log(draft_code_raw)
            draft_code = strip_code_fences(draft_code_raw)
            if not draft_code.strip():
                return RunResult(False, "Model returned empty module draft.")
            




            



    def plan_architecture(self, desc: str, module_path: str) -> RunResult:
        "run a prompt to create instructions for individual files"
        "split those prompts to create separate prompts that are logged as files in the prompt folder"
        "run a loop running those prompts"




    

    def commit_and_push(self, message: str, push: bool) -> RunResult:
        ok, out = self.tools.git_commit(message)
        if not ok:
            return RunResult(False, out)

        if push:
            ok2, out2 = self.tools.git_push()
            if not ok2:
                return RunResult(False, "Commit succeeded, but push failed:\n" + out2)
            return RunResult(True, "Commit and push succeeded.")

        return RunResult(True, "Commit succeeded.")

    def list_available_prompts(self) -> dict[str, list[str]]:
        """List all available prompt tasks and their variants."""
        tasks = self.prompt_manager.list_available_tasks()
        result = {}
        for task in tasks:
            result[task] = self.prompt_manager.list_variants(task)
        return result
