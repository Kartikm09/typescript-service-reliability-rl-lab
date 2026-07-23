from __future__ import annotations

import fnmatch
import hashlib
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Dict, List


DIFF_HEADER = re.compile(r"^diff --git a/(.+) b/(.+)$")


class PatchError(ValueError):
    pass


def parse_changed_paths(patch_text: str) -> List[str]:
    if "GIT binary patch" in patch_text or "new file mode 120000" in patch_text:
        raise PatchError("Binary patches and symbolic links are not supported")
    paths: List[str] = []
    for line in patch_text.splitlines():
        match = DIFF_HEADER.match(line)
        if not match:
            continue
        left, right = match.groups()
        if left != right:
            raise PatchError("Renames are not supported")
        candidate = PurePosixPath(left)
        if candidate.is_absolute() or ".." in candidate.parts or ".git" in candidate.parts:
            raise PatchError(f"Unsafe patch path: {left}")
        paths.append(left)
    if not paths:
        raise PatchError("Patch has no valid diff headers")
    if len(paths) != len(set(paths)):
        raise PatchError("Patch contains duplicate diff entries")
    return sorted(paths)


def prohibited_paths(paths: List[str], allowed_patterns: List[str]) -> List[str]:
    return [
        path
        for path in paths
        if not any(fnmatch.fnmatchcase(path, pattern) for pattern in allowed_patterns)
    ]


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence_before(workspace: Path, paths: List[str]) -> Dict[str, str | None]:
    return {path: sha256(workspace / path) for path in paths}


def apply_patch(workspace: Path, patch_path: Path) -> None:
    check = subprocess.run(
        ["git", "apply", "--check", "--whitespace=error-all", str(patch_path)],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    if check.returncode != 0:
        raise PatchError(check.stderr.strip() or "git apply --check failed")
    applied = subprocess.run(
        ["git", "apply", "--whitespace=error-all", str(patch_path)],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    if applied.returncode != 0:
        raise PatchError(applied.stderr.strip() or "git apply failed")
