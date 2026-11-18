import json
import re
import sys
from pathlib import Path
from closure_common import *

directory = HERE / "staged-review-001"
require(not directory.exists(), "Preserve previous staged review")
directory.mkdir()
guard = start_guard()
try:
    head, tree = mode_tree("author")
    preservation = load(HERE / "author-preserve-001" / "summary.json")
    require(preservation["status"] == "PASS" and preservation["tree"] == tree, "Preservation mismatch")
    identities = load(HERE / "author-preserve-001" / "new-staged-blobs.json")
    require(identities == {path: value for path, value in tree_entries(tree).items() if path in identities},
            "Staged archive identities changed")
    patch = git("diff", "--cached", "--binary", PARENT)
    require(sha(patch) == preservation["patchSha256"], "Exact staged patch differs")
    write(directory / "complete-staged.patch", patch)
    copied_patch = ARCHIVE + "/verification/integration/committed-preserve-001/integration.patch"
    source = SCRATCH / "integration-001-author" / "handoff-001" / "evidence" / "committed-preserve-001" / "integration.patch"
    data = frozen(source)
    require(raw(REPO / copied_patch) == data, "Copied raw integration patch changed")
    code, timeout, stdout, stderr = command(
        ["git", "-c", "core.quotepath=false", "-c", "core.whitespace=cr-at-eol",
         "diff", "--cached", "--check"], directory / "all-file-whitespace", guard)
    require(not timeout and code in (0, 2), "Unexpected whitespace invocation failure")
    diagnostics = stdout.decode("utf-8").splitlines()
    exceptions = []
    for line in diagnostics:
        if line.startswith(ARCHIVE + "/"):
            match = re.fullmatch(re.escape(copied_patch) + r":(\d+): trailing whitespace\.", line)
            require(match is not None, "Unapproved authored/copied whitespace problem: " + line)
            number = int(match.group(1))
            content = data.splitlines()[number - 1]
            require(content.startswith((b" ", b"+", b"-")), "Exception not a raw unified-diff line")
            exceptions.append({"file": copied_patch, "sha256": sha(data), "line": number,
                               "lineBytesHex": content.hex(), "reason": "Byte-exact pre-existing unified-diff context; no normalization permitted."})
    code, timeout, _, _ = command(
        ["git", "-c", "core.quotepath=false", "-c", "core.whitespace=cr-at-eol",
         "diff", "--cached", "--check", "--", ".", ":(exclude)" + copied_patch],
        directory / "strict-authored-whitespace", guard)
    require(code == 0 and not timeout, "Strict authored-file whitespace lint failed")
    code, timeout, _, _ = command(
        [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(HERE), "-p", "test_closure.py", "-v"],
        directory / "focused-tests", guard)
    require(code == 0 and not timeout, "Focused closure tests failed")
    write(directory / "whitespace-exceptions.json", exceptions)
    write(directory / "reviewable-authored.patch", git("diff", "--cached", PARENT, "--",
          LEDGER, ARCHIVE + "/scope-and-lineage.md", ARCHIVE + "/provenance.json",
          ARCHIVE + "/validation-provenance.json"))
    require(mode_tree("author") == (head, tree), "Snapshot changed during staged review")
    write(directory / "summary.json", {
        "status": "PASS", "head": head, "tree": tree, "parent": PARENT,
        "completePatchSha256": sha(patch),
        "allNewStagedBlobIdentitiesVerified": len(identities),
        "identitiesSha256": preservation["newFilesInventorySha256"],
        "review": "Exact full staged binary patch equals the independently verified preserved tree. Every archive blob is byte-bound to its explicit inventory/source; original ledger values and scope/lineage metadata are checked structurally. Raw review inputs are confined to bounded attestations and lossless admitted source chains.",
        "strictAuthoredWhitespace": "PASS", "exactCopiedDiffExceptions": len(exceptions),
        "focusedTests": 4, "producerSha256": sha(raw(Path(__file__))),
    })
    print(json.dumps({"status": "PASS", "tree": tree, "newStagedBlobs": len(identities),
                      "rawDiffWhitespaceExceptions": len(exceptions)}))
finally:
    write(directory / "memory.json", guard.finish())
