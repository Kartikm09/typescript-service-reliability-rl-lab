"""Execute reference, starting-state, scope and behavioral-negative controls."""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
env = dict(os.environ, PYTHONPATH=str(root / 'evaluator/src'))
# A compile/lint/setup failure is never accepted as proof a behavioral negative worked.
behavior_stages = {
    'task-001': ('public_tests', 'held_out_tests'),
    'task-002': ('held_out_tests', 'held_out_tests'),
    'task-003': ('held_out_tests', 'public_tests'),
    'task-004': ('public_tests', 'regression_tests'),
}
for task in sorted((root / 'tasks').glob('task-*')):
    manifest = json.loads((task / 'baseline/manifest.json').read_text())
    for name, digest in manifest['files_sha256'].items():
        if hashlib.sha256((task / 'baseline/workspace' / name).read_bytes()).hexdigest() != digest:
            raise SystemExit(f'{task.name}: fixed baseline was changed: {name}')
    first, second = behavior_stages[task.name]
    cases = [
        ('golden/solution.patch', 'accepted', None),
        ('baseline/identity.patch', 'incomplete_solution' if task.name == 'task-002' else 'test_failure', None),
        ('incorrect_patches/malformed.patch', 'malformed_patch', None),
        ('incorrect_patches/prohibited-file.patch', 'prohibited_file_change', None),
        ('incorrect_patches/plausible-but-wrong.patch', 'test_failure', first),
        ('incorrect_patches/edge-case-regression.patch', 'regression_failure' if second == 'regression_tests' else 'test_failure', second),
    ]
    for relative, expected, failed_stage in cases:
        label = Path(relative).stem
        output = root / 'reports/evaluations' / task.name / label
        command = [sys.executable, '-m', 'rl_evaluator.cli', 'evaluate', '--repo-root', str(root),
                   '--task', task.name, '--patch', str(task / relative), '--output', str(output)]
        completed = subprocess.run(command, cwd=root, env=env, check=False)
        result = json.loads((output / 'result.json').read_text())
        if completed.returncode != (0 if result['accepted'] else 1):
            raise SystemExit(f'{task.name}/{label}: runner/result exit contradiction')
        if expected and result['classification'] != expected:
            raise SystemExit(f"{task.name}/{label}: {result['classification']} != {expected}")
        if relative != 'golden/solution.patch' and result['accepted']:
            raise SystemExit(f'incorrect patch accepted: {task.name}/{label}')
        if relative == 'baseline/identity.patch':
            failures = [stage for stage in result['stages'] if not stage['passed']]
            expected_stage = {'task-001': 'public_tests', 'task-002': 'lint', 'task-003': 'held_out_tests', 'task-004': 'held_out_tests'}[task.name]
            if len(failures) != 1 or failures[0]['name'] != expected_stage:
                raise SystemExit(f'{task.name}: baseline failed an unintended stage')
            output_text = failures[0]['stdout'] + failures[0]['stderr']
            if task.name == 'task-002':
                if "Property 'schedule' does not exist" not in output_text:
                    raise SystemExit('task-002: baseline did not fail its intentionally absent scheduling API')
            elif not re.search(r'(?:ℹ|#) fail [1-9][0-9]*', output_text):
                raise SystemExit(f'{task.name}: baseline did not fail a behavioral test')
        if failed_stage:
            failures = [stage for stage in result['stages'] if not stage['passed']]
            if len(failures) != 1 or failures[0]['name'] != failed_stage:
                raise SystemExit(f'{task.name}/{label}: did not fail intended behavioral stage {failed_stage}')
            output_text = failures[0]['stdout'] + failures[0]['stderr']
            if re.search(r'error TS[0-9]+', output_text) or not re.search(r'(?:ℹ|#) fail [1-9][0-9]*', output_text):
                raise SystemExit(f'{task.name}/{label}: no behavioral test-failure evidence; compile/setup rejection is insufficient')
print('four references accepted; four starting states, eight behavioral negatives and eight scope/syntax controls rejected')
