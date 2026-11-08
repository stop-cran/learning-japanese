"""Source-only completion for the already frozen batch 106; no runtime authoring."""
import argparse
import copy
import gzip
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
S = R / "docs" / "n1-sources"
L = C / "logs" / "1f17514d-4832-4b04-bbfe-7aac0c6241c0"
HEAD = "95227f2ab8846a80061d6de27b1701fe19053161"
NEXT = (
    "SAME106 ONE bounded runtime draft and normal signed LOCAL UNREVIEWED freeze only; "
    "no reviewer/Android/native/publication/107 in that draft checkpoint. Source-complete row117 "
    "勅 is in docs/n1-sources/batch-106-source-completion-plan.json and execution-820.json: "
    "44member+35comparison=79distinct completeJMdictfamilies,10fullrawcharacters,28actual full "
    "articles including11legacytwochoicefallbacks. Preserve exact fullon[チョク]/fullkun"
    "[いまし.める,みことのり] sourceorder; select[チョク]/[] with own linked勅令ちょくれい "
    "example/keyちょく. いまし.める remains explicit characterdictionaryonly/no suitablelexical "
    "example/modernwrittenuseUNVERIFIED; no invented勅める/unsupportedrarearchaicinvalidlabel/"
    "allocationfrom戒めるor縛める. みことのり is documented1604470+actualDaijisen, NOTsearchonly. "
    "Actual▽notationguide now inspected: outsideJoyoREADINGlist, NOTfrequency/obsolescence. "
    "Retain recognitionrow/unselected boundedteachingchoice, no duplicate勅article. "
    "ONEnecessaryNEW勅令/noinferredwordlevel/imperialedict; sovereigns in generalsense versus "
    "MeijiConstitutionlegalform, noJapanese-only/Meiji-only/everyoldedictvoid overclaim. "
    "TWOoriginalnaturalexamples+translations in sourceplan, not attestedquotations. "
    "Proposedkanjititleimperialorder/THREEwrongexisting束効勤/TWOdirectkanjiguards令命; "
    "SIXdirectwordguards命令命じる命ずる法法律規則, conservativeexactlabel/sense safeguards "
    "NOTunrestrictedJapaneseequivalence/transitivecliques. Afterdraft actualfinitequalified "
    "HOST+native word/kanji options in defaultN1/All/custom/reducedpools stillMANDATORY. "
    "AllmappedTWOpairsFOURdirections include令; ZEROactivatedbaselinepairs. ONEexactreused "
    "令CommonwordsadditionisNEWsourcedexampleteaching, NOTnavigationonly; includeinbothblindreviews. "
    "Nootherbaselinebody/metadata/ID/level/reading/exclusionrewrite. Canonical力19right/束left "
    "modernshapemnemonicNOTetymology/structure-unclassified/no phoneticclaim. Convert retained "
    "pinnedNINEpathSVG only through unchangedpinnedconverter16points/path. Proposed20Han "
    "presentallTHREEbundledcmaps, NOTrenderedacceptance; recomputefinalactualHan/freshnative "
    "ALLfourfont/defaultsystem/wholeword/radical/lookalike/readability gates remain. "
    "LaterTWOserialblinddifferentfamilies/serialinternaltools/originalsessionconfirmations/"
    "non-skippedqualifiedAndroidbf30HOST/nativeContentSyncONCE/meaning/curatedreading/drawing/"
    "articles/Back/offline/fonts/rendered/combinedcurrentmain/fullPython/vocabulary/"
    "baseline-membership-links/manifest/perfilemedia-safepaths/normalsigning/ownerfastforward/"
    "terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entries42MiBcompressed"
    "80MiBinflated56MiBretained/verifiedownerissue remainMANDATORY. Verifywhollyclean signedheads/"
    "freshmain/liveparentancestry/decodedlauncher/exactsession. Parent13320ownsrunner.lock:"
    "NOchildacquire/delete/unlock/readprobe; approvedcontrol/committedsource/frozeninputs only,"
    "nooptionalhistoricalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. Published132/1228,1096remainder/1128kanji5079words137N1labels"
    "142namedmembers+separate妖/130necessarysupportsNOTN1vocabulary unchanged. "
    "Sixseparatelyplaced保案派第策結retainN2/noacceptedcredit/noduplicate/relevel. "
    "CompatibleAndroid125+132required;oldclientsignore;qualifiedsignedbf30cdead8515739bc0e671d57a54b9a3109dd46"
    "guard+schemaonlyNOTlatestmain. Original819+818andALLhistoricalsource/review/process/readdepth/"
    "permission/OOM/ANR/routing/rendering/phone/pendinglimits retained in exact "
    "execution820Inherited819Gates and before820snapshot; NOTnew820runs/retroaccepted. "
    "Originalpixels/equalcomprehension/fallbackface/everyrequestretention/native-speaker/phone/"
    "effectivenessremainUNVERIFIED; noforcedfindingwithdrawal/modelvote/newguardfromunprovedhypothesis. "
    "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. "
    "No107/unreviewedpush/authoragents/concurrentheavywork/secondrunner/signingretry/guardincrease."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256 as text_sha256
from extract_n1_jmdict import extract

sys.stdout.reconfigure(encoding="utf-8")


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".820.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(R), *args],
                                   encoding="utf-8").strip()


def start():
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("status", "--porcelain", "--untracked-files=all")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (819, "106", "continue")
    preflight = load(L / "preflight-820.json")
    assert preflight["lockTouched"] is False
    request = (L / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    embedded = json.loads(text.split(marker, 1)[1])
    assert embedded["checkpoint"] == 819
    before = L / "progress-before-820.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 820, "batch": "106", "startingHead": HEAD,
        "scope": "SAME106 bounded source-completion checkpoint only; no runtime draft, reviewer, Android/native, publication,107 or second runner.",
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "request": {
            "sha256": hashlib.sha256(request).hexdigest(),
            "bytes": len(request), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed before implementation. Operative contract, complete approved issue and final819 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."
        },
        "runnerPreflight": preflight,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution820StartingState"] = state
    p.update(stage="batch-106-source-completion-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Source-completion scope persisted with full history retained.")


def frozen():
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, record in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == record["bytes"]
        assert hashlib.sha256(raw).hexdigest() == record["sha256"]
        inputs[name] = raw
    jm = gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert hashlib.sha256(jm).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(kd).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, inputs, ET.fromstring(jm), ET.fromstring(kd)


def supplement():
    snapshot, inputs, jm, kd = frozen()
    terms = ["効く", "効き目", "効果", "効力", "有効", "勤める", "勤務", "通勤",
             "束ねる", "約束", "法", "法律", "規則", "訓", "教え", "指導", "教授"]
    prior = set(load(S / "batch-106-lexical-selection.json")["entryIds"])
    prior.update(load(S / "batch-106-comparison-selection.json")["entryIds"])
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if e.findtext("ent_seq") not in prior
           and any(k.text in terms for k in e.findall("k_ele/keb"))]
    selection = {
        "schemaVersion": 1, "batch": "106", "execution": 820, "entryIds": ids,
        "exactKebTerms": terms,
        "selectionRule": "Every complete frozen family matching an exact listed keb, excluding both intact earlier packets. All aliases, readings, restrictions, sense-local flags and senses retained.",
        "limits": "Extraction is not inspection or unrestricted substitution. These are comparison/distractor/ordinary-secondary-sense sources, not extra support-article commitments."
    }
    save(S / "batch-106-completion-selection.json", selection)
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / "batch-106-completion-comparisons.xml").write_bytes(raw)
    root = ET.Element("kanjidic2")
    root.append(copy.deepcopy(kd.find("header")))
    for char in "効勤力訓教法":
        root.append(copy.deepcopy(next(e for e in kd.findall("character")
                                      if e.findtext("literal") == char)))
    ET.indent(root, space="  ")
    (S / "batch-106-completion-kanjidic2.xml").write_bytes(
        ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n")
    page = (C / "batch-106-notation-820.html").read_bytes()
    decoded = page.decode("utf-8")
    block = re.search(r'<h4 class="ttl">2\. 常用漢字</h4>(.*?)</section>',
                      decoded, re.S).group(1)
    text = "2. 常用漢字\n" + html.unescape(re.sub("<[^>]+>", "", block)).strip() + "\n"
    assert "常用漢字音訓表にない読みの場合には「▽」" in text
    (S / "batch-106-notation-public-text.txt").write_text(text, encoding="utf-8")
    archive = S / "batch-106-notation.html.gz"
    archive.write_bytes(gzip.compress(page, mtime=0))
    save(S / "batch-106-completion-public-receipts.json", [{
        "url": "https://kotobank.jp/hanrei/daijisen/01/",
        "downloadedAt": datetime.fromtimestamp((C / "batch-106-notation-820.html").stat().st_mtime,
                                              timezone.utc).isoformat(),
        "rawSha256": hashlib.sha256(page).hexdigest(), "rawBytes": len(page),
        "archive": archive.name, "archiveSha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
        "extractedText": "batch-106-notation-public-text.txt",
        "extractedTextSha256": hashlib.sha256((S / "batch-106-notation-public-text.txt").read_bytes()).hexdigest(),
        "inspectedScope": "Section2 常用漢字, all five points, including exact outside-Joyo-reading notation. Other page sections not adopted.",
        "limits": "Coordinator retrieval, not independent reviewer lookup. Not a frequency/obsolescence marker."
    }])
    print(json.dumps({"additionalCompleteFamilies": len(ids), "entryIds": ids,
                      "packetLines": len(raw.decode().splitlines())}, ensure_ascii=False))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def preparation():
    from fontTools.ttLib import TTFont

    plan = load(S / "batch-106-source-completion-plan.json")
    inventory = plan["fontPlan"]["proposedTextInventory"]
    han = sorted({c for c in inventory if "\u3400" <= c <= "\u9fff"})
    fonts = []
    folder = C.parent / "kanji-cards-android" / "app" / "src" / "main" / "res" / "font"
    for path in sorted(folder.glob("kanji_*.ttf")):
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            presence = {c: ord(c) in cmap for c in han}
        fonts.append({"path": str(path), "sha256": sha(path.read_bytes()),
                      "keyGlyphPresence": presence,
                      "allProposedMissing": [c for c in han if not presence[c]]})
    assert len(fonts) == 3
    save(S / "batch-106-font-preparation.json", {
        "schemaVersion": 1, "batch": "106", "execution": 820,
        "proposedTextInventory": inventory, "auditedHan": han, "auditedHanCount": len(han),
        "fonts": fonts,
        "defaultSystemFont": "Later native four-mode rendering required; not a fourth bundled file.",
        "limits": "Proposed text only. Cmap presence/absence is not rendered readability, fallback-face identity or native/phone acceptance. Recompute final actual runtime Han after drafting."
    })
    records = {}
    names = (plan["authorInspection"]["existingArticlesReadCompletely"]
             + plan["authorInspection"]["legacyFallbackArticlesReadCompletely"])
    for name in names:
        raw = (R / name).read_bytes()
        records[name] = {"sha256": sha(raw), "bytes": len(raw),
                         "metadata": metadata(R, name),
                         "fullArticle": raw.decode("utf-8")}
    save(S / "batch-106-completion-article-snapshots.json", records)
    baseline = load(S / "batch-106-baseline-plan.json")
    cards = {v["metadata"]["kanji"]: v["metadata"]
             for n, v in baseline["inventory"].items() if n.startswith("kanji/")}
    legacy = {k: {"metadata": v, "actualTitle": v["title"]}
              for k, v in cards.items() if len(v.get("distractors", [])) < 3}
    save(S / "batch-106-fallback-preparation.json", {
        "schemaVersion": 1, "batch": "106", "execution": 820,
        "legacyFewerThanThreeCurated": legacy,
        "incomingCuratedTargetReferences": [k for k, v in cards.items()
                                            if "勅" in v.get("distractors", [])],
        "proposedDirectKanjiPairs": [["勅", other] for other in plan["kanjiPlan"]["quizExclusions"]],
        "proposedDirectWordPairs": [["勅令", other] for other in
                                    plan["supportPlan"]["newNecessary"][0]["quizExclusions"]],
        "productionQuizBuilderSha256": sha((C.parent / "kanji-cards-android" / "core" / "src" /
            "main" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "quiz" /
            "QuizBuilder.kt").read_bytes()),
        "productionWordQuizBuilderSha256": sha((C.parent / "kanji-cards-android" / "core" / "src" /
            "main" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "words" /
            "Words.kt").read_bytes()),
        "laterAcceptance": plan["legacyFallbackPlan"]["laterAcceptance"],
        "limits": "Source and exact-label preparation only, NOT production execution, finite runtime option acceptance, or a claim that every future random pool is safe."
    })
    print(json.dumps({"articleSnapshots": len(records), "legacyFallbacks": len(legacy),
                      "proposedHan": len(han),
                      "bundledMissing": {Path(f["path"]).name: f["allProposedMissing"] for f in fonts}},
                     ensure_ascii=False))


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(c) for c in element))


def audit():
    snapshot, inputs, jm, kd = frozen()
    plan = load(S / "batch-106-source-completion-plan.json")
    assert git("rev-parse", "HEAD") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == plan["publishedBaseline"]
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert plan["membership"] == ["勅"] and plan["sourceRows"] == [117]
    ids_by_packet = {}
    for label, selection in [
        ("jmdict", "lexical-selection"), ("comparisons", "comparison-selection"),
        ("completion-comparisons", "completion-selection")
    ]:
        ids = load(S / f"batch-106-{selection}.json")["entryIds"]
        actual = (S / f"batch-106-{label}.xml").read_bytes()
        assert actual == extract(inputs["n1-implementation-JMdict_e.gz"],
                                 snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        ids_by_packet[label] = ids
    all_ids = [i for ids in ids_by_packet.values() for i in ids]
    assert len(all_ids) == len(set(all_ids)) == 79
    expected_member_ids = [e.findtext("ent_seq") for e in jm.findall("entry")
                          if any("勅" in k.text for k in e.findall("k_ele/keb"))]
    assert ids_by_packet["jmdict"] == expected_member_ids
    selection = load(S / "batch-106-completion-selection.json")
    terms = set(selection["exactKebTerms"])
    prior = set(ids_by_packet["jmdict"] + ids_by_packet["comparisons"])
    assert selection["entryIds"] == [e.findtext("ent_seq") for e in jm.findall("entry")
                                    if e.findtext("ent_seq") not in prior
                                    and any(k.text in terms for k in e.findall("k_ele/keb"))]
    for label, chars in [("kanjidic2", "勅"), ("comparison-kanjidic2", "令命束"),
                         ("completion-kanjidic2", "効勤力訓教法")]:
        actual = ET.parse(S / f"batch-106-{label}.xml").getroot()
        assert canonical(actual.find("header")) == canonical(kd.find("header"))
        assert [e.findtext("literal") for e in actual.findall("character")] == list(chars)
        for char in chars:
            original = next(e for e in kd.findall("character") if e.findtext("literal") == char)
            retained = next(e for e in actual.findall("character") if e.findtext("literal") == char)
            assert canonical(original) == canonical(retained)
    row = load(S / "batch-106-input-metadata.json")["sourceIndexRecord"]
    assert row == next(r for r in load(S / "source-index.json") if r["kanji"] == "勅")
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[116] == "勅"
    assert row["metadata"]["onyomi"] == plan["kanjiPlan"]["onyomi"] == ["チョク"]
    assert row["metadata"]["kunyomi"] == plan["kanjiPlan"]["kunyomi"] == ["いまし.める", "みことのり"]
    assert plan["kanjiPlan"]["quizOnyomi"] == ["チョク"] and plan["kanjiPlan"]["quizKunyomi"] == []
    assert not (R / "kanji" / "勅.md").exists()
    assert not (R / "strokes" / "勅.json").exists()
    assert not (R / "words" / "勅令.md").exists()
    baseline = load(S / "batch-106-baseline-plan.json")
    for name, rec in baseline["inventory"].items():
        assert sha((R / name).read_bytes()) == rec["sha256"]
        assert metadata(R, name) == rec["metadata"]
    assert sha((R / "manifest.json").read_bytes()) == baseline["manifestRawSha256"]
    manifest = load(R / "manifest.json")
    assert manifest == baseline["runtimeManifest"] == build_manifest(R)
    runtime = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, digest in entries.items():
            path = R / name
            actual = (sha(path.read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else text_sha256(path))
            assert actual == digest, name
            runtime += 1
    assert runtime == 8469
    names = plan["authorInspection"]["existingArticlesReadCompletely"]
    legacy_names = plan["authorInspection"]["legacyFallbackArticlesReadCompletely"]
    snapshots = load(S / "batch-106-completion-article-snapshots.json")
    assert set(snapshots) == set(names + legacy_names) and len(snapshots) == 28
    for name, rec in snapshots.items():
        assert sha((R / name).read_bytes()) == rec["sha256"]
        assert (R / name).read_bytes().decode("utf-8") == rec["fullArticle"]
        assert metadata(R, name) == rec["metadata"]
    cards = {v["metadata"]["kanji"]: v["metadata"]
             for n, v in baseline["inventory"].items() if n.startswith("kanji/")}
    assert all(v["title"] != plan["kanjiPlan"]["title"] for v in cards.values())
    distractors = plan["kanjiPlan"]["curatedDistractors"]
    assert [r["kanji"] for r in distractors] == ["束", "効", "勤"]
    assert len({r["actualTitle"] for r in distractors}) == 3
    guards = plan["kanjiPlan"]["quizExclusions"]
    for rec in distractors:
        char = rec["kanji"]
        assert cards[char]["title"] == rec["actualTitle"] and char not in guards
        assert not set(cards[char].get("quiz_exclusions", [])) & {"勅", "束", "効", "勤"}
    assert guards == ["令", "命"]
    fallback = load(S / "batch-106-fallback-preparation.json")
    legacy = {k for k, v in cards.items() if len(v.get("distractors", [])) < 3}
    assert legacy == set(fallback["legacyFewerThanThreeCurated"]) == set("人休何入出口女日月男買")
    assert fallback["incomingCuratedTargetReferences"] == []
    words = {v["metadata"]["word"]: v["metadata"]
             for n, v in baseline["inventory"].items() if n.startswith("words/")}
    candidates = [m["word"] for m in words.values()
                  if "勅" in m["word"] or "勅" in m.get("kanji", [])
                  or m["reading"] in {"ちょくれい", "ちょく", "みことのり", "いましめる"}]
    assert candidates == [], candidates
    support = plan["supportPlan"]["newNecessary"][0]
    assert support["quizExclusions"] == ["命令", "命じる", "命ずる", "法", "法律", "規則"]
    assert all(w in words for w in support["quizExclusions"])
    assert all(v["title"] != support["title"] for v in words.values())
    navigation = load(S / "batch-106-source-navigation.json")
    assert navigation["candidates"] == [] and navigation["baselinePairs"] == []
    assert plan["linkPlan"]["allMappedPairs"] == [["勅", "words/勅令.md"], ["令", "words/勅令.md"]]
    assert len(plan["linkPlan"]["requiredDirections"]) == 4
    reused = plan["linkPlan"]["exactReusedChange"]
    assert reused["afterExistingLine"] in (R / reused["article"]).read_text(encoding="utf-8")
    assert reused["addLine"] not in (R / reused["article"]).read_text(encoding="utf-8")
    for filename in ["batch-106-public-source-receipts.json",
                     "batch-106-completion-public-receipts.json"]:
        for rec in load(S / filename):
            raw = (S / rec["archive"]).read_bytes()
            assert sha(raw) == rec["archiveSha256"]
            assert sha(gzip.decompress(raw)) == rec["rawSha256"]
            assert sha((S / rec["extractedText"]).read_bytes()) == rec["extractedTextSha256"]
    svg = (S / "batch-106-kanjivg.svg").read_bytes()
    stroke = load(S / "batch-106-stroke-evidence.json")
    assert sha(svg) == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")) == 9
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == stroke["converterNormalizedSha256"]
    fonts = load(S / "batch-106-font-preparation.json")
    assert fonts["proposedTextInventory"] == plan["fontPlan"]["proposedTextInventory"]
    assert fonts["auditedHanCount"] == len(fonts["auditedHan"])
    for font in fonts["fonts"]:
        assert sha(Path(font["path"]).read_bytes()) == font["sha256"]
    android = C.parent / "kanji-cards-android"
    assert subprocess.check_output(["git", "-C", str(android), "rev-parse", "HEAD"],
                                   encoding="utf-8").strip() == "bf30cdead8515739bc0e671d57a54b9a3109dd46"
    assert not subprocess.check_output(["git", "-C", str(android), "status", "--porcelain",
                                       "--untracked-files=all"], encoding="utf-8").strip()
    before, now = load(L / "progress-before-820.json"), load(C / "progress.json")
    mutable = {"stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    result = {
        "schemaVersion": 1, "execution": 820, "batch": "106", "sourceCommit": HEAD,
        "membership": ["勅"], "sourceRows": [117], "sourcePreparationComplete": True,
        "completeDictionaryFamilies": 79, "memberFamilies": 44, "comparisonFamilies": 35,
        "completeRawCharacterRecords": 10, "completeExistingArticleSnapshots": 28,
        "legacyFallbackArticles": 11, "threeExistingWrongDistractors": ["束", "効", "勤"],
        "proposedDirectKanjiPairs": 2, "proposedDirectWordPairs": 6,
        "allMappedPairs": 2, "requiredLinkDirections": 4, "activatedBaselinePairs": 0,
        "newNecessarySupport": ["words/勅令.md"],
        "changedReusedPassagePlan": "ONE new sourced common-word line in令; not navigation-only",
        "offeredKeys": plan["kanjiPlan"]["offeredKeys"],
        "sourceReadingOrderPreserved": True,
        "baselineKanjiMetadataAndBytesPreserved": len(cards),
        "baselineWordMetadataAndBytesPreserved": len(words),
        "runtimeManifestHashesVerified": runtime, "runtimeBytesUnchanged": True,
        "manifestBytesUnchanged": True, "contentVersion": manifest["contentVersion"],
        "pinnedSvgPaths": 9, "geometryConverted": False, "proposedHan": fonts["auditedHanCount"],
        "bundledCmapMissing": {Path(f["path"]).name: f["allProposedMissing"] for f in fonts["fonts"]},
        "originalHistoricalRootValuesPreserved": True, "originalRootKeysCompared": len(before),
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False,
        "limits": "Mechanical source completeness/baseline and byte audit, not independent linguistic, production finite quiz/native/font/phone acceptance. Every later acceptance/publication gate remains."
    }
    save(S / "batch-106-source-completion-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    audit_result = load(S / "batch-106-source-completion-audit.json")
    assert audit_result["sourcePreparationComplete"]
    assert git("rev-parse", "HEAD") == HEAD
    tests = (L / "source-tests-820.txt").read_text(encoding="utf-8-sig")
    assert "Ran 43 tests" in tests and "\nOK" in tests
    assert "0 error(s)" in (L / "validate-820.txt").read_text(encoding="utf-8-sig")
    diagnostic = (L / "manifest-diff-820.txt").read_text(encoding="utf-8-sig").strip()
    assert diagnostic in {
        "", "warning: in the working copy of 'manifest.json', LF will be replaced by CRLF the next time Git touches it"
    }
    assert sha((R / "manifest.json").read_bytes()) == load(S / "batch-106-baseline-plan.json")["manifestRawSha256"]
    assert (L / "whitespace-820.txt").stat().st_size == 0
    artifacts = {}
    for label in ["source-tests", "validate", "manifest", "manifest-diff", "budget",
                  "vocabulary", "whitespace", "audit", "audit-820-attempt2"]:
        name = f"{label}-820.txt" if label != "audit-820-attempt2" else label + ".txt"
        source = L / name
        raw = source.read_bytes()
        target = S / ("batch-106-" + name + ".gz")
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        artifacts[name] = {"archive": target.name, "rawSha256": sha(raw),
                           "archiveSha256": sha(target.read_bytes())}
    for filename in ["complete-batch-106-820.py", "preflight-820.ps1",
                     "checks-batch-106-source-820.ps1", "post-batch-106-source-820.ps1"]:
        shutil.copyfile(C / filename, S / ("batch-106-" + filename))
    shutil.copyfile(L / "preflight-820.json", S / "batch-106-runner-role-820.json")
    progress = load(S / "batch-106-progress.json")
    progress.update(
        status="source-complete-not-drafted", sourcePreparationComplete=True,
        sourceCompletionPlan="batch-106-source-completion-plan.json",
        sourceCompletionAudit="batch-106-source-completion-audit.json",
        completeDictionaryFamilies=79, completeRawCharacterRecords=10,
        existingArticlesReadCompletely=28, requiredAllMappedPairs=2,
        requiredLinkDirections=4, activatedBaselinePairs=0,
        proposedQuizOnyomi=["チョク"], proposedQuizKunyomi=[],
        limits="Source completion only, not a local teaching draft, independent review or publication. Every subsequent gate remains mandatory.",
        nextAction=NEXT)
    save(S / "batch-106-progress.json", progress)
    evidence = {
        **audit_result,
        "status": "source-complete-for-normal-signed-local-checkpoint",
        "stage": "batch-106-source-complete-not-drafted",
        "sourcePlan": "batch-106-source-completion-plan.json",
        "focusedTestsPassed": 43, "validatorErrors": 0,
        "manifestFreshAndUnchanged": True,
        "budget": (L / "budget-820.txt").read_text(encoding="utf-8-sig").strip(),
        "vocabulary": (L / "vocabulary-820.txt").read_text(encoding="utf-8-sig").strip(),
        "checkArtifacts": artifacts, "runnerPreflight": load(L / "preflight-820.json"),
        "publishedAdditions": 132, "remainingAdditions": 1096,
        "lastPublishedCommit": "0c582f18b31f65a5e1a908d92e37dde3d34f81ee",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT,
    }
    save(S / "execution-820.json", evidence)
    body = (
        "Batch 106 (勅, frozen row 117): **source preparation complete; no runtime draft or publication**.\n\n"
        "LOCAL_COMMIT_PLACEHOLDER preserves 79 complete dictionary families (44 member + 35 comparison), "
        "10 full raw character records and 28 full existing-article snapshots, including all 11 legacy "
        "two-choice cards. The plan selects チョク via necessary support 勅令; full source readings/order "
        "remain intact. いまし.める is explicitly source-only with modern written use unverified. "
        "みことのり is documented, not search-only; the actual ▽ guide marks a reading outside the Joyo "
        "table, not rarity or obsolescence.\n\n"
        "The source plan fixes three existing wrong distractors, two direct kanji and six conservative "
        "word guards, two all-mapped pairs/four directions, and one new sourced 勅令 example under 令 "
        "(not navigation-only). All 20 proposed Han are present in the three bundled cmaps; this is "
        "**not** rendered/native/phone acceptance. Two helper-only Windows newline/hash audit failures "
        "were preserved and corrected without changing runtime/source bytes or weakening checks.\n\n"
        "43 focused tests passed; validator: 0 errors; manifest unchanged; every 8,469 runtime hash "
        "and all 1,128 kanji/5,079 word baseline metadata/bytes verified. Budget/vocabulary checks pass "
        "(vocabulary remains pilot 2,122/2,431). No reviewer, Android/native run, new denial or lock "
        "operation occurred. Published additions remain **132/1,228; 1,096 outstanding**. "
        "Next: SAME106 bounded signed LOCAL UNREVIEWED draft only, then all original independent-review, "
        "qualified-client HOST/native/rendered/current-main/publication gates. Compatible "
        "stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 clients "
        "required; physical-phone/general-release and whole-set acceptance remain outstanding."
    )
    (C / "batch-106-source-820-issue-template.txt").write_text(body + "\n", encoding="utf-8")
    print("Source evidence and exact check archives persisted; normal local signing is next.")


def checkpoint():
    commit = git("rev-parse", "HEAD")
    assert commit != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    receipt = load(C / "batch-106-source-820-issue-receipt.json")
    assert receipt["verified"] and receipt["author"] == "stop-cran" and receipt["localCommit"] == commit
    before = load(L / "progress-before-820.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 819 and p["batch"] == "106"
    audit_result = load(S / "batch-106-source-completion-audit.json")
    checkpoint = {
        **audit_result, "execution": 820, "checkpoint": 820, "batch": "106",
        "savedCommit": commit, "signature": "G", "status": "continue",
        "stage": "batch-106-source-complete-not-drafted",
        "sourceEvidence": "docs/n1-sources/execution-820.json",
        "sourcePlan": "docs/n1-sources/batch-106-source-completion-plan.json",
        "focusedTestsPassed": 43, "validatorErrors": 0,
        "dedicatedWorktreesClean": True,
        "publishedAdditions": 132, "remainingAdditions": 1096,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["url"], "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": NEXT,
    }
    p["execution820CoordinatorCheckpoint"] = checkpoint
    p["execution820Inherited819Gates"] = {
        "checkpoint": 819, "nextAction": before["nextAction"],
        "invariant": "Preserve exact inherited gates and limitations; source-only820 does not rerun or retroaccept them."
    }
    p["batch106SourceCompletionIssueReceipt"] = receipt
    p["execution820StartingState"]["status"] = "signed-local-source-completion-checkpoint-complete"
    p.update(checkpoint=820, status="continue", stage=checkpoint["stage"], nextAction=NEXT, blocker=None)
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    assert p["lastPublishedCommit"] == before["lastPublishedCommit"]
    assert p["remainingAdditions"] == 1096
    save(C / "progress.json", p)
    after = load(C / "progress.json")
    assert all(after[k] == v for k, v in before.items() if k not in mutable)
    save(L / "checkpoint-820-verification.json", {
        "checkpoint": 820, "savedCommit": commit, "signature": "G",
        "originalHistoricalRootValuesPreserved": True,
        "originalRootKeysCompared": len(before), "worktreeClean": True,
        "ownerIssueAuthorAndBodyVerified": True, "parentLockTouched": False,
        "wholeProjectComplete": False, "nextAction": NEXT
    })
    print(json.dumps({"checkpoint": 820, "savedCommit": commit, "status": "continue",
                      "issue": receipt["url"], "historyPreserved": True}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "supplement", "preparation", "audit", "record", "checkpoint"])
    args = parser.parse_args()
    {"start": start, "supplement": supplement, "preparation": preparation, "audit": audit,
     "record": record, "checkpoint": checkpoint}[args.action]()
