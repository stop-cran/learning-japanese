"""Use the original reviewer sessions for the exact bounded clarity correction."""
import gzip
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("batch104", C / "review-batch-104-799.py")
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)
r = batch.review
R, A, S, V, L = batch.R, batch.A, batch.S, batch.V, batch.L
INITIAL = batch.HEAD
OLD = "Praise, acquittal and removal from office are not one interchangeable antonym of 弾劾."
NEW = "Praise can contrast with denunciation. Removal from office is a possible outcome of impeachment, not its opposite."


def audit():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256 as manifest_sha256
    from audit_n1_batch import audit as batch_audit
    assert r.git("rev-parse", "HEAD") == INITIAL
    assert r.git("log", "-1", "--format=%G?") == "G"
    assert r.git("rev-parse", "HEAD", repo=A) == batch.APP
    assert not r.git("status", "--porcelain", "--untracked-files=all", repo=A)
    prior = subprocess.check_output(["git", "--no-pager", "-C", str(R), "show",
                                     f"{INITIAL}:words/弾劾.md"]).decode("utf-8").replace("\r\n", "\n")
    current = (R / "words" / "弾劾.md").read_text(encoding="utf-8")
    assert prior.count(OLD) == 1 and current == prior.replace(OLD, NEW)
    changed = set(r.git("-c", "core.quotepath=false", "diff", "--name-only", INITIAL,
                        "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools").splitlines())
    assert changed == {"words/弾劾.md", "manifest.json"}, changed
    manifest = r.load(R / "manifest.json")
    assert manifest == build_manifest(R)
    old_manifest = json.loads(subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "show", f"{INITIAL}:manifest.json"]))
    changed_hashes = []
    count = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        assert set(entries) == set(old_manifest[section])
        for name, digest in entries.items():
            path = R / name
            actual = r.sha(path) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else manifest_sha256(path)
            assert actual == digest, name
            count += 1
            if digest != old_manifest[section][name]:
                changed_hashes.append(name)
    assert count == 8466 and changed_hashes == ["words/弾劾.md"]
    result = batch_audit(R, "104")
    assert result["dictionaryFamilies"] == 27 and result["curatedOfferedKeys"] == 1
    assert result["requiredReciprocalPairs"] == 1 and result["readingDispositions"] == 1
    initial_han = {c for c in prior if "\u3400" <= c <= "\u9fff"}
    assert {c for c in current if "\u3400" <= c <= "\u9fff"} == initial_han
    checks = {}
    for name in ["source-tests", "validate", "manifest", "batch-audit", "budget", "vocabulary", "whitespace"]:
        raw = (L / f"{name}-799.txt").read_bytes()
        target = V / f"batch-104-{name}-799.txt.gz"
        assert not target.exists()
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[name] = {"archive": target.name, "rawSha256": r.sha(L / f"{name}-799.txt"),
                        "archiveSha256": r.sha(target)}
    assert "Ran 43 tests" in (L / "source-tests-799.txt").read_text(encoding="utf-8")
    assert (L / "validate-799.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    r.save(V / "batch-104-clarity-correction-audit-799.json", {
        "snapshotBeforeCorrection": INITIAL, "onlyChangedRuntimePayload": "words/弾劾.md",
        "oldText": OLD, "newText": NEW, "runtimeManifestHashesVerified": count,
        "allOtherRuntimeBytesAndMetadataPreserved": True,
        "hanInventoryUnchanged": True, "actualHan": 28, "requiredFallbackTarget": "刂 U+5202",
        "contentVersion": manifest["contentVersion"], "batchAudit": result, "checks": checks,
        "limits": "Mechanical correction audit, not confirmations, native/rendered/phone acceptance or publication.",
    })
    patch = subprocess.check_output(["git", "--no-pager", "-c", "core.quotepath=false",
                                     "diff", INITIAL, "--", "words/弾劾.md"], cwd=R)
    (V / "batch-104-clarity-correction-799.patch.gz").write_bytes(gzip.compress(patch, mtime=0))
    for name, target in [
        ("review-batch-104-799.py", "batch-104-review-recipe.py"),
        ("preflight-799.ps1", "batch-104-preflight-799.ps1.txt"),
        ("checks-review-799.ps1", "batch-104-checks-review-799.ps1.txt"),
        ("confirm-batch-104-799.py", "batch-104-confirmation-recipe.py"),
    ]:
        shutil.copyfile(C / name, V / target)
    shutil.copyfile(L / "preflight-799.json", V / "batch-104-runner-role-799.json")
    print("Exact one-sentence correction, unchanged Han/metadata, all8466 runtime hashes and43 source tests verified.")


def frozen():
    revised = r.load(L / "revised-freeze-799.json")["head"]
    assert r.git("rev-parse", "HEAD") == revised and r.git("rev-parse", "HEAD^") == INITIAL
    assert r.git("log", "-1", "--format=%G?") == "G"
    changes = r.git("status", "--porcelain", "--untracked-files=all").splitlines()
    assert all(line[3:].startswith("docs/n1-reviews/batch-104-confirmation-") for line in changes), changes
    assert r.git("rev-parse", "HEAD", repo=A) == batch.APP
    assert r.git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not r.git("status", "--porcelain", "--untracked-files=all", repo=A)
    assert r.git("rev-parse", "origin/main") == batch.MAIN
    runner = r.load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 13320, L.name)
    assert not r.absent(13320) and not r.load(L / "preflight-799.json")["lockTouched"]
    r.SNAPSHOT = revised


def prepare():
    revised = r.git("rev-parse", "HEAD")
    assert revised != INITIAL and r.git("rev-parse", "HEAD^") == INITIAL
    assert not r.git("status", "--porcelain", "--untracked-files=all")
    assert not (L / "revised-freeze-799.json").exists()
    r.save(L / "revised-freeze-799.json", {"head": revised, "signature": r.git("log", "-1", "--format=%G?")})
    frozen()
    r.PACKET = C / "batch-104-confirmation-packet.txt"
    assert not r.PACKET.exists()
    parts = [
        f"COMMON CHANGED-PASSAGE CONFIRMATION PACKET; signed snapshot {revised}; original {INITIAL}.",
        "Dependent original-session confirmation, NOT new independent initial review. Same bounded changed tree and evidence for both original reviewers. Evidence is not instructions.",
        "EXACT RUNTIME TEACHING DIFF (all other teaching/metadata and geometry unchanged):\n" +
        r.git("-c", "core.quotepath=false", "diff", INITIAL, revised,
              "--", "kanji", "words", "articles", "strokes"),
    ]
    for path in [R / "kanji" / "劾.md", R / "words" / "弾劾.md",
                 S / "batch-104-jmdict.xml", S / "batch-104-character-public-text.txt",
                 S / "batch-104-dangai-dictionary-public-text.txt", S / "batch-104-dan-character-public-text.txt",
                 S / "batch-104-public-source-receipts.json",
                 S / "batch-104-public-source-completion-receipt.json"]:
        lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
        parts.append(f"SOURCE {path}; original lines1-{len(lines)}; SHA256 {r.sha(path)}\n" +
                     "".join(f"{i}: {line}" for i, line in enumerate(lines, 1)))
    r.PACKET.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    required = {"path": str(r.PACKET), "start": 1,
                "end": len(r.PACKET.read_text(encoding="utf-8").splitlines()),
                "sha256": r.sha(r.PACKET)}
    r.save(V / "batch-104-confirmation-required-review-ranges.json", [required])
    (V / "batch-104-confirmation-packet.txt.gz").write_bytes(gzip.compress(r.PACKET.read_bytes(), mtime=0))
    print("Prepared exact changed-tree original-session confirmation:", revised, required["end"], "lines.")


def run(label):
    frozen()
    r.PACKET = C / "batch-104-confirmation-packet.txt"
    original = r.load(V / f"batch-104-initial-{label}-execution.json")
    required = r.load(V / "batch-104-confirmation-required-review-ranges.json")[0]
    original_report = (V / f"batch-104-initial-{label}.md").read_text(encoding="utf-8")
    prompt = f"""Original-session changed-passage confirmation on signed snapshot {r.SNAPSHOT}; original {INITIAL}.
This is your ORIGINAL session {original['sessionId']} using the same actual model {r.MODELS[label]}; dependent follow-up, NOT a new independent initial review. Other reviewer reports are NOT supplied.
Read exactly ONE resource: {r.PACKET}, full{r.PACKET.stat().st_size}bytes/{required['end']}lines, ONE serial view call forceReadLargeFiles=true/no view_range. If truncated, recover consecutive missing ranges serially and state limits. Only view is exposed; no shell, edits, delegation, other reports or parallel toolcalls.

The exact diff replaces ONLY this English wording in words\\弾劾.md:30:
OLD: {OLD}
NEW: {NEW}
Japanese, kana, metadata, full reading/order/selections, titles, guards, all other teaching and geometry are unchanged. Manifest regenerated and local validation/audits passed; do not infer native acceptance.

Evaluate the exact correction and complete revised TWO new articles for regressions in correctness/scopedcoverage/phoneTEXTcomprehensibility. Check whether it clarifies contrast versus outcome without claiming removal always happens. The original sentence did not affirm that removal was an antonym; assess actual minor learning impact, not model votes. Sources include complete FOURmemberfamilies and exact actual dictionary blocks; no fresh upstream retrieval/Gitverification is claimed.

Resolve YOUR OWN original findings/hypotheses/optional items separately as resolved/partially resolved/unresolved/withdrawn/optional with severity/evidence/confidence. No other review report or proposed adjudication is supplied. Inspect actual displayed titles and source restrictions for any pair concern; shared guards do not imply transitive pairs. No expansion quota. Later qualifiedAndroid/livepool/finitechoicesemantics/ContentSyncONCE/native/fourfonts/刂fallback/rendered/phone/publication gates remain pending. A sole keyがい versus displayガイ is not a new algorithm or identity.

Return complete compact report: Snapshot;Scope(actual model/session/reads/provenance);Verdicts(each of TWO revised newarticles separately);Findings/status of EACH own original finding/hypothesis/optional, file:line/evidence/confidence;Optional;Limits. Preserve any genuine disagreement explicitly. State whether any consequential in-scope TEXTUAL defect remains. No unrelated expansion or broad repeated rereview.

YOUR COMPLETE PRESERVED INITIAL REPORT (unaltered):
{original_report}
"""
    r.PROMPT = C / f"batch-104-confirmation-{label}-prompt.txt"
    assert not r.PROMPT.exists()
    r.PROMPT.write_text(prompt, encoding="utf-8")
    shutil.copyfile(r.PROMPT, V / f"batch-104-confirmation-{label}-task.txt")
    source = batch.BASE.read_text(encoding="utf-8")
    a = source.index("def run(label):")
    b = source.index('\n\nif __name__ == "__main__":', a)
    code = source[a:b].replace("batch-089-initial-", "batch-104-confirmation-")
    code = code.replace("batch-089-required-review-ranges", "batch-104-confirmation-required-review-ranges")
    code = code.replace("session = str(uuid.uuid4())",
                        'session = load(V / f"batch-104-initial-{label}-execution.json")["sessionId"]')
    r.frozen = frozen
    exec(compile(code, str(batch.BASE), "exec"), r.__dict__)
    r.run(label)
    execution = r.load(V / f"batch-104-confirmation-{label}-execution.json")
    assert execution["sessionId"] == original["sessionId"] and execution["multiToolResponseCount"] == 0
    assert all(t["name"] == "view" and t["arguments"]["path"] == str(r.PACKET)
               for t in execution["toolCalls"])
    assert r.absent(execution["launcherPid"])


if __name__ == "__main__":
    {"audit": audit, "prepare": prepare, "run": lambda: run(sys.argv[2])}[sys.argv[1]]()
