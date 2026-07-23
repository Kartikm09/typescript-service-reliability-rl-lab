from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import EvaluatorConfig, load_config
from .patching import (
    PatchError,
    apply_patch,
    evidence_before,
    parse_changed_paths,
    prohibited_paths,
    sha256,
)
from .process import run_stage
from .reporting import emit_reports
from .schemas import EvaluationResult, StageResult
from .scoring import calculate_score
from .workspace import WorkspaceSet


ORDERED_STAGES = (
    "format",
    "lint",
    "build",
    "public_tests",
    "held_out_tests",
    "regression_tests",
    "benchmark",
    "determinism",
)


def classify_failure(stage: StageResult, config: EvaluatorConfig) -> str:
    if stage.timed_out:
        return "timeout"
    if stage.return_code is not None and stage.return_code < 0:
        return "runtime_error"
    if stage.name == "build":
        return config.build_failure_class
    if stage.name in {"public_tests", "held_out_tests"}:
        return "test_failure"
    if stage.name == "regression_tests":
        return "regression_failure"
    if stage.name == "benchmark":
        return "performance_regression"
    if stage.name == "determinism":
        return "nondeterministic_result"
    return "incomplete_solution"


def performance_passed(workspace: Path, config: EvaluatorConfig) -> Tuple[bool, str]:
    rule = config.performance
    if rule is None:
        return True, "No task-specific performance rule"
    path = workspace / rule.path
    if not path.is_file():
        return False, f"Missing benchmark result: {rule.path}"
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("metric") != rule.metric:
        return False, f"Unexpected benchmark metric: {raw.get('metric')}"
    value = float(raw["value"])
    if rule.direction == "lower":
        passed = value <= rule.threshold
    elif rule.direction == "higher":
        passed = value >= rule.threshold
    else:
        return False, f"Unsupported performance direction: {rule.direction}"
    return passed, f"{rule.metric}={value}; threshold {rule.direction} {rule.threshold}"


def evaluate(
    repo_root: Path,
    task_id: str,
    patch_path: Path,
    output: Path,
    dry_run: bool,
    keep_candidate: bool,
) -> EvaluationResult:
    config_path = repo_root / "tasks" / task_id / "evaluator_config.json"
    config = load_config(config_path)
    if config.task_id != task_id:
        raise ValueError("Task ID does not match evaluator config")
    workspaces = WorkspaceSet(repo_root, task_id)
    stages: List[StageResult] = []
    changed: List[Dict[str, object]] = []
    classification = "incomplete_solution"
    message = "Evaluation did not run"
    try:
        workspaces.prepare_candidate()
        patch_text = patch_path.read_text(encoding="utf-8")
        try:
            paths = parse_changed_paths(patch_text)
        except (PatchError, UnicodeError) as exc:
            result = EvaluationResult(
                task_id, "malformed_patch", False, 0, config.acceptance_score, dry_run,
                message=str(exc),
            )
            emit_reports(output, result)
            return result
        prohibited = prohibited_paths(paths, config.allowed_paths)
        if prohibited:
            result = EvaluationResult(
                task_id,
                "prohibited_file_change",
                False,
                0,
                config.acceptance_score,
                dry_run,
                changed_files=[{"path": path} for path in paths],
                message="Prohibited paths: " + ", ".join(prohibited),
            )
            emit_reports(output, result)
            return result
        before = evidence_before(workspaces.candidate, paths)
        try:
            apply_patch(workspaces.candidate, patch_path.resolve())
        except PatchError as exc:
            result = EvaluationResult(
                task_id,
                "malformed_patch",
                False,
                0,
                config.acceptance_score,
                dry_run,
                changed_files=[{"path": path} for path in paths],
                message=str(exc),
            )
            emit_reports(output, result)
            return result
        changed = [
            {"path": path, "before_sha256": before[path], "after_sha256": sha256(workspaces.candidate / path)}
            for path in paths
        ]
        workspaces.assert_candidate_isolation()
        missing_docs = [
            path for path in config.required_documentation if not (workspaces.candidate / path).is_file()
        ]
        if dry_run:
            result = EvaluationResult(
                task_id,
                "incomplete_solution",
                False,
                0,
                config.acceptance_score,
                True,
                changed_files=changed,
                message="Dry run validated patch scope and candidate-workspace isolation",
            )
            if keep_candidate:
                workspaces.preserve_candidate(output / "candidate_workspace")
            emit_reports(output, result)
            return result

        for name in ("format", "lint", "build", "public_tests"):
            command = config.commands.get(name)
            if not command:
                continue
            stage = run_stage(
                name,
                command,
                workspaces.candidate,
                repo_root,
                config.timeout_seconds,
                config.output_limit_bytes,
            )
            stages.append(stage)
            if not stage.passed:
                classification = classify_failure(stage, config)
                message = f"Stage failed: {name}"
                break
        else:
            workspaces.prepare_internal()
            for name in ("held_out_tests", "regression_tests", "benchmark"):
                command = config.commands.get(name)
                if not command:
                    continue
                stage = run_stage(
                    name,
                    command,
                    workspaces.internal,
                    repo_root,
                    config.timeout_seconds,
                    config.output_limit_bytes,
                )
                if stage.passed and name == "benchmark":
                    stage.passed, note = performance_passed(workspaces.internal, config)
                    stage.stdout = (stage.stdout + "\n" + note).strip()
                stages.append(stage)
                if not stage.passed:
                    classification = classify_failure(stage, config)
                    message = f"Stage failed: {name}"
                    break
            else:
                determinism = config.commands.get("determinism")
                if determinism:
                    first = run_stage(
                        "determinism",
                        determinism,
                        workspaces.internal,
                        repo_root,
                        config.timeout_seconds,
                        config.output_limit_bytes,
                    )
                    second = run_stage(
                        "determinism-repeat",
                        determinism,
                        workspaces.internal,
                        repo_root,
                        config.timeout_seconds,
                        config.output_limit_bytes,
                    )
                    first.passed = first.passed and second.passed and first.stdout == second.stdout
                    stages.append(first)
                    if not first.passed:
                        classification = "nondeterministic_result"
                        message = "Determinism command produced inconsistent output"
                if classification == "incomplete_solution" and not missing_docs:
                    classification = "accepted"
                    message = "All configured quality gates passed"
        breakdown = calculate_score(stages, config.weights)
        if missing_docs:
            breakdown["missing_documentation"] = missing_docs
            classification = "incomplete_solution"
            message = "Required candidate documentation is missing"
        accepted = classification == "accepted" and int(breakdown["score"]) >= config.acceptance_score
        if classification == "accepted" and not accepted:
            classification = "incomplete_solution"
            message = "Score is below the acceptance threshold"
        result = EvaluationResult(
            task_id=task_id,
            classification=classification,
            accepted=accepted,
            score=int(breakdown["score"]),
            acceptance_score=config.acceptance_score,
            dry_run=False,
            changed_files=changed,
            stages=stages,
            score_breakdown=breakdown,
            message=message,
        )
        if keep_candidate:
            workspaces.preserve_candidate(output / "candidate_workspace")
        emit_reports(output, result)
        return result
    finally:
        workspaces.close()


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Evaluate synthetic coding-agent patches")
    sub = root.add_subparsers(dest="command", required=True)
    evaluate_parser = sub.add_parser("evaluate", help="Evaluate one patch")
    evaluate_parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    evaluate_parser.add_argument("--task", required=True)
    evaluate_parser.add_argument("--patch", required=True, type=Path)
    evaluate_parser.add_argument("--output", required=True, type=Path)
    evaluate_parser.add_argument("--dry-run", action="store_true")
    evaluate_parser.add_argument("--keep-candidate", action="store_true")
    list_parser = sub.add_parser("list-tasks", help="List available tasks")
    list_parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    return root


def main(argv: Optional[List[str]] = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "list-tasks":
        for task in sorted((args.repo_root / "tasks").glob("task-*")):
            print(task.name)
        return 0
    result = evaluate(
        args.repo_root.resolve(),
        args.task,
        args.patch,
        args.output,
        args.dry_run,
        args.keep_candidate,
    )
    print(json.dumps({"classification": result.classification, "score": result.score}, sort_keys=True))
    return 0 if result.accepted or result.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
