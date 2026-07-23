from __future__ import annotations
import re
from pathlib import Path
root=Path(__file__).resolve().parents[1];patterns=[re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),re.compile(r"gh[opusr]_[A-Za-z0-9]{20,}")];findings=[]
for path in root.rglob("*"):
    if not path.is_file() or any(part in {".git","node_modules","dist","dist-tests","coverage","reports"} for part in path.parts):continue
    try:text=path.read_text(encoding="utf-8")
    except UnicodeDecodeError:continue
    if any(pattern.search(text) for pattern in patterns):findings.append(str(path.relative_to(root)))
if findings:raise SystemExit("potential secrets: "+", ".join(findings))
print("secret scan passed")
