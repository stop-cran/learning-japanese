"""Prepare source evidence for one bounded N1 batch; never write runtime content."""
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
L = C / "logs" / "17877b52-6e52-4681-bac3-c9d5a8db76ee"
BASE = "1b00a924a007f32da36894ea92b05f675436e60d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u5263"
PREFIX = "batch-097-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata, offered_keys
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".709.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (708, "096", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1105
    assert not list(S.glob(PREFIX + "*"))
    role = load(L / "preflight-709.json")
    assert role["liveParentPid"] == 19008 and role["sessionId"] == L.name
    assert role["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 708
    assert checkpoint["execution708CoordinatorCheckpoint"] == p["execution708CoordinatorCheckpoint"]
    before = L / "progress-before-709.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 709, "batch": "097", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded097 source-preparation checkpoint for frozen row108 only; no runtime draft, reviewer, Android/native, publication,098 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed. Operative contract, complete approved issue and final708 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals content. Android1c1b7bf4 retains productionf9b59a2, NOT latest app main. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution709StartingState"] = state
    p.update(batch="097", stage="batch-097-source-preparation-in-progress",
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
    for entry in ET.parse(S / (PREFIX + name)).getroot().findall("entry"):
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        lines.append(ET.tostring(entry, encoding="unicode"))
    (C / output).write_text("\n".join(lines) + "\n", encoding="utf-8")


def packet():
    snapshot, inputs, jm, kd = frozen()
    assert load(C / "progress.json")["batch"] == "097"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 108
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[107] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "097", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+5263 in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    (S / (PREFIX + "jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    character_packet(kd, CHAR, "kanjidic2.xml")
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "097", "baseCommit": BASE, "sourceIndexRecord": row,
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
    compact_packet("jmdict.xml", "batch-097-full-family-reading.txt")
    print(json.dumps({"families": len(ids), "candidates": candidates}, ensure_ascii=True, indent=2))


def comparison():
    snapshot, inputs, jm, kd = frozen()
    words = ["剣", "真剣", "刀", "日本刀", "刃", "ナイフ", "包丁", "針", "規則",
             "解剖", "剛健", "検査", "危険", "経験", "まじめ", "本気"]
    chars = "剛剖則刀刃真検険験針"
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(k.text in words for k in e.findall("k_ele/keb"))
           or any(r.text in words for r in e.findall("r_ele/reb"))]
    save(S / (PREFIX + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "097", "exactSpellingsOrReadings": words, "entryIds": ids,
        "rawCharacterOrder": list(chars),
        "rule": "Complete frozen families with exact listed keb or reb, including alternative lexical readings and restrictions.",
        "limits": "Bounded navigation packet, not exhaustive quiz or linguistic acceptance.",
    })
    (S / (PREFIX + "comparison-jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    character_packet(kd, chars, "comparison-kanjidic2.xml")
    compact_packet("comparison-jmdict.xml", "batch-097-comparison-reading.txt")
    compact = []
    for entry in ET.parse(S / (PREFIX + "comparison-kanjidic2.xml")).getroot().findall("character"):
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact.append(ET.tostring(entry, encoding="unicode"))
    (C / "batch-097-comparison-characters-reading.txt").write_text(
        "\n".join(compact) + "\n", encoding="utf-8")
    print(json.dumps({"comparisonFamilies": len(ids), "rawComparisonCharacterRecords": len(chars)}))


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
                self.parts.append("\n[ARTICLE " + dict(attrs).get("class", "") + "]\n")
            if self.depth and tag in {"p", "h2", "h3", "br", "section"}:
                self.parts.append("\n")

        def handle_endtag(self, tag):
            if tag == "article" and self.depth:
                self.depth -= 1
                self.parts.append("\n[END ARTICLE]\n")

        def handle_data(self, data):
            if self.depth:
                self.parts.append(data)

    receipts = {}
    for key, url, heading in [
        ("character", "https://kotobank.jp/word/%E5%89%A3-60233", "つるぎ【剣】"),
        ("shinken", "https://kotobank.jp/word/%E7%9C%9F%E5%89%A3-537225", "しん‐けん"),
    ]:
        path = C / "inputs" / f"batch-097-{key}.html"
        raw = path.read_bytes()
        parser = ArticleText()
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                         if line.strip()) + "\n"
        assert heading in text
        archive = S / (PREFIX + key + ".html.gz")
        archive.write_bytes(gzip.compress(raw, mtime=0))
        target = S / (PREFIX + key + "-public-text.txt")
        target.write_text(text, encoding="utf-8")
        receipts[key] = {
            "url": url, "retrievedAt": datetime.now(timezone.utc).isoformat(),
            "sourcePath": str(path), "sourceSha256": sha(raw),
            "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
            "losslessGzip": gzip.decompress(archive.read_bytes()) == raw,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "extractionLimits": "Article-only HTMLParser extraction; links/formatting stripped. Gaiji images not decoded; no historical/phonetic claim accepted. Supplemental dictionary coverage is not permission to append readings to pinned KANJIDIC2.",
        }
    save(S / (PREFIX + "public-source-receipts.json"), receipts)
    print("Actual character and lexical dictionary pages archived losslessly and attributed article text extracted.")


def plan():
    limits = (
        "Source preparation only, not runtime teaching, independent content review, native font/drawing/quiz acceptance "
        "or publication. Published123/1228 and1105 acceptance remainder unchanged. Six earlier-level source placements "
        "remain separate. Font cmap observations are preflight, not glyph acceptance. Physical-phone/general-release "
        "and whole-set acceptance remain outstanding; qualified TESTONLYAndroid1c1b7bf4 is not latest app main."
    )
    next_action = (
        "SAME097 bounded runtime draft from committed source packet only, then normally signed LOCAL UNREVIEWED freeze. "
        "Preserve full rawケン/[つるぎ] and select both, with existing真剣しんけん N3 vocabulary metadata unchanged "
        "and necessary new剣つるぎ with no inferred word level. Three all-mapped pairs/six directions, one existing "
        "direction, one activated baseline pair; navigation-only edits to words真剣 and kanji真. Four proposed direct "
        "word guards require final-label audit. Generate ten strokes from pinned SVG; final Han/font audit. Then TWO "
        "serial blind different-family textual reviews on one frozen snapshot, evidence reconciliation/original-session "
        "confirmations, fresh non-skipped Android, production ContentSync ONCE/native N1-All/reading/drawing/article/"
        "Back/offline/four-font/all-Han/rendered review, actual combined-main acceptance, normal signing/owner "
        "fast-forward/terminal CI/EVERY immutable public ZIP hash/unchanged budgets/verified ownerissue. Do not start098 "
        "or push unreviewed content. Parent19008 retains runner.lock; no child acquire/delete/unlock/readprobe. "
        "Approved control/committed evidence/frozen inputs only; preserve/report/yield actual new denial/signing hang/"
        "uncertain ownership. Preserve every historical process/evidence/permission/OOM/phone limitation."
    )
    membership = {
        "schemaVersion": 1, "batch": "097", "baseCommit": BASE, "membership": [CHAR],
        "sourceRows": [108], "members": [{"kanji": CHAR, "sourceRow": 108}],
        "selectionReason": "Next absent frozen row after published剛. One character only: 122 complete member families, two readings, sword/blade overlap and a reused easier-level article justify the bound. Earlier deferred rows remain pending.",
        "status": "source-prepared-not-drafted", "drafted": [], "reviewClosed": [], "published": [],
        "limits": limits,
    }
    guards = [
        ("刀", "1446420", "Existing sword/katana label overlaps the selected sword sense. Especially double-edged is not an absolute prohibition on broader sword use."),
        ("日本刀", "1464780", "Existing Japanese-sword label overlaps broad sword usage; familiar single-edged form is not an exclusive lexical partition."),
        ("刃", "1369820", "Existing blade/cutting-edge label overlaps the selected blade gloss. Part-versus-whole explanation does not by itself make every English-label pairing safe."),
        ("真剣", "1363650", "Existing primary label is serious/earnest, but its ordinary secondary noun sense is a real sword. Protect the direct pair, not through an exclusion clique."),
    ]
    pairs = [[CHAR, "words/剣.md"], [CHAR, "words/真剣.md"], ["真", "words/真剣.md"]]
    directions = []
    for char, word in pairs:
        directions.extend([
            {"from": f"kanji/{char}.md", "to": word,
             "reason": "Selected reading/common-word navigation for mapped article."},
            {"from": word, "to": f"kanji/{char}.md",
             "reason": "Substantive component introduction; preserve any existing direction."},
        ])
    nav = load(S / (PREFIX + "source-navigation.json"))
    progress = {
        **membership, "freshOriginMainAtPreparation": BASE,
        "sourceReadingOrder": {"onyomi": ["ケン"], "kunyomi": ["つるぎ"]},
        "readingDispositions": [
            {"kanji": CHAR, "kind": "on", "reading": "ケン", "proposedQuizSelection": True,
             "sourceOnly": False, "example": "真剣 しんけん — serious; earnest; also a real sword",
             "entryIds": ["1363650"],
             "qualification": "Reuse actualしんけん article with N3 vocabulary metadata and originalまじめ exclusion unchanged. Full raw真 suppliesシン; Digital Daijisen剣 character heading explicitly lists真剣 underケン, not merely a whole-word kana substring.",
             "evidence": "Frozen KANJIDIC2剣/真, complete JMdict1363650, actual archived Digital Daijisen剣漢字項目 and真剣 entries."},
            {"kanji": CHAR, "kind": "kun", "reading": "つるぎ", "proposedQuizSelection": True,
             "sourceOnly": False, "example": "剣 つるぎ — sword; especially a double-edged blade",
             "entryIds": ["1256750"],
             "qualification": "Necessary standalone support; no existing剣/つるぎ article. Actual dictionary headingつるぎ【剣】 independently establishes the entire single-character reading. Teach sword especially double-edged, not an absolute taxonomy excluding broader sword uses. Do not transferけん-only senses toつるぎ.",
             "evidence": "Frozen KANJIDIC2剣, complete JMdict1256750 sense1 with senses2-4 restricted toけん; actual archived Digital Daijisenつるぎ【剣】 andけん【剣】."},
        ],
        "proposedCuratedProjection": {
            "kanji": CHAR, "quizOnyomi": ["ケン"], "quizKunyomi": ["つるぎ"],
            "onKeys": ["けん"], "kunKeys": ["つるぎ"],
            "limits": "Exact full-list subsets. Compatible curated-reading client required. No runtime offered-key/started-key acceptance claimed.",
        },
        "outsideFrozenReadingDispositions": [
            {"reading": "つるき; name readings; other old dictionary glosses",
             "disposition": "Preserve raw source and historical/public entries as source context. Do not add old pronunciation, nanori or a gloss such asきる to current metadata/questions; no personal-name or historical-reading course."},
            {"reading": "けん for standalone剣",
             "disposition": "Valid on-reading/alternate whole-word pronunciation; mention without changing the new support article's primaryつるぎ identity or claiming every sense is shared."},
        ],
        "proposedSupportMapping": [
            {"kanji": CHAR, "article": "words/真剣.md", "word": "真剣", "primaryReading": "しんけん",
             "entryId": "1363650", "selectedSenses": [1, 2], "newArticle": False,
             "allWrittenKanji": ["真", "剣"], "wordJlpt": 3,
             "disposition": "Existing true lexical identity. Only link剣 at actual component introduction; preserve all metadata, examples, sense qualifications and primary reading."},
            {"kanji": CHAR, "article": "words/剣.md", "word": "剣", "primaryReading": "つるぎ",
             "entryId": "1256750", "selectedSenses": [1], "newArticle": True,
             "allWrittenKanji": ["剣"], "wordJlpt": None,
             "disposition": "Necessary kun support only, not N1 vocabulary delivery. Noun, wago, no compound split and no inferred level. Mention alternateけん without importing its restricted bayonet/swordsmanship/zoological senses."},
        ],
        "proposedReciprocalPairs": pairs, "proposedDirectedLinkPlan": directions,
        "requiredDirectionCount": 6,
        "alreadyExistingRequiredDirections": [{"from": "words/真剣.md", "to": "kanji/真.md"}],
        "activatedBaselinePairs": nav["baselinePairs"],
        "proposedReusedChanges": [
            {"article": "words/真剣.md", "change": "Wrap existing剣 in component explanation with ../kanji/剣.md link; no prose/metadata change."},
            {"article": "kanji/真.md", "change": "Add one Common words bullet linking真剣しんけん serious/earnest (also literal real sword), completing all-mapped真/真剣 pair. Preserve every existing metadata field and passage."},
        ],
        "proposedQuiz": {
            "kanjiTitle": "sword; double-edged blade", "distractors": ["剛", "剖", "則"],
            "labels": ["sturdy; unyielding strength", "dissect; split open", "rule; follow a model"],
            "rationale": "Three existing right-hand刂 comparisons with different left blocks. Quality, dissecting action and rule meanings do not name a sword/blade. Shared cutting association alone is not lexical identity.",
            "unsafeComparisons": ["刀", "刃", "針"],
            "wordTitle": "sword; double-edged blade",
            "proposedDirectExclusions": [
                {"words": ["剣", word], "entryIds": ["1256750", eid], "evidence": reason}
                for word, eid, reason in guards
            ],
            "otherInspectedComparisons": "ナイフ/包丁 name knives, not the selected sword noun. 針 names a needle/pointer; frozen剣 clock-hand gloss is contextualized by短剣/長剣, not established as standaloneつるぎ. No word guard to針 from character-level gloss alone. まじめ's earnest sense is related to真剣's adjective, not a sword; do not extend a clique through真剣.",
            "legacyFallbackDisposition": "刀/刃/針/真/険/験 and all three proposed distractors have three curated distractors already; no third-option repair required. Not certification of all live pools or seeds.",
            "confusableInventory": "docs/confusable-words.md used as candidate navigation; no剣/つるぎ row established. Actual dictionary families/articles, including secondary真剣 noun, determine safeguards.",
        },
        "proposedTeachingConstraints": [
            "structure-unclassified; labelled modern-shape mnemonic only. Describe pointed roof, horizontal line/box-like口 and spreading lower strokes on left beside right刂; do not print rare component㑒 merely because SVG names it.",
            "Canonical radical刀18, visible as刂. SVG phon attributes and gaiji-incomplete字通 are not accepted historical/phonetic proof; no etymology asserted.",
            "つるぎ is a noun for a sword, especially double-edged; broader dictionary sword usage prevents an absolute刀single-edge/剣double-edge partition.",
            "New support example may use ordinary museum/photograph noun contexts with kana and English; original illustrations must not be presented as source quotations.",
            "Single-character noun is wago with primaryつるぎ; standaloneけん is also valid, but JMdict restricts bayonet/swordsmanship/zoology senses toけん.",
            "Use existing真剣しんけん asケン row, retaining N3 word level. Serious/earnest does not generally mean dangerous/severe. Literal real-sword sense remains qualified against practice swords.",
            "Optional recognition剣道けんどう (bamboo-sword martial art) and諸刃の剣もろはのつるぎ (alsoもろはのけん) are full-family verified, not additional articles. Do not impose one pronunciation for all両刃 variants.",
            "Clock-hand gloss has complete短剣たんけん hour-hand and長剣ちょうけん minute-hand context; no claim that standaloneつるぎ is the everyday word for clock hands. Ordinary針はり is distinct whole-word vocabulary.",
            "Keep spelling/readings/register/sense flags separate; Cambridge ateji, search-only剣吞 and product/train/place names do not add practice readings.",
            "Selective kana and English translations; no frequency ranking from priority flags, no inferred word level or unauthorized media.",
        ],
        "proposedHanText": "剣 真 真剣 刀 刂 口 人 一 剛 剖 則 険 験 刃 日本刀 針 短剣 長剣 剣道 諸刃の剣 両刃 片刃 博物館 古い 剣の写真 まじめ 本気",
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 123, "remainingAdditions": 1105,
        "nextAction": next_action, "limits": limits,
    }
    save(S / (PREFIX + "membership.json"), membership)
    save(S / (PREFIX + "progress.json"), progress)
    special = {
        "1048290": "剣橋 is rarely written ateji for Cambridge, usually kana; not a productive per-character reading model.",
        "1256750": "Necessary new剣つるぎ, selected sense1 sword/blade. Keep alternateけん valid, and preserve senses2-4 stagrけん; do not teach bayonet/swordsmanship/stinger asつるぎ senses.",
        "1256770": "Attested剣を抜く permits bothつるぎをぬく andけんをぬく. Not an additional article or requirement to teach an operational weapon procedure.",
        "1256780": "剣客 hasけんかく/けんきゃく; no single-reading claim or extra support required.",
        "1256790": "けん玉/剣玉 kendama;拳玉 rare spelling. Not a literal sword example invented from characters.",
        "1256910": "剣道けんどう recognition context: martial art using bamboo swords, not a requirement for a sharp metal blade.",
        "1256940": "剣呑けんのん risky/dangerous;剣吞/険吞 search-only and険呑 rare. Do not treat risk as the core standaloneつるぎ noun.",
        "1256980": "Rare expression flag retained; no modern-frequency claim from spelling.",
        "1257010": "剣幕 is ateji; alternatives権幕/見幕 also ateji and rare. No compositional sword+curtain etymology.",
        "1344300": "諸刃の剣/両刃の剣 and spelling/reading restrictions retained. りょうば readings tied to両刃の剣; do not generalize by kana substring.",
        "1363650": "Exact existing真剣しんけん, adjective serious/earnest plus noun real sword. Reuse N3 metadata unchanged; primary and literal senses both retained.",
        "1363660": "真剣勝負 has real-sword contest and earnest-game senses; not unrestricted weapon translation of earnest discussion.",
        "1418690": "短剣たんけん has dagger/short sword and hour-hand senses; contextualizes source clock-hand gloss, not standaloneつるぎ recommendation.",
        "1534620": "木剣ぼっけん wooden sword; three other readings have outdated-kana flags. Keep spelling/pronunciation qualifications separate.",
        "1797680": "長剣ちょうけん long sword/minute hand; do not confuse with別familyながだち ancient longsword.",
        "1838950": "剣峻 spelling is irregular-kanji use in steep険峻 family; no new sword sense.",
        "2002620": "長剣ながだち is a different complete family with長太刀; not the minute-hand reading.",
        "2008010": "剣もほろろ rare spelling, usually kana;けんもほろほろ search-only reading. Not a literal sword collocation.",
        "2168350": "Proverb from English; frozen強し spelling is not a new selected剣 reading.",
        "2168670": "Squid family retains re_nokanji for katakanaケンサキイカ, usually-kana flag and all spelling aliases.",
        "2243650": "Imperial sword name has twoあま/あめ readings; two displayed aliases are search-only. No personal-name reading questions.",
        "2243660": "Rare named regalia alternative; absence of a commonness claim retained.",
        "2461700": "Crustacean name usually kana; katakanaケンミジンコ has re_nokanji, not mechanically paired with剣微塵子.",
        "2524830": "剣石けんいし archaic keystone; no extension to modern sword meaning.",
        "2747100": "剣術者 archaic fencer; not selected support.",
        "2773400": "月の剣つきのつるぎ poetical/archaic crescent-moon expression; no general moon reading for剣.",
        "2773430": "Bayonet expression colloquial/archaic with reading-specific spelling restrictions; preserve both scripts.",
        "2773440": "霜剣 archaic; no modern frequency inference.",
        "2773450": "Sword of Damocles permitsつるぎ andけん; no single-pronunciation rule.",
        "2773460": "利剣 formal/literary sharp sword plus Buddhist wisdom sense; do not treat all wisdom words as swords.",
        "2849615": "剣柄たかび archaic whole word; not an independently allocated reading of剣.",
        "2862524": "豪剣/剛剣ごうけん formal/literary great sword; not the robust adjective剛健.",
        "2869882": "双剣 has fiction dual-sword and historical paired-Chinese-sword senses; not ordinary standalone剣 use in every context.",
    }
    entries = ET.parse(S / (PREFIX + "jmdict.xml")).getroot().findall("entry")
    decisions = []
    for entry in entries:
        eid = entry.findtext("ent_seq")
        flags = [node.text for node in entry.findall("sense/misc")]
        name = any("name" in flag for flag in flags)
        default = (
            "Complete named-work/product/organization family retained as unselected context; do not promote proper-name usage to new general readings."
            if name else
            "Complete family inspected and retained as unselected source context. No additional support necessary for the two selected readings. All aliases, restrictions, sense/register/field flags and priorities remain intact; no frequency, unrestricted substitution or per-character allocation claim inferred."
        )
        decisions.append({"entryIds": [eid], "decision": special.get(eid, default)})
    comp_decisions = {
        "1089890": "Knife loanword is not the selected sword noun; no new guard proposed.",
        "1199270": "Dissection and figurative analysis establish action/analysis comparison; not a sword/blade noun.",
        "1218560": "Danger/risk family for visual険 comparison, not sword identity.",
        "1223021": "Rule/regulation supports則 distractor meaning; not a sword.",
        "1251270": "Experience supports験 comparison; not a sword.",
        "1256750": "Same selected family retained in comparison packet; count once in distinct totals.",
        "1257890": "Inspection family retained for comparison with検; current検 card absent, no broken link or extra kanji authoring.",
        "1284120": "Robust/vigorous quality supports剛 distractor, not sword or weapon identity.",
        "1363650": "Existing primary article plus ordinary literal noun motivates direct剣/真剣 guard; count family once.",
        "1364360": "Existingまじめ identity has serious/earnest senses; preserve prior真剣/まじめ guard, do not infer剣/まじめ guard transitively.",
        "1366210": "All eight針 senses retained; ordinary clock-hand use not a new standaloneつるぎ sense.",
        "1369820": "Primaryは blade/edge family supports direct guard despite part/whole explanation; preserve plug-prong secondary sense.",
        "1369830": "Separateやいば lexical family, including rare rice sense; not a reason to reassign currentは article.",
        "1446420": "Existingかたな sword/katana supports guard; restrictedとう scalpel/chisel/money senses do not transfer toかたな.",
        "1464780": "Japanese sword tradition and two readings retained; generic sword overlap supports direct guard.",
        "1515530": "Kitchen knife, separate archaic cooking sense; not a sword noun or direct guard just because sharp.",
        "1522370": "Serious intent/earnestness in reused真剣 note; no current本気 article and no new support necessary.",
    }
    articles = ["kanji/" + c + ".md" for c in "刀刃真剛剖則針険験"]
    articles += ["words/" + word + ".md" for word in [
        "真剣", "刀", "刃", "日本刀", "ナイフ", "針", "包丁", "剛健", "解剖", "規則", "まじめ"]]
    save(S / (PREFIX + "source-evidence.json"), {
        "schemaVersion": 1, "batch": "097", "baseCommit": BASE,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "attribution": "KANJIDIC2/JMdict: James William Breen and EDRDG, CC BY-SA4.0; KanjiVG: Ulrich Apel and contributors, CC BY-SA3.0; Unicode17.0.0. RepositoryNOTICE retains attribution. Supplemental public dictionary material is attributed in exact source receipts, not an unrestricted reproduction license.",
        "authorInspection": {
            "completeMemberFamilies": 122,
            "memberFamilyReturnedRanges": [[1,20],[21,40],[41,60],[61,80],[81,100],[101,122]],
            "memberFamilyReadingPath": str(C / "batch-097-full-family-reading.txt"),
            "comparisonFamilyReturnedRanges": [[1,9],[10,17]],
            "completeComparisonCharacterRanges": [[1,3],[4,6],[7,10]],
            "method": "Each compact line is one complete parsed/reserialized family/character with all restrictions/flags/senses. Specified compact ranges returned without truncation. Semantic-equivalence audit binds compact lines to original frozen entries. Author inspection, not independent review or comprehension certification.",
            "completeExistingArticlesRead": articles,
            "primaryArticleNavigation": "Full word metadata scan found only真剣 containing/declaratively mapping剣; exactしんけん identity and N3 level inspected. No剣/つるぎ article. Current検 kanji and本気 word absent: inventory absence, not permission denial.",
            "publicSourceScope": "Actual Digital Daijisenけん【剣】/つるぎ【剣】/漢字項目 and真剣 inspected. Character heading explicitly assigns真剣 toケン;つるぎ heading and generic sword definition establish useful native reading without exclusive blade taxonomy. Historical, place, train and product entries kept separate; no etymology or historical classification adopted.",
            "toolLimits": "Initial simplified character web fetch truncated later字通 compound navigation; actual full article text archived separately. Character extraction returned1-100/101-115 plus116-123 later, shinken all27 lines. Gaiji absent from extraction; source bytes preserved. One attempted検 article read returned nonexistent path (not permission denial). No reviewer, native/rendered evidence, optional historical-session helper access, runner-lock acquisition or concurrent heavy job.",
        },
        "selectedLexicalDecisions": decisions,
        "comparisonDecisions": [{"entryIds": [eid], "decision": decision} for eid, decision in comp_decisions.items()],
        "phoneticAndOriginDisposition": "No historical or phonetic assertion proposed. structure-unclassified and labelled modern-shape memory aid. SVG phon attributes and gaiji-incomplete字通 are not independent phonetic verification. Rare component㑒 remains SVG source, not proposed learner-visible glyph.",
        "reviewAndAcceptance": "No reviewer, runtime draft, native test or publication claimed. All original097 gates remain pending.",
    })
    print("Explicit source membership, every reading/family disposition and bounded support/link/quiz plan saved.")


def audit():
    from audit_n1_batch import lexical_pair
    from build_manifest import build_manifest
    from fontTools.ttLib import TTFont
    from freeze_n1_sources import metadata_record

    def distinct(pairs):
        result = {}
        for key, value in pairs:
            assert key not in result, key
            result[key] = value
        return result

    for path in S.glob(PREFIX + "*.json"):
        json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=distinct)
    snapshot, inputs, jm, kd = frozen()
    progress = load(S / (PREFIX + "progress.json"))
    evidence_path = S / (PREFIX + "source-evidence.json")
    evidence = load(evidence_path)
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    named = json.loads(inputs["n1-kanji-source-20261102.json"])
    assert named == load(S / "community-list-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[107] == CHAR
    unicode_rows = [line.split(";") for line in inputs["n1-UnicodeData-17.0.0.txt"]
                    .decode("utf-8").splitlines()]
    assert next(r for r in unicode_rows if r[0] == "2F11")[5] == "<compat> 5200"
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    character = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert metadata_record(character, {18: "\u5200"}) == row["metadata"]
    comparison_selection = load(S / (PREFIX + "comparison-selection.json"))
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
    comparison_ids = [i for i, e in families.items()
                      if any(k.text in comparison_selection["exactSpellingsOrReadings"]
                             for k in e.findall("k_ele/keb"))
                      or any(r.text in comparison_selection["exactSpellingsOrReadings"]
                             for r in e.findall("r_ele/reb"))]
    assert len(exact_ids) == 122 and len(comparison_ids) == 17
    for stem, ids in [("", exact_ids), ("comparison-", comparison_ids)]:
        selected_ids = (comparison_selection["entryIds"] if stem
                        else load(S / (PREFIX + "lexical-selection.json"))["entryIds"])
        assert ids == selected_ids
        assert (S / (PREFIX + stem + "jmdict.xml")).read_bytes() == extract(
            inputs["n1-implementation-JMdict_e.gz"],
            snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        compact_path = C / ("batch-097-comparison-reading.txt" if stem else "batch-097-full-family-reading.txt")
        compact = compact_path.read_text(encoding="utf-8").splitlines()
        entries = ET.parse(S / (PREFIX + stem + "jmdict.xml")).getroot().findall("entry")
        assert len(compact) == len(entries) == len(ids)
        assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(compact, entries))
        (S / (PREFIX + stem + "full-family-reading.txt.gz")).write_bytes(
            gzip.compress(compact_path.read_bytes(), mtime=0))
    compact_characters = C / "batch-097-comparison-characters-reading.txt"
    raw_characters = ET.parse(S / (PREFIX + "comparison-kanjidic2.xml")).getroot().findall("character")
    compact = compact_characters.read_text(encoding="utf-8").splitlines()
    assert len(compact) == len(raw_characters) == 10
    assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(compact, raw_characters))
    (S / (PREFIX + "comparison-character-reading.txt.gz")).write_bytes(
        gzip.compress(compact_characters.read_bytes(), mtime=0))
    for field, ids in [("selectedLexicalDecisions", exact_ids), ("comparisonDecisions", comparison_ids)]:
        decisions = [i for group in evidence[field] for i in group["entryIds"]]
        assert len(decisions) == len(set(decisions)) and set(decisions) == set(ids)
    expected = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                for reading in row["metadata"][field]]
    assert [(d["kind"], d["reading"]) for d in progress["readingDispositions"]] == expected
    assert len(expected) == 2
    assert all(d["kanji"] == CHAR and d["qualification"] and d["evidence"]
               and set(d["entryIds"]) <= set(exact_ids) for d in progress["readingDispositions"])
    assert progress["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    selected = [d for d in progress["readingDispositions"] if d["proposedQuizSelection"]]
    assert [d["reading"] for d in selected] == ["ケン", "つるぎ"]
    projection = progress["proposedCuratedProjection"]
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == ["けん"]
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == ["つるぎ"]
    pairs = set()
    for mapping in progress["proposedSupportMapping"]:
        entry = families[mapping["entryId"]]
        assert lexical_pair(entry, mapping["word"], mapping["primaryReading"])
        assert mapping["entryId"] in exact_ids
        assert all(1 <= i <= len(entry.findall("sense")) for i in mapping["selectedSenses"])
        written = list(dict.fromkeys(c for c in mapping["word"] if 0x4E00 <= ord(c) <= 0x9FFF))
        assert mapping["allWrittenKanji"] == written
        path = R / mapping["article"]
        if mapping["newArticle"]:
            assert not path.exists() and mapping["wordJlpt"] is None
        else:
            m = metadata(R, mapping["article"])
            assert (m["word"], m["reading"], m["jlpt"], m["kanji"]) == (
                mapping["word"], mapping["primaryReading"], mapping["wordJlpt"], written)
            assert m["quiz_exclusions"] == ["まじめ"]
        for char in written:
            if char == CHAR or (R / "kanji" / (char + ".md")).exists():
                pairs.add((char, mapping["article"]))
    assert pairs == {tuple(p) for p in progress["proposedReciprocalPairs"]} and len(pairs) == 3
    directions = {(f"kanji/{char}.md", article) for char, article in pairs}
    directions |= {(article, f"kanji/{char}.md") for char, article in pairs}
    assert {(d["from"], d["to"]) for d in progress["proposedDirectedLinkPlan"]} == directions
    assert progress["requiredDirectionCount"] == len(directions) == 6
    existing = set()
    for origin, target in directions:
        path = R / origin
        if not path.exists():
            continue
        relative = ("../" if origin.split("/")[0] != target.split("/")[0] else "") + target
        if origin.split("/")[0] == target.split("/")[0]:
            relative = target.split("/")[-1]
        if f"]({relative})" in path.read_text(encoding="utf-8"):
            existing.add((origin, target))
    assert existing == {(d["from"], d["to"]) for d in progress["alreadyExistingRequiredDirections"]}
    assert existing == {("words/真剣.md", "kanji/真.md")}
    nav = load(S / (PREFIX + "source-navigation.json"))
    assert nav["baselinePairs"] == progress["activatedBaselinePairs"] and len(nav["baselinePairs"]) == 1
    assert [d["article"] for d in nav["candidates"]] == ["words/真剣.md"]
    assert progress["membership"] == load(S / (PREFIX + "membership.json"))["membership"] == [CHAR]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    assert {d["article"] for d in progress["proposedReusedChanges"]} == {"words/真剣.md", "kanji/真.md"}
    quiz = progress["proposedQuiz"]
    assert quiz["labels"] == [metadata(R, f"kanji/{char}.md")["title"] for char in quiz["distractors"]]
    assert len(quiz["distractors"]) == len(set(quiz["distractors"])) == 3
    assert all(metadata(R, path.relative_to(R).as_posix())["title"] != quiz["kanjiTitle"]
               for path in (R / "kanji").glob("*.md"))
    assert all(len(metadata(R, f"kanji/{char}.md")["distractors"]) == 3 for char in "剛剖則刀刃針真険験")
    guards = quiz["proposedDirectExclusions"]
    assert len(guards) == len({tuple(g["words"]) for g in guards}) == 4
    assert all(g["words"][0] == CHAR and (R / "words" / (g["words"][1] + ".md")).exists()
               and set(g["entryIds"]) <= set(exact_ids + comparison_ids) for g in guards)
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8444 and manifest["contentVersion"] == "54645b95fe8e939c"
    assert sha((R / "manifest.json").read_bytes()) == "8a71c3f56462e62bd625332b734abb4eb49948cf259cb13d52cd1c89a68e814f"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert all(line[3:].startswith("docs/n1-sources/batch-097-")
               for line in git("status", "--porcelain", "--untracked-files=all").splitlines())
    baseline = load(S / "baseline-inventory.json")
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    earlier = set("保案派第策結")
    assert len(accepted) == 123 and accepted <= current - original and accepted <= set(named)
    assert len(current) == 1119 and len(set(named) & current) == 133
    assert current & set(named) == (original & set(named)) | accepted | earlier
    assert len(set(named) - current) == 1099
    assert all(metadata(R, f"kanji/{char}.md")["jlpt"] == 2 for char in earlier)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-05263-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    svg_root = ET.fromstring(svg)
    paths = svg_root.findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 10
    assert [p.attrib["id"] for p in paths] == [f"kvg:05263-s{i}" for i in range(1, 11)]
    variant = next(g for g in svg_root.findall(".//{http://www.w3.org/2000/svg}g")
                   if any(k.endswith("}element") and v == "刂" for k, v in g.attrib.items()))
    assert next(v for k, v in variant.attrib.items() if k.endswith("}original")) == "刀"
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "097", "revision": tree["sha"], "input": str(svg_path),
        "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/05263.svg",
        "dictionaryStrokeCount": 10, "sourceStrokePaths": 10, "converted": False,
        "nativeDrawingAccepted": False, "converterNormalizedSha256": converter,
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repositoryNOTICE.",
        "limits": "Pinned SVG inspected and verified; no runtime geometry/native drawing acceptance. SVG rare-component/phon attributes are source context, not accepted historical evidence or learner-visible glyph inventory.",
    }
    save(S / (PREFIX + "stroke-evidence.json"), stroke)
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg)
    han = sorted({char for char in progress["proposedHanText"] if 0x2E80 <= ord(char) <= 0x2FDF
                  or 0x3400 <= ord(char) <= 0x9FFF or 0xF900 <= ord(char) <= 0xFAFF
                  or 0x20000 <= ord(char) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-096-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {char: ord(char) in cmap for char in han},
                      "allProposedMissing": [char for char in han if ord(char) not in cmap]})
    rare = [char for char in han if 0x2E80 <= ord(char) <= 0x2FDF or 0x3400 <= ord(char) <= 0x4DBF
            or 0xF900 <= ord(char) <= 0xFAFF or 0x20000 <= ord(char) <= 0x2FFFF]
    save(S / (PREFIX + "font-preparation.json"), {
        "schemaVersion": 1, "batch": "097", "proposedTextInventory": progress["proposedHanText"],
        "inventoryScope": "Proposed material and exact two reused navigation changes only; final draft may change inventory.",
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "unicodeRadicalCompatibility": "Frozen Unicode17.0.0 U+2F11 maps to ordinary刀 U+5200; no compatibility radical proposed. Visible刂 is ordinary BMPHan, not RareHan routing range. Rare㑒 remains SVG source, not proposed teaching text.",
        "mechanism": "Unchanged RareHan.kt/RareHanTest.kt inspected at actual app paths; three bundled font cmaps inspected.",
        "limits": "Preflight only, not finalruntimeHan/nativelegibility/fallbackface. Fresh four-font/all-Han native rendering and non-skipped RareHan test remain required. Cmap presence/absence is not glyph acceptance.",
    })
    for receipt in load(S / (PREFIX + "public-source-receipts.json")).values():
        raw = Path(receipt["sourcePath"]).read_bytes()
        assert sha(raw) == receipt["sourceSha256"]
        archive = S / receipt["archive"]
        assert sha(archive.read_bytes()) == receipt["archiveSha256"]
        assert gzip.decompress(archive.read_bytes()) == raw
        assert sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"]
    character_text = (S / (PREFIX + "character-public-text.txt")).read_text(encoding="utf-8")
    word_text = (S / (PREFIX + "shinken-public-text.txt")).read_text(encoding="utf-8")
    assert "けん【剣〔劍〕】［漢字項目］" in character_text
    assert "つるぎ【剣】" in character_text and "／懐剣・撃剣・銃剣・真剣" in character_text
    assert "刀剣の総称" in character_text and "しん‐けん【真剣】" in word_text
    assert "本物の刀剣" in word_text and "［形動］" in word_text
    evidence["actualPacketLineCounts"] = {
        name: len((S / (PREFIX + name)).read_text(encoding="utf-8").splitlines())
        for name in ["jmdict.xml", "kanjidic2.xml", "comparison-jmdict.xml", "comparison-kanjidic2.xml",
                     "character-public-text.txt", "shinken-public-text.txt"]}
    evidence["familyCounts"] = {"allExactMemberFamilies": 122, "comparisonFamilies": 17,
                                "distinctCompleteFamilies": len(set(exact_ids + comparison_ids))}
    save(evidence_path, evidence)
    result = {
        "schemaVersion": 1, "execution": 709, "batch": "097", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 108,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "completeLexicalFamilies": 122,
        "completeComparisonFamilies": 17, "distinctCompleteFamilies": len(set(exact_ids + comparison_ids)),
        "allExtractedEntryIdsAccountedFor": True,
        "freshExactDictionaryExtractionsVerified": 2, "rawCharacterRecordsVerified": 11,
        "compactFullFamilyTextSemanticallyEqualToRawXml": True,
        "proposedMetadataReadingDispositionsVerified": 2,
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 1,
        "allMappedReciprocalPairs": 3, "requiredDirectedLinks": 6,
        "alreadyExistingDirections": 1, "activatedBaselinePairs": 1,
        "proposedNewDirectWordGuards": 4,
        "pinnedSvg": stroke, "proposedHanCount": len(han),
        "fontPreparation": PREFIX + "font-preparation.json",
        "mainFontCmapAbsences": fonts[0]["allProposedMissing"],
        "inspectedArticleHashes": {name: sha((R / name).read_bytes())
                                  for name in evidence["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "contentVersion": manifest["contentVersion"], "publishedAdditions": 123,
        "remainingAcceptanceAdditions": 1105, "actuallyAbsentNamedMembers": 1099,
        "separateEarlierLevelSourceMembers": sorted(earlier),
        "separateEarlierPlacementsCountedAsIssue60AcceptedBatches": False,
        "baselinePreservation": "All runtime bytes unchanged from normally signed published base; no metadata/readings/levels/exclusions/geometry changed.",
        "runtimeChanges": 0, "reviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "optionalHistoricalHelpersAccessed": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "limits": progress["limits"],
    }
    save(S / (PREFIX + "preparation-audit.json"), result)
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ["limits", "pinnedSvg", "inspectedArticleHashes"]},
                     ensure_ascii=True, indent=2))


def record():
    checks = {}
    for name in ["source-tests", "validate", "budget", "audit", "manifest", "whitespace"]:
        path = L / f"{name}-709.txt"
        text = path.read_text(encoding="utf-8-sig")
        assert "Traceback" not in text and "FAILED" not in text
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8444' in text
        archive = S / f"batch-097-{name}-709.txt.gz"
        raw = path.read_bytes()
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {"path": str(path), "sha256": sha(raw),
                        "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
                        "losslessGzip": True,
                        "provenance": "Direct redirected stdout/stderr; exit0 explicitly checked by checks-source-709.ps1."}
    helpers = []
    for name, archive_name in [
        ("source-709.py", PREFIX + "source-recipe.py"),
        ("preflight-709.ps1", PREFIX + "preflight-709.ps1.txt"),
        ("checks-source-709.ps1", PREFIX + "checks-source-709.ps1.txt"),
    ]:
        target = S / archive_name
        target.write_bytes((C / name).read_bytes())
        helpers.append({"durableControlPath": str(C / name), "archive": archive_name,
                        "sha256": sha(target.read_bytes())})
    progress = load(S / (PREFIX + "progress.json"))
    save(S / "execution-709.json", {
        "schemaVersion": 1, "execution": 709, "batch": "097", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution709StartingState"],
        "sourceAudit": PREFIX + "preparation-audit.json", "sourcePacket": PREFIX + "progress.json",
        "sourceEvidence": PREFIX + "source-evidence.json", "durableHelpers": helpers,
        "checks": checks, "runtimeChanged": False, "runtimePublished": False,
        "focusedTestsPassed": 43,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 123, "remainingAdditions": 1105,
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
    changed = git("diff", "--name-only", BASE, "HEAD").splitlines()
    assert changed and all(name.startswith("docs/n1-sources/batch-097-") or name == "docs/n1-sources/execution-709.json"
                           for name in changed)
    before = load(L / "progress-before-709.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert (p["checkpoint"], p["batch"]) == (708, "097")
    assert all(p.get(key) == value for key, value in before.items() if key not in allowed)
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == L.name and runner["status"] == "running"
    issue = load(L / "issue-response-709.json")
    body = (C / "execution709-issue.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    assert issue["issue_url"].endswith("/issues/60")
    receipt = {"id": issue["id"], "url": issue["html_url"], "author": "stop-cran",
               "bodySha256": sha(body.encode("utf-8")), "verified": True}
    audit = load(S / (PREFIX + "preparation-audit.json"))
    state = {
        "schemaVersion": 1, "execution": 709, "checkpoint": 709, "batch": "097",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-097-progress.json",
        "sourceAudit": "docs/n1-sources/batch-097-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-709.json",
        "membership": [CHAR], "sourceRow": 108,
        "lexicalFamilies": 122, "comparisonFamilies": 17,
        "distinctCompleteDictionaryFamilies": audit["distinctCompleteFamilies"],
        "completeRawCharacterRecords": 11, "completeExistingArticlesRead": len(audit["inspectedArticleHashes"]),
        "metadataReadings": 2, "proposedOnKeys": ["けん"], "proposedKunKeys": ["つるぎ"],
        "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 1,
        "allMappedReciprocalPairs": 3, "proposedLinkDirections": 6, "alreadyExistingDirections": 1,
        "activatedBaselinePairs": 1, "proposedReusedChanges": 2,
        "pinnedSvgPaths": 10, "geometryConverted": False, "proposedNewDirectWordGuards": 4,
        "proposedHanCount": audit["proposedHanCount"],
        "mainFontCmapAbsences": audit["mainFontCmapAbsences"],
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 123, "remainingAdditions": 1105,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "runtimeHashesUnchanged": 8444, "contentVersion": "54645b95fe8e939c",
        "originalHistoricalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "issueUpdate": receipt["url"],
        "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
    }
    p["execution709CoordinatorCheckpoint"] = state
    p["batch097SourcePreparation"] = state
    p["batch097SourcePreparationIssueReceipt"] = receipt
    p["execution709StartingState"]["status"] = "signed-local-source-preparation-checkpoint-complete"
    p.update(checkpoint=709, status="continue", stage="batch-097-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(key) == value for key, value in before.items() if key not in allowed)
    save(L / "execution-709-final-checkpoint.json", state)
    print(json.dumps(state, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "packet", "comparison", "public", "plan", "audit", "record", "seal"])
    globals()[parser.parse_args().action]()
