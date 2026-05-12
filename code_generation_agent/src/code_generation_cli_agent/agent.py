from __future__ import annotations

from pathlib import Path
from pdb import run
from typing import Any, Callable
from datetime import datetime
import os
import xml.etree.ElementTree as ET



from .llm import OllamaLLM

from .tools import Tools
from .new_file_name_so_it_works import AgentConfig, RunResult
from .utils import strip_code_fences
from .loader import build_multi_file_planning_prompt, build_single_file_prompt, read
from  .rag.rag import get_context

class Agent:
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg
        self.repo = Path(cfg.repo).resolve()
        self.tools = Tools(self.repo)
        self.prompt_dir = Path(__file__).parent.resolve() / "prompts"

        self.log_number = 1

    def _log(self, message: Any) -> None:

        if self.cfg.verbose:
            print(message)
        name_of_log = f"logs\\log{self.log_number}.md"
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
    
    def _test_gen_phase(self, file_name: str, single_file_plans: str) -> str:   
        """Create tests based off of the plans made by the planning phase and clarification phase, return those tests."""
        run = self._multi_step_chain()
        test_gen_prompt_path = self.prompt_dir / "test_generation_prompt.md"
        prompt = read(test_gen_prompt_path)
        finished_prompt = prompt.replace("<<<plans>>>", single_file_plans)

        self._log(finished_prompt)
        tests = run(finished_prompt).strip()
        if not tests:
            self._log("No tests returned")
            return single_file_plans  # graceful fallback — skip if LLM returns nothing
        self._log(tests)
        
        print(tests,"\n\n")
        approval = input("Do you approve of the generated tests?\n(Please answer \"y\" or \"n\")\n")
        if approval == "y":
            self.tools.write("test_" + file_name, strip_code_fences(tests).rstrip() + "\n")
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self._log("DRAFT " + timestamp +"\n"+ tests)

        enriched = (
            f"{single_file_plans}\n\n"
            "The program must pass these tests:\n" +
            "\n\n".join(strip_code_fences(tests))
        )

        return enriched
    
    def _parse_test_results(self, xml_text: str) -> tuple[bool, str]:
        if not xml_text:
            return False, "No test results available."
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as exc:
            return False, f"Unable to parse test results XML: {exc}"

        problems: list[str] = []
        for testcase in root.findall('.//testcase'):
            name = testcase.get('name', '<unknown>')
            for failure in testcase.findall('failure'):
                message = failure.get('message') or (failure.text or '').strip()
                problems.append(f"FAIL {name}: {message}".strip())
            for error in testcase.findall('error'):
                message = error.get('message') or (error.text or '').strip()
                problems.append(f"ERROR {name}: {message}".strip())

        return len(problems) > 0, '\n'.join(problems)

    def _build_self_review_prompt(self, module_file: str, module_source: str, test_file: str, test_results: str) -> str:
        prompt_template = read(self.prompt_dir / 'self_review_prompt.md')
        return (
            prompt_template
            .replace('<<<module_file>>>', module_file)
            .replace('<<<module_code>>>', module_source)
            .replace('<<<tests>>>', test_file)
            .replace('<<<test_results>>>', test_results)
        )

    def _self_review_phase(self, module_file: str, test_file: str, results_path: str) -> bool:
        self.tools.strip_file_paths(results_path)
        xml_text = self.tools.read(results_path)
        failed, summary = self._parse_test_results(xml_text)
        if not failed:
            return True

        module_source = self.tools.read(module_file)
        if not module_source:
            self._log(f"SELF REVIEW FAILED: could not read module file {module_file}")
            return False

        test_source = self.tools.read(test_file)
        if not test_source:
            self._log(f"SELF REVIEW FAILED: could not read test file {test_file}")
            return False

        prompt = self._build_self_review_prompt(module_file, module_source, test_source, summary)
        self._log('SELF REVIEW PROMPT:\n' + prompt)
        revision_raw = self._call_llm(prompt)
        self._log('SELF REVIEW RESPONSE:\n' + revision_raw)

        revised_code = strip_code_fences(revision_raw)
        if not revised_code.strip():
            self._log(f"SELF REVIEW FAILED: LLM returned empty revision for {module_file}")
            return False

        self.tools.write(module_file, revised_code.rstrip() + '\n')
        return True


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
        print("current directory: ", Path(__file__).parent.resolve())
        print("current file: ", Path(__file__).resolve())
        print("cwd: ", os.getcwd())
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
        
        
        
        file_list = {}
        for i in range(len(unparsed_file_plan_list)):
            print("i = ",i)
            file_name = file_name_list[i].replace("\n", "") #sanitizing the file name because the last one tends to have \n at the end of it.
            unparsed_file_plan = unparsed_file_plan_list[i].split("$$$")   #separates file description from function stuff
            file_description = unparsed_file_plan.pop(0)
            function_plans_string = unparsed_file_plan[0]              #should be the only thing in that list
            
            function_plans_and_tests = self._test_gen_phase(file_name=file_name, single_file_plans=function_plans_string)
            
            p2 =  build_single_file_prompt(file_name=file_name, file_description=file_description, function_plans=function_plans_and_tests)
            rag_output = get_context(p2)
            finished_prompt = p2.replace("<<<rag_output>>>", rag_output)

            # Draft code
            self._log(finished_prompt)
            draft_code_raw = run(finished_prompt)
            self._log(draft_code_raw)
            draft_code = strip_code_fences(draft_code_raw)
            if not draft_code.strip():
                return RunResult(False, "Model returned empty module draft.")
            
            #add to file dictionary for easier processing
            file_list[file_name] = draft_code.rstrip() + "\n"
            
        

        #print and ask for permission to write    
        all_file_drafts = ""
        for key, value in file_list.items():
            all_file_drafts += key + ":\n------------------\n" + value
        print(all_file_drafts,"\n\n")

        approval = input("Do you approve of the generated code?\n(Please answer \"y\" or \"n\")\n")
        if approval == "y":
            for key, value in file_list.items():
                print("key : ", key)
                self.tools.write(self.repo / key, value.rstrip() + "\n")
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self._log("DRAFT " + timestamp +"\n"+ all_file_drafts)

        for key, value in file_list.items():
            test_file_path = str("test_" + key)
            test_results_path =  f"test_results/{str.replace(f"{key}", ".py", "")}_results.md"

            attempts = 0
            while attempts < 4:
                print(f"running: pytest -v --junit-xml={test_results_path} {test_file_path}")
                ok, _ = self.tools.run(f"pytest -v --junit-xml={test_results_path} {test_file_path}")
                self.tools.strip_file_paths(test_results_path)

                if ok:
                    break

                print(f"Self-review triggered for {key} based on test results.")
                if not self._self_review_phase(key, test_file_path, test_results_path):
                    print(f"Self-review failed for {key}; skipping further retries.")
                    break

                print(f"Re-running tests for {key} after self-review revision.")
                attempts += 1
            if attempts == 4:
                print(f"Self-review retry exhausted for {key}.")

        return RunResult(True, f"Wrote modules: {file_name_list}")