import json
from pathlib import Path
from r131_common import *

guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    for name in ("author-gates-001", "author-preservation-001"):
        summary = json.loads((HERE / name / "summary.json").read_text(encoding="utf8"))
        assert summary["status"] == "PASS"
        assert summary["parent"] == PARENT
    origin = git("remote", "get-url", "origin").decode().strip()
    assert origin in ("https://github.com/stop-cran/learning-japanese.git",
                      "https://github.com/stop-cran/learning-japanese")
    owner = [git("config", "user.name").decode().strip(), git("config", "user.email").decode().strip()]
    assert owner == ["Roman Konstantinovskiy", "stop-cran@list.ru"], owner
    assert git("show", "-s", "--format=%an%n%ae", PARENT).decode().splitlines() == owner
    signing_key = git("config", "user.signingkey").decode().strip()
    assert signing_key.upper() == "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
    assert not git("diff", "--cached", "--name-only")
    paths = ["kanji/衛.md", "kanji/霜.md", "manifest.json", "docs/n1-authoring-notes.md",
             "docs/n1-sources/batch-131-progress-reconciliation-001.json",
             "docs/n1-sources/batch-131-reconciliation"]
    git("add", "--sparse", "--", *paths)
    git("-c", "core.whitespace=cr-at-eol", "diff", "--cached", "--check")
    staged = [p for p in git("diff", "--cached", "--name-only", "-z").decode().split("\0") if p]
    hashes = {}
    for path in staged:
        guard.check()
        raw = git("show", ":" + path)
        local = (REPO / path).read_bytes()
        if path.startswith("docs/n1-sources/batch-131-reconciliation/"):
            assert raw == local, path
        else:
            assert raw == local.replace(b"\r\n", b"\n"), path
        hashes[path] = sha(raw)
    assert not git("diff", "--name-only")
    assert not git("ls-files", "--others", "--exclude-standard")
    write(HERE / "staging-001.json", {"status": "PASS", "parent": PARENT, "origin": origin,
                                     "owner": owner, "signingKey": signing_key,
                                     "stagedRawHashes": hashes,
                                     "producerSha256": sha(Path(__file__).read_bytes())})
    print(json.dumps({"stagedFiles": len(staged), "owner": owner, "origin": origin,
                      "rawNewEvidenceEquality": True}))
finally:
    write(HERE / "staging-memory-001.json", guard.finish())
