"""Preserve original mixed newlines outside generated ledger replacements."""
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
name = "docs/n1-sources/batch-095-progress.json"
path = R / name
original = subprocess.check_output(["git", "-C", str(R), "show", "HEAD:" + name]).decode("utf-8")
current = path.read_bytes().decode("utf-8")
before = original.splitlines(keepends=True)
after = current.splitlines(keepends=True)
plain = lambda lines: [line.rstrip("\r\n") for line in lines]
matcher = difflib.SequenceMatcher(a=plain(before), b=plain(after), autojunk=False)
for block in matcher.get_matching_blocks():
    after[block.b:block.b + block.size] = before[block.a:block.a + block.size]
result = "".join(after)
assert json.loads(result) == json.loads(current)
assert result.replace("\r\n", "\n") == current.replace("\r\n", "\n")
path.write_bytes(result.encode("utf-8"))
destination = R / "docs" / "n1-reviews" / Path(__file__).name
assert not destination.exists()
shutil.copyfile(Path(__file__), destination)
evidence_path = R / "docs" / "n1-sources" / "execution-695.json"
evidence = json.loads(evidence_path.read_bytes())
digest = hashlib.sha256(destination.read_bytes()).hexdigest()
evidence["receipts"].append({
    "source": str(Path(__file__)), "archive": destination.relative_to(R).as_posix(),
    "sourceSha256": digest, "archiveSha256": digest,
})
evidence["diagnostics"] = [
    "Ledger generator initially normalized historical mixed newlines. This formatter restored exact original newlines for every unchanged line, with identical parsed JSON and normalized text. Original generator archived unchanged."
]
evidence_path.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
print("Original unchanged-line newlines preserved; ledger JSON and normalized text unchanged.")
