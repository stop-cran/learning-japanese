"""Prepare and preserve source-only evidence for bounded N1 batch 098."""
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
L = C / "logs" / "18c9cb5e-d58a-4304-8222-62ac6b5d7f9a"
BASE = "69af99e5d7bf34b093959d90dddc7d59fe6393b5"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u5264"
PREFIX = "batch-098-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".718.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (717, "097", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1104
    assert not list(S.glob(PREFIX + "*"))
    role = load(L / "preflight-718.json")
    assert role["liveParentPid"] == 19008 and role["sessionId"] == L.name
    assert role["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 717
    assert checkpoint["execution717CoordinatorCheckpoint"] == p["execution717CoordinatorCheckpoint"]
    before = L / "progress-before-718.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 718, "batch": "098", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded098 source-preparation checkpoint for frozen row109 only; no runtime draft, reviewer, Android/native, publication,099 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed. Operative contract, complete approved issue and final717 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals content. Android1c1b7bf4 retains productionf9b59a2, NOT latest app main. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution718StartingState"] = state
    p.update(batch="098", stage="batch-098-source-preparation-in-progress",
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
    assert load(C / "progress.json")["batch"] == "098"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 109
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[108] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "098", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+5264 in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    (S / (PREFIX + "jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    character_packet(kd, CHAR, "kanjidic2.xml")
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "098", "baseCommit": BASE, "sourceIndexRecord": row,
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
    compact_packet("jmdict.xml", "batch-098-full-family-reading.txt")
    print(json.dumps({"families": len(ids), "candidates": candidates}, ensure_ascii=True, indent=2))


def comparison():
    snapshot, inputs, jm, kd = frozen()
    words = ["洗剤", "石鹸", "せっけん", "薬", "薬品", "剤", "剛健", "規則",
             "洗う", "済む", "削る", "刈る"]
    chars = "洗済剛則薬削斉"
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(n.text in words for n in e.findall("k_ele/keb") + e.findall("r_ele/reb"))]
    save(S / (PREFIX + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "098", "exactSpellingsOrReadings": words, "entryIds": ids,
        "rawCharacterOrder": list(chars),
        "rule": "Complete frozen families with exact listed keb or reb; preserve every alias/restriction/sense.",
        "limits": "Bounded comparisons, not exhaustive quiz-pool acceptance.",
    })
    (S / (PREFIX + "comparison-jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    character_packet(kd, chars, "comparison-kanjidic2.xml")
    compact_packet("comparison-jmdict.xml", "batch-098-comparison-reading.txt")
    compact_packet("comparison-kanjidic2.xml", "batch-098-comparison-characters-reading.txt")
    print(json.dumps({"comparisonFamilies": len(ids), "comparisonCharacters": len(chars)}))


def public():
    from html.parser import HTMLParser

    class SelectedText(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth = 0
            self.root_tag = ""
            self.parts = []

        def handle_starttag(self, tag, attrs):
            if self.depth:
                if tag == self.root_tag:
                    self.depth += 1
                if tag in {"p", "h2", "h3", "br", "section", "li"}:
                    self.parts.append("\n")
            elif tag == "article" or (tag == "div" and "kiji" in dict(attrs).get("class", "").split()):
                self.root_tag = tag
                self.depth = 1
                self.parts.append("\n[DICTIONARY BLOCK]\n")

        def handle_endtag(self, tag):
            if self.depth and tag == self.root_tag:
                self.depth -= 1
                if not self.depth:
                    self.parts.append("\n[END BLOCK]\n")

        def handle_data(self, data):
            if self.depth:
                self.parts.append(data)

    receipts = {}
    for key, filename, url, expected, authority in [
        ("character", "batch-098-character-weblio.html", "https://www.weblio.jp/content/%E5%89%A4",
         "ざい【剤〔劑〕】", "Weblio: Digital Daijisen first block; other dictionary blocks separately labelled in source HTML."),
        ("senzai", "batch-098-senzai.html", "https://kotobank.jp/word/%E6%B4%97%E5%89%A4-88273",
         "せん", "Kotobank: Digital Daijisen and other separately headed dictionaries."),
        ("jitsu", "batch-098-character-jitsu.html", "https://kotobank.jp/word/%E5%89%A4-507140",
         "字音", "Actual Kotobank bytes contain Digital Daijisen, Seisenban Nihon Kokugo Daijiten and Fukyuban Jitsu as separate blocks. Initial web_fetch returned only Jitsu; raw bytes were inspected rather than treating that extraction as complete."),
    ]:
        path = C / "inputs" / filename
        raw = path.read_bytes()
        parser = SelectedText()
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
            "sourcePath": str(path), "sourceSha256": sha(raw), "authority": authority,
            "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
            "losslessGzip": gzip.decompress(archive.read_bytes()) == raw,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "extractionLimits": "Article/div.kiji blocks only; formatting/links stripped, image gaiji not decoded. Actual relevant heading and definition inspected, not search snippets. Supplemental entries do not authorize new metadata readings, frequency claims or historical/phonetic acceptance.",
        }
    save(S / (PREFIX + "public-source-receipts.json"), receipts)
    print("Three actual dictionary pages archived losslessly; bounded dictionary blocks extracted.")


def plan():
    limits = (
        "Source preparation only; no runtime draft, independent content review, app/native acceptance or publication. "
        "Published124/1228 and1104 acceptance remainder unchanged. Six earlier-level source placements remain separate. "
        "Font cmap is preflight, not glyph acceptance. Physical-phone/general-release/whole-set acceptance outstanding. "
        "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latest app main."
    )
    next_action = (
        "SAME098 bounded runtime draft from committed source packet, then normally signed LOCAL UNREVIEWED freeze only. "
        "New剤 frozen row109: preserve fullザイ/スイ/セイ andかる/けず.る in source order; explicitly select "
        "quizOnyomi[ザイ], quizKunyomi[] only. Reuse actual洗剤せんざい N2 with all metadata/originalせっけん "
        "exclusion unchanged; no new support word justified. Other four readings get individually qualified source-only "
        "rows, no invented lexical examples or invalid-reading/obsolescence claim. Source includes noncompositional "
        "粘剤ねり;せいin製剤 andすいin推進剤 do NOT allocateセイ/スイ to剤. TWO all-mapped pairs/FOUR directions, "
        "ONE existing direction/ONE activated baseline pair; TWO navigation-only reused changes: link剤 at "
        "words洗剤 component introduction; add洗剤せんざい Common words link to kanji洗. Generate TEN paths "
        "with pinned converter; final Han/font/metadata/curation/quiz/baseline/link audits and validate/regenerate manifest. "
        "Three proposed wrong kanji済/剛/則 require final-title audit;薬 is an unsafe semantic neighbor, not wrong choice. "
        "No word title/exclusion change proposed. Then TWO serial blind different-family textual reviews on same signed "
        "snapshot, evidence reconciliation/original-session confirmations, fresh non-skipped Android, production "
        "ContentSync ONCE/native N1-All/meaning/curated reading/drawing/article/Back/offline/four-font/all-Han/rendered "
        "confirmation, combined-current-main checks, normal signing/owner fast-forward/terminal green CI/EVERY "
        "immutable public ZIP hash/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/per-file/path/media "
        "guards/verified ownerissue remain mandatory. No unreviewed push/099/authoragent/concurrentheavywork/secondrunner. "
        "Parent19008 owns runner.lock; no child acquire/delete/unlock/readprobe. Approved control/committed evidence/"
        "frozen inputs only; preserve/report/yield actual new denial/signing hang/uncertain ownership. Preserve every "
        "historical source/review/process/denial/OOM/read-depth/native/phone limitation. Project incomplete."
    )
    membership = {
        "schemaVersion": 1, "batch": "098", "baseCommit": BASE, "membership": [CHAR],
        "sourceRows": [109], "members": [{"kanji": CHAR, "sourceRow": 109}],
        "selectionReason": "Next absent frozen row after published剣. ONE character: five readings, 336 complete member families and source-only allocation risks justify a bounded packet. Earlier deferred rows remain pending.",
        "status": "source-prepared-not-drafted", "drafted": [], "reviewClosed": [], "published": [],
        "limits": limits,
    }
    nav = load(S / (PREFIX + "source-navigation.json"))
    pairs = [[CHAR, "words/洗剤.md"], ["洗", "words/洗剤.md"]]
    directions = []
    for char, word in pairs:
        directions.extend([
            {"from": f"kanji/{char}.md", "to": word, "reason": "Mapped reading/common-word navigation."},
            {"from": word, "to": f"kanji/{char}.md", "reason": "Substantive component introduction."},
        ])
    readings = [
        {"kanji": CHAR, "kind": "on", "reading": "ザイ", "proposedQuizSelection": True,
         "sourceOnly": False, "example": "洗剤 せんざい — detergent; cleaning agent",
         "entryIds": ["1296370", "1390950"],
         "qualification": "Exact existing N2 vocabulary identity. Actual Digital Daijisen剤漢字項目 lists洗剤 underザイ; segmented洗剤せん‐ざい and full raw洗セン corroborate allocation. General chemical/preparation use, not exclusively swallowed medicine; preserve all metadata and originalせっけん guard.",
         "evidence": "Frozen KANJIDIC2剤/洗, complete JMdict1296370/1390950, actual archived Digital Daijisen剤漢字項目 and洗剤."},
        {"kanji": CHAR, "kind": "on", "reading": "スイ", "proposedQuizSelection": False,
         "sourceOnly": True, "entryIds": [],
         "qualification": "Retain exact frozen character-dictionary reading as lookup only. No applicable independent modern lexical allocation established in all336 selected families. すいin推進剤/水銀剤 belongs to earlier characters, not剤; not a linkedスイ example. No claim that this reading is invalid or necessarily archaic.",
         "evidence": "Complete frozen KANJIDIC2剤; all336 full member families; Weblio KANJIDIC mirror is not independent confirmation."},
        {"kanji": CHAR, "kind": "on", "reading": "セイ", "proposedQuizSelection": False,
         "sourceOnly": True, "entryIds": [],
         "qualification": "Retain exact frozen character-dictionary reading as lookup only. No applicable independent modern lexical allocation established in all336 selected families. 製剤せいざい usesセイfor製 andザイfor剤; it does not demonstrate剤セイ. No invalid-reading or historical-period claim.",
         "evidence": "Complete frozen KANJIDIC2剤; complete JMdict2276330 and all336 member families; Digital Daijisen suppliesザイ but its omission ofセイ is not disproof."},
        {"kanji": CHAR, "kind": "kun", "reading": "かる", "proposedQuizSelection": False,
         "sourceOnly": True, "entryIds": [],
         "qualification": "Retain source's undottedかる exactly as character-reference information. No verified modern word example selected. Do not invent剤る or substitute this spelling for刈る. Separate刈る/苅るかる family does not contain剤 and does not prove its spelling/okurigana boundary. Do not label everyかる pronunciation rare.",
         "evidence": "Complete frozen KANJIDIC2剤 and comparison JMdict1209540; no剤かる whole-word family in the complete member selection."},
        {"kanji": CHAR, "kind": "kun", "reading": "けず.る", "proposedQuizSelection": False,
         "sourceOnly": True, "entryIds": [],
         "qualification": "Retain dottedけず.る exactly as character-reference information. No verified modern lexical example selected; do not manufacture剤るけずる or transfer the ordinary削る article to剤. Dictionary listing establishes recognition, not ordinary spelling or collocation.",
         "evidence": "Complete frozen KANJIDIC2剤 and comparison JMdict1298090/1298100; no剤けずる whole-word family in all336 member families."},
    ]
    progress = {
        **membership, "freshOriginMainAtPreparation": BASE,
        "sourceReadingOrder": {"onyomi": ["ザイ", "スイ", "セイ"], "kunyomi": ["かる", "けず.る"]},
        "readingDispositions": readings,
        "proposedCuratedProjection": {"kanji": CHAR, "quizOnyomi": ["ザイ"], "quizKunyomi": [],
                                     "onKeys": ["ざい"], "kunKeys": [],
                                     "limits": "Exact raw-string subset; compatible curated-reading APK required. No runtime offered-key acceptance claimed."},
        "proposedSupportMapping": [
            {"kanji": CHAR, "article": "words/洗剤.md", "word": "洗剤", "primaryReading": "せんざい",
             "entryId": "1390950", "selectedSenses": [1], "newArticle": False,
             "allWrittenKanji": ["洗", "剤"], "wordJlpt": 2,
             "disposition": "Reuse true lexical identity; preserve metadata/title/readings/N2 level/originalせっけん exclusion and all prose. Link剤 only at substantive component introduction."}
        ],
        "proposedNewSupportArticles": [],
        "proposedReciprocalPairs": pairs, "proposedDirectedLinkPlan": directions,
        "requiredDirectionCount": 4,
        "alreadyExistingRequiredDirections": [{"from": "words/洗剤.md", "to": "kanji/洗.md"}],
        "activatedBaselinePairs": nav["baselinePairs"],
        "proposedReusedChanges": [
            {"article": "words/洗剤.md", "change": "Wrap existing剤 in component explanation with ../kanji/剤.md link only; no prose/metadata change."},
            {"article": "kanji/洗.md", "change": "Add one Common words bullet linking洗剤せんざい detergent/cleaning agent. Completes all-mapped洗/洗剤 pair; no other text/metadata change."},
        ],
        "proposedQuiz": {
            "kanjiTitle": "medicinal preparation; chemical agent", "distractors": ["済", "剛", "則"],
            "labels": ["settle; finish", "sturdy; unyielding strength", "rule; follow a model"],
            "rationale": "済 shares斉-shaped block but adds left氵, not right刂; 剛and則 share right刂 with different left blocks. Completion/strength/rule meanings do not name a medicine or chemical agent.",
            "unsafeComparisons": ["薬"],
            "legacyFallbackDisposition": "薬/済/洗/剛/則/削 all already have three curated distractors. No fallback repair proposed; wider custom/random/legacy pool semantics remain unverified.",
            "newWordTitle": None, "proposedDirectExclusions": [],
            "wordQuizDisposition": "No new/reworded word title. Existing洗剤/せっけん direct exclusion retained. No new薬剤 or剤 word article or inferred word-level assignment; no newly introduced word-label pair.",
            "confusableInventory": "docs/confusable-words.md inspected for剤; no matching entry. Actual source/article senses govern, not title differences or a transitive exclusion clique.",
        },
        "outsideFrozenReadingDispositions": [
            {"reading": "サイ/わりふ/くすり/きる/そろえる/はかる/まぜる and historical readings",
             "disposition": "Supplemental dictionaries cover additional readings/glosses. Keep them source context, not appended metadata/questions; difference does not invalidate either dictionary. Do not manufacture an etymology or transfer all historical senses to modernザイ."}
        ],
        "proposedTeachingConstraints": [
            "structure-unclassified; labelled modern-shape mnemonic only, not a reconstruction. 斉-shaped block with crossed upper strokes and lower bars beside right刂; SVG phon label is not accepted etymological evidence.",
            "Canonical radical刀18 preserved; visible刂explained. Similar済 has left氵and no right刂; do not infer common reading from shared shape.",
            "Modern compound element剤means a preparation/agent and is not confined to swallowed medicine. 洗剤 supplies useful nonmedicalザイsupport; do not call detergent safe to ingest or suitable for all cleaning.",
            "Standalone JMdict剤 entry is suffix-noun, not permission to use剤as an everyday independent noun or numerical dose recommendation. No counters lesson or medical instruction in scope.",
            "Each of four unselected source readings needs its own qualified lookup row. Lack of a selected word does not establish invalidity, obsolescence or rarity of other ordinary words with that pronunciation.",
            "Recognition examples薬剤やくざい,錠剤じょうざい,調剤ちょうざい are fully sourced but need no additional article. 剤isざいeven when another character suppliesせいorすいin a compound.",
            "粘剤ねりis a whole lexical spelling, not evidence that剤independently readsりorねり. Preserve alternate/restricted spellings and source register/sense flags.",
            "Actual archived Daijisen剤and洗剤support allocation/category. Weblio KANJIDIC mirror and Wiktionary are not independent reputable evidence for new reading allocation.",
            "Initial web_fetch Kotobank剤returned only字通, while exact curl bytes include DaijisenandSeisenban too; source inspections use those actual blocks. Jitsu's undecoded gaiji/history not accepted as a phonetic/origin claim.",
            "Selective kana/English; no inferred word level, priority-based frequency rank, new media or broader easier-deck rewrite.",
        ],
        "proposedHanText": "剤 洗 洗剤 刀 刂 斉 済 氵 剛 則 薬 薬剤 錠剤 調剤 文 二 削る 刈る 製剤 推進剤 水銀剤 粘剤",
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 124, "remainingAdditions": 1104,
        "nextAction": next_action, "limits": limits,
    }
    save(S / (PREFIX + "membership.json"), membership)
    save(S / (PREFIX + "progress.json"), progress)
    special = {
        "1105980": "Mixed-script blister-agent spellings have explicit reading restrictions; preserve them, no additional support or usage procedure.",
        "1296370": "剤ざい is suffix noun with medicine/agent/chemical/dose glosses. Establishes bound lexical use, not an ordinary independent noun or numerical medical recommendation.",
        "1390950": "Exact reused洗剤せんざい family; one selected sense, actual N2 article preserves category including soap and originalせっけん exclusion.",
        "1391520": "煎剤せんざい decoction is separate same-reading family, NOT existing洗剤 identity.",
        "1429160": "調剤ちょうざい preparation/dispensing supports optional recognition; transitive/intransitiveする flags retained, no automatic dosing instruction.",
        "1538220": "薬剤やくざい has medicine AND nonmedical chemical-agent senses. Optional recognition; not a necessary new article or independent word-level inference.",
        "1538230": "薬剤師やくざいし pharmacist is occupational noun; no new support article or profession/treatment conflation.",
        "1546140": "溶剤/溶材/熔剤 preserve complete family; hot-charge sense restricted to溶材, not transferable to溶剤.",
        "1594200": "刺激剤/刺戟剤 search-only alias and figurative motivation sense retained; no broader claim that every剤word is a physical medicine.",
        "1689640": "配剤 has compounding and providence/arrangement senses; do not impose a universal medicinal gloss across every compound.",
        "1750660": "清涼剤 includes figurative welcome relief and physical tonic; no unrestricted substitution or claim all剤are consumed.",
        "1783890": "膠着剤 has explicit rare-term flag, separate from spelling frequency; unselected.",
        "1795630": "起爆剤 has figurative trigger/impetus as well as detonator sense; no universal physical-agent reading or operational example.",
        "1951490": "抗がん剤/抗癌剤/抗ガン剤 retain script-specific reading restrictions.",
        "1992620": "抗うつ剤/抗鬱剤 preserve search-only抗欝剤/抗ウツ剤 aliases, not normal-spelling recommendations.",
        "2276330": "製剤せいざい:せいdoes not belong to剤. Optional recognition only; preserve formulation/productionする sense.",
        "2411120": "防カビ剤/防黴剤 retain reading/spelling restrictions, includingぼうばいざい.",
        "2509500": "ワルファリン剤 rare-term flag retained; no medical advice or extra teaching example.",
        "2560780": "シロップ剤 has noun syrup and no-adjective syrupy senses, not universal adjective behavior for剤.",
        "2569220": "推進剤すいしんざい:すいbelongs to推, not剤スイ.",
        "2170160": "水銀剤すいぎんざい likewise does not allocateスイto剤; unselected technical context.",
        "2835044": "神経剤 nerve-agent and medicinal nerve-tonic senses stay distinct; do not choose a hazardous operational example.",
        "2837804": "粘剤ねり is whole-word lexical spelling for washi mucilage. Does not establish剤り/ねり or any of the four unselected metadata readings.",
        "2835813": "ｐＨ調整剤 two full readings preserved; do not normalize fullwidth raw source or add kana-derived character readings.",
        "2851314": "カンフル剤 historical drug sense and figurative stimulus sense separated; source-period flag local to its physical sense.",
        "2867912": "魔剤 slang energy-drink sense, esp. product brand, is not neutral everyday medicine vocabulary.",
        "5308045": "Organization-name family preserved, not ordinary compound practice.",
        "5583029": "Organization-name family preserved withにっぽんreading; no name-use expansion.",
    }
    entries = ET.parse(S / (PREFIX + "jmdict.xml")).getroot().findall("entry")
    default = ("Complete family inspected as unselected context; all aliases/readings/restrictions/senses/register/"
               "field/priority flags preserved. No additional support is necessary for selectedザイ. "
               "No frequency, safety, unrestricted substitution or per-character allocation claim inferred.")
    decisions = [{"entryIds": [e.findtext("ent_seq")],
                  "decision": special.get(e.findtext("ent_seq"), default)} for e in entries]
    comparison_decisions = {
        "1209540": "刈る/苅るかる has no剤spelling. Does not prove剤's spelling/okurigana boundary or invalidate raw sourceかる.",
        "1223021": "規則 rules establishes distractor sense, not medicine or chemical.",
        "1284120": "剛健 sturdy vigor establishes distractor strength, not medicine/agent identity.",
        "1295070": "済むcompletion/result/unease senses retained; no drug noun. Old濟む search-only alias not recommended.",
        "1296370": "Same selected bound剤family, counted once in distinct totals.",
        "1298090": "削るけずる whole modern verb family does not contain剤; do not relabel its spelling.",
        "1298100": "Separate削るはつる family with kana flags; not a剤けずる example.",
        "1382590": "Stone-soap family supports actual kana articleせっけん. Preserve existing洗剤direct guard; search-only石鹼not a new target.",
        "1385390": "せっけんhomophone接見audience/lawyer meeting is not soap; no conflated lexical identity.",
        "1386220": "せっけんhomophone節倹thrift is not soap; unselected.",
        "1390930": "洗うphysical and figurative verb senses retained; washing action distinct from detergent substance.",
        "1390950": "Same selected洗剤family, counted once in distinct totals.",
        "1538160": "薬くすり broad medicinal/chemical/glaze/bribe senses and re_nokanjiクスリ retained. Unsafe as a剤meaning distractor.",
        "1538280": "薬品has medicinal and chemical-agent senses, confirming semantic overlap rather than spelling-based partitions.",
        "1596100": "せっけんhomophone席巻/席捲is overwhelming, not soap.",
        "2220820": "薬やくslang narcotic separate family, not a reason to reassign existingくすりidentity.",
        "2581040": "せっけんhomophone尺縑/尺けんretains silk and trivial-art senses, not soap.",
        "2773390": "石剣せっけんarchaeological sword-shaped stoneware, not soap or剤reading allocation.",
    }
    articles = ["kanji/洗.md", "kanji/済.md", "kanji/剣.md", "kanji/則.md", "kanji/剖.md",
                "kanji/剛.md", "kanji/薬.md", "kanji/削.md", "words/洗剤.md", "words/せっけん.md",
                "words/薬品.md", "words/薬.md", "words/剛健.md", "words/規則.md", "words/洗う.md"]
    save(S / (PREFIX + "source-evidence.json"), {
        "schemaVersion": 1, "batch": "098", "sourceSnapshot": "docs/n1-source-snapshot.json",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG, CC BY-SA4.0; repositoryNOTICE.",
        "selectedLexicalDecisions": decisions,
        "comparisonDecisions": [{"entryIds": [key], "decision": value} for key, value in comparison_decisions.items()],
        "authorInspection": {
            "completeExactMemberFamiliesRead": 336,
            "memberReadingRanges": ["1-64 returned from truncated1-84 request", "65-70", "71-125", "126-180", "181-235", "236-285", "286-336"],
            "completeComparisonFamiliesRead": 18, "rawCharacterRecordsRead": 8,
            "completeExistingArticlesRead": articles,
            "missingArticleNotCountedAsRead": "kanji/斉.md absent; raw character record inspected instead, do not add a broken link.",
            "inspectionLimits": "Coordinator actual compact full-record reads preserve complete content/attributes, not just gloss summaries. First1-84 output truncated;65-70 follow-up read closes gap. Hashes/extraction are not comprehension or independent review. Public source excerpts1-80/1-100/1-130 inspected; supplemental long washing encyclopedia tail not relied on.",
        },
        "publicEvidence": "batch-098-public-source-receipts.json",
        "lookupLimits": [
            "Two guessed Kotobank剤する/剤(漢字) URLs returned404; neither verifies a headword, register or reading. No permission denial.",
            "Initial web_fetch剤 returned only Jitsu; raw curl bytes expose additional properly headed Daijisen/Seisenban blocks. Extracted raw blocks inspected directly.",
            "Weblio mirror and Wiktionary not independent source verification. Machine-generated Weblio example block not accepted as attestation.",
            "No new ordinary lexical example established for four unselected readings; explicit source-only dispositions, not a claim that the readings are false or absolutely unattested.",
            "Jitsu historical/phonetic account not adopted; image gaiji not decoded. Labelled shape mnemonic avoids inventing etymology.",
        ],
        "runtimeChanged": False, "independentReviewersLaunched": 0, "limits": limits,
    })
    print("All five reading dispositions, true reuse, four-direction plan and bounded teaching constraints preserved.")


def canonical(node):
    return (node.tag, tuple(sorted(node.attrib.items())), (node.text or "").strip(),
            tuple(canonical(child) for child in node))


def audit():
    from build_manifest import build_manifest
    from audit_n1_pilot import offered_keys
    from fontTools.ttLib import TTFont

    snapshot, inputs, jm, kd = frozen()
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    selection = load(S / (PREFIX + "lexical-selection.json"))
    comparison_selection = load(S / (PREFIX + "comparison-selection.json"))
    progress = load(S / (PREFIX + "progress.json"))
    evidence_path = S / (PREFIX + "source-evidence.json")
    evidence = load(evidence_path)
    named = json.loads(inputs["n1-kanji-source-20261102.json"])
    assert len(named) == len(set(named)) == 1232 and named[108] == CHAR
    assert row["sourceRow"] == 109 and row["statusAtFreeze"] == "pending"
    assert progress["membership"] == [CHAR] and progress["sourceRows"] == [109]
    assert progress["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    for name, chars in [
        ("kanjidic2.xml", [CHAR]),
        ("comparison-kanjidic2.xml", comparison_selection["rawCharacterOrder"]),
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
               if any("劑" in k.text for k in e.findall("k_ele/keb"))]
    assert old_ids == []
    comparison_ids = [i for i, e in families.items()
                      if any(n.text in comparison_selection["exactSpellingsOrReadings"]
                             for n in e.findall("k_ele/keb") + e.findall("r_ele/reb"))]
    assert len(exact_ids) == 336 and len(comparison_ids) == 18
    assert selection["entryIds"] == exact_ids and comparison_selection["entryIds"] == comparison_ids
    assert len(set(exact_ids + comparison_ids)) == 352
    for stem, ids, compact_name in [
        ("", exact_ids, "batch-098-full-family-reading.txt"),
        ("comparison-", comparison_ids, "batch-098-comparison-reading.txt"),
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
    compact_path = C / "batch-098-comparison-characters-reading.txt"
    compact = compact_path.read_text(encoding="utf-8").splitlines()
    original = list(ET.parse(S / (PREFIX + "comparison-kanjidic2.xml")).getroot())
    assert len(compact) == len(original) == 8
    assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(compact, original))
    (S / (PREFIX + "comparison-character-reading.txt.gz")).write_bytes(
        gzip.compress(compact_path.read_bytes(), mtime=0))
    for field, ids in [("selectedLexicalDecisions", exact_ids), ("comparisonDecisions", comparison_ids)]:
        decisions = [i for group in evidence[field] for i in group["entryIds"]]
        assert len(decisions) == len(set(decisions)) and set(decisions) == set(ids)
    expected = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                for reading in row["metadata"][field]]
    assert [(d["kind"], d["reading"]) for d in progress["readingDispositions"]] == expected
    assert len(expected) == 5
    assert all(d["kanji"] == CHAR and d["qualification"] and d["evidence"]
               and set(d["entryIds"]) <= set(exact_ids) for d in progress["readingDispositions"])
    assert [d["reading"] for d in progress["readingDispositions"] if d["proposedQuizSelection"]] == ["ザイ"]
    assert sum(d["sourceOnly"] for d in progress["readingDispositions"]) == 4
    projection = progress["proposedCuratedProjection"]
    assert projection["quizOnyomi"] == ["ザイ"] and projection["quizKunyomi"] == []
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == ["ざい"]
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == []
    pairs = set()
    for mapping in progress["proposedSupportMapping"]:
        entry = families[mapping["entryId"]]
        assert mapping["word"] in [n.text for n in entry.findall("k_ele/keb")]
        reading = next(n for n in entry.findall("r_ele") if n.findtext("reb") == mapping["primaryReading"])
        restrictions = [n.text for n in reading.findall("re_restr")]
        assert reading.find("re_nokanji") is None
        assert not restrictions or mapping["word"] in restrictions
        for i in mapping["selectedSenses"]:
            sense = entry.findall("sense")[i - 1]
            assert not sense.findall("stagk") or mapping["word"] in [n.text for n in sense.findall("stagk")]
            assert not sense.findall("stagr") or mapping["primaryReading"] in [n.text for n in sense.findall("stagr")]
        assert mapping["newArticle"] is False
        m = metadata(R, mapping["article"])
        assert (m["word"], m["reading"], m["jlpt"], m["kanji"]) == (
            mapping["word"], mapping["primaryReading"], mapping["wordJlpt"], mapping["allWrittenKanji"])
        assert m["quiz_exclusions"] == ["せっけん"]
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
        if not path.exists():
            continue
        relative = "../" + target if origin.split("/")[0] != target.split("/")[0] else target.split("/")[-1]
        if f"]({relative})" in path.read_text(encoding="utf-8"):
            existing.add((origin, target))
    assert existing == {(d["from"], d["to"]) for d in progress["alreadyExistingRequiredDirections"]}
    assert existing == {("words/洗剤.md", "kanji/洗.md")}
    nav = load(S / (PREFIX + "source-navigation.json"))
    assert nav["baselinePairs"] == progress["activatedBaselinePairs"] and len(nav["baselinePairs"]) == 1
    assert [d["article"] for d in nav["candidates"]] == ["words/洗剤.md"]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    assert {d["article"] for d in progress["proposedReusedChanges"]} == {"words/洗剤.md", "kanji/洗.md"}
    quiz = progress["proposedQuiz"]
    assert quiz["labels"] == [metadata(R, f"kanji/{char}.md")["title"] for char in quiz["distractors"]]
    assert len(quiz["distractors"]) == len(set(quiz["distractors"])) == 3
    assert all(metadata(R, path.relative_to(R).as_posix())["title"] != quiz["kanjiTitle"]
               for path in (R / "kanji").glob("*.md"))
    assert all(len(metadata(R, f"kanji/{char}.md")["distractors"]) == 3 for char in "薬済洗剛則削")
    assert quiz["proposedDirectExclusions"] == [] and quiz["newWordTitle"] is None
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8447 and manifest["contentVersion"] == "a066afceaf1f447a"
    manifest_hash = sha((R / "manifest.json").read_bytes())
    assert manifest_hash == "1328431c07136d7d1f2f22f8a1e31dd9a7d2f497898cedbbfc3e821997bbb781"
    runtime = ["kanji", "words", "articles", "strokes", "manifest.json", "tools"]
    assert not git("diff", BASE, "--", *runtime)
    assert all(line[3:].startswith("docs/n1-sources/batch-098-")
               for line in git("status", "--porcelain", "--untracked-files=all").splitlines())
    baseline = load(S / "baseline-inventory.json")
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    earlier = set("保案派第策結")
    assert len(accepted) == 124 and accepted <= current - original and accepted <= set(named)
    assert len(current) == 1120 and len(set(named) & current) == 134
    assert current & set(named) == (original & set(named)) | accepted | earlier
    assert len(set(named) - current) == 1098
    assert all(metadata(R, f"kanji/{char}.md")["jlpt"] == 2 for char in earlier)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-05264-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    svg_root = ET.fromstring(svg)
    paths = svg_root.findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 10
    assert [p.attrib["id"] for p in paths] == [f"kvg:05264-s{i}" for i in range(1, 11)]
    variant = next(g for g in svg_root.findall(".//{http://www.w3.org/2000/svg}g")
                   if any(k.endswith("}element") and v == "刂" for k, v in g.attrib.items()))
    assert next(v for k, v in variant.attrib.items() if k.endswith("}original")) == "刀"
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "098", "revision": tree["sha"], "input": str(svg_path),
        "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/05264.svg",
        "dictionaryStrokeCount": 10, "sourceStrokePaths": 10, "converted": False,
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
    for old in load(S / "batch-097-font-preparation.json")["fonts"]:
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
        "schemaVersion": 1, "batch": "098", "proposedTextInventory": progress["proposedHanText"],
        "inventoryScope": "Proposed card and exact two reused navigation additions only; draft may change inventory.",
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
    character_text = (S / (PREFIX + "jitsu-public-text.txt")).read_text(encoding="utf-8")
    assert "ざい【剤〔劑〕】［漢字項目］" in character_text
    assert "［音］ザイ（呉）" in character_text and "錠剤・洗剤・調剤" in character_text
    word_text = (S / (PREFIX + "senzai-public-text.txt")).read_text(encoding="utf-8")
    assert "せん‐ざい【洗剤】" in word_text and "石鹸せっけんや合成洗剤" in word_text
    evidence["familyCounts"] = {"allExactMemberFamilies": 336, "comparisonFamilies": 18,
                                "distinctCompleteFamilies": 352, "oldFormContainingFamilies": 0}
    evidence["actualPacketLineCounts"] = {
        name: len((S / (PREFIX + name)).read_text(encoding="utf-8").splitlines())
        for name in ["jmdict.xml", "kanjidic2.xml", "comparison-jmdict.xml", "comparison-kanjidic2.xml",
                     "character-public-text.txt", "senzai-public-text.txt", "jitsu-public-text.txt"]}
    save(evidence_path, evidence)
    result = {
        "schemaVersion": 1, "execution": 718, "batch": "098", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 109,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "completeLexicalFamilies": 336,
        "completeComparisonFamilies": 18, "distinctCompleteFamilies": 352,
        "allExtractedEntryIdsAccountedFor": True, "oldFormContainingFamilies": 0,
        "freshExactDictionaryExtractionsVerified": 2, "rawCharacterRecordsVerified": 8,
        "compactFullFamilyTextSemanticallyEqualToRawXml": True,
        "proposedMetadataReadingDispositionsVerified": 5, "sourceOnlyReadingCount": 4,
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "proposedNewSupportArticles": 0, "proposedReusedSupportArticles": 1,
        "allMappedReciprocalPairs": 2, "requiredDirectedLinks": 4, "alreadyExistingDirections": 1,
        "activatedBaselinePairs": 1, "proposedNewDirectWordGuards": 0,
        "pinnedSvg": stroke, "proposedHanCount": len(han),
        "fontPreparation": PREFIX + "font-preparation.json",
        "mainFontCmapAbsences": fonts[0]["allProposedMissing"],
        "inspectedArticleHashes": {name: sha((R / name).read_bytes())
                                  for name in evidence["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "manifestSha256": manifest_hash, "contentVersion": manifest["contentVersion"],
        "publishedAdditions": 124, "remainingAcceptanceAdditions": 1104, "actuallyAbsentNamedMembers": 1098,
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
        path = L / f"{name}-718.txt"
        text = path.read_text(encoding="utf-8-sig")
        assert "Traceback" not in text and "FAILED" not in text
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8447' in text
        archive = S / f"batch-098-{name}-718.txt.gz"
        raw = path.read_bytes()
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {
            "path": str(path), "sha256": sha(raw), "archive": archive.name,
            "archiveSha256": sha(archive.read_bytes()), "losslessGzip": True,
            "provenance": "Direct redirected stdout/stderr; exit0 explicitly checked by checks-source-718.ps1.",
        }
    helpers = []
    for name, archive_name in [
        ("source-718.py", PREFIX + "source-recipe.py"),
        ("preflight-718.ps1", PREFIX + "preflight-718.ps1.txt"),
        ("checks-source-718.ps1", PREFIX + "checks-source-718.ps1.txt"),
    ]:
        target = S / archive_name
        target.write_bytes((C / name).read_bytes())
        helpers.append({"durableControlPath": str(C / name), "archive": archive_name,
                        "sha256": sha(target.read_bytes())})
    progress = load(S / (PREFIX + "progress.json"))
    save(S / "execution-718.json", {
        "schemaVersion": 1, "execution": 718, "batch": "098", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution718StartingState"],
        "sourceAudit": PREFIX + "preparation-audit.json", "sourcePacket": PREFIX + "progress.json",
        "sourceEvidence": PREFIX + "source-evidence.json", "durableHelpers": helpers,
        "checks": checks, "runtimeChanged": False, "runtimePublished": False,
        "focusedTestsPassed": 43,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 124, "remainingAdditions": 1104,
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
    assert changed and all(name.startswith("docs/n1-sources/batch-098-") or name == "docs/n1-sources/execution-718.json"
                           for name in changed.splitlines())
    before = load(L / "progress-before-718.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert (p["checkpoint"], p["batch"]) == (717, "098")
    assert all(p.get(key) == value for key, value in before.items() if key not in allowed)
    role = load(L / "preflight-718.json")
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == L.name and runner["status"] == "running"
    assert role["liveParentPid"] == 19008 and role["lockTouched"] is False
    issue = load(L / "issue-response-718.json")
    body = (C / "execution718-issue.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    assert issue["issue_url"].endswith("/issues/60")
    receipt = {"id": issue["id"], "url": issue["html_url"], "author": "stop-cran",
               "bodySha256": sha(body.encode("utf-8")), "verified": True}
    audit = load(S / (PREFIX + "preparation-audit.json"))
    state = {
        "schemaVersion": 1, "execution": 718, "checkpoint": 718, "batch": "098",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-098-progress.json",
        "sourceAudit": "docs/n1-sources/batch-098-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-718.json", "membership": [CHAR], "sourceRow": 109,
        "lexicalFamilies": 336, "comparisonFamilies": 18, "distinctCompleteDictionaryFamilies": 352,
        "completeRawCharacterRecords": 8, "completeExistingArticlesRead": len(audit["inspectedArticleHashes"]),
        "metadataReadings": 5, "sourceOnlyReadings": 4,
        "proposedOnKeys": ["ざい"], "proposedKunKeys": [],
        "proposedNewSupportArticles": 0, "proposedReusedSupportArticles": 1,
        "allMappedReciprocalPairs": 2, "proposedLinkDirections": 4, "alreadyExistingDirections": 1,
        "activatedBaselinePairs": 1, "proposedReusedChanges": 2,
        "pinnedSvgPaths": 10, "geometryConverted": False, "proposedNewDirectWordGuards": 0,
        "proposedHanCount": audit["proposedHanCount"], "mainFontCmapAbsences": audit["mainFontCmapAbsences"],
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False, "focusedTestsPassed": 43,
        "publishedAdditions": 124, "remainingAdditions": 1104,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "runtimeHashesUnchanged": 8447, "contentVersion": "a066afceaf1f447a",
        "originalHistoricalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "issueUpdate": receipt["url"],
        "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
    }
    p["execution718CoordinatorCheckpoint"] = state
    p["batch098SourcePreparation"] = state
    p["batch098SourcePreparationIssueReceipt"] = receipt
    p["execution718StartingState"]["status"] = "signed-local-source-preparation-checkpoint-complete"
    p.update(checkpoint=718, status="continue", stage="batch-098-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(key) == value for key, value in before.items() if key not in allowed)
    save(L / "execution-718-final-checkpoint.json", state)
    print(json.dumps(state, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "packet", "comparison", "public", "plan", "audit", "record", "seal"])
    globals()[parser.parse_args().action]()
