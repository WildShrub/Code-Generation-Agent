from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Tuple
import re

class Tools:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path.resolve()

    def _safe(self, rel_path: str) -> Path:
        p = (self.repo_path / rel_path).resolve()
        if not str(p).startswith(str(self.repo_path)):
            raise ValueError("Unsafe path traversal blocked.")
        return p

    def read(self, rel_path: str, max_chars: int = 20000) -> str:
        p = self._safe(rel_path)
        if not p.exists():
            return ""
        return p.read_text(encoding="utf-8", errors="replace")[:max_chars]

    def write(self, rel_path: str, content: str) -> None:
        p = self._safe(rel_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def run(self, cmd: str, timeout_s: int = 600) -> Tuple[bool, str]:
        print(self.repo_path)
        proc = subprocess.run(
            cmd,
            cwd=self.repo_path,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        print(self.repo_path)
        out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        out = (out.strip() or "[NO OUTPUT]")
        return proc.returncode == 0, out[:20000]

    def git_commit(self, message: str) -> Tuple[bool, str]:
        ok1, out1 = self.run("git add -A")
        if not ok1:
            return False, out1
        safe_msg = message.replace('"', "'")
        return self.run(f'git commit -m "{safe_msg}"')
    
    def strip_file_paths(self, rel_path: str) -> None:
        "rewrites a file to not include any file paths"
        text = self.read(rel_path=rel_path)
        pattern = r'([A-Za-z]:\\[^\s]+|\/[^\s]+)'
        cleaned_text = re.sub(pattern,lambda m: Path(m.group(0)).name,text)
        self.write(rel_path=rel_path, content=cleaned_text)

    def git_push(self) -> Tuple[bool, str]:
        return self.run("git push")



