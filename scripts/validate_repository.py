from __future__ import annotations
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1];tasks=sorted((root/"tasks").glob("task-*"))
if len(tasks)!=4:raise SystemExit(f"expected four tasks, found {len(tasks)}")
required=["README.md","LICENSE","package.json","package-lock.json","Dockerfile","evaluator",".github/workflows/ci.yml"];missing=[p for p in required if not(root/p).exists()]
for task in tasks:
    for p in ["task.yaml","evaluator_config.json","golden/solution.patch","public_tests","held_out_tests"]:
        if not(task/p).exists():missing.append(str((task/p).relative_to(root)))
    json.loads((task/"evaluator_config.json").read_text())
if missing:raise SystemExit("missing: "+", ".join(missing))
print("repository structure validation passed")
