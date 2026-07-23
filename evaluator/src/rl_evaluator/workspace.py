from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Iterator


class WorkspaceSet:
    def __init__(self, repo_root: Path, task_id: str) -> None:
        self.repo_root = repo_root
        self.task_root = repo_root / "tasks" / task_id
        self._temporary = tempfile.TemporaryDirectory(prefix=f"rl-eval-{task_id}-")
        self.root = Path(self._temporary.name)
        self.candidate = self.root / "candidate"
        self.internal = self.root / "internal-evaluation"

    def prepare_candidate(self) -> None:
        baseline = self.task_root / "baseline" / "workspace"
        if not baseline.is_dir():
            raise FileNotFoundError(f"Missing baseline workspace: {baseline}")
        shutil.copytree(baseline, self.candidate)
        self._overlay(self.task_root / "public_tests", self.candidate)
        self.assert_candidate_isolation()

    def prepare_internal(self) -> None:
        shutil.copytree(self.candidate, self.internal)
        self._overlay(self.task_root / "held_out_tests", self.internal)

    @staticmethod
    def _overlay(source: Path, target: Path) -> None:
        if not source.is_dir():
            return
        for item in source.rglob("*"):
            relative = item.relative_to(source)
            destination = target / relative
            if item.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
            elif item.is_file():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, destination)

    def assert_candidate_isolation(self) -> None:
        forbidden_names = {"golden", "held_out_tests", "solution.patch", "evaluator_config.json"}
        leaked = [
            str(path.relative_to(self.candidate))
            for path in self.candidate.rglob("*")
            if path.name in forbidden_names
        ]
        if leaked:
            raise RuntimeError(f"Candidate workspace contains evaluation-only assets: {leaked}")

    def preserve_candidate(self, destination: Path) -> None:
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(self.candidate, destination)

    def close(self) -> None:
        self._temporary.cleanup()
