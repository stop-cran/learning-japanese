import hashlib
import json
import subprocess
import sys
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
receipts = []
commands = [
    ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
    ("validate", ["tools\\validate.py"]),
    ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
    ("manifest", ["tools\\build_manifest.py"]),
    ("source-audit", [str(c / "audit-batch-058-acceptance.py")]),
    ("budget", ["tools\\check_content_budget.py"]),
]
for name, arguments in commands:
    path = c / "logs" / f"execution-349-{name}.txt"
    assert not path.exists(), path
    with path.open("wb") as stream:
        process = subprocess.run([sys.executable, "-X", "utf8", "-B", *arguments],
                                 cwd=r, stdout=stream, stderr=subprocess.STDOUT)
    receipts.append({
        "check": name, "command": ["python", "-X", "utf8", "-B", *arguments],
        "exitCode": process.returncode, "log": str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    })
    print(json.dumps(receipts[-1]), flush=True)
    if process.returncode:
        print(path.read_text(encoding="utf-8")[-6000:])
        raise SystemExit(process.returncode)
target = c / "artifacts" / "execution-349-validation-receipts.json"
assert not target.exists()
target.write_text(json.dumps(receipts, indent=2) + "\n", encoding="utf-8")
