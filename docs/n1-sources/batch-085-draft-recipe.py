"""Bounded batch085 draft operations; never acquires the parent's runner lock."""
import argparse
import ast
import copy
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "5f96404a-07d2-462b-9918-eb0db59b4ad3"
HEAD = "011cec4634c4c5cf3d72aa461e001dd50c90dfc6"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u51dd"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".592.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def start():
    for root, head in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (591, "085", "continue")
    assert not (L / "progress-before-592.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-592.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 591
    state = {
        "execution": 592, "batch": "085", "startingHead": HEAD, "androidHead": APP,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME085 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,086 or second runner.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint decoded; operative contract, complete approved issue and final591 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified child29432 of live launcher19008; launcher command decodes to approved control runner.ps1. Child never acquires/deletes/unlocks parent lock.",
        "artifactPathPreflight": "Committed source packets and approved frozen workspace inputs only; reusable helper in control. No optional historical-session helper accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution592StartingState"] = state
    p.update(stage="batch-085-runtime-drafting", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with complete live history.")


def comparisons():
    from extract_n1_jmdict import extract
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    path = C / "inputs" / "n1-implementation-JMdict_e.gz"
    raw = path.read_bytes()
    expected = snapshot["inputs"][path.name]
    assert hashlib.sha256(raw).hexdigest() == expected["sha256"]
    root = ET.fromstring(gzip.decompress(raw))
    words = ["固まる", "凍る", "集中", "熱中", "夢中", "硬い", "固い", "こりこり",
             "かちかち", "がちがち", "工夫", "趣向", "凝った", "懲らす",
             "准", "冗", "凹", "熱心", "ねっしん", "注ぐ", "冷凍", "注目",
             "注意", "気を付ける", "気をつける", "堅い", "濃度", "濃い",
             "焦点", "的", "中心"]
    ids = [e.findtext("ent_seq") for e in root.findall("entry")
           if any(k.text in words for k in e.findall("k_ele/keb") + e.findall("r_ele/reb"))]
    save(S / "batch-085-comparison-selection.json", {
        "schemaVersion": 1, "batch": "085", "entryIds": ids, "exactSpellings": words,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "limits": "Complete applicable comparison families; extraction is not semantic inspection.",
    })
    (S / "batch-085-comparison-jmdict.xml").write_bytes(extract(raw, expected["sha256"], ids))
    kd_path = C / "inputs" / "n1-planning-kanjidic2.xml.gz"
    kd_raw = kd_path.read_bytes()
    assert hashlib.sha256(kd_raw).hexdigest() == snapshot["inputs"][kd_path.name]["sha256"]
    kd = ET.fromstring(gzip.decompress(kd_raw))
    packet = ET.Element("kanjidic2")
    packet.append(copy.deepcopy(kd.find("header")))
    for entry in kd.findall("character"):
        if entry.findtext("literal") in ["准", "冗", "凹"]:
            packet.append(copy.deepcopy(entry))
    ET.indent(packet, space="  ")
    (S / "batch-085-comparison-kanjidic2.xml").write_bytes(
        ET.tostring(packet, encoding="utf-8", xml_declaration=True) + b"\n")
    print("Full comparison families extracted:", len(ids))


def geometry():
    from generate_strokes import convert, KANJIVG_REVISION
    evidence = load(S / "batch-085-stroke-evidence.json")
    raw = (S / "batch-085-kanjivg.svg").read_bytes()
    assert len(raw) == evidence["bytes"]
    assert hashlib.sha256(raw).hexdigest() == evidence["sha256"]
    assert hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == evidence["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(
        b"\r\n", b"\n")).hexdigest() == evidence["converterNormalizedSha256"]
    data = convert(CHAR, raw.decode("utf-8"))
    assert data["strokeCount"] == 16 and data["sourceRevision"] == KANJIVG_REVISION
    target = R / "strokes" / (CHAR + ".json")
    assert not target.exists()
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    print("Generated pinned16-stroke geometry using unchanged converter.")


def ledger():
    from audit_n1_pilot import metadata
    p = load(S / "batch-085-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR])
    p["dictionaryPackets"] = [
        {"selection": "batch-085-lexical-selection.json", "xml": "batch-085-jmdict.xml"},
        {"selection": "batch-085-comparison-selection.json", "xml": "batch-085-comparison-jmdict.xml"},
    ]
    for row in p["readingDispositions"]:
        row.update(kanji=CHAR, selected=row["proposedQuizSelection"],
                   reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [{
        "kanji": CHAR, "article": row["article"], "primaryReading": row["primaryReading"],
        "entryIds": [row["entryId"]], "newArticle": True,
        "allWrittenKanji": row["allWrittenKanji"], "wordJlpt": None,
        "selectedSenses": row["selectedTeaching"], "status": "local-unreviewed-draft",
    } for row in p["proposedSupportMapping"]]
    p["curatedProjection"] = [dict(p["proposedCuratedProjection"], kanji=CHAR)]
    p["requiredReciprocalPairs"] = [[CHAR, r["article"]] for r in p["supportMappings"]]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["changedReusedPassages"] = [{
        "article": "kanji/\u56fa.md",
        "before": "- \u56fa\u4f53 \u3053\u305f\u3044 - solid; solid body\n\n## Notes",
        "after": "- \u56fa\u4f53 \u3053\u305f\u3044 - solid; solid body\n"
                 "- [\u51dd\u56fa](../words/\u51dd\u56fa.md) \u304e\u3087\u3046\u3053 \u2014 coagulation; solidification\n\n## Notes",
        "reason": "One navigation-only Common words bullet; all original metadata and prose preserved.",
    }]
    card = metadata(R, "kanji/\u51dd.md")
    p["quizAudit"] = {CHAR: {
        "title": card["title"], "distractors": card["distractors"],
        "labels": [metadata(R, f"kanji/{c}.md")["title"] for c in card["distractors"]],
        "meaningDecisions": [
            {"kanji": "\u51c6", "reason": "Associate/quasi rank and approval are not congealing or absorption.",
             "evidence": "Complete frozen character record and complete unchanged article."},
            {"kanji": "\u5197", "reason": "Superfluity/uselessness, including joke compounds, is not stiffness or concentrated attention.",
             "evidence": "Complete character record, JMdict1355480 and complete unchanged article."},
            {"kanji": "\u51f9", "reason": "Concavity/hollow/sunken shape is not congealing or absorption.",
             "evidence": "Complete character record, JMdict1179150/2756450 and complete unchanged article."},
        ],
        "legacyFallbackDisposition": "Related existing\u51cd/\u56fa/\u786c each already have three wrong choices, so no default four-choice fallback slot newly opens for\u51dd. No metadata change; larger/custom pools remain outside exhaustive certification.",
    }}
    words = ["\u51dd\u56fa", "\u51dd\u308b", "\u51dd\u3089\u3059"]
    p["wordQuizAudit"] = {
        "titles": {w: metadata(R, f"words/{w}.md")["title"] for w in words},
        "directExclusions": [{
            "word": w, "exclude": metadata(R, f"words/{w}.md")["quiz_exclusions"],
            "reason": "Direct conservative guards for the sense/label overlap described below; not unrestricted substitution or a transitive cluster.",
        } for w in words],
        "decisions": [
            {"word": "\u51dd\u56fa", "neighbors": ["\u56fa\u307e\u308b", "\u51cd\u308b", "\u51b7\u51cd", "\u51dd\u308b"],
             "entryIds": ["1239120", "1266550", "1593100", "1557170", "1239070"],
             "reason": "Solidification/freezing labels overlap materially. Daijisen\u3053\u308b4/5 also documents gathering/cold solidification, beyond the introductory muscle/hobby senses. Guard that documented branch without claiming all freezing is blood coagulation."},
            {"word": "\u51dd\u308b", "neighbors": ["\u71b1\u4e2d", "\u5922\u4e2d", "\u306d\u3063\u3057\u3093", "\u96c6\u4e2d", "\u6ce8\u3050", "\u51dd\u3089\u3059"],
             "entryIds": ["1239070", "1467950", "1529500", "1467910", "1333750", "1581730", "1239010"],
             "reason": "Absorption/devotion/concentrated effort can make either broad English gloss defensible. Actual\u306b\u51dd\u308b and\u3092\u51dd\u3089\u3059 constructions remain distinct; kana-headed\u306d\u3063\u3057\u3093 is the existing\u71b1\u5fc3 identity, not a new spelling article."},
            {"word": "\u51dd\u308b", "neighbors": ["\u3053\u308a\u3053\u308a", "\u786c\u3044", "\u56fa\u3044", "\u5805\u3044", "\u304c\u3061\u304c\u3061", "\u304b\u3061\u304b\u3061"],
             "entryIds": ["1239070", "2414740", "1257110", "1003110", "1002840"],
             "reason": "Muscle stiffness and broad stiff/rigid labels overlap. Complete\u304b\u305f\u3044 spelling family and mimetic secondary senses retained, not an unrestricted food-texture interchangeability rule."},
            {"word": "\u51dd\u308b", "neighbors": ["\u56fa\u307e\u308b", "\u51cd\u308b", "\u51b7\u51cd"],
             "entryIds": ["1266550", "1593100", "1557170"],
             "reason": "Conservative protection for the broader Daijisen\u3053\u308b4/5 solidifying/cold senses; not a claim that the shoulder or golf examples mean freezing."},
            {"word": "\u51dd\u3089\u3059", "neighbors": ["\u96c6\u4e2d", "\u6ce8\u3050", "\u6ce8\u76ee", "\u6ce8\u610f", "\u6c17\u3092\u4ed8\u3051\u308b", "\u71b1\u4e2d", "\u5922\u4e2d", "\u306d\u3063\u3057\u3093"],
             "entryIds": ["1239010", "1333750", "1581730", "1426670", "1426530", "1591990", "1467950", "1529500", "1467910"],
             "reason": "Concentrating, directing attention and devotion overlap under broad quiz labels. Guard the individual pairs while preserving objects/particles and the warning versus focused-looking distinction."},
            {"word": "\u51dd\u3089\u3059", "neighbors": ["\u7126\u70b9", "\u7684", "\u4e2d\u5fc3", "\u6fc3\u5ea6"],
             "entryIds": ["1350810", "1437270", "1424550", "1469970"],
             "reason": "Conservative English-label guards: bare focus/concentration labels can conceal noun/verb and physical/mental distinctions. These are not assertions that\u51dd\u3089\u3059 means chemical concentration or the noun focal point. Full primary and separate homograph families retained."},
        ],
        "unselectedNavigation": [
            {"words": ["\u6fc3\u3044"], "entryIds": ["1469890"],
             "reason": "Deep/strong/dense description is not the concentrated-attention action in the final verb title. No direct guard added merely for a shared English substring."},
            {"words": ["\u5de5\u592b", "\u8da3\u5411", "\u61f2\u3089\u3059"],
             "entryIds": ["1278220", "1278230", "1328970", "1428180"],
             "reason": "Ingenuity/design are objects in attested constructions; the dated punishment homophone is a different meaning. No exclusion for spelling/reading alone; no\u8da3\u5411/\u61f2\u3089\u3059 article exists."},
        ],
        "confusableInventory": "Inspected inventory entry/quiz contract and exact candidate search, especially stiffness/mimetic family. No direct\u51dd row; guards rely on actual complete entries and displayed articles.",
        "limits": "Targeted label navigation and applicable complete families/selected article bodies, not an exhaustive live candidate-pool or whole-corpus ambiguity certification. Existing exclusion fields untouched.",
    }
    p["draftAuthorInspection"] = {
        "execution": 592, "sourceCheckpoint": HEAD,
        "completeLexicalPacketRanges": [[1, 300], [301, 600], [601, 900], [901, 1200], [1201, 1500]],
        "lexicalFamilies": 78, "comparisonFamilies": 31,
        "comparisonReadLimits": "Initial17 families fully returned in original packet1-300/301-620 through EOF. After expanding selection to31, every added full family returned at407-641/642-780/819-937/963-1010; original unchanged families not needlessly reread. One duplicate family\u51dd\u3063\u305f occurs across packets;109 occurrences/108 unique families.",
        "rawCharacterPackets": {"batch-085-kanjidic2.xml": [1, 90],
                                "batch-085-comparison-kanjidic2.xml": [1, 225]},
        "completeExistingArticlesRead": [
            "kanji/\u56fa.md", "kanji/\u51c6.md", "kanji/\u5197.md", "kanji/\u51f9.md",
            "kanji/\u7591.md", "kanji/\u51cd.md", "kanji/\u786c.md",
        ] + [f"words/{w}.md" for w in [
            "\u56fa\u307e\u308b", "\u51cd\u308b", "\u96c6\u4e2d", "\u71b1\u4e2d", "\u5922\u4e2d",
            "\u3053\u308a\u3053\u308a", "\u304b\u3061\u304b\u3061", "\u304c\u3061\u304c\u3061",
            "\u786c\u3044", "\u56fa\u3044", "\u5de5\u592b", "\u306d\u3063\u3057\u3093", "\u6ce8\u3050",
            "\u51b7\u51cd", "\u6ce8\u76ee", "\u6ce8\u610f", "\u6c17\u3092\u4ed8\u3051\u308b", "\u5805\u3044",
            "\u6fc3\u5ea6", "\u6fc3\u3044", "\u7126\u70b9", "\u7684", "\u4e2d\u5fc3",
        ]],
        "publicSources": [
            {"url": "https://kotobank.jp/word/\u51dd\u308b-500448", "maxLength": 14000,
             "scope": "Daijisen\u3053\u308b all5 senses and\u3053\u3054\u308b initial definitions; later material truncated, not freshly claimed read."},
            {"url": "https://kotobank.jp/word/\u51dd\u3089\u3059-500443", "maxLength": 11000,
             "scope": "Complete returned Daijisen\u3053\u3089\u3059/\u3053\u3054\u3089\u3059 and Seisen headings."},
            {"url": "https://kotobank.jp/word/\u51dd\u56fa-52596", "maxLength": 9000,
             "scope": "Daijisen all3 senses and Seisen headings; later encyclopedia truncated, no full scientific audit."},
        ],
        "examples": "Blood coagulation, shoulder stiffness, golf\u306b\u51dd\u308b and elaborate outfit use the inspected Daijisen constructions. Eyes/ingenuity/breath have exact complete JMdict construction families. Original English translations and standard inflections; no invented rare collocation.",
        "limits": "Author inspection only, not independent review or native/phone certification. A failed view of absent\u8da3\u5411.md is not evidence that the lexical family is absent; full family1328970 retained.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only. Original source-preparation proposals and limits remain historical; runtime teaching needs both serial blind different-family reviews.",
        "All6 metadata readings/order retained;3 selected raw strings produce2 scheduled keys: on\u304e\u3087\u3046 and kun\u3053\u308b. Selected\u3053.\u3089\u3059 shares stem\u3053; no independent queued mastery or algorithm change claimed.",
        "Three unselected\u3053\u3054 readings are dictionary-verified recognition material, not source-only gaps or unsupported rare/archaic assertions.",
        "No reviewer, Android/native, fourfont/system-fallback legibility or phone acceptance performed in this draft checkpoint. Original all40 evidence remains inherited with its limits.",
        "Published111/1228 and1117 acceptance-remainder unchanged. Six separately published earlierN2 source members\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50 are not issue60 accepted additions or candidates to duplicate/relevel.",
        "CompatibleAndroidf9b59a2+ required; qualifiedTESTONLY1c1b7bf4 is not latestappmain. Physicalphone/generalrelease/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combinedmain/signing/ownerpush/terminalCI/eachimmutableZIPhash/budget/issue gates unchanged. No optional historicalsessionhelper or parentlock access; no086.",
    ]
    p["nextAction"] = "SAME085 two serial blind different-family initial textual reviews on the normally signed LOCAL UNREVIEWED snapshot, including all4 new articles and exact one-bullet solid-card diff. Reconcile source-backed findings before subsequent fresh non-skipped Android/native/fourfont/visual/combinedmain/normal-signing/ownerpush/CI/immutableZIP/originalbudget/issue gates. No086 or push from unreviewed branch."
    save(S / "batch-085-progress.json", p)
    print("Draft ledger records6 readings,3 primary supports and4 all-mapped pairs.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert

    result = batch_audit(R, "085")
    p = load(S / "batch-085-progress.json")
    assert p["status"] == "local-unreviewed-draft" and p["reviewClosed"] == p["published"] == []
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and hashlib.sha256(raw).hexdigest() == info["sha256"], name
    raw_jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    raw_kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert hashlib.sha256(gzip.decompress(raw_jm)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(gzip.decompress(raw_kd)).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    packet_receipts = []
    for packet in p["dictionaryPackets"]:
        selection = load(S / packet["selection"])
        expected = extract(raw_jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"],
                           selection["entryIds"])
        assert expected == (S / packet["xml"]).read_bytes()
        packet_receipts.append({"path": packet["xml"], "families": len(selection["entryIds"]),
                                "lines": len(expected.splitlines()),
                                "sha256": hashlib.sha256(expected).hexdigest(),
                                "freshFrozenExtractionMatches": True})
    assert sum(x["families"] for x in packet_receipts) == 109
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(raw_kd)).findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    character_count = 0
    for name in ["batch-085-kanjidic2.xml", "batch-085-comparison-kanjidic2.xml"]:
        for record in ET.parse(S / name).getroot().findall("character"):
            assert canonical(record) == canonical(records[record.findtext("literal")])
            character_count += 1
    assert character_count == 4
    baseline = load(S / "baseline-inventory.json")
    exceptions = {"words/\u864e.md": ["\u9154\u3063\u6255\u3044"],
                  "words/\u733f.md": ["\u99ac\u9e7f"],
                  "words/\u4e18.md": ["\u5742", "\u5c71"],
                  "words/\u5197\u8ac7.md": ["\u30e6\u30fc\u30e2\u30a2"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(info["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/\u5c71.md":
                expected["distractors"] = ["\u5ddd", "\u51fa", "\u6728"]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert hashlib.sha256((R / name).read_bytes()).hexdigest() == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and named[93] == CHAR
    published = set("\u5e79\u6c0f\u6271\u4e43\u51f9\u51f8\u77db\u9df9\u5f57\u6f31\u681e\u8389")
    for path in S.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    old = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {path.stem for path in (R / "kanji").glob("*.md")}
    separate = set("\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50")
    separate_other = set("\u574a\u7684\u8ab0\u8eab\u962a")
    assert len(published) == 111
    assert current - old == published | separate | separate_other | {CHAR}
    base_manifest = json.loads(git("show", p["baseCommit"] + ":manifest.json"))
    assert all(f"kanji/{c}.md" in base_manifest["files"] for c in separate | separate_other)
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    pairs = {(c, row["article"]) for row in p["supportMappings"]
             for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(row) for row in p["allMappedReciprocalPairs"]} and len(pairs) == 4
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    assert {f"words/{path.name}" for path in (R / "words").glob("*.md")
            if CHAR in metadata(R, f"words/{path.name}")["kanji"]} == {r["article"] for r in p["supportMappings"]}
    for row in p["supportMappings"]:
        assert "jlpt" not in metadata(R, row["article"])
    guards = {tuple(sorted([row["word"], other])) for row in p["wordQuizAudit"]["directExclusions"]
              for other in row["exclude"]}
    assert len(guards) == 31
    for c in ["\u51cd", "\u56fa", "\u786c"]:
        assert len(metadata(R, f"kanji/{c}.md")["distractors"]) == 3
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = (hashlib.sha256((R / name).read_bytes()).hexdigest() if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name))
                assert actual == expected, name
                checked += 1
    assert checked == 8413
    svg = (S / "batch-085-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / "\u51dd.json") == convert(CHAR, svg.decode("utf-8"))
    save(S / "batch-085-draft-stroke-audit.json", dict(
        load(S / "batch-085-stroke-evidence.json"), converted=True,
        output="strokes/\u51dd.json",
        outputSha256=hashlib.sha256((R / "strokes" / "\u51dd.json").read_bytes()).hexdigest(),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False,
        limits="Pinned unchanged converter and exact SVG output only; no native drawing acceptance."))
    scope = ["kanji/\u51dd.md"] + [r["article"] for r in p["supportMappings"]]
    changed = p["changedReusedPassages"][0]["after"].split("\n")[1]
    text = "".join((R / name).read_text(encoding="utf-8") for name in scope) + changed
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-085-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    assert not rare, rare
    save(S / "batch-085-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "085", "completeNewArticleScope": scope,
        "changedReusedScope": {"kanji/\u56fa.md": changed}, "actualHanCount": len(han), "actualHan": han,
        "articleHashes": {name: hashlib.sha256((R / name).read_bytes()).hexdigest() for name in scope},
        "fonts": fonts, "rareHanRangeCharacters": rare, "nativeFontAcceptance": "pending",
        "limits": "Actual complete new draft and changed bullet Han/cmaps only. Cmap absence is not a glyph failure or actual fallback-face evidence. Fresh non-skipped RareHan/native/fourfont/visual acceptance remains required.",
    })
    result.update(schemaVersion=1, execution=592, stage="local-unreviewed-draft",
                  sourceCheckpoint=HEAD, packets=packet_receipts, frozenInputHashesVerified=5,
                  decompressedDictionaryHashesVerified=2, completeRawCharacterRecordsVerified=character_count,
                  originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
                  baselineKanjiDistractorException={"kanji/\u5c71.md": ["\u5ddd", "\u51fa", "\u6728"]},
                  allMappedReciprocalPairs=len(pairs), directedLinksVerified=len(pairs) * 2,
                  directWordExclusionPairs=len(guards), allRuntimePayloadHashesVerified=checked,
                  currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                                 "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                                 "namedSourceMembersPresent": len(current & set(named))},
                  separateEarlierLevelSourceMembers=sorted(separate),
                  separateNonN1SourceMainAdditions=sorted(separate_other),
                  actualHanCount=len(han), pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
                  publishedAdditions=111, remainingAdditions=1117, draftOnlyAdditions=[CHAR],
                  runtimePublished=False, independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
                  physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
                  wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
                  actualNewPermissionDenials=[], limits=p["limits"])
    save(S / "batch-085-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    result = load(S / "batch-085-draft-audit.json")
    receipts = {}
    test_count = 0
    for stem in ["validate", "manifest", "draft-audit", "draft-n1-tests",
                 "draft-format-tests", "vocabulary-consistency", "budget"]:
        raw = (L / f"{stem}-592.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8413" in text and result["contentVersion"] in text
        elif stem == "draft-audit":
            assert json.loads(text) == result
        elif stem in {"draft-n1-tests", "draft-format-tests"}:
            import re
            assert text.rstrip().endswith("OK") and "skipped" not in text
            test_count += int(re.search(r"Ran (\d+) tests", text)[1])
        elif stem == "vocabulary-consistency":
            assert "reviewed prompts" in text
        elif stem == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000
            assert budget["retainedBytes"] <= 56 * 1024 ** 2
            assert budget["inflatedBytes"] <= 80 * 1024 ** 2
            assert budget["localZipBytes"] <= 42 * 1024 ** 2
        target = S / f"batch-085-{stem}-592.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(),
                          "sha256": hashlib.sha256(packed).hexdigest(),
                          "uncompressedSha256": hashlib.sha256(raw).hexdigest()}
    evidence = {
        "schemaVersion": 1, "execution": 592, "batch": "085",
        "stage": "local-unreviewed-draft", "sourceCheckpoint": HEAD,
        "baseCommit": result["baseCommit"], "runtimePublished": False,
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "focusedTestsPassed": test_count, "validatorErrors": 0, "localBudget": budget,
        "audit": "docs/n1-sources/batch-085-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-085-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-085-draft-stroke-audit.json",
        "diagnostics": "docs/n1-sources/batch-085-draft-diagnostics.json",
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "recipe": "docs/n1-sources/batch-085-draft-recipe.py",
        "artifactPathPreflight": "Committed source packets and approved workspace inputs only; no optional historicalsessionhelper requested/accessed.",
        "runnerLockRole": "Parent19008 owns runner.lock throughout child29432 lifetime; no child acquisition/deletion/unlock.",
        "actualNewPermissionDenials": [], "publishedAdditions": 111, "remainingAdditions": 1117,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": load(S / "batch-085-progress.json")["nextAction"],
    }
    (S / "batch-085-draft-recipe.py").write_bytes(Path(__file__).read_bytes())
    evidence["recipeSha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    save(S / "execution-592.json", evidence)
    print("All local draft check receipts and durable recipe archived.")


def finish():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    evidence = load(S / "execution-592.json")
    result = load(S / "batch-085-draft-audit.json")
    for receipt in evidence["checks"].values():
        raw = (R / receipt["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == receipt["sha256"]
        assert hashlib.sha256(gzip.decompress(raw)).hexdigest() == receipt["uncompressedSha256"]
    assert hashlib.sha256((S / "batch-085-draft-recipe.py").read_bytes()).hexdigest() == evidence["recipeSha256"]
    before = load(L / "progress-before-592.json")
    p = load(C / "progress.json")
    allowed = {"stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 592, "checkpoint": 592, "batch": "085",
        "status": "continue", "stage": "local-unreviewed-draft", "savedCommit": head,
        "signature": "G", "sourceCommit": HEAD, "evidence": "docs/n1-sources/execution-592.json",
        "membership": [CHAR], "sourceRow": 94, "runtimeDrafted": [CHAR],
        "reviewClosed": [], "published": [], "runtimePublished": False,
        "focusedTestsPassed": evidence["focusedTestsPassed"], "validatorErrors": 0,
        "allRuntimePayloadHashesVerified": 8413, "readingDispositions": 6,
        "selectedRawReadings": 3, "curatedOfferedKeys": 2, "sourceOnlyOfferedKeys": 0,
        "uniqueCompleteDictionaryFamilies": 108, "familyOccurrences": 109,
        "rawCharacterRecords": 4, "allMappedReciprocalPairs": 4,
        "directWordExclusionPairs": result["directWordExclusionPairs"], "pinnedConvertedStrokes": 16,
        "actualHanCount": result["actualHanCount"], "nativeFontAcceptance": "pending",
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 111, "remainingAdditions": 1117,
        "lastPublishedCommit": p["lastPublishedCommit"], "dedicatedWorktreesClean": True,
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "originalHistoricalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": evidence["nextAction"],
    }
    p["execution592CoordinatorCheckpoint"] = checkpoint
    p.update(checkpoint=592, status="continue", stage="batch-085-signed-local-unreviewed-draft",
             nextAction=evidence["nextAction"], blocker=None)
    allowed |= {"checkpoint", "status"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(C / "progress.json", p)
    body = (
        f"Batch 085 **local unreviewed draft** preserved at normally signed `{head}` "
        f"(source `{HEAD}`).\n\n"
        "Added only \u51dd, necessary \u51dd\u56fa/\u51dd\u308b/\u51dd\u3089\u3059 support, pinned generated16-stroke geometry "
        "and one navigation-only \u56fa bullet. All6 source readings/order retained; raw selected "
        "\u30ae\u30e7\u30a6/\u3053.\u308b/\u3053.\u3089\u3059 produce only2 scheduled keys (\u304e\u3087\u3046/\u3053\u308b), not independent "
        "\u3053\u3089\u3059 queue mastery. All3 unselected\u3053\u3054 readings have verified recognition examples, "
        "not invented source-only/archaic labels. 108 unique complete dictionary families "
        "(109 packet occurrences),4 raw character records,4 all-mapped reciprocal pairs "
        f"and{result['directWordExclusionPairs']} direct word guards recorded. "
        f"{evidence['focusedTestsPassed']} focused tests, validator, regenerated manifest, vocabulary consistency "
        "and original local budget checks passed; all8413 runtime hashes verified. "
        "Baseline metadata/strokes preserved apart from historical documented exceptions.\n\n"
        "**Not review-closed or published.** No reviewers, new Android/native/fourfont/phone acceptance claimed. "
        "Actual \u51dd/\u7591/\u51ab and all draft Han legibility remains pending; cmap absence is not glyph failure. "
        "Next is both serial blind different-family textual reviews, reconciliation, then every original "
        "fresh Android/native/visual/latest-main/normal-signing/owner-push/terminalCI/immutableZIP/budget/issue gate. "
        "111/1228 issue additions published;1117 remain. Six separately published earlierN2 source "
        "members are not counted as accepted issue60 additions or duplicated. Physical-phone/general-release/"
        "whole-set acceptance remains outstanding. Checkpoint592 saved with complete history and status "
        "`continue`; no086, second runner, parentlock touch or optional historicalsessionhelper access.\n"
    )
    (C / "batch-085-draft-592-issue.txt").write_text(body, encoding="utf-8")
    print("Signed clean local draft checkpoint persisted:", head)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["start", "comparisons", "geometry", "ledger", "audit",
                                             "record", "finish"])
    args = parser.parse_args()
    globals()[args.operation]()
