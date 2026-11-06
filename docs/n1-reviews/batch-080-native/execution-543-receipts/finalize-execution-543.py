import gzip
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
NATIVE = ROOT / "docs" / "n1-reviews" / "batch-080-native"
EVIDENCE = ROOT / "docs" / "n1-sources" / "execution-543.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
assert "freshContentChecks" not in evidence
for name in ("adb-operations.txt", "emulator-stdout.txt"):
    path = NATIVE / "attempt-1" / name
    compressed = path.with_name(name[:-4] + ".raw.txt.gz")
    raw_hash = hashlib.sha256(gzip.decompress(compressed.read_bytes())).hexdigest()
    text = path.read_text(encoding="utf-8-sig")
    path.write_text("\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n", encoding="utf-8")
    row, = (r for r in evidence["archivedReceipts"] if r["path"] == str(path.relative_to(ROOT)))
    assert row["originalSha256"] == raw_hash
    assert row["compressedRawSha256"] == sha(compressed)
    row.update(sha256=sha(path), bytes=path.stat().st_size)
destination = NATIVE / "execution-543-receipts" / Path(__file__).name
assert not destination.exists()
shutil.copyfile(Path(__file__), destination)
assert sha(Path(__file__)) == sha(destination)
assert (NATIVE / "execution-543-validate.txt").read_text().strip() == "0 error(s)"
manifest_log = NATIVE / "execution-543-manifest.txt"
assert "8366 files" in manifest_log.read_text()
assert "version 4572f7b1d0d95059" in manifest_log.read_text()
assert sha(ROOT / "manifest.json") == evidence["manifestSha256"]
assert not subprocess.check_output(
    ["git", "--no-pager", "diff", "4033c82b7c1e7b690ccb2c9b510e04820fe1ba1a",
     "--", "kanji", "words", "articles", "strokes", "manifest.json"], cwd=ROOT
)
evidence["freshContentChecks"] = {
    "validatorErrors": 0, "manifestRegeneratedUnchanged": True,
    "receipts": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)}
                 for p in (NATIVE / "execution-543-validate.txt", manifest_log)],
}
evidence["archivedExecutionRecipes"] = [
    {"path": str(p.relative_to(ROOT)), "sha256": sha(p)}
    for p in sorted((NATIVE / "execution-543-receipts").iterdir())
]
evidence["diagnostics"] = [
    "Initial complete request summary encountered cp1252 UnicodeEncodeError only while printing the final checkpoint; complete file already decoded and checkpoint parsed. Subsequent UTF8 reads completed before mutation.",
    "Staged whitespace check identified terminal blank/trailing spaces in generated adb/emulator logs. Readable copies whitespace-normalized; exact original bytes retained in verified deterministic raw gzip and outside-Git attempt originals. Original PNG/JSON/instrumentation bytes unchanged.",
]
EVIDENCE.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Finalized native evidence, content-check receipts and exact raw-log provenance.")
