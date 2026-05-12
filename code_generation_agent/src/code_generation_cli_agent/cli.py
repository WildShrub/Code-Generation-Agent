from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .agent import Agent
from .new_file_name_so_it_works import AgentConfig
from .utils import ensure_repo_path, generate_repo_name, sanitize_name

DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "devstral-small-2:24b-cloud")
DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_TEMPERATURE = float(os.environ.get("OLLAMA_TEMPERATURE", "0.0"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cca",
        description="Generate code.",
    )

    parser.add_argument("description", help="Short description of the program to generate")

    return parser


def build_repo_path(description: str) -> str:
    words = description.lower().split()
    stop_words = {"a", "an", "the", "with", "for", "to", "in", "on", "of", "and", "or"}
    project_words = [word for word in words if word not in stop_words]
    project_name = sanitize_name("_".join(project_words[:4])) or "project"
    return generate_repo_name(project_name)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    repo = build_repo_path(args.description)
    repo_path = Path(repo)
    if not repo_path.exists():
        repo_path.mkdir(parents=True, exist_ok=True)

    ensure_repo_path(repo)

    cfg = AgentConfig(
        repo=repo,
        model=DEFAULT_MODEL,
        host=DEFAULT_HOST,
        temperature=DEFAULT_TEMPERATURE,
        verbose=False,
    )
    agent = Agent(cfg)

    print(f"Repository: {repo}")


    result = agent.create_multiple_files(
        desc=args.description,
        module_path="",

    )

    if result.ok:
        print("Success:", result.details)
        return 0

    print("Error:", result.details, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
