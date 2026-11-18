"""Verify B132's finite evidence inventory without accepting semantic dispositions."""
import json
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath

from common import GUARD_SHA, WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b132_payload_v2 import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER
from verify_b132_sources import Git
from build_b131_neutral_packet_001 import union_records

TOOLS = Path(__file__).resolve().parent
SCRATCH = HERE.parent
CANDIDATE = "2e618b38ae5b420f7a1fe6783268093348367c51"
PROOFS = {
    "source-verification-001.json": "da96caae19030d3facd5d8c91ef196d857ddfff4d723ebd6e4b514acfbbac078",
    "payload-verification-001.json": "d4a77b1abdd90b547fddb5efbe449641b218846fd3e6f7bfe3a136003d96e482",
    "gate-verification-001/verification.json": "d51652ee878d4462ea7fa418ec903e7a2db709bcacb1b9d95ede80fdb0c11ecc",
}


def safe_relative(name):
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and ".." not in path.parts


def pair_coverage(disposition, card, scan, comparisons):
    require(disposition["base"] == BASE and len(disposition["members"]) == 1,
            "Pair-table base or member inventory differs")
    item = disposition["members"][0]
    rows = item["pairs"]
    others = [row["pair"][1] for row in rows]
    require(item["kanji"] == MEMBERS[0] and item["targetTitle"] == card["title"]
            and item["scanRows"] == len(scan["rows"]) == 1257
            and all(row["pair"][0] == MEMBERS[0] and row["pair"][1] not in MEMBERS for row in rows)
            and len(others) == len(set(others)) and set(others) == set(comparisons)
            and set(scan["matches"]) <= set(others), "Finite comparison or scan coverage differs")
    for row in rows:
        title, digest = comparisons[row["pair"][1]]
        require(row["decision"] in {"guard", "curated", "distinct", "rejected"}
                and row["comparisonTitle"] == title and row["baselineCardSha256"] == digest
                and row["scanMatch"] is (row["pair"][1] in scan["matches"])
                and row["targetLabelOnComparison"].strip() and row["comparisonLabelOnTarget"].strip(),
                "Pair snapshot or bidirectional coverage differs")
    require({row["pair"][1] for row in rows if row["decision"] == "guard"}
            == set(card["quiz_exclusions"])
            and {row["pair"][1] for row in rows if row["decision"] == "curated"}
            == set(card["distractors"]), "Direct guards or curated options differ")
    return len(rows)


def main():
    output = HERE / "packet-verification-001"
    require(not output.exists(), "Preserve packet verification")
    source, payload, gates = [json.loads(frozen(HERE / name, digest))
                              for name, digest in PROOFS.items()]
    require(all(p["candidate"] == CANDIDATE and p["base"] == BASE and p["status"] == "PASS"
                and not p["memory"]["breach"] for p in (source, payload, gates)),
            "Verification proofs bind another snapshot")
    require(payload["sourceProof"]["sha256"] == PROOFS["source-verification-001.json"]
            and gates["payloadProof"]["sha256"] == PROOFS["payload-verification-001.json"],
            "Verification proof graph differs")
    handoff_raw = frozen(HERE / "author-handoff-observed-001.json")
    handoff = json.loads(handoff_raw)
    require(handoff["candidate"] == CANDIDATE and handoff["base"] == BASE
            and handoff["manifestSha256"] == payload["manifestSha256"]
            and handoff["committedGates"]["summarySha256"] == gates["gates"]["committed"]["summarySha256"]
            and handoff["authorGates"]["summarySha256"] == gates["gates"]["author-recheck"]["summarySha256"]
            and handoff["preservation"]["summarySha256"] == gates["preservation"]["summarySha256"]
            and handoff["preservation"]["runtimeHashesSha256"]
            == gates["capturedInputs"]["preservation/runtime-hashes.json"]["sha256"],
            "Observed handoff differs from actual verified outputs")
    helper_binding = {"path": str(TOOLS / "build_b131_neutral_packet_001.py"),
                      "sha256": sha(frozen(TOOLS / "build_b131_neutral_packet_001.py"))}
    guard, _ = start_guard("B132 complete finite evidence verification")
    git = Git(REPO, RUNNER, guard)
    signed, captures, history_bindings = {}, {}, {}
    sys.path.insert(0, str(WS / "lean"))
    from n1lib import parse
    from fontTools.ttLib import TTFont

    def blob(name):
        raw = git("show", CANDIDATE + ":" + PREFIX + name)
        signed[PREFIX + name] = sha(raw)
        return raw

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout differs")

    try:
        clean()
        inventory_raw = blob("evidence-inventory.json")
        require(sha(inventory_raw) == handoff["inventorySha256"], "Handoff inventory differs")
        inventory = json.loads(inventory_raw)
        names = {name.removeprefix(PREFIX) for name in
                 git("ls-tree", "-r", "--name-only", CANDIDATE, "--", PREFIX).decode().splitlines()}
        require(inventory["selfExcluded"] is True
                and names == set(inventory["files"]) | {"evidence-inventory.json"},
                "Signed evidence inventory is incomplete")
        for name, digest in inventory["files"].items():
            require(safe_relative(name) and sha(blob(name)) == digest, "Changed packet file: " + name)
            guard.check()
        require(signed[PREFIX + "producers/package_132.py"] == inventory["producerSha256"],
                "Evidence inventory producer differs")
        for name, key in (("independent-source-verification.json", "sourceVerificationSha256"),
                          ("supplemental-verification.json", "supplementalVerificationSha256")):
            require(signed[PREFIX + name] == handoff[key], "Author source-verification handoff differs")
        facts = json.loads(frozen(source["facts"]["path"], source["facts"]["sha256"]))
        verified_records = {item["path"]: item["sha256"] for item in source["sourceRecords"]}
        require(set(verified_records) == {PREFIX + item["file"] for item in
                                        facts["jmdictSelections"] + facts["kanjidic2Selections"]}
                and all(signed[name] == digest for name, digest in verified_records.items()),
                "Signed complete source selections differ from independent verification")
        jm, jm_bindings = union_records(facts["jmdictSelections"], "entry", "ent_seq", blob)
        kd, kd_bindings = union_records(facts["kanjidic2Selections"], "character", "literal", blob)
        require(len(jm) == 95 and len(kd) == 7, "Canonical-equal complete record union differs")
        comparisons = {}
        for char in source["packetComparisonCards"]:
            raw = blob(f"comparison-cards/{char}.md")
            metadata, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
            comparisons[char] = (metadata["title"], sha(raw))
            readback = json.loads(blob(f"comparison-readback/{char}.json"))
            require(readback["kanji"] == char
                    and readback["completeCard"] == raw.decode("utf-8").replace("\r\n", "\n"),
                    "Comparison readback card differs")
        scan = json.loads(blob(f"scans/{MEMBERS[0]}.json"))
        disposition = json.loads(blob("pair-dispositions.json"))
        pair_count = pair_coverage(disposition, payload["members"][0]["metadata"], scan, comparisons)
        require(pair_count == len(comparisons) == 6, "Observed comparison count differs")
        for row in disposition["members"][0]["pairs"]:
            require(sha(blob(f"comparison-readback/{row['pair'][1]}.json")) == row["readbackSha256"],
                    "Pair readback binding differs")
        history = json.loads(blob("local-history-bindings.json"))
        require(Path(history["directory"]).resolve() == SCRATCH.resolve(), "Wrong history root")
        for name, digest in history["files"].items():
            path = SCRATCH / name
            require(safe_relative(name) and path.resolve().is_relative_to(SCRATCH.resolve())
                    and sha(path.read_bytes()) == digest, "Historical evidence changed: " + name)
            history_bindings[name] = digest
        external = json.loads(blob("external-capture-bindings.json"))
        require(external["fullCapturesLocalOnly"] is True and len(external["captures"]) == 2
                and {(item["character"], item["provider"]) for item in external["captures"]}
                == {(MEMBERS[0], provider) for provider in ("kotobank", "weblio")},
                "Complete external capture inventory differs")
        for item in external["captures"]:
            path = Path(item["localRawCapture"])
            require(path.parent == SCRATCH / "survey-001" / "external"
                    and path.name == item["character"] + "-" + item["provider"] + ".html",
                    "External capture path differs")
            raw, text = path.read_bytes(), path.with_suffix(".txt").read_bytes()
            require(sha(raw) == item["rawSha256"] and len(raw) == item["rawBytes"]
                    and sha(text) == item["textSha256"], "External capture bytes changed")
            captures["external/" + path.name] = raw
            captures["external/" + path.with_suffix(".txt").name] = text
        fonts = json.loads(blob("stroke-font-evidence.json"))
        require(fonts["producerSha256"] == signed[PREFIX + "producers/prepare_132.py"]
                and fonts["converterSha256"] == payload["converterSha256"],
                "Font/geometry producer differs")
        points = fonts["codePoints"]
        chars = {point["character"] for point in points}
        teaching = "\n".join(git("show", CANDIDATE + ":" + name).decode("utf-8") for name in
                             (f"kanji/{MEMBERS[0]}.md", f"words/{MEMBERS[0]}.md"))
        require(len(chars) == len(points)
                and all(len(point["character"]) == 1
                        and point["codePoint"] == f"U+{ord(point['character']):04X}"
                        and point["unicodeName"] == unicodedata.name(point["character"]) for point in points)
                and chars == set(re.findall("[\u3400-\u9fff]", teaching)) | set(comparisons) | set("\u5893\u83ab\u571f"),
                "Finite taught/component/font inventory differs")
        require(len(fonts["fonts"]) == 3 and {item["filename"] for item in fonts["fonts"]}
                == {"kanji_brush.ttf", "kanji_mincho.ttf", "kanji_textbook.ttf"},
                "Bundled font inventory differs")
        missing = {}
        for item in fonts["fonts"]:
            path = WS / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font" / item["filename"]
            require(sha(path.read_bytes()) == item["sha256"], "Actual bundled font changed")
            with TTFont(path) as font:
                cmap = font.getBestCmap()
                coverage = {point["codePoint"]: ord(point["character"]) in cmap for point in points}
            require(coverage == item["coverage"], "Actual font cmap differs")
            missing[item["filename"]] = sorted(key for key, present in coverage.items() if not present)
            guard.check()
        tools = json.loads(blob("tool-bindings.json"))
        require(tools["guardSha256"] == GUARD_SHA
                and set(tools["leanTools"]) == {"n1lib.py", "n1_batch_tool.py", "quiz_safety.py",
                                               "n1_linkplan.py", "reading_exposure.py", "reading_options.py"},
                "Lean tool inventory differs")
        for name, digest in tools["leanTools"].items():
            require(sha((WS / "lean" / name).read_bytes()) == digest, "Actual lean tool changed: " + name)
        progress_raw = git("show", CANDIDATE + ":docs/n1-sources/batch-132-progress.json")
        progress = json.loads(progress_raw)
        require(progress["batch"] == 132 and progress["status"] == "local-unreviewed-author-candidate"
                and progress["base"] == BASE and progress["members"] == MEMBERS
                and progress["sourceRows"] == [197] and progress["publishedDelivered"] == 267
                and progress["undelivered"] == 961 and progress["deliveryNotIncremented"] is True
                and progress["localUnpublishedDrafts"] == 1 and progress["proseException"] is None
                and progress["manifestSha256"] == payload["manifestSha256"]
                and progress["completeJmdictFamilies"] == len(jm)
                and progress["completeKanjidicRecords"] == len(kd),
                "Progress record expands scope or prematurely credits delivery")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    captures = {name: write_frozen(output / name, raw) for name, raw in captures.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 132, "status": "PASS", "candidate": CANDIDATE, "base": BASE, "proofs": PROOFS,
        "handoffSha256": sha(handoff_raw), "signedInputs": signed, "localHistoryBindings": history_bindings,
        "capturedInputs": captures, "sourceSelections": jm_bindings + kd_bindings,
        "verifiedJmdictFamilies": len(jm), "verifiedKanjidicRecords": len(kd),
        "finiteBaselinePairs": pair_count, "finiteNewPairs": 0, "externalCaptures": len(external["captures"]),
        "fontCodePoints": len(points), "fontMissingCodePoints": missing, "fontScope": fonts["scope"],
        "leanTools": tools["leanTools"], "progressSha256": sha(progress_raw),
        "unionHelper": helper_binding, "memory": memory, "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "Mechanical signed-inventory, complete canonical-equal source union, finite "
                  "bidirectional pair coverage, local historical bytes, external captures and "
                  "actual bounded font cmap checks. No semantic pair judgment, historical "
                  "manual-reading depth, rendered/native/device, independent review or publication.",
    })))


if __name__ == "__main__":
    main()
