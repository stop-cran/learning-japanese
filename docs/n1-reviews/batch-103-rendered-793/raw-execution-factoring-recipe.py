"""Losslessly factor repeated image payloads; reconstruct exact original stdout."""
import base64
import gzip
import hashlib
import json
from pathlib import Path
import shutil

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
W = C / "batch-103-rendered-793"
D = R / "docs" / "n1-reviews" / "batch-103-rendered-793"


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def save(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


index = load(D / "archive-integrity.json")
payloads = D / "image-payloads"
assert not payloads.exists()
payloads.mkdir()
factored = []
for label in ["claude", "gpt"]:
    source = W / (label + ".jsonl")
    raw = source.read_bytes()
    old = D / (label + ".jsonl.gz")
    assert gzip.decompress(old.read_bytes()) == raw
    transformed = []
    replacements = {}
    for line in raw.splitlines(keepends=True):
        event = json.loads(line)
        if event["type"] == "tool.execution_complete":
            result = event.get("data", {}).get("result", {})
            for item in result.get("binaryResultsForLlm", []):
                if item.get("type") == "image" and isinstance(item.get("data"), str):
                    encoded = item["data"].encode("ascii")
                    data = base64.b64decode(encoded, validate=True)
                    assert base64.b64encode(data) == encoded
                    digest = sha(data)
                    marker = ("__N1_IMAGE_PAYLOAD_SHA256_" + digest + "__").encode("ascii")
                    assert marker not in raw
                    assert encoded in line
                    target = payloads / (digest + ".png")
                    if target.exists():
                        assert target.read_bytes() == data
                    else:
                        target.write_bytes(data)
                    replacements[marker] = encoded
                    line = line.replace(encoded, marker)
        transformed.append(line)
    content = b"".join(transformed)
    restored = content
    for marker, encoded in replacements.items():
        restored = restored.replace(marker, encoded)
    assert restored == raw
    archive = D / (label + ".jsonl.factored.gz")
    assert not archive.exists()
    archive.write_bytes(gzip.compress(content, compresslevel=9, mtime=0))
    restored = gzip.decompress(archive.read_bytes())
    for marker, encoded in replacements.items():
        restored = restored.replace(marker, encoded)
    assert sha(restored) == sha(raw)
    row = {
        "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
        "factoredSha256": sha(content), "rawSha256": sha(raw), "rawBytes": len(raw),
        "archiveBytes": archive.stat().st_size,
        "payloadDirectory": "image-payloads",
        "payloadMarker": "__N1_IMAGE_PAYLOAD_SHA256_<sha256>__",
        "distinctPayloadsUsed": len(replacements),
        "reconstruction": "Decompress; replace every ASCII marker with canonical base64 of the named PNG; exact original stdout bytes/hash verified.",
    }
    original_rows = [r for r in index if r["archive"] == old.name]
    assert len(original_rows) == 1 and original_rows[0]["rawSha256"] == sha(raw)
    index[index.index(original_rows[0])] = row
    factored.append(row)
    old.unlink()
save(D / "archive-integrity.json", index)
payload_index = [{"file": str(p.relative_to(D)).replace("\\", "/"),
                  "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
                 for p in sorted(payloads.glob("*.png"))]
assert len(payload_index) == 33
save(D / "image-payload-index.json", payload_index)
receipt = {
    "mode": "Lossless exact-byte factoring, not event omission or source-image reconstruction.",
    "source": "Unmodified original raw stdout remains under approved control/batch-103-rendered-793.",
    "executions": factored, "distinctActualDeliveredPayloads": len(payload_index),
    "payloadBytes": sum(p["bytes"] for p in payload_index),
    "allOriginalRawBytesReconstructedExactly": True,
    "limits": "These900x2000 payloads preserve what view returned; they are NOT1080x2400 source images, a fresh review, or evidence of every model request's image retention.",
}
save(D / "raw-execution-packaging.json", receipt)
e = load(R / "docs" / "n1-sources" / "execution-793.json")
e["rawExecutionPackaging"] = receipt
e["validation"] = {
    "commands": [
        "python -B tools\\validate.py", "python -B tools\\build_manifest.py",
        "git diff --exit-code -- manifest.json", "git diff --check",
    ],
    "observedTerminalExitCode": 0, "validatorErrors": 0, "manifestFiles": 8463,
    "contentVersion": "38c32a8df5fd6063", "manifestUnchanged": True,
    "fullPythonOrAndroidOrNativeRerun": False,
}
save(R / "docs" / "n1-sources" / "execution-793.json", e)
shutil.copyfile(Path(__file__), D / "raw-execution-factoring-recipe.py")
save(W / "factoring-summary.json", {
    "factoredArchives": 2, "distinctActualPayloads": 33,
    "archiveBytes": sum(r["archiveBytes"] for r in index),
    "payloadBytes": receipt["payloadBytes"], "roundTripExact": True,
})
print(json.dumps(load(W / "factoring-summary.json")))
