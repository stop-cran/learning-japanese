"""Verify an immutable public archive against the accepted local runtime."""
import hashlib
import json
import stat
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent / "learning-japanese"
sys.path.insert(0, str(ROOT / "tools"))
from build_manifest import build_manifest
from check_content_budget import (
    CONTENT_FOLDERS, MAX_COMPRESSED, MAX_ENTRIES, MAX_INFLATED,
    MAX_RETAINED, MAX_TASK_MEDIA,
)


def verify(commit, archive_path, receipt_path):
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert head == commit, (head, commit)
    expected = build_manifest(ROOT)
    assert expected == json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    assert archive_path.stat().st_size <= MAX_COMPRESSED
    with zipfile.ZipFile(archive_path) as archive:
        rows = archive.infolist()
        names = [row.filename for row in rows]
        assert len(names) == len(set(names)) and len(names) <= MAX_ENTRIES
        roots = {name.split("/")[0] for name in names}
        assert len(roots) == 1
        prefix = roots.pop() + "/"
        assert prefix.endswith(commit[:7] + "/"), prefix
        payload = {}
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
            assert name and name.split("/")[0] not in {"docs", "tools", ".github"}
            data = archive.read(row)
            assert len(data) == row.file_size
            inflated += len(data)
            assert inflated <= MAX_INFLATED
            payload[name] = data
            pieces = name.split("/")
            wanted = name == "manifest.json" or len(pieces) == 2 and (
                pieces[0] in CONTENT_FOLDERS
                or pieces[0] == "images" and name.endswith(".webp"))
            if wanted:
                retained += len(data)
                limit = (150 * 1024 if pieces[0] in {"images", "task-images"} else
                         512 * 1024 if pieces[0] in {"audio", "task-audio"} else
                         2 * 1024 * 1024)
                assert len(data) <= limit, name
                if pieces[0] in {"task-audio", "task-images"}:
                    task_media += len(data)
            assert retained <= MAX_RETAINED and task_media <= MAX_TASK_MEDIA
        actual = json.loads(payload["manifest.json"])
        assert actual == expected
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
            "url": f"https://api.github.com/repos/stop-cran/learning-japanese/zipball/{commit}",
            "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
            "manifestEqual": True,
            "contentVersion": expected["contentVersion"],
            "verifiedRuntimeHashes": verified,
            "zipEntries": len(rows),
            "compressedBytes": archive_path.stat().st_size,
            "inflatedBytes": inflated,
            "retainedBytes": retained,
            "listeningTaskMediaBytes": task_media,
            "allPublishingBudgetsPassed": True,
            "contributorEvidenceExcluded": True,
            "perFileLimitsAndSafePathsPassed": True,
        }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
