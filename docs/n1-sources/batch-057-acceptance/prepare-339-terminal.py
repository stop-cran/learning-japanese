import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
s = r / "docs" / "n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
p = load(s / "batch-057-publication.json")
assert p["acceptedCommit"] == "a4b4f890e3769b5fc8fe23f3090867598e1f5352"
assert p["ci"]["conclusion"] == "success"
dest = s / "batch-057-acceptance"
for path in [
    c / "artifacts" / "batch-057-accepted-ci.json",
    c / "artifacts" / "content-a4b4f89-acceptance.json",
    c / "publish-batch-057.py",
    c / "push-batch-057.ps1",
    c / "verify-batch-057-publication.ps1",
    c / "verify-batch-028-publication.ps1",
    c / "verify-batch-002-publication.py",
    Path(__file__),
]:
    assert not (dest / path.name).exists()
    shutil.copyfile(path, dest / path.name)
checks = []
for name, arguments in [
    ("validate", ["tools\\validate.py"]),
    ("manifest", ["tools\\build_manifest.py"]),
    ("budget", ["tools\\check_content_budget.py"]),
]:
    path = dest / f"execution-339-terminal-{name}.txt"
    assert not path.exists()
    with path.open("wb") as stream:
        process = subprocess.run([sys.executable, "-X", "utf8", "-B", *arguments],
                                 cwd=r, stdout=stream, stderr=subprocess.STDOUT)
    checks.append({
        "command": ["python", "-X", "utf8", "-B", *arguments], "exitCode": process.returncode,
        "log": path.relative_to(r).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    })
    assert process.returncode == 0, path
assert not subprocess.check_output(
    ["git", "diff", "acc397033503a38aa88506fc3ad966761793db72", "--",
     "kanji", "words", "articles", "strokes", "manifest.json", "tools"], cwd=r)
record = s / "batch-057-terminal-validation.json"
assert not record.exists()
record.write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
print("Accepted CI/public archive receipts staged; terminal validator/manifest/budget passed, runtime unchanged.")
