from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


SUPPORTED_CLASSIFICATIONS = (
    "accepted",
    "compile_error",
    "build_error",
    "test_failure",
    "regression_failure",
    "runtime_error",
    "timeout",
    "performance_regression",
    "malformed_patch",
    "prohibited_file_change",
    "nondeterministic_result",
    "incomplete_solution",
)


@dataclass
class StageResult:
    name: str
    command: List[str]
    passed: bool
    return_code: Optional[int]
    duration_ms: int
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvaluationResult:
    task_id: str
    classification: str
    accepted: bool
    score: int
    acceptance_score: int
    dry_run: bool
    changed_files: List[Dict[str, Any]] = field(default_factory=list)
    stages: List[StageResult] = field(default_factory=list)
    score_breakdown: Dict[str, Any] = field(default_factory=dict)
    message: str = ""
    evaluator_version: str = "0.1.0"

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["supported_classifications"] = list(SUPPORTED_CLASSIFICATIONS)
        return payload
