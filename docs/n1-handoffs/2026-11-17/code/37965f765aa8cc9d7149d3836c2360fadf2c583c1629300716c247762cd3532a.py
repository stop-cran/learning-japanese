"""Verify B133's finite signed evidence without accepting its semantic dispositions."""
import itertools
import json
import re
import unicodedata
from pathlib import Path, PurePosixPath

from common import GUARD_SHA, WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b133_payload import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, SUPPORTS
from verify_b133_sources import Git
from build_b131_neutral_packet_001 import union_records

TOOLS = Path(__file__).resolve().parent
SCRATCH = HERE.parent
CANDIDATE = "ad047ace020579f81bde250ac948b9a4cb597887"
PROOFS = {
    "source-verification-001.json": "5d8c9aee7a31a35e5eeae047d35ff3a79aedb4ecc81cb7f72358d9515974cd12",
    "payload-verification-001.json": "692ecc9d3af90157b97733ff29c2b11ebe4d271893308a2c6eb2cf4e9b61c2cb",
    "gate-verification-001/verification.json": "65e292b34893b15862d70f37a9dfdb94bc22972bbc70044bc6431716349181fb",
}
DECISIONS = {"guard", "curated", "distinct", "rejected"}
NAMED_GLYPHS = "\u7389\u738b\u4eca\u91d1\u516b\u53e3\u6c34\u6c35\u7adc\u9f8d\u73e1\u7439\u9206\u7027"


def safe_relative(name):
    path = PurePosixPath(name)
    return bool(name) and "\\" not in name and not path.is_absolute() and ".." not in path.parts


def pair_coverage(disposition, cards, scans, comparisons, additional):
    require(disposition["base"] == BASE
            and [item["kanji"] for item in disposition["members"]] == MEMBERS,
            "Pair-table base or member inventory differs")
    new = disposition["newMemberPairs"]
    require([row["pair"] for row in new] == [list(pair) for pair in itertools.combinations(MEMBERS, 2)]
            and all(row["decision"] in DECISIONS and row["bothDirections"].strip() for row in new),
            "New/new pair coverage differs")
    new_guards, new_curated = ({char: set() for char in MEMBERS} for _ in range(2))
    for row in new:
        target = {"guard": new_guards, "curated": new_curated}.get(row["decision"])
        if target is not None:
            left, right = row["pair"]
            target[left].add(right)
            target[right].add(left)
    used, count = set(), 0
    for item in disposition["members"]:
        char = item["kanji"]
        rows, card, scan = item["pairs"], cards[char], scans[char]
        others = [row["pair"][1] for row in rows]
        require(item["targetTitle"] == card["title"] and item["scanRows"] == len(scan["rows"]) == 1258
                and len(others) == len(set(others))
                and all(row["pair"][0] == char and row["pair"][1] not in MEMBERS for row in rows)
                and set(others) <= comparisons.keys() and set(scan["matches"]) <= set(others),
                "Finite baseline comparison/scan coverage differs")
        for row in rows:
            other = row["pair"][1]
            title, digest = comparisons[other]
            require(row["decision"] in DECISIONS and row["comparisonTitle"] == title
                    and row["baselineCardSha256"] == digest
                    and row["scanMatch"] is (other in scan["matches"])
                    and row["additionalSourceDrivenComparison"] is (other in additional)
                    and row["targetLabelOnComparison"].strip() and row["comparisonLabelOnTarget"].strip(),
                    "Pair snapshot or bidirectional coverage differs")
        require({row["pair"][1] for row in rows if row["decision"] == "guard"} | new_guards[char]
                == set(card["quiz_exclusions"])
                and {row["pair"][1] for row in rows if row["decision"] == "curated"} | new_curated[char]
                == set(card["distractors"]), "Direct guards or curated options differ")
        used.update(others)
        count += len(rows)
    require(used == set(comparisons), "Unused or missing comparison copy")
    return count, len(new)


def main():
    output = HERE / "packet-verification-001"
    require(not output.exists(), "Preserve packet verification")
    source, payload, gates = [json.loads(frozen(HERE / name, digest)) for name, digest in PROOFS.items()]
    require(all(p["candidate"] == CANDIDATE and p["base"] == BASE and p["status"] == "PASS"
                and not p["memory"]["breach"] for p in (source, payload, gates)),
            "Verification proofs bind another snapshot")
    require(payload["sourceProof"]["sha256"] == PROOFS["source-verification-001.json"]
            and gates["payloadProof"]["sha256"] == PROOFS["payload-verification-001.json"],
            "Verification proof graph differs")
    handoff_raw = frozen(HERE / "author-handoff-observed-001.json",
                         "f2c951b0814b87202eb66117c425ac02bbc5a5847b21255c010ce6955ce8f4b2")
    handoff = json.loads(handoff_raw)
    helper_binding = {"path": str(TOOLS / "build_b131_neutral_packet_001.py"),
                      "sha256": sha(frozen(TOOLS / "build_b131_neutral_packet_001.py"))}
    guard, _ = start_guard("B133 complete finite evidence verification")
    git = Git(REPO, RUNNER, guard)
    signed, captures, history_bindings = {}, {}, {}
    sys_path = str(WS / "lean")
    import sys
    sys.path.insert(0, sys_path)
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
        require(sha(inventory_raw) == "ceedf13e5a50e3f360c4326e3a495fe23e8b9ec3cf3db5fd72de9204c8ea607c",
                "Reported inventory differs")
        inventory = json.loads(inventory_raw)
        names = {name.removeprefix(PREFIX) for name in
                 git("ls-tree", "-r", "--name-only", CANDIDATE, "--", PREFIX).decode().splitlines()}
        require(inventory["selfExcluded"] is True
                and names == set(inventory["files"]) | {"evidence-inventory.json"} and len(names) == 217,
                "Signed evidence inventory is incomplete")
        for name, digest in inventory["files"].items():
            require(safe_relative(name) and sha(blob(name)) == digest, "Changed packet file: " + name)
            guard.check()
        require(signed[PREFIX + "producers/package_133.py"] == inventory["producerSha256"],
                "Evidence inventory producer differs")
        facts = json.loads(frozen(source["facts"]["path"], source["facts"]["sha256"]))
        verified_records = {item["path"]: item["sha256"] for item in source["sourceRecords"]}
        require(set(verified_records) == {PREFIX + item["file"] for item in
                                        facts["jmdictSelections"] + facts["kanjidic2Selections"]}
                and all(signed[name] == digest for name, digest in verified_records.items()),
                "Complete source selections differ from independent verification")
        jm, jm_bindings = union_records(facts["jmdictSelections"], "entry", "ent_seq", blob)
        kd, kd_bindings = union_records(facts["kanjidic2Selections"], "character", "literal", blob)
        require(len(jm) == 515 and len(kd) == 83, "Complete record union differs")
        comparisons, additional = {}, set()
        for name in sorted(names):
            if not (name.startswith("comparison-cards/") or name.startswith("additional/comparison-cards/")):
                continue
            char = PurePosixPath(name).stem
            require(name.endswith(".md") and char not in comparisons, "Duplicate or invalid comparison")
            raw = blob(name)
            require(raw == git("show", f"{BASE}:kanji/{char}.md"), "Comparison differs from actual baseline")
            metadata, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
            comparisons[char] = (metadata["title"], sha(raw))
            if name.startswith("additional/"):
                additional.add(char)
            else:
                readback = json.loads(blob(f"comparison-readback/{char}.json"))
                require(readback["kanji"] == char
                        and readback["completeCard"] == raw.decode("utf-8").replace("\r\n", "\n"),
                        "Comparison readback card differs")
        require(len(comparisons) == 68 and len(additional) == 6
                and comparisons.keys() - additional == set(source["packetComparisonCards"]),
                "Original/additional comparison inventory differs")
        scans = {char: json.loads(blob(f"scans/{char}.json")) for char in MEMBERS}
        cards = {item["kanji"]: item["metadata"] for item in payload["members"]}
        pair_count, new_count = pair_coverage(json.loads(blob("pair-dispositions.json")),
                                             cards, scans, comparisons, additional)
        require(pair_count == 74 and new_count == 3, "Observed finite pair counts differ")
        history = json.loads(blob("local-history-bindings.json"))
        require(Path(history["directory"]).resolve() == SCRATCH.resolve(), "Wrong history root")
        for name, digest in history["files"].items():
            path = SCRATCH / name
            require(safe_relative(name) and path.resolve().is_relative_to(SCRATCH.resolve())
                    and sha(path.read_bytes()) == digest, "Historical evidence changed: " + name)
            history_bindings[name] = digest
            guard.check()
        failed_raw = blob("author-evidence/author-gates-001/lint.json")
        failed_log = blob("author-evidence/author-gates-001/lint.log")
        failed = json.loads(failed_raw)
        require(failed["exitCode"] != 0 and failed["logSha256"] == sha(failed_log)
                and sha(failed_raw) == handoff["preservedOriginalFailure"]["lintReceiptSha256"]
                and failed_raw == (SCRATCH / "author-gates-001" / "lint.json").read_bytes()
                and failed_log == (SCRATCH / "author-gates-001" / "lint.log").read_bytes(),
                "Original author failure was altered or relabeled")
        external = json.loads(blob("external-capture-bindings.json"))
        require(external["fullCapturesLocalOnly"] is True and len(external["captures"]) == 6
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
        for row in excerpts:
            item, text = external_text[row["character"], row["provider"]]
            lines = text.decode("utf-8").splitlines()
            require(row["textSha256"] == item["textSha256"] and row["url"] == item["finalUrl"],
                    "Excerpt attribution differs")
            for excerpt in row["excerpts"]:
                require(1 <= excerpt["line"] <= len(lines)
                        and excerpt["text"] in lines[excerpt["line"] - 1], "Excerpt text or line differs")
        fonts = json.loads(blob("stroke-font-evidence.json"))
        require(fonts["converterSha256"] == payload["converterSha256"]
                and [item["kanji"] for item in fonts["members"]] == MEMBERS,
                "Font/geometry producer or members differ")
        for item in fonts["members"]:
            require(sha(git("show", f"{CANDIDATE}:strokes/{item['kanji']}.json")) == item["strokeSha256"],
                    "Font evidence stroke binding differs")
        points = fonts["codePoints"]
        chars = {point["character"] for point in points}
        paths = [f"kanji/{char}.md" for char in MEMBERS]
        paths += [f"words/{word}.md" for words in SUPPORTS.values() for word in words]
        teaching = "\n".join(git("show", CANDIDATE + ":" + name).decode("utf-8") for name in paths)
        require(len(chars) == len(points)
                and all(len(point["character"]) == 1
                        and point["codePoint"] == f"U+{ord(point['character']):04X}"
                        and point["unicodeName"] == unicodedata.name(point["character"]) for point in points)
                and chars == set(re.findall("[\u3400-\u9fff]", teaching)) | set(comparisons) | set(NAMED_GLYPHS),
                "Finite taught/component/font inventory differs")
        require(len(fonts["fonts"]) == 3 and {item["filename"] for item in fonts["fonts"]}
                == {"kanji_brush.ttf", "kanji_mincho.ttf", "kanji_textbook.ttf"}, "Font inventory differs")
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
        progress_raw = git("show", CANDIDATE + ":docs/n1-sources/batch-133-progress.json")
        progress = json.loads(progress_raw)
        require(progress["batch"] == 133 and progress["status"] == "local-unreviewed-author-candidate"
                and progress["base"] == BASE and progress["members"] == MEMBERS
                and progress["sourceRows"] == [707, 1120, 643] and progress["publishedDelivered"] == 268
                and progress["undelivered"] == 960 and progress["deliveryNotIncremented"] is True
                and progress["localUnpublishedDrafts"] == 3 and progress["proseException"] is None
                and progress["manifestSha256"] == payload["manifestSha256"]
                and progress["completeJmdictFamilies"] == len(jm)
                and progress["completeKanjidicRecords"] == len(kd)
                and progress["baselinePairRows"] == pair_count and progress["newMemberPairRows"] == new_count,
                "Progress record expands scope or prematurely credits delivery")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    captures = {name: write_frozen(output / name, raw) for name, raw in captures.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 133, "status": "PASS", "candidate": CANDIDATE, "base": BASE, "proofs": PROOFS,
        "handoffSha256": sha(handoff_raw), "signedInputs": signed, "localHistoryBindings": history_bindings,
        "capturedInputs": captures, "sourceSelections": jm_bindings + kd_bindings,
        "verifiedJmdictFamilies": len(jm), "verifiedKanjidicRecords": len(kd),
        "finiteBaselinePairs": pair_count, "finiteNewPairs": new_count, "comparisonCopies": len(comparisons),
        "externalCaptures": len(external["captures"]), "fontCodePoints": len(points),
        "fontMissingCodePoints": missing, "fontScope": fonts["scope"],
        "leanTools": tools["leanTools"], "progressSha256": sha(progress_raw),
        "unionHelper": helper_binding, "memory": memory, "verifierSha256": sha(frozen(Path(__file__))),
        "limits": "Mechanical signed-inventory, complete canonical-equal source union, finite "
                  "bidirectional pair coverage, historical byte preservation, reused external "
                  "capture/excerpt bindings and actual bounded font cmap checks. No semantic "
                  "pair judgment, historical read-depth, fresh web fetch, rendered/native/device, "
                  "independent linguistic review or publication acceptance.",
    })))


if __name__ == "__main__":
    main()
