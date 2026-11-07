"""Preserve original CLI output losslessly without tracked trailing whitespace."""
import gzip
import hashlib
import json
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
E = R / "docs" / "n1-sources" / "execution-706.json"
evidence = json.loads(E.read_bytes())
old = "docs/n1-reviews/batch-096-rendered-cli-config-706.txt"
record = next(row for row in evidence["receipts"] if row["archive"] == old)
source = Path(record["source"])
target = R / (old + ".gz")
assert not target.exists()
raw = source.read_bytes()
assert hashlib.sha256(raw).hexdigest() == record["sourceSha256"]
target.write_bytes(gzip.compress(raw, mtime=0))
assert gzip.decompress(target.read_bytes()) == raw
record.update(archive=old + ".gz", archiveSha256=hashlib.sha256(target.read_bytes()).hexdigest(),
              losslessGzip=True)
helper = R / "docs" / "n1-reviews" / Path(__file__).name
assert not helper.exists()
helper.write_bytes(Path(__file__).read_bytes())
digest = hashlib.sha256(helper.read_bytes()).hexdigest()
evidence["receipts"].append({
    "source": str(Path(__file__)), "archive": helper.relative_to(R).as_posix(),
    "sourceSha256": digest, "archiveSha256": digest,
})
evidence["diagnostics"] = [
    "Generated batch progress was formatted back to its original CRLF convention; only intended root fields changed.",
    "First staged diff-check detected the installed CLI config help's original blank EOF line. Original bytes retained in control and lossless deterministic gzip; no whitespace stripping or evidence loss. Full raw reviewer returns remain lossless gzip.",
]
E.write_text(json.dumps(evidence, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
