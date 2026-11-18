"""Verify B134's finite signed evidence without accepting its semantic dispositions."""
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path, PurePosixPath

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b134_payload import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, SUPPORTS
from verify_b134_sources import Git
from build_b131_neutral_packet_001 import union_records

TOOLS = Path(__file__).resolve().parent
SCRATCH = HERE.parent
CANDIDATE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
PROOFS = {
    "source-proof-002.json": "f3a80ee569a1bfd4f452e3f413a6377f5d01cac665e978dfc3e6db722c809393",
    "payload-proof-001.json": "ec47228ee313a82d872e7235f6f4a6b048737f24254d26405418c840dbd65d1a",
    "gate-verification-002/verification.json": "1caed56d80a213605d59eac6cc7ecc69829083cbdaa606b684edd77fb9162694",
}
INVENTORY_SHA = "fd3732a51af35285176666e25339394896cfa60e7b7c612e630445e06369e03e"
PAIR_PRODUCER_SHA = "166c86cdbbde0256d0df19add1394c191d15fd0b677a0571e67bb19e8dad0cb6"
DECISIONS = {"guard", "curated", "distinct", "rejected"}
ROW_KEYS = {"pair", "comparisonTitle", "decision", "comparisonLabelOnTarget", "targetLabelOnComparison",
            "baselineCardSha256", "readbackSha256", "scanMatch"}
NAMED_GLYPHS = "\u6b62\u6bd4\u8308"
EXPECTED_MISSING = ["U+8308"]
SCAN_ROWS = 1261
FONT_DIR = WS / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font"
FONTS = {"kanji_brush.ttf", "kanji_mincho.ttf", "kanji_textbook.ttf"}


def safe_relative(name):
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and ".." not in path.parts


def tree(node):
    return [node.tag, dict(node.attrib), (node.text or "").strip(), [tree(child) for child in node]]


def pair_coverage(disposition, cards, scans, comparisons, readbacks):
    require(disposition["base"] == BASE and disposition["producerSha256"] == PAIR_PRODUCER_SHA
            and [item["kanji"] for item in disposition["members"]] == MEMBERS,
            "Pair-table base, producer or member inventory differs")
    require(len(MEMBERS) == 1 and disposition["newMemberPairs"] == [], "New/new pair coverage differs")
    used, count, decisions = set(), 0, Counter()
    for item in disposition["members"]:
        char = item["kanji"]
        rows, card, scan = item["pairs"], cards[char], scans[char]
        others = [row["pair"][1] for row in rows]
        require(item["targetTitle"] == card["title"] and item["scanRows"] == len(scan["rows"]) == SCAN_ROWS
                and len(others) == len(set(others))
                and all(row["pair"] == [char, row["pair"][1]] and row["pair"][1] not in MEMBERS for row in rows)
                and set(others) <= comparisons.keys() and set(scan["matches"]) <= set(others),
                "Finite baseline comparison/scan coverage differs")
        for row in rows:
            other = row["pair"][1]
            title, digest = comparisons[other]
            require(set(row) == ROW_KEYS and row["decision"] in DECISIONS and row["comparisonTitle"] == title
                    and row["baselineCardSha256"] == digest and row["readbackSha256"] == readbacks[other]
                    and row["scanMatch"] is (other in scan["matches"])
                    and row["targetLabelOnComparison"].strip() and row["comparisonLabelOnTarget"].strip(),
                    "Pair snapshot or bidirectional coverage differs")
            decisions[row["decision"]] += 1
        require({row["pair"][1] for row in rows if row["decision"] == "guard"} == set(card["quiz_exclusions"])
                and {row["pair"][1] for row in rows if row["decision"] == "curated"} == set(card["distractors"]),
                "Direct guards or curated options differ")
        used.update(others)
        count += len(rows)
    require(used == set(comparisons), "Unused or missing comparison copy")
    return count, dict(sorted(decisions.items()))


def main():
    output = HERE / "packet-verification-001"
    require(not output.exists(), "Preserve packet verification")
    source, payload, gates = [json.loads(frozen(HERE / name, digest)) for name, digest in PROOFS.items()]
    require(all(p["candidate"] == CANDIDATE and p["base"] == BASE and p["status"] == "PASS"
                and not p["memory"]["breach"] for p in (source, payload, gates)),
            "Verification proofs bind another snapshot")
    require(payload["sourceProof"]["sha256"] == PROOFS["source-proof-002.json"]
            and gates["payloadProof"]["sha256"] == PROOFS["payload-proof-001.json"],
            "Verification proof graph differs")
    helper_binding = {"path": str(TOOLS / "build_b131_neutral_packet_001.py"),
                      "sha256": sha(frozen(TOOLS / "build_b131_neutral_packet_001.py"))}
    guard, _ = start_guard("B134 complete finite evidence verification")
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
        require(sha(inventory_raw) == INVENTORY_SHA, "Reported inventory differs")
        inventory = json.loads(inventory_raw)
        names = {name.removeprefix(PREFIX) for name in
                 git("ls-tree", "-r", "--name-only", CANDIDATE, "--", PREFIX).decode().splitlines()}
        require(set(inventory) == {"algorithm", "files", "limits"}
                and names == set(inventory["files"]) | {"evidence-inventory.json"} and len(names) == 215
                and not any(name.startswith("additional/") for name in names),
                "Signed evidence inventory is incomplete")
        for name, digest in inventory["files"].items():
            require(safe_relative(name) and sha(blob(name)) == digest, "Changed packet file: " + name)
            guard.check()
        facts = json.loads(frozen(source["facts"]["path"], source["facts"]["sha256"]))
        verified_records = {item["path"]: item["sha256"] for item in source["sourceRecords"]}
        require(set(verified_records) == {PREFIX + item["file"] for item in
                                        facts["jmdictSelections"] + facts["kanjidic2Selections"]}
                and all(signed[name] == digest for name, digest in verified_records.items()),
                "Complete source selections differ from independent verification")
        jm, jm_bindings = union_records(facts["jmdictSelections"], "entry", "ent_seq", blob)
        kd, kd_bindings = union_records(facts["kanjidic2Selections"], "character", "literal", blob)
        require(len(jm) == 399 and len(kd) == 59, "Complete record union differs")
        target_records = Counter()
        for line in blob("complete-target-\u7d2b.jsonl").decode("utf-8").splitlines():
            row = json.loads(line)
            union = {"entry": jm, "character": kd}[row["record"][0]]
            require(row["record"] == tree(union[row["id"]]), "Complete target record differs: " + row["id"])
            target_records[row["record"][0]] += 1
        comparisons, readbacks, readback_entries = {}, {}, 0
        for name in sorted(names):
            if not name.startswith("comparison-cards/"):
                continue
            char = PurePosixPath(name).stem
            require(name.endswith(".md") and char not in comparisons, "Duplicate or invalid comparison")
            raw = blob(name)
            require(raw == git("show", f"{BASE}:kanji/{char}.md"), "Comparison differs from actual baseline")
            metadata, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
            comparisons[char] = (metadata["title"], sha(raw))
            readback_raw = blob(f"comparison-readback/{char}.json")
            readbacks[char] = sha(readback_raw)
            readback = json.loads(readback_raw)
            require(set(readback) == {"kanji", "completeCard", "completeKanjidic", "completeApplicableJmdict"}
                    and readback["kanji"] == char
                    and readback["completeCard"] == raw.decode("utf-8").replace("\r\n", "\n")
                    and readback["completeKanjidic"] == tree(kd[char]),
                    "Comparison readback card or character record differs")
            for entry in readback["completeApplicableJmdict"]:
                ids = [child[2] for child in entry[3] if child[0] == "ent_seq"]
                require(len(ids) == 1 and entry == tree(jm[ids[0]]), "Comparison readback word record differs")
                readback_entries += 1
        require(len(comparisons) == 53 and set(comparisons) == set(source["packetComparisonCards"])
                and {name for name in names if name.startswith("comparison-readback/")}
                == {f"comparison-readback/{char}.json" for char in comparisons},
                "Comparison inventory differs")
        scans = {char: json.loads(blob(f"scans/{char}.json")) for char in MEMBERS}
        require(all(scan["base"] == BASE and scan["kanji"] == char for char, scan in scans.items()),
                "Scan identity differs")
        cards = {item["kanji"]: item["metadata"] for item in payload["members"]}
        pair_count, decisions = pair_coverage(json.loads(blob("pair-dispositions.json")),
                                              cards, scans, comparisons, readbacks)
        require(pair_count == 53 and decisions == {"curated": 3, "distinct": 11, "guard": 39}
                and len(scans["\u7d2b"]["matches"]) == 50, "Observed finite pair counts differ")
        history = json.loads(blob("local-history-bindings.json"))
        require(Path(history["directory"]).resolve() == SCRATCH.resolve() and len(history["files"]) == 227,
                "Wrong history root or inventory")
        for name, digest in history["files"].items():
            path = SCRATCH / name
            require(safe_relative(name) and path.resolve().is_relative_to(SCRATCH.resolve())
                    and sha(path.read_bytes()) == digest, "Historical evidence changed: " + name)
            history_bindings[name] = digest
            guard.check()
        author_runs = 0
        for run in ("author-gates-001", "author-gates-002"):
            signed_run = {name.rsplit("/", 1)[1] for name in names
                          if name.startswith(f"author-evidence/{run}/")}
            require(signed_run == {path.name for path in (SCRATCH / run).iterdir()} and len(signed_run) == 22,
                    "Author gate history inventory differs: " + run)
            for leaf in sorted(signed_run):
                require(blob(f"author-evidence/{run}/{leaf}") == (SCRATCH / run / leaf).read_bytes(),
                        f"Author gate history was altered: {run}/{leaf}")
                author_runs += 1
        external = json.loads(blob("external-capture-bindings.json"))
        require(external["fullCapturesLocalOnly"] is True and len(external["captures"]) == 2
                and {(item["character"], item["provider"]) for item in external["captures"]}
                == {(char, provider) for char in MEMBERS for provider in ("kotobank", "weblio")},
                "Complete external capture inventory differs")
        external_text = {}
        for item in external["captures"]:
            path = Path(item["localRawCapture"])
            require(path.parent == WS / "scratch-132" / "survey-001" / "external"
                    and path.name == item["character"] + "-" + item["provider"] + ".html",
                    "Reused external capture path differs")
            raw, text = path.read_bytes(), path.with_suffix(".txt").read_bytes()
            require(sha(raw) == item["rawSha256"] and len(raw) == item["rawBytes"]
                    and sha(text) == item["textSha256"], "External capture bytes changed")
            captures["external/" + path.name] = raw
            captures["external/" + path.with_suffix(".txt").name] = text
            external_text[item["character"], item["provider"]] = (item, text)
        excerpts = json.loads(blob("bounded-excerpts.json"))["captures"]
        require(len(excerpts) == len(external_text)
                and {(row["character"], row["provider"]) for row in excerpts} == external_text.keys(),
                "Excerpt attribution inventory differs")
        excerpt_count = 0
        for row in excerpts:
            item, text = external_text[row["character"], row["provider"]]
            lines = text.decode("utf-8").splitlines()
            require(row["textSha256"] == item["textSha256"] and row["url"] == item["finalUrl"],
                    "Excerpt attribution differs")
            for excerpt in row["excerpts"]:
                require(1 <= excerpt["line"] <= len(lines)
                        and excerpt["text"] in lines[excerpt["line"] - 1], "Excerpt text or line differs")
                excerpt_count += 1
        fonts = json.loads(blob("stroke-font-evidence.json"))
        geometry = {item["kanji"]: item for item in payload["generatedGeometry"]}
        require(fonts["converterSha256"] == payload["converterSha256"]
                and [item["character"] for item in fonts["members"]] == MEMBERS,
                "Font/geometry producer or members differ")
        for item in fonts["members"]:
            char, expected = item["character"], geometry[item["character"]]
            svg_name = f"kanjivg/{ord(char):05x}.svg"
            require(sha(git("show", f"{CANDIDATE}:strokes/{char}.json")) == item["strokeSha256"]
                    == expected["strokeSha256"] and item["strokeCount"] == expected["strokeCount"]
                    and item["svgSha256"] == expected["svgSha256"] == signed[PREFIX + svg_name]
                    and item["svgGitBlob"] == expected["svgGitBlob"]
                    and item["converterSha256"] == payload["converterSha256"]
                    and item["revision"] == fonts["kanjivgRevision"], "Font evidence stroke binding differs")
        points = fonts["codePoints"]
        chars = {point["character"] for point in points}
        paths = [f"kanji/{char}.md" for char in MEMBERS]
        paths += [f"words/{word}.md" for words in SUPPORTS.values() for word in words]
        teaching = "\n".join(git("show", CANDIDATE + ":" + name).decode("utf-8") for name in paths)
        require(len(chars) == len(points) == 74
                and all(len(point["character"]) == 1
                        and point["codePoint"] == f"U+{ord(point['character']):04X}"
                        and point["unicodeName"] == unicodedata.name(point["character"]) for point in points)
                and chars == set(re.findall("[\u3400-\u9fff]", teaching)) | set(comparisons) | set(NAMED_GLYPHS),
                "Finite taught/component/font inventory differs")
        require({item["filename"] for item in fonts["fonts"]} == FONTS and len(fonts["fonts"]) == 3,
                "Font inventory differs")
        missing = {}
        for item in fonts["fonts"]:
            path = FONT_DIR / item["filename"]
            require(sha(path.read_bytes()) == item["sha256"], "Actual bundled font changed")
            with TTFont(path) as font:
                cmap = font.getBestCmap()
                coverage = {point["codePoint"]: ord(point["character"]) in cmap for point in points}
            require(coverage == item["coverage"], "Actual font cmap differs")
            missing[item["filename"]] = sorted(key for key, present in coverage.items() if not present)
            require(missing[item["filename"]] == EXPECTED_MISSING, "Font gap differs from author disclosure")
            guard.check()
        progress_raw = git("show", CANDIDATE + ":docs/n1-sources/batch-134-progress.json")
        progress = json.loads(progress_raw)
        require(progress["batch"] == 134 and progress["base"] == BASE and progress["governingIssue"] == 60
                and progress["status"] == "local-unreviewed-authoring-candidate"
                and progress["members"] == MEMBERS and progress["sourceRows"] == [831]
                and progress["supports"] == [["\u7d2b", "\u7d2b"]]
                and progress["runtimePublished"] is False and progress["reviewClosed"] == []
                and progress["published"] == []
                and progress["accounting"] == {
                    "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 271,
                    "publishedN1Additions": 265, "n2Placements": 6, "undelivered": 957,
                    "localUnreviewedDrafts": 1, "overallN1TaskComplete": False},
                "Progress record expands scope or prematurely credits delivery")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    captures = {name: write_frozen(output / name, raw) for name, raw in captures.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 134, "status": "PASS", "candidate": CANDIDATE, "base": BASE, "proofs": PROOFS,
        "gateHandoff": gates["handoff"], "signedInputs": signed, "localHistoryBindings": history_bindings,
        "capturedInputs": captures, "sourceSelections": jm_bindings + kd_bindings,
        "verifiedJmdictFamilies": len(jm), "verifiedKanjidicRecords": len(kd),
        "targetRecords": dict(sorted(target_records.items())), "readbackJmdictEntries": readback_entries,
        "finiteBaselinePairs": pair_count, "pairDecisions": decisions, "finiteNewPairs": 0,
        "comparisonCopies": len(comparisons), "scanMatches": len(scans["\u7d2b"]["matches"]),
        "authorGateHistoryFiles": author_runs, "externalCaptures": len(external["captures"]),
        "boundedExcerpts": excerpt_count, "fontCodePoints": len(points), "namedGlyphs": NAMED_GLYPHS,
        "fontMissingCodePoints": missing, "fontScope": fonts["scope"],
        "progressSha256": sha(progress_raw), "unionHelper": helper_binding, "memory": memory,
        "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "Mechanical signed-inventory, complete canonical-equal source union, target and "
                  "comparison readback record equality, finite bidirectional pair coverage, historical "
                  "byte preservation, reused external capture/excerpt bindings and actual bounded font "
                  "cmap checks. Producers are bound by the signed inventory and gate proof, not re-run. "
                  "No semantic pair judgment, historical read-depth, fresh web fetch, rendered/native/"
                  "device, independent linguistic review or publication acceptance.",
    }), ensure_ascii=False))


if __name__ == "__main__":
    main()
