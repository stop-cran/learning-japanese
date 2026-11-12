"""Download and verify the exact GitHub zipball of a pushed commit against the local runtime.

python n1_zipverify.py <repo-root> <commit> <out-dir>

The working tree at <repo-root> must be at <commit>. GH_TOKEN, when present, is sent only to
api.github.com (never to the redirect target) and is never printed or stored.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True

REPO = "stop-cran/learning-japanese"
EXPORT_IGNORED = {"docs", "tools", ".github"}


def download(commit: str, dest: Path) -> str:
    url = f"https://api.github.com/repos/{REPO}/zipball/{commit}"
    request = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json", "User-Agent": "n1-zipverify"})
    token = os.environ.get("GH_TOKEN")
    if token:
        request.add_unredirected_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=600) as response, dest.open("wb") as out:
        while chunk := response.read(1 << 20):
            out.write(chunk)
    return url


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=root)


def verify(root: Path, commit: str, out_dir: Path) -> dict:
    sys.path.insert(0, str(root / "tools"))
    from build_manifest import build_manifest
    from check_content_budget import (
        CONTENT_FOLDERS, MAX_COMPRESSED, MAX_ENTRIES, MAX_INFLATED, MAX_RETAINED, MAX_TASK_MEDIA)

    head = git(root, "rev-parse", "HEAD").decode().strip()
    assert head == commit, ("working tree is not at the commit", head, commit)
    expected = build_manifest(root)
    assert expected == json.loads((root / "manifest.json").read_text(encoding="utf-8"))

    out_dir.mkdir(parents=True, exist_ok=False)
    archive_path = out_dir / f"zipball-{commit[:12]}.zip"
    url = download(commit, archive_path)
    assert archive_path.stat().st_size <= MAX_COMPRESSED

    tree = git(root, "ls-tree", "-r", "-z", "--name-only", commit).decode("utf-8")
    tree_names = {n for n in tree.split("\0") if n and n.split("/")[0] not in EXPORT_IGNORED}

    with zipfile.ZipFile(archive_path) as archive:
        rows = archive.infolist()
        names = [row.filename for row in rows]
        assert len(names) == len(set(names)) and len(names) <= MAX_ENTRIES
        roots = {name.split("/")[0] for name in names}
        assert len(roots) == 1, roots
        prefix = roots.pop() + "/"
        assert prefix.endswith(commit[:7] + "/"), prefix
        payload: dict[str, bytes] = {}
        inflated = retained = task_media = 0
        for row in rows:
            parts = PurePosixPath(row.filename).parts
            assert not row.filename.startswith(("/", "\\")) and "\\" not in row.filename
            assert all(p not in {".", ".."} and ":" not in p for p in parts)
            assert not stat.S_ISLNK(row.external_attr >> 16)
            assert not row.flag_bits & 1
            assert row.filename.startswith(prefix)
            if row.is_dir():
                assert row.file_size == 0
                continue
            name = row.filename[len(prefix):]
            assert name and name.split("/")[0] not in EXPORT_IGNORED, name
            data = archive.read(row)
            assert len(data) == row.file_size
            inflated += len(data)
            assert inflated <= MAX_INFLATED
            payload[name] = data
            pieces = name.split("/")
            wanted = name == "manifest.json" or len(pieces) == 2 and (
                pieces[0] in CONTENT_FOLDERS or pieces[0] == "images" and name.endswith(".webp"))
            if wanted:
                retained += len(data)
                limit = (150 * 1024 if pieces[0] in {"images", "task-images"} else
                         512 * 1024 if pieces[0] in {"audio", "task-audio"} else 2 * 1024 * 1024)
                assert len(data) <= limit, name
                if pieces[0] in {"task-audio", "task-images"}:
                    task_media += len(data)
            assert retained <= MAX_RETAINED and task_media <= MAX_TASK_MEDIA
        assert set(payload) == tree_names, (
            sorted(set(payload) ^ tree_names)[:10], len(set(payload) ^ tree_names))
        manifest_bytes = payload["manifest.json"]
        assert json.loads(manifest_bytes) == expected
        verified = 0
        binary = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
        for section, entries in expected.items():
            if not isinstance(entries, dict):
                continue
            for name, digest in entries.items():
                data = payload[name]
                if section not in binary:
                    data = data.replace(b"\r\n", b"\n")
                assert hashlib.sha256(data).hexdigest() == digest, name
                verified += 1
        receipt = {
            "commit": commit,
            "url": url,
            "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
            "manifestEqual": True,
            "contentVersion": expected["contentVersion"],
            "manifestSha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "verifiedRuntimeHashes": verified,
            "zipEntries": len(rows),
            "zipFiles": len(payload),
            "compressedBytes": archive_path.stat().st_size,
            "inflatedBytes": inflated,
            "retainedBytes": retained,
            "listeningTaskMediaBytes": task_media,
            "zipNamesEqualExportedTree": True,
            "allPublishingBudgetsPassed": True,
            "contributorEvidenceExcluded": True,
            "perFileLimitsAndSafePathsPassed": True,
        }
    (out_dir / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    print(json.dumps(verify(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])), indent=2))
