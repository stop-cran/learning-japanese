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
p = load(s / "batch-058-publication.json")
assert p["acceptedCommit"] == "f6d192dba8862a4cb9097410ff630c2ee74aa55e"
assert p["ci"]["conclusion"] == "success"
dest = s / "batch-058-acceptance"
for path in [
    c / "artifacts" / "batch-058-accepted-ci.json",
    c / "artifacts" / "content-f6d192d-acceptance.json",
    c / "publish-batch-058.py",
    c / "push-batch-058.ps1",
    c / "verify-batch-058-publication.ps1",
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
    path = dest / f"execution-349-terminal-{name}.txt"
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
    ["git", "diff", "58b53fd31b6d55baba32c049fba62ac739feb004", "--",
     "kanji", "words", "articles", "strokes", "manifest.json", "tools"], cwd=r)
record = s / "batch-058-terminal-validation.json"
assert not record.exists()
record.write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
print("Accepted CI/public archive receipts staged; terminal validator/manifest/budget passed, runtime unchanged.")
