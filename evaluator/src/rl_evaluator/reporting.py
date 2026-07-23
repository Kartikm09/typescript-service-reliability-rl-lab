from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable

from .schemas import EvaluationResult, StageResult


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def markdown_report(result: EvaluationResult) -> str:
    rows = ["| Stage | Result | Duration |", "| --- | --- | ---: |"]
    for stage in result.stages:
        rows.append(
            f"| `{stage.name}` | {'pass' if stage.passed else 'fail'} | {stage.duration_ms} ms |"
        )
    changed = "\n".join(f"- `{item['path']}`" for item in result.changed_files) or "- None"
    return "\n".join(
        [
            f"# Evaluation Report: {result.task_id}",
            "",
            f"- Classification: **{result.classification}**",
            f"- Accepted: **{str(result.accepted).lower()}**",
            f"- Score: **{result.score}/{result.score_breakdown.get('maximum', 0)}**",
            f"- Acceptance threshold: **{result.acceptance_score}**",
            f"- Message: {result.message}",
            "",
            "## Stage evidence",
            "",
            *rows,
            "",
            "## Changed files",
            "",
            changed,
            "",
            "## Safety boundary",
            "",
            "This report came from local process execution with path checks, timeouts, and output caps.",
            "The evaluator is not a hardened sandbox for untrusted code.",
            "",
        ]
    )


def emit_reports(output: Path, result: EvaluationResult) -> None:
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "result.json", result.to_dict())
    (output / "evaluation_report.md").write_text(markdown_report(result), encoding="utf-8")
    write_json(
        output / "test_summary.json",
        {"task_id": result.task_id, "stages": [stage.to_dict() for stage in result.stages]},
    )
    write_json(output / "changed_files.json", result.changed_files)
    write_json(
        output / "timing.json",
        {
            "task_id": result.task_id,
            "total_duration_ms": sum(stage.duration_ms for stage in result.stages),
            "stages": {stage.name: stage.duration_ms for stage in result.stages},
        },
    )
    write_json(output / "score_breakdown.json", result.score_breakdown)
