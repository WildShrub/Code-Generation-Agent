from pathlib import Path
import os



def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_multi_file_planning_prompt(module_path: str, description: str) -> str:
    current_dir = Path(__file__).parent.resolve()
    prompts_dir = current_dir / "prompts"
    formatting_file_path = prompts_dir / "multi_file_planning_response_format.md"
    system_prompt_file_path = prompts_dir / "multi_file_planning_system_prompt.md"
    formatting = read(formatting_file_path)
    system_prompt = read(system_prompt_file_path)
    modified_prompt_1 = system_prompt.replace("<<<FORMATING>>>", formatting)
    modified_prompt_2 = modified_prompt_1.replace("<<<module_path>>>", module_path)
    modified_prompt_3 = modified_prompt_2.replace("<<<description>>>", description)
    return modified_prompt_3

def build_single_file_prompt(file_name: str, file_description: str, function_plans: str) -> str:
    current_dir = Path(__file__).parent.resolve()
    prompts_dir = current_dir / "prompts"
    system_prompt_file_path = prompts_dir / "single_file_writing_prompt.md"
    
    system_prompt = read(system_prompt_file_path)
    modified_prompt_1 = system_prompt.replace("<<<file_name>>>", file_name)
    modified_prompt_2 = modified_prompt_1.replace("<<<file_description>>>", file_description)
    finished_prompt = modified_prompt_2.replace("<<<function_plans_string>>>", function_plans)
    return finished_prompt


print("current directory: ", Path(__file__).parent.resolve())
print("current file: ", Path(__file__).resolve())
print("cwd: ", os.getcwd())