import json
import subprocess
import sys
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
checks = [
    ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
    ("validate", [str(Path("tools") / "validate.py")]),
    ("vocabulary", [str(Path("tools") / "grammar_vocabulary.py"), "check"]),
    ("manifest", [str(Path("tools") / "build_manifest.py")]),
    ("budget", [str(Path("tools") / "check_content_budget.py")]),
]
receipts = []
for name, arguments in checks:
    path = control / "logs" / f"execution-234-{name}.txt"
    assert not path.exists(), path
    with path.open("wb") as stream:
        process = subprocess.run([sys.executable, "-X", "utf8", "-B", *arguments],
                                 cwd=root, stdout=stream, stderr=subprocess.STDOUT)
    receipts.append({"check": name, "exitCode": process.returncode, "log": str(path)})
    print(json.dumps(receipts[-1]), flush=True)
    if process.returncode:
        print(path.read_text(encoding="utf-8")[-6000:])
        raise SystemExit(process.returncode)
(control / "execution-234-validation-receipts.json").write_text(json.dumps(receipts, indent=2) + "\n", encoding="utf-8")
