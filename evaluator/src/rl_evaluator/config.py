from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass(frozen=True)
class PerformanceRule:
    path: str
    metric: str
    direction: str
    threshold: float


@dataclass(frozen=True)
class EvaluatorConfig:
    task_id: str
    language: str
    allowed_paths: List[str]
    commands: Dict[str, List[str]]
    weights: Dict[str, int]
    acceptance_score: int
    timeout_seconds: int
    output_limit_bytes: int
    build_failure_class: str
    required_documentation: List[str]
    performance: Optional[PerformanceRule]


def load_config(path: Path) -> EvaluatorConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    performance = raw.get("performance")
    rule = PerformanceRule(**performance) if performance else None
    return EvaluatorConfig(
        task_id=str(raw["task_id"]),
        language=str(raw["language"]),
        allowed_paths=list(raw["allowed_paths"]),
        commands={name: list(argv) for name, argv in raw["commands"].items()},
        weights={name: int(value) for name, value in raw["weights"].items()},
        acceptance_score=int(raw.get("acceptance_score", 80)),
        timeout_seconds=int(raw.get("timeout_seconds", 120)),
        output_limit_bytes=int(raw.get("output_limit_bytes", 200_000)),
        build_failure_class=str(raw.get("build_failure_class", "build_error")),
        required_documentation=list(raw.get("required_documentation", [])),
        performance=rule,
    )
