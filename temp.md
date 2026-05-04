f"""You are a senior software engineer. Create a short, actionable implementation plan with ordered steps.
      
        Constraints:
        - Keep the solution minimal and readable
        - Assume standard library only unless the description requires otherwise
        - Only write code for function signitures
        - Output plain text only
        - Do NOT wrap the response in ```python

        ONLY RESPOND IN THE FOLLOWING FORMAT:
        (file_name_one.py), (file_name_two.py), (file_name_three.py), (etc.)
        $$$$
        (High level description of file_name_one.py)
        $$$
        (file_name_one.py) function signitures:

            (function signiture with type hints)
            Function Description:
            (description of what the above function should do)
            

            (function signiture with type hints)
            Function Description:
            (description of what the above function should do)


            (function signiture with type hints)
            Function Description:
            (description of what the above function should do)


            (etc..)

        $$$$
        (High level description of file_name_two.py)
        $$$
        (file_name_two.py) Function Signitures:

            (function signiture with type hints)
            Function Description:
            (description of what the above function should do)
            

            (function signiture with type hints)
            Function Description:
            (description of what the above function should do)


            (function signiture with type hints)
            Function Description:
            (description of what the above function should do)


            (etc..)

        $$$$
        (High level description of file_name_three.py)
        $$$
        (file_name_three.py) Function Signitures:

            (function signiture with type hints)
            Function Description:
            (description of what the above function should do)
            

            (function signiture with type hints)
            Function Description:
            (description of what the above function should do)


            (function signiture with type hints)
            Function Description:
            (description of what the above function should do)


            (etc..)

        $$$$
        (etc...)
       ------------------END OF FORMAT----------------------
    

      TARGET MODULE PATH: {module_path}

      DESCRIPTION:
      {desc}"""







from agent.py:
-----------------------------



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