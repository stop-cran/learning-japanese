"""Verify prepared integration code/dependency pins without opening any repository."""
import hashlib
import json
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOLS = Path(r"C:\Users\stop-\n1-kanji-workspace\review-tools")


def verify(path, expected, readonly):
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError("Prepared input changed: " + str(path))
    if readonly and path.stat().st_mode & stat.S_IWRITE:
        raise ValueError("Prepared input became writable: " + str(path))


def main():
    new = json.loads((ROOT / "tool-inventory.json").read_bytes())["files"]
    dependencies = json.loads((ROOT / "dependency-inventory.json").read_bytes())["files"]
    for name, digest in {**dependencies, **new}.items():
        if Path(name).name != name:
            raise ValueError("Invalid prepared tool name")
        verify(TOOLS / name, digest, name in new)
    review = ROOT.parent
    verify(review / "guarded-test-v3.py",
           "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283", True)
    verify(Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-115\confirm\ram-guard\verify-zip-streaming.py"),
           "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84", True)
    print(json.dumps({"status": "PASS_PREPARED_INPUT_HASHES_ONLY",
                      "newTools": len(new), "dependencies": len(dependencies)}))


if __name__ == "__main__":
    main()
