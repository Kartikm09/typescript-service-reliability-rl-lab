from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Dict, List

from .limits import bounded_text, redact_paths
from .schemas import StageResult


def expand_command(command: List[str], repo_root: Path) -> List[str]:
    replacements = {
        "{repo_root}": str(repo_root),
        "{python}": os.environ.get("PYTHON", "python3"),
    }
    return [replacements.get(part, part.replace("{repo_root}", str(repo_root))) for part in command]


def report_command(command: List[str], repo_root: Path) -> List[str]:
    """Remove machine-specific repository paths from persisted evidence."""
    root = str(repo_root)
    return [part.replace(root, "<repo-root>") for part in command]


def run_stage(
    name: str,
    command: List[str],
    workspace: Path,
    repo_root: Path,
    timeout_seconds: int,
    output_limit_bytes: int,
    extra_env: Dict[str, str] | None = None,
) -> StageResult:
    argv = expand_command(command, repo_root)
    env = os.environ.copy()
    env.update({"RL_EVAL_SEED": "20260723", "TZ": "UTC", "LC_ALL": "C"})
    if extra_env:
        env.update(extra_env)
    started = time.monotonic_ns()
    try:
        completed = subprocess.run(
            argv,
            cwd=workspace,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        duration_ms = (time.monotonic_ns() - started) // 1_000_000
        stdout = redact_paths(bounded_text(completed.stdout, output_limit_bytes), workspace)
        stderr = redact_paths(bounded_text(completed.stderr, output_limit_bytes), workspace)
        return StageResult(
            name=name,
            command=report_command(argv, repo_root),
            passed=completed.returncode == 0,
            return_code=completed.returncode,
            duration_ms=int(duration_ms),
            stdout=stdout,
            stderr=stderr,
        )
    except subprocess.TimeoutExpired as exc:
        duration_ms = (time.monotonic_ns() - started) // 1_000_000
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return StageResult(
            name=name,
            command=report_command(argv, repo_root),
            passed=False,
            return_code=None,
            duration_ms=int(duration_ms),
            stdout=redact_paths(bounded_text(stdout, output_limit_bytes), workspace),
            stderr=redact_paths(bounded_text(stderr, output_limit_bytes), workspace),
            timed_out=True,
        )
