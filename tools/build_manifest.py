#!/usr/bin/env python3
"""Write manifest.json: schema version, content version and a SHA-256 per content file.

Usage: python tools/build_manifest.py
The output is deterministic (no timestamps) so it only changes when content changes.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = ["kanji", "words", "articles", "strokes"]
SCHEMA_VERSION = 1


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def main() -> None:
    files = {}
    for folder in FOLDERS:
        for path in sorted((ROOT / folder).glob("*")):
            if path.is_file():
                files[path.relative_to(ROOT).as_posix()] = sha256(path)
    combined = hashlib.sha256(json.dumps(files, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    manifest = {"schemaVersion": SCHEMA_VERSION, "contentVersion": combined[:16], "files": files}
    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"manifest.json: {len(files)} files, version {manifest['contentVersion']}")


if __name__ == "__main__":
    main()
