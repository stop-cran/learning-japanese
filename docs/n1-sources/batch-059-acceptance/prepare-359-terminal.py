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
p = load(s / "batch-059-publication.json")
assert p["acceptedCommit"] == "bdcad7c4b0aec217f42a0fdb880f7a364a49f34f"
assert p["ci"]["conclusion"] == "success"
dest = s / "batch-059-acceptance"
for path in [
    c / "artifacts" / "batch-059-accepted-ci.json",
    c / "artifacts" / "content-bdcad7c-acceptance.json",
    c / "publish-batch-059.py",
    c / "push-batch-059.ps1",
    c / "verify-batch-059-publication.ps1",
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
    path = dest / f"execution-359-terminal-{name}.txt"
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
    ["git", "diff", "769293c824dc41abb9386e76c4dd5f8c676e48e0", "--",
     "kanji", "words", "articles", "strokes", "manifest.json", "tools"], cwd=r)
record = s / "batch-059-terminal-validation.json"
assert not record.exists()
record.write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
print("Accepted CI/public archive receipts staged; terminal validator/manifest/budget passed, runtime unchanged.")
