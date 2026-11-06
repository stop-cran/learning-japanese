import hashlib
import json
import shutil
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-080-native" / "execution-543-receipts"
EVIDENCE = ROOT / "docs" / "n1-sources" / "execution-543.json"
LOGS = CONTROL / "logs" / "4d6594cd-479f-4796-871c-9b0e50f053c4"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


receipt = json.loads((LOGS / "issue-response-543.json").read_text(encoding="utf-8-sig"))
raw_body = (LOGS / "issue-body-543.txt").read_bytes().decode("utf-8")
assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == raw_body
assert raw_body.count("\r\n") == 8
evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
original = FOLDER / "execution-543.py"
preserved = FOLDER / "execution-543-before-receipt-fix.py"
assert not preserved.exists()
old_hash = sha(original)
shutil.copyfile(original, preserved)
shutil.copyfile(CONTROL / "execution-543.py", original)
shutil.copyfile(Path(__file__), FOLDER / Path(__file__).name)
evidence["checkpointReceiptDiagnostic"] = {
    "nativeEvidenceCommit": "b8050da4105382e11fe6b5bb54b5cc6b2136d0e9",
    "failure": "Python checkpoint receipt assertion used read_text universal-newline conversion, producing 1882 characters versus the exact 1890-character CRLF issue body. Owner/body POST and fresh readback checks had both passed.",
    "remedy": "Compare UTF8-decoded original bytes without newline conversion; no repost, no relaxed equality and no native rerun.",
    "ownerAndExactOriginalBodyReverified": True,
    "originalBodyCharacters": len(raw_body),
    "issueUpdate": receipt["html_url"],
    "originalExecutionRecipe": str(preserved.relative_to(ROOT)),
    "originalExecutionRecipeSha256": old_hash,
    "nativeRuntimeAndScreenshotEvidenceUnchanged": True,
    "checkpointParentCheck": "Allow normally signed descendant evidence-fix commit while retaining exact original starting BASE ancestry and unchanged runtime assertions.",
}
evidence["archivedExecutionRecipes"] = [
    {"path": str(path.relative_to(ROOT)), "sha256": sha(path)}
    for path in sorted(FOLDER.iterdir())
]
EVIDENCE.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Exact owner/body equality verified from raw UTF8; original failed recipe preserved; no repost.")
