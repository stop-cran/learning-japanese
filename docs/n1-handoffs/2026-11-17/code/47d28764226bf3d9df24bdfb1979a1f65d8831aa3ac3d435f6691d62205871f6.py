"""Rebuild B134 packet identities for the published baseline, parent, and signed candidate."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
OUT = ROOT / "fresh-independent-002" / "projected-successor-008"
PACKET = OUT / "packet"
OLD_PACKET = ROOT / "neutral-preparation-001" / "projected-successor-001" / "packet"
REPO = WS / "b134-worktree"
PUBLISHED = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
PARENT = "ba80afffc20a72d31be68b355b6f90aab36a5726"
CANDIDATE = "355cccb840d22e7313e79f234eb93d1367e00352"


def git(*args):
    return subprocess.run(
        ["git", "-C", str(REPO), "-c", "core.quotepath=false", *args],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def put(relative, raw):
    path = PACKET / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw


def manifest_runtime_count(raw):
    manifest = json.loads(raw)
    groups = ("audio", "curriculum", "files", "images", "listening", "listeningTaskAudio",
              "listeningTaskImages", "listeningTasks", "scenes")
    return sum(len(manifest[name]) for name in groups), groups


def diff_body(raw):
    lines = raw.splitlines(keepends=True)
    start = next((index for index, line in enumerate(lines) if line.startswith(b"@@ ")), None)
    if start is None:
        raise RuntimeError("Diff has no unified hunk")
    result = []
    for line in lines[start:]:
        match = re.match(rb"(@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@)", line)
        result.append(match.group(1) + b"\n" if match else line)
    return b"".join(result)


def make_runtime_summary(before_raw, after_raw, before_id, after_id):
    before, after = json.loads(before_raw), json.loads(after_raw)
    groups = {}
    for name in ("audio", "curriculum", "files", "images", "listening", "listeningTaskAudio",
                 "listeningTaskImages", "listeningTasks", "scenes"):
        if before[name].keys() != after[name].keys():
            groups[name] = {
                "baseline": len(before[name]), "candidate": len(after[name]),
                "membershipChanged": True,
            }
        else:
            groups[name] = {
                "baseline": len(before[name]), "candidate": len(after[name]),
                "unchanged": sum(before[name][key] == after[name][key] for key in before[name]),
                "membershipChanged": False,
            }
    return {
        "status": "SIGNED_MANIFEST_PRESERVATION_SUMMARY_NOT_SEMANTIC_ACCEPTANCE",
        "scope": f"{before_id}-to-{after_id}",
        "baselineManifestSha256": digest(before_raw),
        "candidateManifestSha256": digest(after_raw),
        "baselineEntries": manifest_runtime_count(before_raw)[0],
        "candidateEntries": manifest_runtime_count(after_raw)[0],
        "groups": groups,
        "limits": "Mechanical manifest membership/value comparison only; not content, semantic, or runtime acceptance.",
    }


def main():
    sums_path = PACKET / "SHA256SUMS.json"
    if not sums_path.is_file():
        raise RuntimeError("The copied packet seed is missing")

    e17_support = git("show", f"{PUBLISHED}:words/紫.md")
    parent_support = git("show", f"{PARENT}:words/紫.md")
    candidate_support = git("show", f"{CANDIDATE}:words/紫.md")
    parent_card = git("show", f"{PARENT}:kanji/紫.md")
    candidate_card = git("show", f"{CANDIDATE}:kanji/紫.md")
    if digest(parent_card) != "3278c3e8a47dbcf86302e08441eb84d2b59e0166c769a98acccbe9218640aa35":
        raise RuntimeError("Parent target card differs from verified identity")
    if digest(candidate_card) != "7ad1f9736e86dbd8da9abd54dc3a08c3d144f451292ea82d1f3a5b0f5e8f058b":
        raise RuntimeError("Candidate target card differs from verified identity")
    published_to_parent_support_diff = git(
        "diff", "--no-ext-diff", "--unified=3", PUBLISHED, PARENT, "--", "words/紫.md")
    parent_to_candidate_card_diff = git(
        "diff", "--no-ext-diff", "--unified=3", PARENT, CANDIDATE, "--", "kanji/紫.md")
    e17_manifest = git("show", f"{PUBLISHED}:manifest.json")
    parent_manifest = git("show", f"{PARENT}:manifest.json")
    candidate_manifest = git("show", f"{CANDIDATE}:manifest.json")
    e17_paths = set(git("ls-tree", "-r", "--name-only", PUBLISHED, "--", "kanji").decode().splitlines())
    parent_paths = set(git("ls-tree", "-r", "--name-only", PARENT, "--", "kanji").decode().splitlines())
    candidate_paths = set(git("ls-tree", "-r", "--name-only", CANDIDATE, "--", "kanji").decode().splitlines())
    if "kanji/紫.md" in e17_paths or "kanji/紫.md" not in parent_paths or "kanji/紫.md" not in candidate_paths:
        raise RuntimeError("Target-card commit membership differs")
    if len(e17_paths) != 1261 or len(parent_paths) != 1262 or len(candidate_paths) != 1262:
        raise RuntimeError("Kanji article inventory differs")

    if digest(e17_support) != "14db0466741ec80b0dc5e78e4f187c8ba2adfbddd519a2dcfecc562ff068e300":
        raise RuntimeError("Published support source differs from verified identity")
    if digest(parent_support) != "b7acdf54c18ff78abe0aee53478fa9d782fb9668bca5956815161445a62b4e86":
        raise RuntimeError("Parent support source differs from verified identity")
    if candidate_support != parent_support:
        raise RuntimeError("Candidate support article changed relative to its reconciliation parent")
    if digest(e17_manifest) != "f29fd2000d9ae078382df44711e3af1b5b5e81424160f5ab06c74ec8a416a11a":
        raise RuntimeError("Published manifest differs from verified identity")
    if digest(parent_manifest) != "2a3373ec1a529cfcd8f1b1bc5686915e4335facc62a1f593b94ed26914273a77":
        raise RuntimeError("Parent manifest differs from verified identity")
    if digest(candidate_manifest) != "d16cf5a73bcfd6f837bfab1b92ce7e8d683a5baf57610357ae9cf3c0a6493ca3":
        raise RuntimeError("Candidate manifest differs from verified identity")

    # Keep every revision-specific teaching source under a path labeled with its actual identity.
    put("baseline/words/紫.md", e17_support)
    put("parent/words/紫.md", parent_support)
    put("snapshot/words/紫.md", candidate_support)
    put("parent/kanji/紫.md", parent_card)
    put("snapshot/kanji/紫.md", candidate_card)
    if diff_body((PACKET / "diffs" / "existing.diff").read_bytes()) != diff_body(published_to_parent_support_diff):
        raise RuntimeError("Existing-support diff does not equal published-baseline-to-parent")
    if diff_body((PACKET / "diffs" / "reconciliation-card.diff").read_bytes()) != diff_body(parent_to_candidate_card_diff):
        raise RuntimeError("Card diff does not equal signed parent-to-candidate diff")
    put("baseline/manifest.json", e17_manifest)
    put("parent/manifest.json", parent_manifest)
    put("repo/manifest.json", candidate_manifest)
    stale_baseline_card = PACKET / "baseline" / "kanji" / "紫.md"
    if stale_baseline_card.exists():
        stale_baseline_card.unlink()

    candidate_index = (PACKET / "evidence" / "title-index.txt").read_bytes()
    parent_index = (PACKET / "evidence" / "baseline-title-index.txt").read_bytes()
    published_index = (OLD_PACKET / "evidence" / "baseline-title-index.txt").read_bytes()
    line = "紫 purple; violet\n".encode("utf-8")
    if candidate_index != parent_index or candidate_index.count(line) != 1:
        raise RuntimeError("Parent/candidate title indexes are not byte-identical with one target line")
    if candidate_index.replace(line, b"", 1) != published_index:
        raise RuntimeError("Published title index is not the exact one-line reconstruction")
    if len(published_index.splitlines()) != 1261 or len(parent_index.splitlines()) != 1262:
        raise RuntimeError("Title index line counts differ")

    put("evidence/published-title-index-e17.txt", published_index)
    put("evidence/parent-title-index-ba80.txt", parent_index)
    old_delta = json.loads((OLD_PACKET / "evidence" / "baseline-title-delta.json").read_text(encoding="utf-8"))
    old_delta.update({
        "representation": "Published e17 index reconstructed byte-exactly from the complete ba80 parent index by deleting the one candidate card title.",
        "baselineCommit": PUBLISHED,
        "candidateCommit": PARENT,
        "candidateSource": "evidence/parent-title-index-ba80.txt",
        "candidateSha256": digest(parent_index),
        "baselineSha256": digest(published_index),
        "reconstructedBaselineSha256": digest(published_index),
        "baselineLines": 1261,
        "candidateLines": 1262,
        "originalBaseline": "evidence/published-title-index-e17.txt",
        "exactByteReconstructionVerified": True,
        "signedCandidateCommit": CANDIDATE,
        "signedCandidateIndexSha256": digest(candidate_index),
        "reconciliationParentIndexSha256": digest(parent_index),
        "reconciliationParentAndCandidateIndexesByteEqual": parent_index == candidate_index,
    })
    put("evidence/baseline-title-delta.json", json_bytes(old_delta))
    parent_candidate_delta = {
        "baselineCommit": PARENT,
        "candidateCommit": CANDIDATE,
        "baselineSource": "evidence/parent-title-index-ba80.txt",
        "candidateSource": "evidence/title-index.txt",
        "baselineSha256": digest(parent_index),
        "candidateSha256": digest(candidate_index),
        "baselineLines": 1262,
        "candidateLines": 1262,
        "removedCompleteLinesUtf8": [],
        "addedCompleteLinesUtf8": [],
        "byteEqual": parent_index == candidate_index,
        "limits": "Title index identity comparison only; the candidate and reconciliation parent are separate sources despite equal bytes.",
    }
    put("evidence/reconciliation-title-delta.json", json_bytes(parent_candidate_delta))

    e17_entries, group_names = manifest_runtime_count(e17_manifest)
    parent_entries, _ = manifest_runtime_count(parent_manifest)
    candidate_entries, _ = manifest_runtime_count(candidate_manifest)
    if (e17_entries, parent_entries, candidate_entries) != (8745, 8747, 8747):
        raise RuntimeError("Runtime manifest entry counts differ")

    put("evidence/published-baseline-identity.json", json_bytes({
        "commit": PUBLISHED, "kanjiArticles": 1261, "kanjiPurpleArticle": "absent",
        "supportArticle": "baseline/words/紫.md", "supportArticleSha256": digest(e17_support),
        "manifest": "baseline/manifest.json", "manifestSha256": digest(e17_manifest),
        "runtimeEntries": e17_entries, "titleIndex": "evidence/published-title-index-e17.txt",
        "titleIndexSha256": digest(published_index), "titleIndexLines": 1261,
        "source": "Direct signed published commit membership and manifest; title index exact one-line reconstruction.",
    }))
    put("evidence/reconciliation-parent-identity.json", json_bytes({
        "commit": PARENT, "kanjiArticles": 1262, "kanjiPurpleArticle": "parent/kanji/紫.md",
        "kanjiPurpleSha256": digest(parent_card), "supportArticle": "parent/words/紫.md",
        "supportArticleSha256": digest(parent_support), "manifest": "parent/manifest.json",
        "manifestSha256": digest(parent_manifest), "runtimeEntries": parent_entries,
        "titleIndex": "evidence/parent-title-index-ba80.txt",
        "titleIndexSha256": digest(parent_index), "titleIndexLines": 1262,
        "source": "Direct signed reconciliation-parent commit contents.",
    }))
    put("checks/published-baseline-runtime-summary.json",
        json_bytes(make_runtime_summary(e17_manifest, candidate_manifest, PUBLISHED, CANDIDATE)))
    published_runtime = make_runtime_summary(e17_manifest, candidate_manifest, PUBLISHED, CANDIDATE)
    parent_runtime = make_runtime_summary(parent_manifest, candidate_manifest, PARENT, CANDIDATE)
    put("checks/full-runtime-summary.json", json_bytes({
        "status": "THREE_IDENTITY_SIGNED_MANIFEST_PRESERVATION_SUMMARY_NOT_SEMANTIC_ACCEPTANCE",
        "publishedBaseline": published_runtime,
        "reconciliationParent": parent_runtime,
        "limits": "Mechanical manifest membership/value comparisons only; not content, semantic, or runtime acceptance.",
    }))

    packet_meta = json.loads((PACKET / "packet.json").read_text(encoding="utf-8"))
    packet_meta.update({
        "candidate": CANDIDATE, "base": PARENT, "publishedBaseline": PUBLISHED,
        "reconciliationParent": PARENT,
        "baselineKanjiArticles": 1261, "reconciliationParentKanjiArticles": 1262,
        "candidateKanjiArticles": 1262, "publishedBaselineRuntimeEntries": e17_entries,
        "baselineRuntimeEntries": parent_entries, "candidateRuntimeEntries": candidate_entries,
        "publishedBaselineManifestSha256": digest(e17_manifest),
        "reconciliationParentManifestSha256": digest(parent_manifest),
        "manifestSha256": digest(candidate_manifest),
        "contentVersion": json.loads(candidate_manifest)["contentVersion"],
        "baselineMeaning": "published e17 commit; no 紫 card",
        "parentMeaning": "ba80 reconciliation parent; existing 紫 card",
        "supportSources": {
            "publishedBefore": {"path": "baseline/words/紫.md", "sha256": digest(e17_support)},
            "parentAfter": {"path": "parent/words/紫.md", "sha256": digest(parent_support)},
            "candidateAfter": {"path": "snapshot/words/紫.md", "sha256": digest(candidate_support)},
        },
        "titleIndexSources": {
            "published": {"path": "evidence/published-title-index-e17.txt",
                          "sha256": digest(published_index), "lines": 1261},
            "parent": {"path": "evidence/parent-title-index-ba80.txt",
                       "sha256": digest(parent_index), "lines": 1262},
            "candidate": {"path": "evidence/title-index.txt",
                          "sha256": digest(candidate_index), "lines": 1262},
        },
    })
    put("packet.json", json_bytes(packet_meta))

    provenance_path = PACKET / "evidence" / "provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    provenance["publishedBaselineCommit"] = PUBLISHED
    provenance["publishedBaselineManifestSha256"] = digest(e17_manifest)
    provenance["reconciliationParentCommit"] = PARENT
    provenance["reconciliationParentManifestSha256"] = digest(parent_manifest)
    provenance["publishedBaselineSupportSha256"] = digest(e17_support)
    provenance["reconciliationParentSupportSha256"] = digest(parent_support)
    provenance["candidateSupportSha256"] = digest(candidate_support)
    provenance["publishedBaselineTitleIndexSha256"] = digest(published_index)
    provenance["reconciliationParentTitleIndexSha256"] = digest(parent_index)
    provenance["candidateTitleIndexSha256"] = digest(candidate_index)
    put("evidence/provenance.json", json_bytes(provenance))

    binding_path = PACKET / "evidence" / "signed-reconciliation-binding.json"
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    binding.update({
        "publishedBaselineCommit": PUBLISHED,
        "publishedBaselineManifestSha256": digest(e17_manifest),
        "publishedBaselineSupportSha256": digest(e17_support),
        "publishedBaselineTitleIndexSha256": digest(published_index),
        "reconciliationParentTitleIndexSha256": digest(parent_index),
        "reconciliationParentAndCandidateIndexesByteEqual": parent_index == candidate_index,
        "publishedTitleIndexRepresentation": "1261-line published e17 index; exact one-line deletion from parent index.",
    })
    put("evidence/signed-reconciliation-binding.json", json_bytes(binding))

    disclosure = f"""# B134 neutral review packet

This packet distinguishes three immutable content identities: published baseline `{PUBLISHED}`, reconciliation parent `{PARENT}`, and signed candidate `{CANDIDATE}`. The published baseline has 1,261 kanji articles and no `kanji/紫.md`; the reconciliation parent and signed candidate each have 1,262 kanji articles. The target card and its parent version are separately labeled, and the candidate card is bound to the signed revision.

The complete published `words/紫.md` is preserved at `baseline/words/紫.md` (SHA-256 `{digest(e17_support)}`). The complete reconciliation-parent version is at `parent/words/紫.md` (SHA-256 `{digest(parent_support)}`), and the signed candidate version is separately preserved at `snapshot/words/紫.md` (SHA-256 `{digest(candidate_support)}`). The parent and candidate support articles are byte-identical; `diffs/existing.diff` separately preserves the published-baseline-to-parent support wrapper change. `diffs/reconciliation-card.diff` is the exact parent-to-candidate card revision.

The full published 1,261-line title index is preserved at `evidence/published-title-index-e17.txt` and reconstructed byte-exactly by deleting the single `紫 purple; violet` line from the complete 1,262-line parent index. The parent index is at `evidence/parent-title-index-ba80.txt`; the signed candidate index remains at `evidence/title-index.txt`. Parent and candidate index bytes are equal, and their separate identity and hash bindings are explicit.

All 522 unique complete JMdict families and all 85 unique complete KANJIDIC2 records are retained, with canonical-equal overlaps merged only after exact full-record equality. The original 399/59 selection membership, every original predicate and zero-match record, all supplemental predicates, and complete membership indexes are preserved. The bounded review core uses only the established KD field projection if the full-record trial does not pass; every complete union record remains separately available as an optional unit, together with the three full derived-index units. No other source reduction is authorized.

All 1,262 candidate kanji articles, curated `古`, `右`, and `川` articles, title indexes, complete native captures, final committed host gates, and source proofs are retained. The candidate's exclusion set contains 56 characters. Author response, original reports/verdicts, report-derived assertions, pair dispositions/reasons, scan matches, and comparison recommendations are excluded from reviewer inputs.

Capacity figures are conservative forecasts, not tokenizer measurements. The startup gate remains 700,000 with 80,000 bootstrap, 30,000 report, and 20,000 shared optional allowance. Permitted caps remain D25/E10, D20/E10, D15/E10, D10/E10, D10/E5 in order. All actual-telemetry and explicit long-context admission checks remain mandatory; the current forecast decision is HOLD and does not authorize reviewer launch.

This is preparation only. It makes no teaching, native/device, rendering, whole-set, or publication acceptance claim; no reviewer is launched by this packet.
"""
    put("REVIEW.md", disclosure.encode("utf-8"))
    put("DISCLOSURE.txt", disclosure.encode("utf-8"))

    core_path = ROOT / "fresh-independent-002" / "projected-successor-007" / "core-sources-001.json"
    core = json.loads(core_path.read_text(encoding="utf-8"))
    names = [("parent/kanji/紫.md" if name == "baseline/kanji/紫.md" else name)
             for name in core["sources"]]
    for name in names:
        if not (PACKET / name).is_file():
            raise RuntimeError("Core source is missing: " + name)
    core["publishedBaseline"] = PUBLISHED
    core["candidate"] = CANDIDATE
    core["base"] = PARENT
    core["sources"] = names
    core.pop("segments", None)
    core.pop("sourceBindings", None)
    (OUT / "core-sources-003.json").write_bytes(json_bytes(core))

    sums = {
        path.relative_to(PACKET).as_posix(): digest(path.read_bytes())
        for path in sorted(PACKET.rglob("*")) if path.is_file() and path.name != "SHA256SUMS.json"
    }
    put("SHA256SUMS.json", json_bytes(sums))
    print(json.dumps({
        "status": "PACKET_IDENTITIES_REBUILT",
        "candidate": CANDIDATE, "reconciliationParent": PARENT, "publishedBaseline": PUBLISHED,
        "articles": {"published": len(e17_paths), "parent": len(parent_paths), "candidate": len(candidate_paths)},
        "runtimeEntries": {"published": e17_entries, "parent": parent_entries, "candidate": candidate_entries},
        "titleIndexes": {
            "published": {"lines": 1261, "sha256": digest(published_index)},
            "parent": {"lines": 1262, "sha256": digest(parent_index)},
            "candidate": {"lines": 1262, "sha256": digest(candidate_index)},
        },
        "packetFiles": len(sums), "packetManifestSha256": digest((PACKET / "SHA256SUMS.json").read_bytes()),
        "coreSources": len(names),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
