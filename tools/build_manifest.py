#!/usr/bin/env python3
"""Write manifest.json: schema version, content version and a SHA-256 per content file.

Usage: python tools/build_manifest.py
The output is deterministic (no timestamps) so it only changes when content changes.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = ["kanji", "words", "articles", "strokes", "counters", "grammar"]
SCHEMA_VERSION = 1


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def build_manifest(root: Path) -> dict:
    files = {}
    for folder in FOLDERS:
        for path in sorted((root / folder).glob("*")):
            if path.is_file():
                files[path.relative_to(root).as_posix()] = sha256(path)
    # Binary images are hashed byte-for-byte (no CRLF normalisation) and listed apart from `files`,
    # so apps that predate images ignore the unknown key instead of reporting every image as missing.
    images = {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((root / "images").glob("*")) if path.is_file()
    }
    scenes = {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted((root / "scenes").glob("*")) if path.is_file()
    }
    listening = {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted((root / "listening").glob("*.json")) if path.is_file()
    }
    audio = {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((root / "audio").glob("*.ogg")) if path.is_file()
    }
    curriculum = {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted((root / "curriculum").glob("*")) if path.is_file()
    }
    payloads = {"files": files}
    if images:
        payloads["images"] = images
    if scenes:
        payloads["scenes"] = scenes
    if listening:
        payloads["listening"] = listening
    if audio:
        payloads["audio"] = audio
    if curriculum:
        payloads["curriculum"] = curriculum
    for key, folder, pattern, binary in (
        ("listeningTasks", "listening-tasks", "*.json", False),
        ("listeningTaskAudio", "task-audio", "*.ogg", True),
        ("listeningTaskImages", "task-images", "*.webp", True),
    ):
        entries = {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() if binary else sha256(path)
            for path in sorted((root / folder).glob(pattern)) if path.is_file()
        }
        if entries:
            payloads[key] = entries
    combined = hashlib.sha256(
        json.dumps(payloads if len(payloads) > 1 else files, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return {"schemaVersion": SCHEMA_VERSION, "contentVersion": combined[:16], **payloads}


def main() -> None:
    manifest = build_manifest(ROOT)
    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    count = sum(len(manifest.get(key, {})) for key in (
        "files", "images", "scenes", "listening", "audio", "curriculum",
        "listeningTasks", "listeningTaskAudio", "listeningTaskImages",
    ))
    print(f"manifest.json: {count} files incl. {len(manifest.get('images', {}))} images, "
          f"{len(manifest.get('scenes', {}))} scene catalogs, {len(manifest.get('listening', {}))} listening passages, "
          f"{len(manifest.get('curriculum', {}))} curriculum catalogs, "
          f"{len(manifest.get('listeningTasks', {}))} listening tasks, "
          f"version {manifest['contentVersion']}")


if __name__ == "__main__":
    main()
