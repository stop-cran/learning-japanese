import hashlib
import json
import shutil
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-080-native" / "execution-543-receipts"
EVIDENCE = ROOT / "docs" / "n1-sources" / "execution-543.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
assert evidence["articleRoute"]["contentVersion"] == "4572f7b1d0d95059"
assert "contentVersion" not in evidence
assert sha(CONTROL / "execution-543.py") == sha(FOLDER / "execution-543.py")
evidence["contentVersion"] = evidence["articleRoute"]["contentVersion"]
evidence["checkpointReceiptDiagnostic"]["summaryFieldCorrection"] = (
    "Second checkpoint finalization stopped before saving progress because the top-level "
    "contentVersion summary was absent although the exact value was already in articleRoute. "
    "Copied the verified route value into the summary and made checkpoint read articleRoute "
    "directly. No native evidence, issue comment, acceptance result or original history changed."
)
shutil.copyfile(Path(__file__), FOLDER / Path(__file__).name)
evidence["archivedExecutionRecipes"] = [
    {"path": str(path.relative_to(ROOT)), "sha256": sha(path)}
    for path in sorted(FOLDER.iterdir())
]
EVIDENCE.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Verified contentVersion summary populated from unchanged production route evidence.")
