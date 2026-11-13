"""Update the source ledger after the accepted evidence archive has been verified."""
import hashlib
import json
from pathlib import Path

REPO = Path(r"C:\Users\stop-\n1-kanji-workspace\rollout-recovered\learning-japanese")
ROOT = REPO / "docs/n1-reviews/batch-114-closure"
LEDGER = REPO / "docs/n1-sources/batch-114-progress.json"
FIX = "1c2b2c6a6658fa968f724657868ccae1eb61b198"


def main():
    provenance = json.loads((ROOT / "provenance.json").read_bytes())
    for path, info in provenance["files"].items():
        data = (ROOT / path).read_bytes()
        assert len(data) == info["bytes"]
        assert hashlib.sha256(data).hexdigest() == info["sha256"], path
    reports = []
    for run in provenance["runs"]:
        adj = json.loads((ROOT / "adjudications" / (run["id"] + ".json")).read_bytes())
        assert adj["status"] == "ACCEPTED_AS_REVIEW_EVIDENCE"
        if run["id"].startswith("delta-"):
            assert adj["confirmationVerdict"] in ("CONFIRMED", "UNVERIFIED")
            assert adj["remainingActionableFindings"] == []
        reports.append({
            "id": run["id"], "actualModels": run["actualModels"],
            "snapshot": run["snapshot"], "reportSha256": run["reportSha256"],
            "report": f"../n1-reviews/batch-114-closure/reports/{run['id']}.md",
            "confirmationVerdict": run["confirmationVerdict"],
        })
    ledger = json.loads(LEDGER.read_bytes())
    assert ledger["status"] == "drafted-validated-awaiting-independent-review"
    ledger["status"] = "review-closed-awaiting-publication"
    ledger["reviewClosed"] = ledger["membership"]
    ledger["accounting"].update(
        localDoneIncludingN2Placements=231, localInProgress=0, localNotStarted=997,
        note="All fifteen B114 cards are textually review-closed. Publication remains pending; "
             "published totals remain 210 N1 additions plus six N2 placements, 1,012 not delivered."
    )
    ledger["draftRuntimeCandidate"] = ledger["runtimeCandidate"]
    manifest_bytes = (REPO / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    ledger["runtimeCandidate"] = {
        "contentVersion": manifest["contentVersion"],
        "runtimeEntries": sum(len(v) for v in manifest.values() if isinstance(v, dict)),
        "manifestSha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "representation": "Working bytes after the fresh manifest rebuild; Git JSON content matches.",
    }
    ledger["review"] = {
        "status": "closed-with-disclosed-limits",
        "initialSnapshot": provenance["initialSnapshot"],
        "reviewedSnapshot": FIX, "reports": reports,
        "reconciliation": {
            "commit": FIX, "firstFix": provenance["firstFix"], "newDirectExclusionPairs": 9,
            "cardsChanged": ["寮", "症", "碁", "穀", "穫", "魅"],
            "readingsTitlesDistractorsWordsStrokesUnchanged": True,
            "remainingActionableFindings": [],
            "record": "../n1-reviews/batch-114-closure/README.md",
        },
        "independence": "Two serial blind initial reviews on one freeze; each original reviewer "
                        "then received only its own report plus the same revision and diff.",
        "voidEvidenceUsed": False,
    }
    ledger["closureValidation"] = {
        "gates": "../n1-reviews/batch-114-closure/gates",
        "unitTests": 431, "validationErrors": 0, "scopedLintErrors": 0,
        "scopedLintJmdictMode": "No full JMdict cache load; pinned complete source-family evidence "
                                "and earlier source inspection retained separately.",
        "requiredWordLinkPairs": 15, "wordLinkProblems": 0, "quizSafetyErrors": 0,
        "manifestReproducible": True, "baselineRuntimePreserved": True,
        "vocabulary": "2122/2431 reviewed prompts, unchanged pilot status",
        "nativeJvmEmulatorPhone": "NOT RUN",
    }
    ledger["limits"] = [
        "CLEAN/CONFIRMED are bounded textual-review judgments, not exhaustive correctness or native certification.",
        "No later B113 fix is included; its UNVERIFIED verdict and missing Claude confirmation remain historical.",
        "No current Kotlin execution, custom/caller-built or multi-borrow Starter pool acceptance, native or phone test.",
        "The exposure helper is a Python model: zero N1/All and padded hits, one latent 碁/き collision in smaller pools.",
        "Supplemental dictionary claims and wider unread comparison candidates retain the reviewers' explicit limits.",
        "No fresh visual Joyo PDF-glyph or stroke-geometry review in confirmation.",
        "The installed 5c000bd APK predates kanji quiz_exclusions and is not upgraded by content publication.",
        "Exact served ZIP and CI acceptance are pending publication, not established by local closure.",
    ]
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    verdicts = {r["id"]: r["confirmationVerdict"] for r in provenance["runs"]}
    rows = "\n".join(
        f"| {r['id']} | {', '.join(r['actualModels'])} | `{r['snapshot'][:8]}` | "
        f"{r['firstToolUtc'][11:19]}-{r['lastToolUtc'][11:19]} | {r['toolCalls']} | {r['fetches']} |"
        for r in sorted(provenance["runs"], key=lambda r: r["firstToolUtc"]))
    readme = f"""# Batch 114: textual-review closure

The fifteen cards are textually review-closed, with the source/runtime limits below.
Publication is **pending** at this closure commit; the subsequent publication receipt records
the actual remote commit, CI and exact served ZIP. No native or phone acceptance is implied.

## Snapshot and scope

Members: **娯 寮 廊 栓 汽 症 砲 碁 磁 穀 穫 糖 紺 雰 魅**.
Source rows: 232, 262, 319, 539, 600, 725, 757, 760, 764, 789, 793, 817, 835, 1170, 1210.
Base: `0485c873d2ac636373c7bdf739df97ff66f9160f`.
Blind-review freeze: `8c2bdc27e5d556e639a4d0e9239ae5f2009c400f`.
First reconciliation: `ac38b8e4427afc2c10a957871c5ec99e9cb92bda`.
Final two-card correction: `{FIX}`.

Exactly fifteen kanji and fifteen stroke files are added, with fifteen link wrappers in fifteen
existing word articles. No new word article, unrelated old-card fix or later B113 fix is included.
The final reconciliation changes six batch cards, with **nine net direct meaning-exclusion pairs**,
a narrower 重症 gloss, and retained grain/head and game/board comparisons. No selected/full reading,
title or curated distractor changed after the freeze.

## Review execution and provenance

All windows below are on 2026-11-13, UTC. Every run was serial, with one tool request per response
and no overlapping requests. Initial reviewers used the same immutable candidate independently.
Later packets contained each reviewer's own preceding report, the revision and exact diff, not
the other reviewer's report. Actual models come from usage records rather than model self-labels.

| Run | Actual model | Snapshot | Tool window (UTC) | Calls | Fetches |
|---|---|---|---|---:|---:|
{rows}

Each initial run read 40 core segments and its own 11-segment requested extension in full.
The first confirmations read 27 Claude / 29 GPT segments; the final two-card delta read 5 / 6.
Every delivered kickoff and bootstrap matched frozen text exactly. Each run wrote one report and
read it back completely. All reports and accepted full-record/claim adjudications are retained.
The sole final report-binding note in each confirmation is LF creation versus CRLF disk bytes;
the readback equals the actual disk report. This is not another write.

GPT's initial raw audit was HOLD for five empty runtime autopilot continuation messages.
Their identities and original/derived snapshot hashes are retained in
`adjudications/initial-gpt-continuations.json`. They conveyed no content and induced no extra
evidence reads. The unmodified frozen auditor passed on the explicitly adjudicated derived record.
No reviewer breach was erased; subsequent assignments used interactive mode to avoid those nudges.
No B113 void report, observation or hint is included or used.

Raw execution payloads remain local because they can contain private system/context data.
This archive publishes original reports/prompts, source chains, packet evidence, bounded call metadata,
source/snapshot hashes and explicit adjudications. Compressed chains/XML reconstruct their original
bytes; `provenance.json` records stored and uncompressed hashes. CRLF packet snapshots are not
misrepresented as raw-byte-equal to LF Git blobs. Hashes establish consistency, not comprehension.

## Reconciliation and supersession

| Item | Final disposition |
|---|---|
| Claude F3 / GPT F1: 寮-房 | Resolved, with the room/accommodation qualification. |
| Claude O2 / GPT F1: 寮-庁 | Resolved for the qualified historical bureau/agency sense. |
| GPT F1: 寮-部 and 寮-課 | Resolved with historical organizational-unit wording, not modern institutional interchangeability. |
| Claude O3 / GPT F2: 穫-集 and 穫-拾 | Resolved for gathering; bare 穫 is not made a general verb for collection. |
| GPT F2: 穫-利 and 穫-績 | Resolved within the useful-gain/result senses of 収穫. |
| GPT F3: 魅-怪 | Resolved for the supernatural sense, distinct from suspicion and personal appeal. |
| Claude O7: 重症 gloss | Resolved to JMdict's “serious illness”. |
| Claude F1/F2: 穀-穂 and 碁-盤 | Initial conservative additions withdrawn in `{FIX[:8]}` after exact full-label adjudication. |

Both initial reports were NEEDS FIX. The first Claude confirmation was **CONFIRMED**;
the first GPT confirmation was **NEEDS FIX**, while resolving all its original F1-F3.
GPT's new Finding 1 challenged only the two additional part/equipment exclusions.
The author checked the canonical rule and the complete labels: **grain-bearing head** denotes
a qualified plant part, and **board; disc** denotes equipment, not the **Go board game**.
A shared token or relationship alone does not establish a defensible translation of the target.
The two guards and their misleading rationales were removed, not the useful comparisons.
The 板 note now describes material without an absolute prohibition on its use as game equipment.
Existing unrelated guards were not swept into this correction.

This is an evidence-based reversal, not majority vote or a general model benchmark.
In its delta, Claude explicitly accepts D1/D2 and supersedes its earlier approval for these two
pairs only; its other dispositions remain. Final delta verdicts:
**Claude {verdicts['delta-claude']}; GPT {verdicts['delta-gpt']}**.
Each accepted delta has no remaining actionable finding in the assigned two-card revision.
Prior NEEDS FIX and UNVERIFIED facet judgments remain verbatim in their original reports.

Shared observations include optional/per-card material: 寮-庁 and 穫-集/拾 are not credited as
GPT-only discoveries merely because Claude labeled them optional. Claude proposed the two stricter
guards and the 重症 polish; GPT supplied the 部/課, 利/績 and 怪 comparisons, then the evidence-backed
guard correction. These are contributions to this bounded sample, not model rankings.

Claude O1 (板/行 exclusions), O4 (no change) and O6 (extra provenance citations) were declined
with confirmation acceptance. O5, 気.md's “汽 is steam only” wording/link, remains a separate later fix;
it is not silently completed here. Other conservative inherited exclusions were not globally reviewed.

## Evidence limits

- Full extra-reading inventories, arbitrary custom/caller-built pools, multi-borrow Starter, parser propagation,
  actual Kotlin draws, native/phone behavior and old-client compatibility are not established.
  The installed `5c000bd` APK predates kanji exclusions and is not upgraded by this publication.
- The host reading model reports zero N1/All and padded hits, with one latent 碁/き collision for smaller
  hypothetical pools. The 100-seed reading-options helper does not include every supplemental attested reading.
  Neither log establishes universal safety; removing meaning guards does not change reading questions.
- GPT's first confirmation freshly verifies 碁/キ, 穀 beans/classical たなつもの and 魅's supernatural sense.
  Other supplemental Daijisen-only statements retain each report's UNVERIFIED limits; author inspection
  is separate evidence, not relabeled independent confirmation.
- Confirmation does not freshly inspect raw SVG geometry, visual Joyo pages, all word articles or every
  comparison-card body. Initial source/metadata and stroke-count coverage is not visual/device acceptance.
- 銃, 棋 and 陶 and other report-listed missing cards remain absent, not substituted. Unread candidate bodies
  are not certified safe by the title index. Modern community-source membership is mechanically audited
  separately; historical KANJIDIC2 JLPT fields are not current community-level evidence.
- Final delta confirmations cover two cards only. Their CLEAN facets do not overwrite retained evidence
  limits or amount to a fresh exhaustive review of all fifteen cards.

## Validation and accounting

The final runtime tree passed 431 host tests, content validation, scoped lint, required-link verification,
quiz-safety checks, reproducible manifest generation, vocabulary consistency and archive budgets.
Gates are retained under `gates/`, separated by the first reconciliation and final delta.
Final runtime version: **1531e050487c8a64**, **8,664 entries**.
Local archive estimate: 8,671 files / 8,686 entries, within unchanged publishing limits.
The refreshed published base remained 0485c873, already an ancestor; no integration merge was needed.

The scope verifier establishes exactly thirty new runtime files, fifteen changed word entries and no
other baseline runtime changes. All 1,221 kanji and 5,083 words remain. Source accounting after local
closure is **231 done / 0 in progress / 997 not started**: 225 N1 additions plus six earlier N2 placements.
Published accounting remains **216 delivered / 1,012 not delivered** until the separate remote/CI/ZIP
receipt succeeds. Overall issue #60 is not complete.
"""
    with (ROOT / "README.md").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(readme)
    notes_path = REPO / "docs/n1-authoring-notes.md"
    notes = notes_path.read_text(encoding="utf-8")
    assert "## Batch 114:" not in notes
    section = f"""## Batch 114: textually closed, publication pending

The fifteen cards are **娯 寮 廊 栓 汽 症 砲 碁 磁 穀 穫 糖 紺 雰 魅**, with stroke files and
fifteen links in fifteen existing word articles; no word article is added.
Two serial independent initial reviews covered freeze `8c2bdc27`.
Reconciliation `ac38b8e4` added eleven pairs and narrowed the 重症 gloss.
After a valid GPT confirmation finding, `{FIX[:8]}` removed two unsupported
part/equipment guards (穀-穂, 碁-盤) while retaining the useful comparisons.
Nine net new direct pairs remain. Claude explicitly accepted the full-label
adjudication in the bounded delta; final delta verdicts are Claude
**{verdicts['delta-claude']}**, GPT **{verdicts['delta-gpt']}**.

The [closure record](n1-reviews/batch-114-closure/README.md) preserves all six reports,
including the earlier conflicting confirmation judgments and their supersession,
complete bounded-read provenance, dispositions and evidence limits. No B113 void
material or later B113 fix is included. Native/phone, old-APK, broader reading-pool,
supplemental-source and visual-asset limits remain explicit.

Local source accounting is **231 done / 0 in progress / 997 not started**.
Publication remains pending: **216 delivered / 1,012 not delivered**.
The final runtime candidate is `1531e050487c8a64`, 8,664 entries.
See the [B114 ledger](n1-sources/batch-114-progress.json).

"""
    notes_path.write_text(notes.replace("## Batch 113:", section + "## Batch 113:", 1), encoding="utf-8")
    print("B114 ledger is review-closed; publication totals remain unchanged.")


if __name__ == "__main__":
    main()
