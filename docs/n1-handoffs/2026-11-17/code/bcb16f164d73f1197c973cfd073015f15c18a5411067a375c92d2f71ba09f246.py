import json
from pathlib import Path

from common_134 import BASE, HERE, REPO, git, sha, start_guard, write

guard = start_guard()
try:
    head = git("rev-parse", "HEAD").decode().strip()
    assert head == "ba80afffc20a72d31be68b355b6f90aab36a5726"
    paths = git("diff", "--name-only", "-z", BASE, head).decode().strip("\0").split("\0")
    hashes = {}
    for path in paths:
        guard.check()
        committed = git("show", f"{head}:{path}")
        local = (REPO / path).read_bytes()
        assert committed == local, path
        hashes[path] = sha(committed)
    write(HERE / "committed-bytes-001.json", {
        "head": head, "base": BASE, "status": "PASS", "paths": hashes,
        "meaning": "Every changed contributor and runtime file exactly matches its signed commit blob bytes, not just Git's clean-filter comparison.",
        "producerSha256": sha(Path(__file__).read_bytes())})
finally:
    write(HERE / "committed-bytes-memory-001.json", guard.finish())
