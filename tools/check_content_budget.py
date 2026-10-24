"""Check a complete publishable working tree against conservative Android archive budgets."""
from __future__ import annotations

import io
import subprocess
import zipfile
from pathlib import Path

MAX_RETAINED = 40 * 1024 * 1024
MAX_INFLATED = 80 * 1024 * 1024
MAX_COMPRESSED = 28 * 1024 * 1024
MAX_ENTRIES = 7000
MAX_TASK_MEDIA = 6 * 1024 * 1024
CONTENT_FOLDERS = {
    "kanji", "words", "articles", "strokes", "counters", "grammar", "scenes", "listening", "audio",
    "curriculum", "listening-tasks", "task-audio", "task-images",
}


def check(root: Path, names: list[str]) -> dict:
    retained = inflated = task_media = 0
    directories = {"repository/"}
    entries = []
    for name in sorted(set(names)):
        path = root / name
        if not path.is_file():
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"unsupported archive link/path: {name}")
        data = path.read_bytes()
        inflated += len(data)
        parts = name.split("/")
        directories.update("repository/" + "/".join(parts[:i]) + "/" for i in range(1, len(parts)))
        wanted = name == "manifest.json" or len(parts) == 2 and (
            parts[0] in CONTENT_FOLDERS or parts[0] == "images" and name.endswith(".webp"))
        if wanted:
            retained += len(data)
            limit = (150 * 1024 if parts[0] in {"images", "task-images"} else
                     512 * 1024 if parts[0] in {"audio", "task-audio"} else 2 * 1024 * 1024)
            if len(data) > limit:
                raise ValueError(f"{name}: exceeds per-file import limit {limit}")
            if parts[0] in {"task-audio", "task-images"}:
                task_media += len(data)
                if task_media > MAX_TASK_MEDIA:
                    raise ValueError("new unique audio/images exceed the combined 6 MiB budget")
        entries.append((name, data))
        if retained > MAX_RETAINED or inflated > MAX_INFLATED:
            raise ValueError("content exceeds retained/inflated archive headroom")
    if len(entries) + len(directories) > MAX_ENTRIES:
        raise ValueError("content exceeds archive entry headroom")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for directory in sorted(directories):
            archive.writestr(directory, b"")
        for name, data in entries:
            archive.writestr(f"repository/{name}", data)
    compressed = buffer.tell()
    if compressed > MAX_COMPRESSED:
        raise ValueError("content exceeds compressed archive headroom")
    return {"files": len(entries), "entries": len(entries) + len(directories),
            "retainedBytes": retained, "inflatedBytes": inflated, "localZipBytes": compressed,
            "listeningTaskMediaBytes": task_media}


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    names = subprocess.check_output(
        ["git", "ls-files", "-c", "-o", "--exclude-standard", "-z"], cwd=root,
    ).decode("utf-8").split("\0")
    print(check(root, [name for name in names if name]))


if __name__ == "__main__":
    main()
