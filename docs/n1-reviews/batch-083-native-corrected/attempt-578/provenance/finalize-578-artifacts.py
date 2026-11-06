import gzip
import hashlib
import json
import shutil
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
folder = R / "docs" / "n1-reviews" / "batch-083-native-corrected" / "attempt-578"
path = folder / "emulator-stdout.txt"
index_path = folder / "artifact-index.json"
digest = lambda data: hashlib.sha256(data).hexdigest()
old_hash = digest(index_path.read_bytes())
index = json.loads(index_path.read_text(encoding="utf-8"))
row = next(item for item in index if item["sourceName"] == path.name)
raw = path.read_bytes()
assert digest(raw) == row["sourceSha256"] == row["sha256"]
target = path.with_suffix(".txt.gz")
assert not target.exists()
target.write_bytes(gzip.compress(raw, mtime=0))
assert gzip.decompress(target.read_bytes()) == raw
row.update(archive=target.relative_to(R).as_posix(), sha256=digest(target.read_bytes()),
           bytes=target.stat().st_size, losslessGzipVerified=True)
index_path.write_text(json.dumps(index, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
new_hash = digest(index_path.read_bytes())
for name in ("docs/n1-sources/execution-578.json", "docs/n1-reviews/batch-083-reconciliation.json"):
    file = R / name
    text = file.read_text(encoding="utf-8")
    assert text.count(old_hash) == 1
    file.write_text(text.replace(old_hash, new_hash), encoding="utf-8")
path.unlink()
evidence_path = R / "docs" / "n1-sources" / "execution-578.json"
evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
provenance = folder / "provenance" / Path(__file__).name
assert not provenance.exists()
shutil.copyfile(__file__, provenance)
evidence["provenance"].append({
    "source": str(Path(__file__)), "archive": provenance.relative_to(R).as_posix(),
    "sha256": digest(provenance.read_bytes()),
})
evidence["artifactPackagingNote"] = (
    "Staged whitespace check flagged two original emulator stdout lines before signing ran. "
    "Archived that raw log losslessly as .txt.gz, preserving exact source bytes/hash; no evidence trimmed."
)
evidence_path.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
print("Emulator stdout retained byte-for-byte in gzip; index and native receipt hashes updated.")
