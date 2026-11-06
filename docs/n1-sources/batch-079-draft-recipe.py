"""Persist and audit the bounded, unreviewed batch 079 runtime draft."""
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CONTROL = Path(r"C:\Users\stop-\n1-kanji-workspace\control")
ROOT = CONTROL.parent / "learning-japanese"
LOGS = CONTROL / "logs" / "e7bae115-6f0c-4c1e-b771-35e9c47b0227"
OUT = ROOT / "docs" / "n1-sources"
SOURCE = "529c4e0d367abfb08381038978dafc3f9f6b1048"
BASE = "2a6777503de6c23c2ac5582b0265dd68d224f44c"
EXECUTION = 530
sys.path.insert(0, str(ROOT / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(
        ["git", "--no-pager", *args], cwd=ROOT, encoding="utf-8").strip()


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 529 and progress["batch"] == "079"
    assert progress["lastPublishedCommit"] == BASE
    assert git("rev-parse", "HEAD") == SOURCE
    assert git("rev-parse", "origin/main") == BASE
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    backup = LOGS / "checkpoint-full-start.json"
    assert not backup.exists()
    save(backup, progress)
    request = (LOGS / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 529
    progress["execution530StartingState"] = {
        "execution": EXECUTION, "batch": "079", "startingHead": SOURCE,
        "freshOriginMain": BASE,
        "scope": "SAME079 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,080 or second runner.",
        "status": "runtime-draft-in-progress",
        "authorization": {
            "requestSha256": digest(request), "bytes": len(request),
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, final529 and complete approved issue inspected directly. Historical middle loaded/parsed, not freshly semantically re-reviewed.",
        },
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "inputs": "Committed source packets and approved workspace inputs.",
            "durableHelper": str(Path(__file__)),
            "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        },
        "worktrees": "Dedicated worktrees clean; normally signed G content529c4e0d and Androidf9b59a2. Fresh main2a677750; canonical repositories not accessed.",
        "startedAt": datetime.now().astimezone().isoformat(),
    }
    progress.update(status="continue", stage="batch-079-runtime-draft-in-progress",
                    blocker=None, nextAction="SAME079 bounded runtime draft only; normally signed LOCAL UNREVIEWED freeze, then yield before later gates.")
    save(CONTROL / "progress.json", progress)
    print("Starting scope persisted with full live history.")


def strokes():
    from generate_strokes import convert

    record = load(OUT / "batch-079-stroke-evidence.json")
    svg = Path(record["input"]).read_bytes()
    assert digest(svg) == record["sha256"]
    converter = (ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")
    assert digest(converter) == record["converterNormalizedSha256"]
    data = convert("冠", svg.decode("utf-8"))
    assert data["strokeCount"] == len(data["strokes"]) == 9
    assert data["sourceRevision"] == record["revision"]
    target = ROOT / "strokes" / "冠.json"
    assert not target.exists()
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print("Generated nine strokes with unchanged pinned converter.")


def ledger():
    data = load(OUT / "batch-079-progress.json")
    assert data["status"] == "source-prepared-not-drafted"
    data["status"] = "local-unreviewed-draft"
    data["drafted"] = ["冠"]
    for row in data["readingDispositions"]:
        row["selected"] = row["proposedQuizSelection"]
        row["reason"] = (
            "Useful crown compound; complete JMdict1181450 and the Daijisenカン character branch "
            "explicitly listing王冠 establish the spelling/reading and allocation. Own linked王冠 row."
            if row["kind"] == "on" else
            "Exact single-character native noun in complete JMdict1577620; existing N2 primaryかんむり "
            "and all exclusions preserved. Own linked冠 row.")
    data["supportMappings"] = []
    for proposal in data["proposedSupportMapping"]:
        mapping = dict(proposal)
        mapping["entryIds"] = [mapping.pop("entryId")]
        mapping["newArticle"] = mapping.pop("newArticleNecessary")
        mapping["status"] = "local-unreviewed-draft"
        data["supportMappings"].append(mapping)
    data["requiredReciprocalPairs"] = [
        ["冠", "words/冠.md"], ["冠", "words/王冠.md"]]
    data["allMappedReciprocalPairs"] = data["proposedReciprocalPairs"]
    data["changedReusedPassages"] = data["proposedChangedReusedPassages"]
    data["curatedProjection"] = [data["proposedCuratedProjection"]]
    proposal = data["proposedKanjiQuizAudit"]
    data["quizAudit"] = {"冠": {
        "title": proposal["title"],
        "distractors": [r["kanji"] for r in proposal["distractors"]],
        "labels": [r["title"] for r in proposal["distractors"]],
        "meaningDecisions": proposal["distractors"],
        "legacyFallbackDisposition": proposal["legacyFallbackDisposition"],
    }}
    word_quiz = data["proposedWordQuizAudit"]
    data["wordQuizAudit"] = {
        "directExclusions": [{
            "word": "王冠", "exclude": word_quiz["directExclusions"],
            "reason": word_quiz["reason"],
        }],
        "comparisonDisposition": word_quiz["otherInspectedComparisons"],
        "confusableInventory": word_quiz["confusableInventory"],
        "limits": "Coordinator scoped judgment only; independent two-family review pending.",
    }
    data["draftAuthorInspection"] = {
        "execution": EXECUTION, "sourceCheckpoint": SOURCE,
        "inheritedSourceInspection": "Committed source079 retains complete177-family/5-raw-record/15-article inspection with returned ranges; not claimed as a fresh complete177-family reread in execution530.",
        "freshInspection": [
            "Complete JMdict1181450 and1577620 including all restrictions and senses",
            "Complete18-family comparison and one-family related packet",
            "Complete existing冠/王/帽子/蓋/栓/冗/完/守 articles",
            "Daijisen冠 characterカン branch explicitly listing王冠, separateかん andかんむり headings",
            "Complete Daijisen王冠 general-word heading; separate named-work/cultivar headings not used",
        ],
        "liveWebReturns": [
            {"url": "https://www.weblio.jp/content/冠", "range": [0, 14500],
             "scope": "All three applicable headings returned; later historical entry truncated, not used."},
            {"url": "https://www.weblio.jp/content/王冠", "range": [0, 9000],
             "scope": "Complete general-word heading returned; later encyclopedia remainder truncated, not used."},
        ],
        "examples": "Two original simple learner sentences; not claimed as dictionary quotations or corpus attestations. Wearing-stateかぶっています and bottlecap-removal外しました preserve actual object and event stage.",
        "historicalClaims": "None introduced. Modern-shape mnemonic explicitly invented; source SVG phon annotation is not used as historical proof.",
    }
    data["runtimeDraftEvidence"] = "batch-079-draft-audit.json"
    data["fontDisposition"] = "Reinventory complete four affected runtime articles in batch-079-draft-font-audit.json. Exact冖/宀 require later native fallback inspection; no glyph failure or actual acceptance inferred."
    data["nextAction"] = "Two serial blind initial different-family textual reviewers on the same normally signed local079 draft, then evidence-based reconciliation. Do not start080 or publish unreviewed content."
    data["limits"] = (
        "LOCAL UNREVIEWED runtime draft only. No independent review, fresh Android/native/font/phone "
        "acceptance, review closure, publication or080. Frozen source stage remains historical evidence. "
        "Every original acceptance gate, archive guard, source/reviewer/process/denial/OOM/read-depth "
        "limitation and reviewed baseline exception is preserved. Physical-phone, general-release and "
        "whole-set acceptance remain outstanding.")
    save(OUT / "batch-079-progress.json", data)
    print("Runtime draft ledger generated; source-only proposals retained as history.")


def audit():
    import xml.etree.ElementTree as ET
    from audit_n1_batch import audit as batch_audit, base_file, lexical_pair
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert

    data = load(OUT / "batch-079-progress.json")
    result = batch_audit(ROOT, "079")
    assert data["status"] == "local-unreviewed-draft"
    assert data["reviewClosed"] == data["published"] == []
    snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        assert digest((CONTROL / "inputs" / name).read_bytes()) == info["sha256"], name
    raw = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    families, packet_receipts = {}, []
    for item in data["dictionaryPackets"]:
        selection = load(OUT / item["selection"])
        path = OUT / item["xml"]
        expected = extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"],
                           selection["entryIds"])
        assert expected == path.read_bytes()
        entries = ET.fromstring(expected).findall("entry")
        families.update((e.findtext("ent_seq"), e) for e in entries)
        packet_receipts.append({"path": path.name, "families": len(entries),
                                "sha256": digest(expected), "freshExtractionMatches": True})
    assert len(families) == 177
    assert lexical_pair(families["1181450"], "王冠", "おうかん")
    assert lexical_pair(families["1577620"], "冠", "かんむり")
    assert [g.text for g in families["1181450"].findall("sense/gloss")] == ["crown", "diadem", "bottle cap"]
    assert families["1577620"].findall("sense")[4].findtext("stagr") == "かん"
    mappings = data["supportMappings"]
    pairs = {(c, row["article"]) for row in mappings
             for c in metadata(ROOT, row["article"])["kanji"]
             if (ROOT / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in data["allMappedReciprocalPairs"]}
    assert len(pairs) == 3
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (ROOT / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (ROOT / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    assert metadata(ROOT, "words/冠.md") == metadata_from_base("words/冠.md")
    assert metadata(ROOT, "kanji/王.md") == metadata_from_base("kanji/王.md")
    assert "jlpt" not in metadata(ROOT, "words/王冠.md")
    baseline = load(OUT / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(info["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/山.md":
                expected["distractors"] = ["川", "出", "木"]
            assert metadata(ROOT, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert digest((ROOT / name).read_bytes()) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert named[87] == "冠"
    old_kanji = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current_kanji = {p.stem for p in (ROOT / "kanji").glob("*.md")}
    published = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in OUT.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    assert len(published) == 105 and current_kanji - old_kanji == published | {"冠"}
    assert len(current_kanji) == 1091 and len(current_kanji & set(named)) == 110
    assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
    assert sum(metadata(ROOT, f"kanji/{p.name}")["jlpt"] == 1
               for p in (ROOT / "kanji").glob("*.md")) == 111
    assert len(list((ROOT / "words").glob("*.md"))) == 5047
    manifest = build_manifest(ROOT)
    assert manifest == load(ROOT / "manifest.json")
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = digest((ROOT / name).read_bytes()) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(ROOT / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8363
    stroke_source = load(OUT / "batch-079-stroke-evidence.json")
    svg = Path(stroke_source["input"]).read_bytes()
    assert digest(svg) == stroke_source["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke_source["gitBlob"]
    assert digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == stroke_source["converterNormalizedSha256"]
    stroke = load(ROOT / "strokes" / "冠.json")
    assert stroke == convert("冠", svg.decode("utf-8"))
    assert stroke["strokeCount"] == 9
    assert [s["id"] for s in stroke["strokes"]] == list(range(1, 10))
    stroke_receipt = dict(stroke_source, converted=True,
                          outputSha256=digest((ROOT / "strokes" / "冠.json").read_bytes()),
                          output="strokes/冠.json", geometryExactlyRegenerated=True,
                          nativeDrawingAccepted=False,
                          limits="Unchanged pinned conversion only; not native rendering, recognition, handwriting or human recall acceptance.")
    save(OUT / "batch-079-draft-stroke-audit.json", stroke_receipt)
    scope = ["kanji/冠.md", "words/王冠.md", "words/冠.md", "kanji/王.md"]
    text = "".join((ROOT / name).read_text(encoding="utf-8") for name in scope)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(OUT / "batch-079-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert digest(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        missing = [c for c in han if ord(c) not in cmap]
        assert missing == ["冖", "宀"]
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "allActualMissing": missing,
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    font_record = {
        "schemaVersion": 1, "batch": "079", "completeRuntimeScope": scope,
        "articleHashes": {n: digest((ROOT / n).read_bytes()) for n in scope},
        "actualHanCount": len(han), "actualHan": han, "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "pendingNativeFallbackLabels": ["冖", "宀"],
        "limits": "Actual complete four-article draft inventory and bundled cmaps only. 冖/宀 lie outside RareHan ranges. Cmap absence is not glyph failure. Actual native/viewport/font acceptance is pending, not inherited from previous batch.",
    }
    save(OUT / "batch-079-draft-font-audit.json", font_record)
    result.update({
        "schemaVersion": 1, "execution": EXECUTION, "stage": "local-unreviewed-draft",
        "sourceCheckpoint": SOURCE, "packets": packet_receipts,
        "frozenInputHashesVerified": 5,
        "allMappedReciprocalPairs": len(pairs), "directedLinksVerified": len(pairs) * 2,
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "baselineMetadataExceptions": exceptions,
        "baselineKanjiDistractorException": {"kanji/山.md": ["川", "出", "木"]},
        "allRuntimePayloadHashesVerified": checked,
        "publishedAdditions": 105, "draftOnlyAdditions": ["冠"], "remainingAdditions": 1123,
        "currentCounts": {"kanji": 1091, "words": 5047, "n1Labels": 111,
                          "namedSourceMembersPresent": 110},
        "actualHanCount": len(han), "pendingNativeFallbackLabels": ["冖", "宀"],
        "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "limits": data["limits"],
    })
    save(OUT / "batch-079-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def metadata_from_base(name):
    import yaml
    from audit_n1_batch import base_file
    return yaml.safe_load(base_file(ROOT, BASE, name).split("---", 2)[1])


def record():
    import ast

    audit_result = load(OUT / "batch-079-draft-audit.json")
    receipts = {}
    for name in ("validate-530.txt", "manifest-530.txt", "audit-530.txt",
                 "draft-tests-530.txt", "budget-530.txt"):
        path = LOGS / name
        text = path.read_text(encoding="utf-8-sig")
        if name.startswith("validate"):
            assert "0 error(s)" in text
        elif name.startswith("manifest"):
            assert "8363" in text and "a01eb85b17601ac0" in text
        elif name.startswith("draft-tests"):
            assert "Ran 22 tests" in text and "OK" in text
            assert "FAILED" not in text and "skipped" not in text
        elif name.startswith("budget"):
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] == 8385
        else:
            assert json.loads(text) == audit_result
        receipts[name] = {"path": str(path), "sha256": digest(path.read_bytes()),
                          "completeOutput": text}
    recipe = OUT / "batch-079-draft-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(OUT / "execution-530.json", {
        "schemaVersion": 1, "execution": EXECUTION, "batch": "079",
        "stage": "local-unreviewed-draft",
        "sourceCheckpoint": SOURCE, "baseCommit": BASE,
        "startingState": load(CONTROL / "progress.json")["execution530StartingState"],
        "runtimeScope": ["kanji/冠.md", "strokes/冠.json", "words/王冠.md",
                         "words/冠.md", "kanji/王.md", "manifest.json"],
        "sourcePacket": "batch-079-progress.json",
        "draftAudit": "batch-079-draft-audit.json",
        "strokeAudit": "batch-079-draft-stroke-audit.json",
        "fontAudit": "batch-079-draft-font-audit.json",
        "durableRecipe": {"controlPath": str(Path(__file__)), "archive": recipe.name,
                          "sha256": digest(recipe.read_bytes())},
        "checks": receipts, "archiveBudget": budget,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runtimePublished": False, "reviewClosed": [], "published": [],
        "publishedAdditions": 105, "remainingAdditions": 1123,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": "Normally sign LOCAL UNREVIEWED079 freeze; preserve owner issue receipt and full live checkpoint, then yield. Next coordinator runs two serial blind different-family textual reviewers on this exact snapshot; no080.",
        "limits": audit_result["limits"],
    })
    print("Complete draft check outputs, source-derived audit and durable recipe archived.")


def issue_body():
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == BASE
    body = (
        f"Batch 079 runtime draft is frozen at normally signed LOCAL {head} (not pushed or published): "
        "one new kanji 冠, its pinned nine-stroke file, and one necessary 王冠おうかん support article "
        "without an inferred vocabulary level. Full source カン / かんむり and their order remain; both "
        "have their own linked practice rows. Existing 冠かんむり keeps its N2 level, primary reading, "
        "examples and all eight exclusions; only navigation changes. Older 王 gains the exact reciprocal link.\n\n"
        "The draft distinguishes royal crown, crown-type metal bottle cap, ceremonial headgear and "
        "reading-specific peerless uses. Three curated wrong meanings are 冗/完/守. Direct 王冠 safeguards "
        "cover 冠/帽子/蓋/栓; these are not transitive synonym groups. All three mapped pairs/six directions, "
        "the activated baseline pair, exact membership, all 8,363 runtime hashes, frozen source packets "
        "and original baseline invariants pass the draft audits, with all previously reviewed exceptions preserved.\n\n"
        "Validator, regenerated manifest, 22 focused draft-audit regressions and unchanged archive guards pass "
        "(8,385 entries; 44,145,678 retained bytes; 44,414,016 inflated; 30,168,306 local compressed). "
        "Manifest contentVersion is a01eb85b17601ac0. All 35 actual Han across the four affected articles "
        "were checked against the three bundled cmaps; exact 冖/宀 need later native fallback inspection. "
        "Cmap absence is not a glyph failure or actual visual acceptance. Committed source079 retains "
        "177 complete families/five raw records; this execution does not claim a fresh full177-family "
        "linguistic reread. The exact support families, comparison packet and applicable live Daijisen "
        "headings were freshly inspected.\n\n"
        "Checkpoint530 yields before the SAME079 two serial blind different-family textual initial reviews. "
        "No reviewer, Android/native run, review closure, content publication or batch080 is claimed. "
        "Reusable helper is in the approved control workspace and archived with evidence; no optional "
        "historical session helper was accessed and no new permission denial occurred. Published coverage "
        "remains 105/1,228 additions, 1,123 remaining. Every original gate, archive guard and historical "
        "source/review/process/denial/OOM/read-depth limitation remains. Compatible Android f9b59a2+ is "
        "required; physical-phone/general-release and whole-set acceptance remain outstanding.\n")
    (LOGS / "issue-update-530.txt").write_text(body, encoding="utf-8")
    save(LOGS / "signed-draft-530.json", {
        "commit": head, "signature": "G", "sourceCommit": SOURCE,
        "originMain": BASE, "bodySha256": digest(body.encode("utf-8")),
        "clean": True, "runtimePublished": False,
    })
    print(f"Normally signed local unreviewed freeze {head}; owner issue body prepared.")


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == BASE
    body = (LOGS / "issue-update-530.txt").read_text(encoding="utf-8")
    response = load(LOGS / "issue-response-530.json")
    assert response["user"]["login"] == "stop-cran"
    assert response["body"].replace("\r\n", "\n") == body.replace("\r\n", "\n")
    original = load(LOGS / "checkpoint-full-start.json")
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == original["checkpoint"] == 529
    next_action = (
        f"Batch079 normally signed LOCAL UNREVIEWED draft {head}; not pushed/reviewed/published. "
        "NEXT fresh coordinator: read entire request/final checkpoint/scoped live keys, preserve FULL history, "
        "verify clean signed dedicated heads/fresh main and SAME079 exact snapshot. Execute TWO serial blind "
        "initial different-family textual reviewers on this unchanged snapshot, preserving complete reports "
        "and actual model/process/read evidence; serial internal tools and actual first process exit before "
        "second. Use actual CLI help/catalog; no author agents/nested trees/concurrent heavy work/second runner. "
        "Scope new冠 and necessary王冠, complete reused冠 and exact王 addition; both full/curated linked rows, "
        "カン/かんむり allocation, crown/ceremonial/bottlecap/peerless senses, threewrong冗完守 labels and actual "
        "direct冠帽子蓋栓 guards, all3mappedpairs6directions/activatedpair, natural examples and phone comprehensibility. "
        "Use committed177completefamilies/5rawrecords/source529 and exact runtime diff; authorfreshreads530 "
        "explicitly bounded, not full177reread. New王冠 has NO inferred wordlevel; existing冠N2/all8guards/primary/examples "
        "and王metadata preserved. Stroke9 exactly regenerated pinnedconverter/SVG;35actualHan all3cmaps,冖/宀 "
        "nativefallback PENDING, not presumedfailure.22focusedtests/validator/manifest/all8363hashes/exact "
        "base runtime delta/baseline/membership/source/link/reading/font/budget audits pass. "
        "Reconcile source-backed findings and confirm bounded corrections with original sessions where possible; "
        "normally sign LOCAL textual checkpoint and yield before freshAndroid/native/publication/080. "
        "All later gates remain required including non-skippedAndroid/native/currentmain/normal signing/"
        "ownerfastforward/greenCI/EVERYimmutableZIPhash/originalbudgets. No unreviewedpush/signingretry/"
        "permissionworkaround. Use approved workspace inputs/committed source; reusable helper "
        "control\\draft-batch-079.py archived with packet. Optional historicalsession recipes NOT required; "
        "no deniedpath retry. Preserve/report/yield on actualnewdenials. Published105/1228,remaining1123; "
        "draft counts1091kanji5047words111N1labels110namedmembers plus妖; new support is NOTN1vocabulary. "
        "Preserve accepted078publication2a677750 and ALL historical source/review/process/denial/OOM/"
        "lookup/readdepth/loadingtree limits, reviewed虎/猿/丘/山 plus冗談 exceptions; do not rerun acceptedheavywork "
        "absentnewconcern. HOST-only2GiBinit NEVER enters nativebuilds; no app/guestheap/archiveguard changes. "
        "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete.")
    receipt = {
        "url": response["html_url"], "commentId": response["id"], "author": "stop-cran",
        "bodyVerified": True, "body": body,
        "rawResponseSha256": digest((LOGS / "issue-response-530.json").read_bytes()),
    }
    audit_result = load(OUT / "batch-079-draft-audit.json")
    progress["execution530StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    progress["execution530IssueReceipt"] = receipt
    progress["execution530CoordinatorCheckpoint"] = {
        "schemaVersion": 1, "execution": EXECUTION, "checkpoint": 530, "batch": "079",
        "savedCommit": head, "signature": "G", "sourceCommit": SOURCE,
        "status": "continue", "stage": "local-unreviewed-draft",
        "dedicatedWorktreesClean": True, "membership": ["冠"], "sourceRow": 88,
        "runtimeDrafted": ["冠"], "reviewClosed": [], "published": [],
        "runtimeChanged": True, "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "checks": {"focusedTests": 22, "validatorErrors": 0, "manifestFresh": True,
                   "runtimePayloadHashes": 8363, "contentVersion": audit_result["contentVersion"]},
        "allMappedPairs": 3, "directedLinks": 6, "strokeCount": 9,
        "actualHan": 35, "pendingNativeFallbackLabels": ["冖", "宀"],
        "evidence": "docs/n1-sources/execution-530.json",
        "sourcePacket": "docs/n1-sources/batch-079-progress.json",
        "draftAudit": "docs/n1-sources/batch-079-draft-audit.json",
        "issueUpdate": response["html_url"], "ownerAuthorAndBodyVerified": True,
        "publishedAdditions": 105, "remainingAdditions": 1123, "lastPublishedCommit": BASE,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": next_action, "verifiedAt": datetime.now().astimezone().isoformat(),
    }
    progress["batch079Draft"] = {
        "checkpoint": head, "sourceCheckpoint": SOURCE, "status": "local-unreviewed-draft",
        "sourcePacket": "docs/n1-sources/batch-079-progress.json",
        "draftAudit": "docs/n1-sources/batch-079-draft-audit.json",
        "issueUpdate": response["html_url"], "runtimePublished": False,
    }
    progress.update(checkpoint=530, status="continue", stage="batch-079-local-unreviewed-draft",
                    blocker=None, nextAction=next_action)
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    changed = [k for k in original if progress[k] != original[k]]
    assert set(changed) <= allowed, changed
    assert original.keys() <= progress.keys()
    progress["execution530CoordinatorCheckpoint"].update(
        allOriginalHistoricalRootKeysPreservedExactly=True,
        originalRootKeyCountCompared=len(original), changedRootFields=changed)
    save(CONTROL / "progress.json", progress)
    assert load(CONTROL / "progress.json") == progress
    save(LOGS / "checkpoint-final-530.json", progress["execution530CoordinatorCheckpoint"])
    print(json.dumps(progress["execution530CoordinatorCheckpoint"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    {"start": start, "strokes": strokes, "ledger": ledger, "audit": audit,
     "record": record, "issue-body": issue_body, "checkpoint": checkpoint}[sys.argv[1]]()
