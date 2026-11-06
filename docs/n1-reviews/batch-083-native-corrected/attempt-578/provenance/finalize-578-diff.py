import hashlib
import json
import shutil
import subprocess
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
path = R / "docs" / "n1-reviews" / "batch-083-reconciliation.json"
current = json.loads(path.read_text(encoding="utf-8-sig"))
original = subprocess.check_output(
    ["git", "-C", str(R), "show", "HEAD:docs/n1-reviews/batch-083-reconciliation.json"]
).decode("utf-8").replace("\r\n", "\n").rstrip()
before = json.loads(original)
assert {k: v for k, v in current.items() if k != "correctedNativeAcceptance"} == {
    **before, "status": "corrected-native-passed-awaiting-original-family-visual-confirmation"
}
assert original.endswith("\n}")
old_status = '"status": "corrected-choice-textually-confirmed-awaiting-fresh-host-native"'
assert original.count(old_status) >= 1
text = original.replace(
    old_status, '"status": "corrected-native-passed-awaiting-original-family-visual-confirmation"', 1
)
addition = json.dumps({"correctedNativeAcceptance": current["correctedNativeAcceptance"]},
                      ensure_ascii=True, indent=2)
text = text[:-2] + ",\n" + addition[2:-2] + "\n}\n"
assert json.loads(text) == current
path.write_text(text, encoding="utf-8")
evidence_path = R / "docs" / "n1-sources" / "execution-578.json"
evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
target = R / "docs" / "n1-reviews" / "batch-083-native-corrected" / "attempt-578" / "provenance" / Path(__file__).name
assert not target.exists()
shutil.copyfile(__file__, target)
evidence["provenance"].append({
    "source": str(Path(__file__)), "archive": target.relative_to(R).as_posix(),
    "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
})
evidence_path.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
print("Preserved all historical reconciliation text; only status and new native receipt differ.")
