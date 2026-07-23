from __future__ import annotations

import re
from pathlib import Path


TEMP_PATH = re.compile(r"/(?:private/)?var/folders/[^\s:]+|/tmp/[^\s:]+")
HOME_PATH = re.compile(r"/(?:Users|home)/[^\s:]+")


def bounded_text(value: str, limit: int) -> str:
    encoded = value.encode("utf-8", errors="replace")
    if len(encoded) <= limit:
        return value
    marker = b"\n...[output truncated by evaluator]...\n"
    return (encoded[: max(0, limit - len(marker))] + marker).decode(
        "utf-8", errors="replace"
    )


def redact_paths(value: str, workspace: Path) -> str:
    rendered = TEMP_PATH.sub("<temporary-path>", value)
    rendered = rendered.replace(str(workspace), "<candidate-workspace>")
    return HOME_PATH.sub("<local-path>", rendered)
