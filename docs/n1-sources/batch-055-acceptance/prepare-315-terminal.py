import json
import shutil
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
s = r / "docs" / "n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
p = load(s / "batch-055-publication.json")
assert p["acceptedCommit"] == "37586858eefef6b9d07c14cd4efd77a9afa12576"
assert p["ci"]["conclusion"] == "success"
e = load(s / "execution-315.json")
e.update(publishedAdditions=82, remainingAdditions=1146)
(s / "execution-315.json").write_text(json.dumps(e, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
dest = s / "batch-055-acceptance"
for path in [
    c / "artifacts" / "batch-055-accepted-ci.json",
    c / "artifacts" / "content-3758685-acceptance.json",
    c / "publish-batch-055.py",
    c / "verify-batch-002-publication.py",
    Path(__file__),
]:
    assert not (dest / path.name).exists()
    shutil.copyfile(path, dest / path.name)
print("Verified accepted CI/public archive receipts staged for terminal signed evidence.")
