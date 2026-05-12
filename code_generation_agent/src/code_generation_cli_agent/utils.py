from __future__ import annotations

import re
from pathlib import Path
from datetime import datetime

def ensure_repo_path(repo: str) -> Path:
    p = Path(repo).resolve()

    # Create the repo directory if it does not exist.
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

    if not p.is_dir():
        raise SystemExit(f"Invalid repo path (not a directory): {repo}")

    return p


def strip_code_fences(text: str) -> str:
    if not text:
        return ""

    s = text.strip()
    #s = re.sub(r"^\s*Here is the code:\s*", "", s, flags=re.IGNORECASE)
    #s = re.sub(r"```python", "", s)
    #s = re.sub(r"```", "", s)
    s = str.replace(s, "```python", "")
    s = str.replace(s, "```", "")
    lines = s.splitlines()

    if lines and lines[0].lstrip().startswith("```python"):
        lines = lines[1:]
    if lines and lines[-1].lstrip().startswith("```"):
        lines = lines[:-1]

    return "\n".join(lines).strip()




def sanitize_name(text: str) -> str:
    """Convert text to a valid directory/file name."""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[\s-]+', '_', text)
    return text.strip('_')


def generate_repo_name(project_name: str) -> str:
    """Generate repository path with timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"output/{project_name}_{timestamp}"
