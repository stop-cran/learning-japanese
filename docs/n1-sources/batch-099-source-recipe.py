"""Prepare source evidence only for N1 batch 099 from authorized frozen inputs."""
import argparse
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
L = C / "logs" / "ed6bc253-af32-4a11-a507-efe1ca5273b6"
BASE = "d5a376ee2b014aae3c47c58eea47b327e44be6d2"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u5270"
PREFIX = "batch-099-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".728.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root)


def frozen():
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, record in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == record["bytes"] and sha(raw) == record["sha256"], name
        inputs[name] = raw
    jm = gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(jm) == snapshot["jmdict"]["xmlSha256"]
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, inputs, ET.fromstring(jm), ET.fromstring(kd)


def start():
    clean(R, BASE)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == BASE
    assert git("branch", "--show-current") == "content/n1-kanji"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (727, "098", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1103
    assert not list(S.glob(PREFIX + "*"))
    role = load(L / "preflight-728.json")
    assert role["liveParentPid"] == 15692 and role["sessionId"] == L.name
    assert role["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 727
    assert checkpoint["execution727CoordinatorCheckpoint"] == p["execution727CoordinatorCheckpoint"]
    before = L / "progress-before-728.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 728, "batch": "099", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded099 source-preparation checkpoint for frozen row110 only; no runtime draft, reviewer, Android/native, publication,100 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed. Operative contract, complete approved issue and final727 directly inspected; historical middle parsed, not freshly semantically re-reviewed. Initial scalar output encoding failure occurred after full request loading/decoding."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals content. Android1c1b7bf4 retains productionf9b59a2, NOT latest app main. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution728StartingState"] = state
    p.update(batch="099", stage="batch-099-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Source-preparation starting scope persisted; complete historical values preserved.")


def character_packet(kd, chars, name):
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in chars:
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    (S / (PREFIX + name)).write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")


def compact_packet(name, output):
    lines = []
    for entry in ET.parse(S / (PREFIX + name)).getroot():
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        lines.append(ET.tostring(entry, encoding="unicode"))
    (C / output).write_text("\n".join(lines) + "\n", encoding="utf-8")


def packet():
    snapshot, inputs, jm, kd = frozen()
    assert load(C / "progress.json")["batch"] == "099"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 110
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[109] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "099", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+5270 in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    (S / (PREFIX + "jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    character_packet(kd, CHAR, "kanjidic2.xml")
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "099", "baseCommit": BASE, "sourceIndexRecord": row,
        "characters": [CHAR], "rawCharacterPacket": PREFIX + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha((S / (PREFIX + "kanjidic2.xml")).read_bytes()),
        "provenance": "Complete frozen character record/header parsed and reserialized.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repositoryNOTICE.",
    })
    candidates = []
    for path in sorted((R / "words").glob("*.md")):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if CHAR in m.get("kanji", []) or CHAR in m["word"]:
            candidates.append({"article": name, "metadata": m})
    save(S / (PREFIX + "source-navigation.json"), {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == CHAR],
    })
    compact_packet("jmdict.xml", "batch-099-full-family-reading.txt")
    print(json.dumps({"families": len(ids), "candidates": candidates}, ensure_ascii=True, indent=2))


def comparison():
    snapshot, inputs, jm, kd = frozen()
    words = ["余る", "剰る", "余り", "剰り", "剰え", "剰", "あまつさえ",
             "乗る", "剣", "規則", "余分", "超過", "余裕", "不足"]
    chars = "剩余乗利則過刀剣"
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(n.text in words for n in e.findall("k_ele/keb") + e.findall("r_ele/reb"))
           or any("剩" in n.text for n in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "099", "exactSpellingsOrReadings": words,
        "additionalRule": "Every full family with old-form U+5269 in any keb.",
        "entryIds": ids, "rawCharacterOrder": list(chars),
        "rule": "Complete frozen families; preserve every alias/restriction/sense.",
        "limits": "Bounded comparisons, not exhaustive quiz-pool acceptance.",
    })
    (S / (PREFIX + "comparison-jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    character_packet(kd, chars, "comparison-kanjidic2.xml")
    compact_packet("comparison-jmdict.xml", "batch-099-comparison-reading.txt")
    compact_packet("comparison-kanjidic2.xml", "batch-099-comparison-characters-reading.txt")
    print(json.dumps({"comparisonFamilies": len(ids), "comparisonCharacters": len(chars)}))


def public():
    from html.parser import HTMLParser

    class ArticleText(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth = 0
            self.parts = []

        def handle_starttag(self, tag, attrs):
            if tag == "article":
                self.depth += 1
                self.parts.append("\n[DICTIONARY BLOCK]\n")
            if self.depth and tag in {"p", "h2", "h3", "br", "section", "li"}:
                self.parts.append("\n")

        def handle_endtag(self, tag):
            if tag == "article" and self.depth:
                self.depth -= 1
                self.parts.append("\n[END BLOCK]\n")

        def handle_data(self, data):
            if self.depth:
                self.parts.append(data)

    receipts = {}
    for key, url, expected in [
        ("character", "https://kotobank.jp/word/%E5%89%B0-530513", "じょう【剰〔剩〕】"),
        ("kajo", "https://kotobank.jp/word/%E9%81%8E%E5%89%B0-161855", "か‐じょう"),
    ]:
        path = C / "inputs" / (PREFIX + key + ".html")
        raw = path.read_bytes()
        parser = ArticleText()
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                         if line.strip()) + "\n"
        assert expected in text, (key, text[:300])
        target = S / (PREFIX + key + "-public-text.txt")
        target.write_text(text, encoding="utf-8")
        archive = S / (PREFIX + key + ".html.gz")
        archive.write_bytes(gzip.compress(raw, mtime=0))
        receipts[key] = {
            "url": url, "retrievedAt": datetime.now(timezone.utc).isoformat(),
            "sourcePath": str(path), "sourceSha256": sha(raw),
            "authority": "Kotobank: Digital Daijisen and other separately headed dictionaries.",
            "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
            "losslessGzip": gzip.decompress(archive.read_bytes()) == raw,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "extractionLimits": "Article blocks; formatting/links stripped, image gaiji not decoded. Actual relevant heading and definition inspected, not search snippets. Supplemental entries do not authorize appended metadata, frequency or historical/phonetic claims.",
        }
    save(S / (PREFIX + "public-source-receipts.json"), receipts)
    print("Actual character and word dictionary pages archived losslessly.")


def plan():
    limits = (
        "Source preparation only; no runtime draft, independent content review, app/native acceptance or publication. "
        "Published125/1228 and1103 acceptance remainder unchanged. Six earlier-level source placements remain separate. "
        "Font cmap is preflight, not glyph acceptance. Physical-phone/general-release/whole-set acceptance outstanding. "
        "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latest app main."
    )
    next_action = (
        "SAME099 bounded runtime draft from committed source packet, then normally signed LOCAL UNREVIEWED freeze only. "
        "New剰 frozen row110: preserve fullジョウ andあまつさえ/あま.り/あま.る in source order; explicitly select "
        "quizOnyomi[ジョウ], quizKunyomi[] only. Reuse actual過剰かじょう N2 with all metadata/original seven "
        "exclusions unchanged; no new support word justified. Three kun readings each need qualified recognition/"
        "lookup rows:剰えあまつさえ rare spelling/dated usually-kana adverb,剰りあまり search-only spelling "
        "(noun sense restricted toあまり,notあんまり),あま.る character-dictionary reading with ordinary "
        "word spelled余る; don't invent a modern剰る example. No invalid-reading/blanket-obsolescence claim. "
        "TWO all-mapped pairs/FOUR directions, ONE existing direction/ONE activated baseline pair. TWO exact reused "
        "changes: words過剰 component link and remove only now-stale no-separate-card sentence; kanji過 add "
        "過剰かじょう Common words link. Generate ELEVEN paths with pinned converter; final Han/font/metadata/"
        "curation/quiz/baseline/link audits and validate/regenerate manifest. Proposed title remainder; surplus amount "
        "and wrong options乗/剣/則 require final-title semantic audit;余/過 unsafe as wrong meanings. No newword "
        "title/exclusion changes proposed. Proposed12Han includes刂andoldform剩 absent in allthree maincmaps; "
        "absence is NOT glyph failure. Fresh native actual rendering mandatory if retained. Then TWO serial blind different-family textual reviews on same signed "
        "snapshot, evidence reconciliation/original-session confirmations, fresh non-skipped Android, production "
        "ContentSync ONCE/native N1-All/meaning/curated reading/drawing/article/Back/offline/four-font/all-Han/rendered "
        "confirmation, combined-current-main checks, normal signing/owner fast-forward/terminal green CI/EVERY "
        "immutable public ZIP hash/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/per-file/path/media "
        "guards/verified ownerissue remain mandatory. No unreviewed push/100/authoragent/concurrentheavywork/secondrunner. "
        "Parent15692 owns runner.lock; no child acquire/delete/unlock/readprobe. Approved control/committed evidence/"
        "frozen inputs only; preserve/report/yield actual new denial/signing hang/uncertain ownership. Preserve every "
        "historical source/review/process/denial/OOM/read-depth/native/phone limitation. Project incomplete."
    )
    membership = {
        "schemaVersion": 1, "batch": "099", "baseCommit": BASE, "membership": [CHAR],
        "sourceRows": [110], "members": [{"kanji": CHAR, "sourceRow": 110}],
        "selectionReason": "Next absent frozen row after published剤. ONE character: four readings, rare/search-only spelling and existing easier-deck overlap justify bounded evidence. Earlier deferred rows remain pending.",
        "status": "source-prepared-not-drafted", "drafted": [], "reviewClosed": [], "published": [],
        "limits": limits,
    }
    nav = load(S / (PREFIX + "source-navigation.json"))
    pairs = [[CHAR, "words/過剰.md"], ["過", "words/過剰.md"]]
    directions = []
    for char, word in pairs:
        directions.extend([
            {"from": f"kanji/{char}.md", "to": word, "reason": "Mapped reading/common-word navigation."},
            {"from": word, "to": f"kanji/{char}.md", "reason": "Substantive component introduction."},
        ])
    readings = [
        {"kanji": CHAR, "kind": "on", "reading": "ジョウ", "proposedQuizSelection": True,
         "sourceOnly": False, "example": "過剰 かじょう — excess; too much",
         "entryIds": ["1196170"],
         "qualification": "Exact existing N2 vocabulary identity. Actual Digital Daijisen剰漢字項目 lists過剰 underジョウ; segmentedか‐じょう and frozen過カ corroborate allocation. Excess relative to need, not simply a large quantity; preserve all metadata and seven original exclusions.",
         "evidence": "Frozen KANJIDIC2剰/過, complete JMdict1196170, archived actual Digital Daijisen剰 and過剰."},
        {"kanji": CHAR, "kind": "kun", "reading": "あまつさえ", "proposedQuizSelection": False,
         "sourceOnly": False, "example": "剰え あまつさえ — besides; to make matters worse",
         "entryIds": ["1580500"],
         "qualification": "Recognition only: JMdict marks剰え rare kanji spelling, bare剰 search-only, whole adverb dated and usually kana, usually negative nuance. Search-onlyあまっさえ is separate from preferred raw metadataあまつさえ. Source has no dot; lexical spelling still writes finalえ. Do not select or create support solely for this rare spelling.",
         "evidence": "Complete frozen KANJIDIC2剰; complete JMdict1580500 and actual Digital Daijisen剰訓listing. Do not infer this adverb is invalid from its register."},
        {"kanji": CHAR, "kind": "kun", "reading": "あま.り", "proposedQuizSelection": False,
         "sourceOnly": True, "entryIds": ["1584930"],
         "qualification": "Lookup only.剰り is a search-only kanji form in this frozen family, not a recommended normal spelling or useful quiz prompt. The noun remainder sense is restricted toあまり, notあんまり. Ordinary余り/kanaあまり do not prove every adverbial sense or reading belongs to剰 as a productive spelling. No dedicated word support necessary.",
         "evidence": "Complete frozen KANJIDIC2剰; complete JMdict1584930 ke_inf and sense-local stagr; existingあまり/あんまり articles inspected."},
        {"kanji": CHAR, "kind": "kun", "reading": "あま.る", "proposedQuizSelection": False,
         "sourceOnly": True, "entryIds": [],
         "qualification": "Retain exact character-dictionary reading as lookup only. Actual Digital Daijisen剰 listsあまる, but the inspected modern JMdictあまる family spells余る only; it does not license invented剰る collocations. Explain ordinary余るあまる without linking it as proof of this kanji's spelling. No claim the pronunciation itself is rare or invalid.",
         "evidence": "Frozen KANJIDIC2剰; archived actual Digital Daijisen剰; full comparison JMdict1543910 and actual existing余るarticle."},
    ]
    reused = [
        {"article": "words/過剰.md",
         "before": "[過](../kanji/過.md) contributes going beyond; 剰 contributes a remainder or surplus. The two ideas reinforce being beyond what is required. Their on readings are カ + ジョウ. 剰 remains part of the spelling even though it has no separate card here.",
         "after": "[過](../kanji/過.md) contributes going beyond; [剰](../kanji/剰.md) contributes a remainder or surplus. The two ideas reinforce being beyond what is required. Their on readings are カ + ジョウ.",
         "reason": "Add activated component link and remove only obsolete no-card sentence; preserve all other prose and metadata."},
        {"article": "kanji/過.md", "before": "- 過去 かこ — the past\n\n## Notes",
         "after": "- 過去 かこ — the past\n- [過剰](../words/過剰.md) かじょう — excess; too much\n\n## Notes",
         "reason": "Complete existing-component reciprocal pair; no other change."},
    ]
    progress = {
        **membership, "freshOriginMainAtPreparation": BASE,
        "sourceReadingOrder": {"onyomi": ["ジョウ"], "kunyomi": ["あまつさえ", "あま.り", "あま.る"]},
        "readingDispositions": readings,
        "proposedCuratedProjection": {"kanji": CHAR, "quizOnyomi": ["ジョウ"], "quizKunyomi": [],
                                     "onKeys": ["じょう"], "kunKeys": [],
                                     "limits": "Exact raw-string subset; compatible curated-reading APK required. No runtime offered-key acceptance claimed."},
        "proposedSupportMapping": [
            {"kanji": CHAR, "article": "words/過剰.md", "word": "過剰", "primaryReading": "かじょう",
             "entryId": "1196170", "selectedSenses": [1], "newArticle": False,
             "allWrittenKanji": ["過", "剰"], "wordJlpt": 2,
             "disposition": "Reuse true lexical identity; preserve metadata/title/readings/N2 level/seven original exclusions. Link new component and remove obsolete no-card sentence only."}
        ],
        "proposedNewSupportArticles": [],
        "proposedReciprocalPairs": pairs, "proposedDirectedLinkPlan": directions,
        "requiredDirectionCount": 4,
        "alreadyExistingRequiredDirections": [{"from": "words/過剰.md", "to": "kanji/過.md"}],
        "activatedBaselinePairs": nav["baselinePairs"], "proposedReusedChanges": reused,
        "proposedQuiz": {
            "kanjiTitle": "remainder; surplus amount", "distractors": ["乗", "剣", "則"],
            "labels": ["ride; board", "sword; double-edged blade", "rule; follow a model"],
            "rationale": "乗 shares dense left shape but lacks right刂;剣/則 share blade radical with different left blocks. Riding, sword and rule labels do not name a surplus or mean besides.",
            "unsafeComparisons": ["余", "過"],
            "legacyFallbackDisposition": "余/過/乗/利/剣/則 already have three curated distractors. No fallback repair proposed; wider custom/random/legacy pool semantics unverified.",
            "newWordTitle": None, "proposedDirectExclusions": [],
            "wordQuizDisposition": "No new/reworded word title. Existing過剰 guards preserved exactly; no unnecessary new余剰/剰余/剰えarticle or N1 vocabulary assignment.",
            "confusableInventory": "docs/confusable-words.md inspected for剰/surplus/excess/remainder; no match. Actual sense overlap controls, not transitive cliques or distinct label strings.",
        },
        "outsideFrozenReadingDispositions": [
            {"reading": "ショウ/のり/ます",
             "disposition": "Supplemental dictionaries include other on/name readings; not appended to frozen metadata/questions. Nanori out of scope, differences are not evidence of invalidity."}
        ],
        "proposedTeachingConstraints": [
            "structure-unclassified; labelled modern-shape mnemonic only. Left compressed乗-like block with right刂; no surplus-made-by-cutting etymology or historical/phonetic claim. SVG phon tag not independent historical evidence.",
            "Canonical radical刀18 preserved and visible刂explained; do not substitute the visible variant into canonical metadata.",
            "Meaning surplus/remainder with useful過剰 support.余and剰 meanings overlap; never manufacture fixed semantic compartments or use余 as wrong answer.",
            "余剰よじょう surplus and剰余じょうよ surplus/remainder are recognition words, not necessary support articles. Mathematical remainder sense belongs to剰余; not a new arithmetic lesson.",
            "Each unselected kun needs its own qualified row. Distinguish rare spelling剰え, search-only剰り, and character lookupあま.る with usual余る spelling. Do not call all あまり orあまる uses rare.",
            "Do not link剰えto a kana/other-reading article or present search-only bare剰as the normal spelling ofあまつさえ. A metadata dot is not an exhaustive orthographic rule.",
            "Old form剩has12strokes versus target剰11; any recognition mention needs its own native/font inventory and cannot change target geometry/count.",
            "Exact reused過剰 change removes only newly obsolete no-card sentence; N2 vocabulary level and seven direct guards stay. Other easier articles read for comparison, not reopened for wholesale revision.",
            "Selective kana/English; no inferred frequency from priorities, no media or wider vocabulary scope.",
        ],
        "proposedHanText": "剰 剩 過 過剰 余 余る 余り 余剰 剰余 剰え 剰り 刀 刂 乗 利 剣 則 千 木",
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 125, "remainingAdditions": 1103,
        "nextAction": next_action, "limits": limits,
    }
    save(S / (PREFIX + "membership.json"), membership)
    save(S / (PREFIX + "progress.json"), progress)
    special = {
        "1196170": "Selected actual過剰かじょうsense1; existing N2noun/na-adjective preserved with all original guards.",
        "1355490": "冗員/剰員aliases share excess-personnel sense; useless-staff sense is especially冗員. Do not copy unrestricted evaluative meaning to every剰word.",
        "1355690": "剰余じょうよhas general surplus/balance/remainder and separate mathematics remainder sense; optional recognition, not required support.",
        "1543860": "剰すis attested alias of余すあます, butあま.すis not frozen target metadata. Do not append/drop readings or treat alias as frequency evidence.",
        "1544260": "余剰よじょうsurplus/remainder, noun/no-adjective. Useful recognition but no new necessary support justified.",
        "1580060": "出生過剰hasしゅっしょう/しゅっせいreadings; variation belongs to出生, not剰'sallocation.",
        "1580500": "剰えrare spelling; bare剰search-only.あまっさえsearch-only reading. Dated/usually-kana/usually-negative nuance kept distinct. Recognition only, not selected prompt.",
        "1584930": "剰りsearch-only spelling;餘りoutdated-kanji flag differs. Remainder-noun and suffix-more-than senses restricted toあまり; do not transfer toあんまり. No preferred modern剰り recommendation.",
        "1595440": "冗語/剰語family:剰語rare kanji form; no universal rarity claim forジョウor unflaggedcompounds.",
        "2344610": "Frozen過剰規制has computing flag; retained as source, no broad taxonomy claim.",
        "2830071": "Frozen過剰適応has mathematics field; not authority for universal usage/technical-field claims.",
        "2868185": "過剰適合has separately scoped statistics and computing overfitting senses; unselected.",
    }
    entries = ET.parse(S / (PREFIX + "jmdict.xml")).getroot().findall("entry")
    default = ("Complete family inspected as unselected context; all aliases/readings/restrictions/senses/"
               "register/field/priority flags preserved. No additional support needed for selectedジョウ. "
               "No frequency, unrestricted substitution or per-character allocation claim inferred.")
    comparisons = {
        "1223021": "規則rule/regulation supports wrong-title contrast, not surplus.",
        "1256750": "剣readings/old aliases andけん-only senses remain separate; sword/blade does not mean surplus.",
        "1355120": "乗るfull nine senses inspected; no surplus noun sense.乘るsearch-only,ノるre_nokanji retained.",
        "1429410": "超過overlap with過剰already guarded; no new word title. Intransitiveする classification retained.",
        "1493700": "不足shortage vs dissatisfaction senses kept separate; only shortage contrasts with excess.",
        "1543910": "余るあまるonly spelling in frozen family; does not establish剰るmodern spelling. Whole reading not rare merely because剰kununselected.",
        "1544520": "余分extra/surplus can be useful; guarded by existing過剰. No strict good-vs-bad semantic compartments.",
        "1544590": "余裕margin/leeway vs composure separate; existing過剰guard retained.余猶search-only, not ordinary recommendation.",
        "1580500": special["1580500"],
        "1584930": special["1584930"],
    }
    save(S / (PREFIX + "source-evidence.json"), {
        "schemaVersion": 1, "batch": "099", "sourceSnapshot": "docs/n1-source-snapshot.json",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG, CC BY-SA4.0; repositoryNOTICE.",
        "selectedLexicalDecisions": [{"entryIds": [e.findtext("ent_seq")],
                                     "decision": special.get(e.findtext("ent_seq"), default)} for e in entries],
        "comparisonDecisions": [{"entryIds": [key], "decision": value} for key, value in comparisons.items()],
        "authorInspection": {
            "completeMemberFamilies": 58, "completeComparisonFamilies": 10,
            "completeRawCharacterRecords": 9,
            "completeExistingArticlesRead": [
                "words/過剰.md", "kanji/過.md", "words/余る.md", "words/あまり.md",
                "words/あんまり.md", "words/余分.md", "words/超過.md", "words/余裕.md",
                "words/不足.md", "kanji/乗.md", "kanji/利.md", "kanji/余.md",
                "kanji/剣.md", "kanji/則.md",
            ],
            "method": "Fresh complete compact XML family reads (58member+10comparison), complete selected/reused/comparison articles, actual raw target and eight comparison records, pinned SVG and actual dictionary blocks. Compact text losslessness audited separately. Author inspection, not independent review.",
            "limits": "No exhaustive quiz-pool semantics/native-font certification or fresh earlier-batch review.",
        },
        "sourceLookupDiagnostics": [
            {"requested": "https://kotobank.jp/word/%E5%89%B0-533206",
             "actual": "https://kotobank.jp/word/%E5%93%A8%E5%85%B5-533206",
             "disposition": "Successful fetch was irrelevant哨兵entry, rejected as evidence. Unsuffixed剰resolved actual530513; only correct actual bytes archived."},
            {"requested": "https://www.weblio.jp/content/%E5%89%B0",
             "disposition": "Supplemental Digital Daijisen block corroborated; other Wiktionary/KANJIDIC mirror blocks are not independent reading-allocation evidence. Not required source; archived actualKotobankblocks used."},
            {"requested": "https://kotobank.jp/word/%E5%89%B0%E3%81%88",
             "actual": "https://kotobank.jp/word/%E5%89%B0%E3%81%88-427058",
             "disposition": "Historical variants redirected toSeisenbanあまっさえ/あまさえ/あまりさえheadings. Not used to override frozen modernJMdictregister or append readings; exact modern spelling decisions rely on complete frozen family1580500."},
            {"requested": "https://kotobank.jp/word/%E4%BD%99%E3%82%8B",
             "actual": "https://kotobank.jp/word/%E4%BD%99%E3%82%8B-427227",
             "disposition": "Actual Digital Daijisenあま・る【余る】inspected as supplemental comparison; long synonym section truncated byweb_fetch. No claim of full page read; actual frozen full family used for spelling decision."},
        ],
        "limits": limits,
    })
    print("Membership, per-family/readings/support/link/quiz decisions persisted; no runtime content authored.")


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(child) for child in element))


def audit():
    from fontTools.ttLib import TTFont
    from audit_n1_pilot import offered_keys
    from audit_n1_batch import lexical_pair
    from build_manifest import build_manifest

    snapshot, inputs, jm, kd = frozen()
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    selection = load(S / (PREFIX + "lexical-selection.json"))
    cmp = load(S / (PREFIX + "comparison-selection.json"))
    progress = load(S / (PREFIX + "progress.json"))
    evidence_path = S / (PREFIX + "source-evidence.json")
    evidence = load(evidence_path)
    named = json.loads(inputs["n1-kanji-source-20261102.json"])
    assert len(named) == len(set(named)) == 1232 and named[109] == CHAR
    assert row["sourceRow"] == 110 and row["statusAtFreeze"] == "pending"
    assert progress["membership"] == [CHAR] and progress["sourceRows"] == [110]
    assert progress["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    for name, chars in [
        ("kanjidic2.xml", [CHAR]), ("comparison-kanjidic2.xml", cmp["rawCharacterOrder"]),
    ]:
        packet_root = ET.parse(S / (PREFIX + name)).getroot()
        assert canonical(packet_root.find("header")) == canonical(kd.find("header"))
        assert [e.findtext("literal") for e in packet_root.findall("character")] == chars
        for entry in packet_root.findall("character"):
            original = next(o for o in kd.findall("character")
                            if o.findtext("literal") == entry.findtext("literal"))
            assert canonical(entry) == canonical(original)
    families = {e.findtext("ent_seq"): e for e in jm.findall("entry")}
    exact_ids = [i for i, e in families.items()
                 if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    old_ids = [i for i, e in families.items()
               if any("剩" in k.text for k in e.findall("k_ele/keb"))]
    comparison_ids = [i for i, e in families.items()
                      if any(n.text in cmp["exactSpellingsOrReadings"]
                             for n in e.findall("k_ele/keb") + e.findall("r_ele/reb"))
                      or i in old_ids]
    assert old_ids == []
    assert len(exact_ids) == 58 and len(comparison_ids) == 10
    assert selection["entryIds"] == exact_ids and cmp["entryIds"] == comparison_ids
    assert len(set(exact_ids + comparison_ids)) == 66
    for stem, ids, compact_name in [
        ("", exact_ids, "batch-099-full-family-reading.txt"),
        ("comparison-", comparison_ids, "batch-099-comparison-reading.txt"),
    ]:
        path = S / (PREFIX + stem + "jmdict.xml")
        assert path.read_bytes() == extract(inputs["n1-implementation-JMdict_e.gz"],
                                           snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        compact_path = C / compact_name
        compact = compact_path.read_text(encoding="utf-8").splitlines()
        entries = ET.parse(path).getroot().findall("entry")
        assert len(compact) == len(entries) == len(ids)
        assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(compact, entries))
        (S / (PREFIX + stem + "full-family-reading.txt.gz")).write_bytes(
            gzip.compress(compact_path.read_bytes(), mtime=0))
    compact_path = C / "batch-099-comparison-characters-reading.txt"
    compact = compact_path.read_text(encoding="utf-8").splitlines()
    original = list(ET.parse(S / (PREFIX + "comparison-kanjidic2.xml")).getroot())
    assert len(compact) == len(original) == 9
    assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(compact, original))
    (S / (PREFIX + "comparison-character-reading.txt.gz")).write_bytes(
        gzip.compress(compact_path.read_bytes(), mtime=0))
    for field, ids in [("selectedLexicalDecisions", exact_ids), ("comparisonDecisions", comparison_ids)]:
        decisions = [i for group in evidence[field] for i in group["entryIds"]]
        assert len(decisions) == len(set(decisions)) and set(decisions) == set(ids)
    expected = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                for reading in row["metadata"][field]]
    assert [(d["kind"], d["reading"]) for d in progress["readingDispositions"]] == expected
    assert len(expected) == 4
    assert all(d["kanji"] == CHAR and d["qualification"] and d["evidence"]
               and set(d["entryIds"]) <= set(exact_ids) for d in progress["readingDispositions"])
    assert [d["reading"] for d in progress["readingDispositions"] if d["proposedQuizSelection"]] == ["ジョウ"]
    projection = progress["proposedCuratedProjection"]
    assert projection["quizOnyomi"] == ["ジョウ"] and projection["quizKunyomi"] == []
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == ["じょう"]
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == []
    pairs = set()
    for mapping in progress["proposedSupportMapping"]:
        entry = families[mapping["entryId"]]
        assert lexical_pair(entry, mapping["word"], mapping["primaryReading"])
        for i in mapping["selectedSenses"]:
            sense = entry.findall("sense")[i - 1]
            assert not sense.findall("stagk") or mapping["word"] in [n.text for n in sense.findall("stagk")]
            assert not sense.findall("stagr") or mapping["primaryReading"] in [n.text for n in sense.findall("stagr")]
        assert mapping["newArticle"] is False
        m = metadata(R, mapping["article"])
        assert (m["word"], m["reading"], m["jlpt"], m["kanji"]) == (
            mapping["word"], mapping["primaryReading"], mapping["wordJlpt"], mapping["allWrittenKanji"])
        assert m["quiz_exclusions"] == ["余分", "超過", "オーバー", "あまり", "あんまり", "余る", "余裕"]
        for char in m["kanji"]:
            if char == CHAR or (R / "kanji" / (char + ".md")).exists():
                pairs.add((char, mapping["article"]))
    assert pairs == {tuple(p) for p in progress["proposedReciprocalPairs"]} and len(pairs) == 2
    directions = {(f"kanji/{char}.md", article) for char, article in pairs}
    directions |= {(article, f"kanji/{char}.md") for char, article in pairs}
    assert {(d["from"], d["to"]) for d in progress["proposedDirectedLinkPlan"]} == directions
    assert progress["requiredDirectionCount"] == len(directions) == 4
    existing = set()
    for origin, target in directions:
        path = R / origin
        if path.exists() and f"](../{target})" in path.read_text(encoding="utf-8"):
            existing.add((origin, target))
    assert existing == {(d["from"], d["to"]) for d in progress["alreadyExistingRequiredDirections"]}
    assert existing == {("words/過剰.md", "kanji/過.md")}
    nav = load(S / (PREFIX + "source-navigation.json"))
    assert nav["baselinePairs"] == progress["activatedBaselinePairs"] and len(nav["baselinePairs"]) == 1
    assert [d["article"] for d in nav["candidates"]] == ["words/過剰.md"]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    for change in progress["proposedReusedChanges"]:
        assert (R / change["article"]).read_text(encoding="utf-8").count(change["before"]) == 1
    quiz = progress["proposedQuiz"]
    assert quiz["labels"] == [metadata(R, f"kanji/{char}.md")["title"] for char in quiz["distractors"]]
    assert len(quiz["distractors"]) == len(set(quiz["distractors"])) == 3
    assert all(metadata(R, path.relative_to(R).as_posix())["title"] != quiz["kanjiTitle"]
               for path in (R / "kanji").glob("*.md"))
    assert all(len(metadata(R, f"kanji/{char}.md")["distractors"]) == 3 for char in "余過乗利剣則")
    assert quiz["proposedDirectExclusions"] == [] and quiz["newWordTitle"] is None
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8449 and manifest["contentVersion"] == "0cbdc2723b0433f2"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(line[3:].startswith("docs/n1-sources/batch-099-")
               for line in git("status", "--porcelain", "--untracked-files=all").splitlines())
    baseline = load(S / "baseline-inventory.json")
    original_chars = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    earlier = set("保案派第策結")
    assert len(accepted) == 125 and accepted <= current - original_chars and accepted <= set(named)
    assert len(current) == 1121 and len(set(named) & current) == 135
    assert current & set(named) == (original_chars & set(named)) | accepted | earlier
    assert len(set(named) - current) == 1097
    assert all(metadata(R, f"kanji/{char}.md")["jlpt"] == 2 for char in earlier)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    assert len(list((R / "words").glob("*.md"))) == 5073
    assert sum(metadata(R, f"kanji/{char}.md")["jlpt"] == 1 for char in current) == 130
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-05270-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    svg_root = ET.fromstring(svg)
    paths = svg_root.findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 11
    assert [p.attrib["id"] for p in paths] == [f"kvg:05270-s{i}" for i in range(1, 12)]
    variant = next(g for g in svg_root.findall(".//{http://www.w3.org/2000/svg}g")
                   if any(k.endswith("}element") and v == "刂" for k, v in g.attrib.items()))
    assert next(v for k, v in variant.attrib.items() if k.endswith("}original")) == "刀"
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "099", "revision": tree["sha"], "input": str(svg_path),
        "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/05270.svg",
        "dictionaryStrokeCount": 11, "sourceStrokePaths": 11, "converted": False,
        "nativeDrawingAccepted": False, "converterNormalizedSha256": converter,
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repositoryNOTICE.",
        "limits": "Pinned SVG verified, not runtime geometry/native acceptance. SVGphon tags not accepted historical evidence.",
    }
    save(S / (PREFIX + "stroke-evidence.json"), stroke)
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg)
    han = sorted({char for char in progress["proposedHanText"] if 0x2E80 <= ord(char) <= 0x2FDF
                  or 0x3400 <= ord(char) <= 0x9FFF or 0xF900 <= ord(char) <= 0xFAFF
                  or 0x20000 <= ord(char) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-098-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {char: ord(char) in cmap for char in han},
                      "allProposedMissing": [char for char in han if ord(char) not in cmap]})
    rare = [char for char in han if 0x2E80 <= ord(char) <= 0x2FDF or 0x3400 <= ord(char) <= 0x4DBF
            or 0xF900 <= ord(char) <= 0xFAFF or 0x20000 <= ord(char) <= 0x2FFFF]
    unicode_line = next(line for line in inputs["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines()
                        if line.startswith("2F11;"))
    assert unicode_line.split(";")[5] == "<compat> 5200"
    save(S / (PREFIX + "font-preparation.json"), {
        "schemaVersion": 1, "batch": "099", "proposedTextInventory": progress["proposedHanText"],
        "inventoryScope": "Proposed card and exact two reused passage additions only; draft may change inventory.",
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "rareHanRangeCharacters": rare, "unicodeRadicalRecord": unicode_line,
        "mechanism": "Unchanged RareHan.kt and RareHanTest.kt inspected; three bundled font cmaps checked. All proposed Han ordinary BMP; no rare compatibility-radical text proposed.",
        "limits": "Preflight only, not finalruntimeHan/nativelegibility/fallbackface. Fresh four-font/all-Han native rendering and non-skipped RareHan test remain required. Cmap presence/absence is not glyph acceptance.",
    })
    for receipt in load(S / (PREFIX + "public-source-receipts.json")).values():
        raw = Path(receipt["sourcePath"]).read_bytes()
        assert sha(raw) == receipt["sourceSha256"]
        archive = S / receipt["archive"]
        assert sha(archive.read_bytes()) == receipt["archiveSha256"]
        assert gzip.decompress(archive.read_bytes()) == raw
        assert sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"]
    text = (S / (PREFIX + "character-public-text.txt")).read_text(encoding="utf-8")
    assert "じょう【剰〔剩〕】" in text and "［音］ジョウ" in text and "剰余／過剰・余剰" in text
    text = (S / (PREFIX + "kajo-public-text.txt")).read_text(encoding="utf-8")
    assert "か‐じょう" in text and "必要な程度や数量を越えて多いこと" in text
    evidence["familyCounts"] = {"allExactMemberFamilies": 58, "comparisonFamilies": 10,
                                "distinctCompleteFamilies": 66, "oldFormContainingFamilies": 0}
    evidence["actualPacketLineCounts"] = {
        name: len((S / (PREFIX + name)).read_text(encoding="utf-8").splitlines())
        for name in ["jmdict.xml", "kanjidic2.xml", "comparison-jmdict.xml", "comparison-kanjidic2.xml",
                     "character-public-text.txt", "kajo-public-text.txt"]}
    save(evidence_path, evidence)
    result = {
        "schemaVersion": 1, "execution": 728, "batch": "099", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 110,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "completeLexicalFamilies": 58,
        "completeComparisonFamilies": 10, "distinctCompleteFamilies": 66,
        "allExtractedEntryIdsAccountedFor": True, "oldFormContainingFamilies": 0,
        "freshExactDictionaryExtractionsVerified": 2, "rawCharacterRecordsVerified": 9,
        "compactFullFamilyTextSemanticallyEqualToRawXml": True,
        "proposedMetadataReadingDispositionsVerified": 4,
        "sourceOnlyReadingCount": sum(d["sourceOnly"] for d in progress["readingDispositions"]),
        "unselectedRecognitionReadingCount": 1, "proposedOnKeys": projection["onKeys"],
        "proposedKunKeys": [], "proposedNewSupportArticles": 0, "proposedReusedSupportArticles": 1,
        "allMappedReciprocalPairs": 2, "requiredDirectedLinks": 4, "alreadyExistingDirections": 1,
        "activatedBaselinePairs": 1, "proposedNewDirectWordGuards": 0,
        "pinnedSvg": stroke, "proposedHanCount": len(han),
        "fontPreparation": PREFIX + "font-preparation.json", "mainFontCmapAbsences": fonts[0]["allProposedMissing"],
        "inspectedArticleHashes": {name: sha((R / name).read_bytes())
                                  for name in evidence["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "manifestSha256": sha((R / "manifest.json").read_bytes()), "contentVersion": manifest["contentVersion"],
        "publishedAdditions": 125, "remainingAcceptanceAdditions": 1103, "actuallyAbsentNamedMembers": 1097,
        "separateEarlierLevelSourceMembers": sorted(earlier),
        "separateEarlierPlacementsCountedAsIssue60AcceptedBatches": False,
        "baselinePreservation": "Every runtime byte unchanged from normally signed published base; no metadata/readings/levels/exclusions/geometry changed.",
        "runtimeChanges": 0, "reviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "optionalHistoricalHelpersAccessed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "limits": progress["limits"],
    }
    save(S / (PREFIX + "preparation-audit.json"), result)
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ["limits", "pinnedSvg", "inspectedArticleHashes"]}, indent=2))


def record():
    checks = {}
    for name in ["source-tests", "validate", "budget", "vocabulary", "audit", "manifest", "manifest-diff", "whitespace"]:
        path = L / f"{name}-728.txt"
        text = path.read_text(encoding="utf-8-sig")
        assert "Traceback" not in text and "FAILED" not in text
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8449' in text
        archive = S / f"batch-099-{name}-728.txt.gz"
        raw = path.read_bytes()
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {
            "path": str(path), "sha256": sha(raw), "archive": archive.name,
            "archiveSha256": sha(archive.read_bytes()), "losslessGzip": True,
            "provenance": "Direct redirected stdout/stderr; exit0 explicitly checked by checks-source-728.ps1.",
        }
    helpers = []
    for name, archive_name in [
        ("source-728.py", PREFIX + "source-recipe.py"),
        ("preflight-728.ps1", PREFIX + "preflight-728.ps1.txt"),
        ("checks-source-728.ps1", PREFIX + "checks-source-728.ps1.txt"),
    ]:
        target = S / archive_name
        target.write_bytes((C / name).read_bytes())
        helpers.append({"durableControlPath": str(C / name), "archive": archive_name,
                        "sha256": sha(target.read_bytes())})
    progress = load(S / (PREFIX + "progress.json"))
    save(S / "execution-728.json", {
        "schemaVersion": 1, "execution": 728, "batch": "099", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution728StartingState"],
        "sourceAudit": PREFIX + "preparation-audit.json", "sourcePacket": PREFIX + "progress.json",
        "sourceEvidence": PREFIX + "source-evidence.json", "durableHelpers": helpers,
        "checks": checks, "runtimeChanged": False, "runtimePublished": False,
        "focusedTestsPassed": 43,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 125, "remainingAdditions": 1103,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": progress["nextAction"], "limits": progress["limits"],
    })
    print("Source evidence/checks and durable helpers archived; normal local signing next, no push.")


def seal():
    head = git("rev-parse", "HEAD")
    clean(R, head)
    clean(A, APP)
    assert head != BASE and git("rev-parse", "origin/main") == BASE
    assert git("rev-list", "--count", f"{BASE}..HEAD") == "1"
    assert git("merge-base", BASE, head) == BASE
    assert not git("diff", BASE, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    changed = git("diff", "--name-only", BASE, "HEAD")
    assert changed and all(name.startswith("docs/n1-sources/batch-099-") or name == "docs/n1-sources/execution-728.json"
                           for name in changed.splitlines())
    before = load(L / "progress-before-728.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert (p["checkpoint"], p["batch"]) == (727, "099")
    assert all(p.get(key) == value for key, value in before.items() if key not in allowed)
    role = load(L / "preflight-728.json")
    runner = load(C / "runner.json")
    assert runner["pid"] == 15692 and runner["sessionId"] == L.name and runner["status"] == "running"
    assert role["liveParentPid"] == 15692 and role["lockTouched"] is False
    issue = load(L / "issue-response-728.json")
    body = (C / "execution728-issue.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    assert issue["issue_url"].endswith("/issues/60")
    receipt = {"id": issue["id"], "url": issue["html_url"], "author": "stop-cran",
               "bodySha256": sha(body.encode("utf-8")), "verified": True}
    audit_result = load(S / (PREFIX + "preparation-audit.json"))
    state = {
        "schemaVersion": 1, "execution": 728, "checkpoint": 728, "batch": "099",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-099-progress.json",
        "sourceAudit": "docs/n1-sources/batch-099-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-728.json", "membership": [CHAR], "sourceRow": 110,
        "lexicalFamilies": 58, "comparisonFamilies": 10, "distinctCompleteDictionaryFamilies": 66,
        "completeRawCharacterRecords": 9, "completeExistingArticlesRead": len(audit_result["inspectedArticleHashes"]),
        "metadataReadings": 4, "sourceOnlyReadings": 2, "unselectedRecognitionReadings": 1,
        "proposedOnKeys": ["じょう"], "proposedKunKeys": [],
        "proposedNewSupportArticles": 0, "proposedReusedSupportArticles": 1,
        "allMappedReciprocalPairs": 2, "proposedLinkDirections": 4, "alreadyExistingDirections": 1,
        "activatedBaselinePairs": 1, "proposedReusedChanges": 2,
        "pinnedSvgPaths": 11, "geometryConverted": False, "proposedNewDirectWordGuards": 0,
        "proposedHanCount": audit_result["proposedHanCount"],
        "mainFontCmapAbsences": audit_result["mainFontCmapAbsences"],
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False, "focusedTestsPassed": 43,
        "publishedAdditions": 125, "remainingAdditions": 1103,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "runtimeHashesUnchanged": 8449, "contentVersion": "0cbdc2723b0433f2",
        "originalHistoricalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "issueUpdate": receipt["url"],
        "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
    }
    p["execution728CoordinatorCheckpoint"] = state
    p["batch099SourcePreparation"] = state
    p["batch099SourcePreparationIssueReceipt"] = receipt
    p["execution728StartingState"]["status"] = "signed-local-source-preparation-checkpoint-complete"
    p.update(checkpoint=728, status="continue", stage="batch-099-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(key) == value for key, value in before.items() if key not in allowed)
    save(L / "execution-728-final-checkpoint.json", state)
    print(json.dumps(state, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=["start", "packet", "comparison", "public", "plan", "audit", "record", "seal"])
    globals()[parser.parse_args().step]()
