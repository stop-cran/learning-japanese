"""Verify the B118 reconciliation-002 descendant; the first-correction verifier stays unchanged."""
import difflib
import json
import sys
from pathlib import Path
from urllib.parse import quote

from common import WS, freeze_json, frozen, git, load_batch, require, sha, start_guard
from confirm_v2 import clean
from verify_b118_revision import verify_gates, verify_sources

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse

PRIOR = "fa2f64f2472cf9ef10b8ac5f48db14dcaa248cd2"
PRIOR_PROOF = WS / "scratch-118" / "revision-verification-001" / "revision-verification.json"
PRIOR_PROOF_SHA = "6478e7ba70e7bde9d01ef005d173d83b7e3f6d686f95df6cc3c58d70fffd7e62"
PRESERVED = ["分", "解", "割", "切", "破", "剖", "板", "別", "離", "刻", "盤"]
REQUIRED = "研"
REVIEWED = ["研", "断", "絶", "折", "究", "査", "調", "察", "考", "討", "論", "批"]
RECORDS = WS / "scratch-118" / "review"
NEW = RECORDS / "reconciliation-002"
OLD = RECORDS / "reconciliation-001"
REPO_DIR = "docs/n1-sources/batch-118/reconciliation-002/"
PINNED = "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed"
ORIGINAL_TARGET = WS / "scratch-118" / "character-source-析.html"
ORIGINAL_SECTION = WS / "scratch-118" / "neutral-source-sections-001" / "daijisen.html"


def inserted_lines(before, after):
    """Return inserted lines, requiring every earlier line to survive unchanged and in order."""
    old, new = before.split("\n"), after.split("\n")
    added = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=old, b=new, autojunk=False).get_opcodes():
        require(op in ("equal", "insert"), f"Earlier body text changed: {op} {old[i1:i2]!r}")
        if op == "insert":
            added.extend(new[j1:j2])
    return added


def title(card):
    meta, _ = parse(card.decode("utf-8"))
    return meta["title"]


def verify_dispositions(dispositions, appended, cards):
    require(dispositions["candidate"] == PRIOR
            and dispositions["confirmation"] == "N1-B118-GPT-001-CONFIRM-002"
            and dispositions["confirmationAcceptance"] is False, "Disposition binding differs")
    require(dispositions["originalExclusionsPreservedInOrder"] == PRESERVED
            and dispositions["appendedDirectExclusions"] == appended, "Disposition exclusions differ")
    pairs = dispositions["pairs"]
    require([pair["pair"] for pair in pairs] == [["析", other] for other in REVIEWED],
            "Each reviewed comparison needs exactly one ordered disposition")
    guards = []
    for pair in pairs:
        other = pair["pair"][1]
        require(pair["disposition"] in ("guard", "no-new-guard"), f"Unknown disposition: {other}")
        require(pair["displayedTitle"] == title(cards[other]), f"Displayed title differs: {other}")
        require(all(pair.get(key) for key in ("sourceSenseAnchor", "reasoning", "targetEvidence", "sources")),
                f"Incomplete disposition: {other}")
        text = frozen(NEW / "sections" / f"{other}.txt").decode("utf-8")
        require(all(part in text for part in pair["sourceSenseAnchor"].split("／")),
                f"Source anchor absent from the captured section: {other}")
        for item in pair["sources"]:
            path = WS / item.split(":")[0].replace("\\", "/")
            require(path.is_file(), f"Cited source missing: {item}")
        if pair["disposition"] == "guard":
            guards.append(other)
    require(guards == appended and REQUIRED in guards, "Guard dispositions differ from the card")
    return {pair["pair"][1]: pair["disposition"] for pair in pairs}


def verify_captures(receipt, blob, guard):
    require(receipt["candidate"] == PRIOR and receipt["status"] == "complete", "Capture receipt binding differs")
    require(receipt["kanjidicInputSha256"] == PINNED
            and receipt["kanjidicRecordsSha256"] == sha(frozen(NEW / "kanjidic2-records.xml")),
            "Capture receipt dictionary binding differs")
    require([row["character"] for row in receipt["records"]] == REVIEWED, "Capture membership differs")
    captures = []
    for row in receipt["records"]:
        character = row["character"]
        url = "https://www.weblio.jp/content/" + quote(character)
        require(row["url"] == row["finalUrl"] == url and row["contentType"].startswith("text/html")
                and row["sectionLabel"] == "デジタル大辞泉", f"Capture origin differs: {character}")
        raw = frozen(WS / row["rawPath"], row["rawSha256"])
        section = frozen(WS / row["sectionPath"], row["sectionSha256"])
        require(len(raw) == row["rawBytes"] and len(section) == row["sectionBytes"]
                and raw[row["startByteInclusive"]:row["endByteExclusive"]] == section,
                f"Section is not the exact response slice: {character}")
        frozen(WS / row["textPath"], row["textSha256"])
        card = frozen(WS / row["cardPath"], row["cardSha256"])
        require(card == blob(PRIOR, f"kanji/{character}.md"), f"Comparison card is not the reviewed blob: {character}")
        captures.append({"character": character, "rawSha256": row["rawSha256"],
                         "sectionSha256": row["sectionSha256"], "retrievedAt": row["retrievedAt"]})
        guard.check()
    target_raw = frozen(NEW / receipt["targetSections"])
    target = receipt["targetCapture"]
    require(receipt["targetCardSha256"] == sha(blob(PRIOR, "kanji/析.md"))
            == sha(frozen(NEW / "comparison-cards" / "析.md")), "Target card binding differs")
    raw = frozen(WS / target["rawPath"], target["rawSha256"])
    section = frozen(WS / target["sectionPath"], target["sectionSha256"])
    page = json.loads(blob(PRIOR, "docs/n1-sources/batch-118/source-receipt.json"))["sources"]["characterPage"]
    # The original capture predates scratch freezing, so the committed original receipt binds it.
    require(ORIGINAL_TARGET.read_bytes() == raw and sha(raw) == page["responseSha256"]
            and target["url"] == page["url"] and len(raw) == page["responseBytes"]
            and section == frozen(ORIGINAL_SECTION)
            and sha(section) == page["neutralSections"]["daijisenSha256"]
            and raw[target["startByteInclusive"]:target["endByteExclusive"]] == section,
            "Target section is not the preserved original capture")
    frozen(WS / target["textPath"], target["textSha256"])
    return {"receiptSha256": sha(frozen(NEW / "source-receipt.json")),
            "targetReceiptSha256": sha(target_raw), "sections": captures,
            "targetReusesOriginalCapture": True}


def verify(candidate, gates, output):
    config = load_batch(118)
    clean(config, candidate)
    require(git(config, "rev-parse", f"{candidate}^").decode().strip() == PRIOR,
            "Correction must directly descend from the first correction")
    prior_proof = json.loads(frozen(PRIOR_PROOF, PRIOR_PROOF_SHA))
    require(prior_proof["candidate"] == PRIOR and prior_proof["status"] == "PASS", "Prior proof differs")
    guard, _ = start_guard("B118 reconciliation-002 revision verification")
    try:
        blob = lambda commit, path: git(config, "show", f"{commit}:{path}")
        raw_manifest = blob(candidate, "manifest.json")
        manifest = json.loads(raw_manifest)
        runtime = lambda value: {p: h for entries in value.values() if isinstance(entries, dict)
                                 for p, h in entries.items()}
        current = runtime(manifest)
        old = runtime(json.loads(blob(config["base"], "manifest.json")))
        previous = runtime(json.loads(blob(PRIOR, "manifest.json")))
        require(current.keys() - old.keys() == {"kanji/析.md", "strokes/析.json"}
                and old.keys() <= current.keys()
                and {path for path in old if current[path] != old[path]} == {"words/分析.md"},
                "Unexpected baseline runtime change")
        require(current.keys() == previous.keys()
                and {path for path in current if current[path] != previous[path]} == {"kanji/析.md"},
                "Runtime changed beyond the target card")
        card = blob(candidate, "kanji/析.md")
        require(current["kanji/析.md"] == sha(card), "Manifest does not bind the committed card")
        original, original_body = parse(blob(PRIOR, "kanji/析.md").decode("utf-8"))
        revised, revised_body = parse(card.decode("utf-8"))
        require({k: v for k, v in original.items() if k != "quiz_exclusions"}
                == {k: v for k, v in revised.items() if k != "quiz_exclusions"},
                "Correction changed preserved metadata")
        exclusions = revised["quiz_exclusions"]
        require(original["quiz_exclusions"] == PRESERVED and exclusions[:len(PRESERVED)] == PRESERVED
                and len(set(exclusions)) == len(exclusions), "Earlier guards not preserved in order")
        appended = exclusions[len(PRESERVED):]
        require(REQUIRED in appended and set(appended) <= set(REVIEWED), "Unexpected or missing new guard")
        cards = {other: blob(candidate, f"kanji/{other}.md") for other in REVIEWED}
        require(all(cards[other] == blob(PRIOR, f"kanji/{other}.md") for other in REVIEWED),
                "A comparison card changed")
        added = "\n".join(inserted_lines(original_body, revised_body))
        require(all(f"[{other}]({other}.md)" in added for other in appended), "New guard lacks a Notes rationale")
        for path in ("strokes/析.json", "words/分析.md"):
            require(blob(candidate, path) == blob(PRIOR, path), f"Preserved runtime file changed: {path}")
        for path in git(config, "ls-tree", "-r", "--name-only", PRIOR, "--",
                        "docs/n1-sources/batch-118").decode("utf-8").splitlines():
            require(blob(PRIOR, path) == blob(candidate, path), f"Earlier source or receipt rewritten: {path}")
        changed = git(config, "diff", "--name-only", PRIOR, candidate).decode("utf-8").splitlines()
        require({"kanji/析.md", "manifest.json"} <= set(changed)
                and all(path in ("kanji/析.md", "manifest.json") or path.startswith(REPO_DIR) for path in changed),
                "Unexpected correction scope")
        for name in ("pair-dispositions.json", "source-receipt.json"):
            require(blob(candidate, REPO_DIR + name) == frozen(NEW / name), f"Committed receipt differs: {name}")
        dispositions = json.loads(frozen(NEW / "pair-dispositions.json"))
        decisions = verify_dispositions(dispositions, appended, cards)
        require(frozen(NEW / "kanjidic2-records.xml") == frozen(OLD / "kanjidic2-records.xml")
                and frozen(NEW / "kanjidic2-extraction.json") == frozen(OLD / "source-extraction.json"),
                "Reconciliation-002 dictionary evidence differs from verified records")
        captures = verify_captures(json.loads(frozen(NEW / "source-receipt.json")), blob, guard)
        index = json.loads(blob(candidate, "docs/n1-sources/source-index.json"))
        pending = {row["kanji"] for row in index if row["statusAtFreeze"] == "pending"}
        present = {Path(path).stem for path in current if path.startswith("kanji/")}
        prior = {Path(path).stem for path in old if path.startswith("kanji/")}
        require(len(pending) == 1228 and len(pending & prior) == 246 and len(pending & present) == 247,
                "Source accounting differs")
        receipts = verify_gates(gates, raw_manifest, config, guard)
        source_proof = verify_sources(config, candidate, OLD, guard)
        result = {"batch": 118, "candidate": candidate, "prior": PRIOR, "initial": config["candidate"],
                  "base": config["base"], "status": "PASS", "ownerSignature": "G", "worktreeClean": True,
                  "priorProofSha256": PRIOR_PROOF_SHA, "manifestSha256": sha(raw_manifest),
                  "contentVersion": manifest["contentVersion"], "runtimeEntries": len(current),
                  "targetCardSha256": sha(card), "exclusions": exclusions, "appendedGuards": appended,
                  "decisions": decisions, "gates": receipts, "dictionaryProof": source_proof,
                  "captureProof": captures, "priorRuntimeChangedOnlyTargetCard": True,
                  "earlierMetadataStrokesGuardsBodyAndReceiptsPreserved": True,
                  "sourceMembersPublishedBeforeBatch": 246, "sourceMembersInCandidate": 247,
                  "linguisticAcceptance": False, "publicationAccepted": False}
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Verification RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
