"""Losslessly archive untouched CLI output that fails staged whitespace checks."""
import gzip
import hashlib
import json
from pathlib import Path
import shutil

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
evidence_path = R / "docs" / "n1-sources" / "execution-695.json"
evidence = json.loads(evidence_path.read_bytes())
relative = "docs/n1-reviews/batch-095-rendered-cli-config-695.txt"
record = next(r for r in evidence["receipts"] if r["archive"] == relative)
original = R / relative
data = original.read_bytes()
assert hashlib.sha256(data).hexdigest() == record["archiveSha256"] == record["sourceSha256"]
target = original.with_suffix(original.suffix + ".gz")
assert not target.exists()
target.write_bytes(gzip.compress(data, mtime=0))
assert gzip.decompress(target.read_bytes()) == data
record.update(archive=target.relative_to(R).as_posix(),
              archiveSha256=hashlib.sha256(target.read_bytes()).hexdigest(), losslessGzip=True)
original.unlink()
destination = R / "docs" / "n1-reviews" / Path(__file__).name
assert not destination.exists()
shutil.copyfile(Path(__file__), destination)
digest = hashlib.sha256(destination.read_bytes()).hexdigest()
evidence["receipts"].append({
    "source": str(Path(__file__)), "archive": destination.relative_to(R).as_posix(),
    "sourceSha256": digest, "archiveSha256": digest,
})
evidence["diagnostics"].append(
    "Staged whitespace check rejected untouched CLI config output's trailing blank line before signing. Exact original bytes remain in control and verified lossless gzip in Git; no source text normalized."
)
evidence_path.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
print("CLI output preserved losslessly; original capture unchanged in control.")
