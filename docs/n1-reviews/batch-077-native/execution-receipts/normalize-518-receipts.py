import gzip
import hashlib
import json
import shutil
from pathlib import Path

control = Path(__file__).resolve().parent
content = control.parent / "learning-japanese"
root = content / "docs" / "n1-reviews" / "batch-077-native"
record_path = content / "docs" / "n1-sources" / "execution-518.json"
record = json.loads(record_path.read_text(encoding="utf-8"))
paths = [
    root / "attempt-1" / "adb-operations.txt",
    root / "attempt-1" / "emulator-stdout.txt",
    root / "execution-receipts" / "run-518-native-expanded.ps1",
]
for path in paths:
    original = path.read_bytes()
    raw_path = path.with_name(path.name + ".raw.gz")
    assert not raw_path.exists()
    raw_path.write_bytes(gzip.compress(original, mtime=0))
    assert gzip.decompress(raw_path.read_bytes()) == original
    text = original.decode("utf-8-sig")
    normalized = "\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n"
    path.write_text(normalized, encoding="utf-8")
shutil.copy2(__file__, root / "execution-receipts" / Path(__file__).name)
existing = {row["path"]: row for row in record["artifacts"]}
artifacts = []
for directory in [root / "attempt-1", root / "execution-receipts"]:
    for path in sorted(directory.iterdir()):
        if path.is_file():
            relative = str(path.relative_to(content))
            row = existing.get(relative, {"path": relative})
            row.update(bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            artifacts.append(row)
record["artifacts"] = artifacts
record["diagnostics"] = [
    "Pre-signing staged whitespace check caught trailing spaces in two raw logs and a final blank in the expanded recipe. Readable copies normalized; exact original bytes preserved in adjacent .raw.gz files and control. No signing invoked before correction."
]
record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Readable receipts normalized; exact raw bytes retained and artifact hashes updated.")
