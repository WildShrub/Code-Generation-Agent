from __future__ import annotations

from pathlib import Path
from pdb import run
from typing import Any, Callable

from prompt_toolkit import prompt

from .llm import OllamaLLM
from .prompt_manager import PromptManager
from .tools import Tools
from .new_file_name_so_it_works import AgentConfig, RunResult
from .utils import strip_code_fences
from .loader import build_multi_file_planning_prompt, build_single_file_prompt
from  .rag.rag import get_context

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
        self.log_number = 1

    def _log(self, message: Any) -> None:
        if self.cfg.verbose:
            print(message)
        name_of_log = f"log{self.log_number}.md"
        self.tools.write(name_of_log, message)
        self.log_number += 1

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
    
    def _clarification_phase(self, desc: str) -> str:
        """Ask the user clarifying questions and return enriched description."""
        run = self._multi_step_chain()

        prompt = (
            "You are a senior software engineer about to plan a project.\n"
            "Given the following description, generate 3-5 targeted clarifying questions\n"
            "about architecture, design patterns, and dependencies/libraries.\n"
            "Ask ONLY questions whose answers would meaningfully change your implementation plan.\n"
            "Output each question on its own numbered line. Nothing else.\n\n"
            f"DESCRIPTION:\n{desc}"
        )

        questions_raw = run(prompt).strip()
        if not questions_raw:
            return desc  # graceful fallback — skip if LLM returns nothing

        print("\n--- Clarification Phase ---")
        print("Please answer the following questions before planning begins:\n")
        print(questions_raw)
        print()

        answers = []
        for line in questions_raw.splitlines():
            line = line.strip()
            if not line:
                continue
            answer = input(f"{line}\n> ").strip()
            answers.append(f"{line}\n{answer}")

        enriched = (
            f"{desc}\n\n"
            "Additional clarifications from user:\n" +
            "\n\n".join(answers)
        )
        return enriched

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
        """
        # Clarification phase
        desc = self._clarification_phase(desc)
        
        run = self._multi_step_chain()

        # Plan
        p1 = build_multi_file_planning_prompt(module_path=module_path, description=desc)

        rag_output = get_context(p1)
        finished_prompt = p1.replace("<<<rag_output>>>", rag_output)

        self._log(finished_prompt)
        plan = run(finished_prompt).strip()
        if not plan:
            return RunResult(False, "Model returned empty plan.")
        self._log(plan)
        unparsed_file_plan_list = plan.split("$$$$")
        file_name_list = unparsed_file_plan_list.pop(0).split(", ")
        #print(file_name_list)
        #print(len(file_name_list))
        #print(len(unparsed_file_plan_list))
        for i in range(len(unparsed_file_plan_list)):
            print("i = ",i)
            file_name = file_name_list[i].replace("\n", "") #sanitizing the file name because the last one tends to have \n at the end of it.
            unparsed_file_plan = unparsed_file_plan_list[i].split("$$$")   #separates file description from function stuff
            file_description = unparsed_file_plan.pop(0)
            function_plans_string = unparsed_file_plan[0]              #should be the only thing in that list

            p2 =  build_single_file_prompt(file_name=file_name, file_description=file_description, function_plans=function_plans_string)
            rag_output = get_context(p2)
            finished_prompt = p1.replace("<<<rag_output>>>", rag_output)
            # Draft code
            self._log(finished_prompt)
            draft_code_raw = run(finished_prompt)
            self._log(draft_code_raw)
            draft_code = strip_code_fences(draft_code_raw)
            if not draft_code.strip():
                return RunResult(False, "Model returned empty module draft.")
            
            #print and ask for permission to write here
            self.tools.write(file_name, draft_code.rstrip() + "\n")
        return RunResult(True, f"Wrote modules: {file_name_list}")


