"""Prepare one source-bounded N1 batch without changing runtime content."""
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
L = C / "logs" / "8226f3e2-f844-45f6-b574-1273599b0329"
BASE = "4c2416e4c5925e6910b32215412bb1b795f60524"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u525b"
PREFIX = "batch-096-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata, offered_keys
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".700.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (699, "095", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1106
    assert not list(S.glob(PREFIX + "*"))
    role = load(L / "preflight-700.json")
    assert role["liveParentPid"] == 19008 and role["sessionId"] == L.name
    assert role["lockTouched"] is False
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["status"] == "running" and runner["sessionId"] == L.name
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 699
    assert checkpoint["execution699CoordinatorCheckpoint"] == p["execution699CoordinatorCheckpoint"]
    before = L / "progress-before-700.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 700, "batch": "096", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded096 source-preparation checkpoint for frozen row107 only; no runtime draft, reviewer, Android/native, publication,097 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed. Operative contract, complete approved issue and final699 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals content. Android1c1b7bf4 retains productionf9b59a2, NOT latest app main. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution700StartingState"] = state
    p.update(batch="096", stage="batch-096-source-preparation-in-progress",
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
    assert load(C / "progress.json")["batch"] == "096"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 107
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[106] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "096", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+525B in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    (S / (PREFIX + "jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    character_packet(kd, CHAR, "kanjidic2.xml")
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "096", "baseCommit": BASE, "sourceIndexRecord": row,
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
    compact_packet("jmdict.xml", "batch-096-full-family-reading.txt")
    print(json.dumps({"families": len(ids), "candidates": candidates}, ensure_ascii=True, indent=2))


def comparison():
    snapshot, inputs, jm, kd = frozen()
    words = ["剛健", "健", "丈夫", "健康", "元気", "強力", "体力", "力", "活気",
             "もりもり", "生き生き", "活躍", "硬い", "堅い", "固い", "頑丈", "強い",
             "弱い", "柔らかい", "規則", "削除", "解剖", "ぴんぴん"]
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(k.text in words for k in e.findall("k_ele/keb"))
           or any(r.text in words for r in e.findall("r_ele/reb"))]
    save(S / (PREFIX + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "096", "exactSpellingsOrReadings": words, "entryIds": ids,
        "rawCharacterOrder": list("削剖則強硬固力健刀岡柔"),
        "rule": "Complete frozen families with exact listed keb or reb, including alternative lexical readings and restrictions.",
        "limits": "Bounded navigation packet, not exhaustive quiz or linguistic acceptance.",
    })
    (S / (PREFIX + "comparison-jmdict.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids))
    character_packet(kd, "削剖則強硬固力健刀岡柔", "comparison-kanjidic2.xml")
    compact_packet("comparison-jmdict.xml", "batch-096-comparison-reading.txt")
    compact = []
    for entry in ET.parse(S / (PREFIX + "comparison-kanjidic2.xml")).getroot().findall("character"):
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact.append(ET.tostring(entry, encoding="unicode"))
    (C / "batch-096-comparison-characters-reading.txt").write_text(
        "\n".join(compact) + "\n", encoding="utf-8")
    print(json.dumps({"comparisonFamilies": len(ids), "rawComparisonCharacterRecords": 11}))


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
        ("character", "https://kotobank.jp/word/%E5%89%9B-493908", "ゴウ"),
        ("gouken", "https://kotobank.jp/word/%E5%89%9B%E5%81%A5-494996", "ごう‐けん"),
    ]:
        path = C / "inputs" / f"batch-096-{key}.html"
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
    next_action = (
        "SAME096 bounded runtime draft from committed source packet only, then normally signed LOCAL UNREVIEWED freeze. "
        "Preserve full rawゴウ/[] and selectゴウ/[] with necessary new剛健ごうけん; no inferred word level. "
        "Keep健 in word metadata though its card is absent. ONE all-mapped pair/TWO directions/ZERO activated baseline pairs; "
        "eleven proposed direct word safeguards require exact final-label audit. Generate ten strokes from pinned SVG; "
        "final Han/font audit. Then TWO serial blind different-family textual reviews on one frozen snapshot, evidence "
        "reconciliation/original-session confirmations, fresh non-skipped Android, production ContentSync ONCE/native "
        "N1-All/reading/drawing/article/Back/offline/four-font/all-Han/rendered review, actual combined-main acceptance, "
        "normal signing/owner fast-forward/terminal CI/EVERY immutable public ZIP hash/unchanged budgets/verified ownerissue. "
        "Do not start097 or push unreviewed content. Parent19008 retains runner.lock; no child acquire/delete/unlock/readprobe. "
        "Approved control/committed evidence/frozen inputs only; preserve/report/yield actual new denial/signing hang/uncertain ownership."
    )
    limits = (
        "Source preparation only, not runtime teaching, independent content review, native font/drawing/quiz acceptance "
        "or publication. Published122/1228 and1106 acceptance remainder unchanged. Six earlier-level source placements "
        "remain separate. Font cmap observations are preflight, not glyph acceptance. Physical-phone/general-release "
        "and whole-set acceptance remain outstanding; qualified TESTONLYAndroid1c1b7bf4 is not latest app main."
    )
    membership = {
        "schemaVersion": 1, "batch": "096", "baseCommit": BASE, "membership": [CHAR],
        "sourceRows": [107], "members": [{"kanji": CHAR, "sourceRow": 107}],
        "selectionReason": "Next absent frozen row after published剖. One character only; 78 complete member families make a smaller batch appropriate despite the sole on-reading. Earlier deferred rows remain pending.",
        "status": "source-prepared-not-drafted", "drafted": [], "reviewClosed": [], "published": [],
        "limits": limits,
    }
    guards = [
        ("丈夫", "1580480", "Existing sturdy/durable label and robust-constitution sense overlap directly."),
        ("健康", "1256170", "Health/healthy label overlaps the healthy robust sense; not a medical equivalence claim."),
        ("元気", "1260720", "Existing well/energetic label overlaps vigor and health senses."),
        ("強い", "1236070", "Existing strong/powerful label includes physical/mental strength."),
        ("強力", "1236600", "Conservative broad strong/powerful English-label guard; not free Japanese substitution."),
        ("体力", "1409760", "Conservative physical-strength/stamina label guard for robust bodily vigor."),
        ("力", "1554820", "Conservative strength/power label guard; the noun/adjective difference is not shown in every quiz."),
        ("活気", "1208270", "Vigor in existing English label; atmosphere emphasis does not remove all broad-label overlap."),
        ("もりもり", "1012700", "Existing full-of-vigor label and strength-welling sense; Daijisen synonym navigation alone is not unrestricted substitutability."),
        ("生き生き", "1609130", "Conservative energetic/vitality label safeguard, not its distinct vivid-portrayal sense."),
        ("ぴんぴん", "1010960", "Existing full-of-life label and vigorous-well body use overlap; colloquial register does not make every alternative wrong."),
    ]
    progress = {
        **membership, "freshOriginMainAtPreparation": BASE,
        "sourceReadingOrder": {"onyomi": ["ゴウ"], "kunyomi": []},
        "readingDispositions": [{
            "kanji": CHAR, "kind": "on", "reading": "ゴウ", "proposedQuizSelection": True,
            "sourceOnly": False, "example": "剛健 ごうけん — robust; vigorous", "entryIds": ["1284120"],
            "qualification": "Necessary new support; no existing spelling/primary-reading article. Digital Daijisen's actual剛漢字項目 lists剛健 underゴウ; complete frozen lexical family givesごうけん and health/sturdiness/vigor. Full健 record suppliesケン, not an allocation inferred solely from a kana substring.",
            "evidence": "Complete frozen KANJIDIC2剛/健; JMdict1284120; actual Digital Daijisenごう【剛】 andごう‐けん【剛健】 entries archived in this packet.",
        }],
        "proposedCuratedProjection": {
            "kanji": CHAR, "quizOnyomi": ["ゴウ"], "quizKunyomi": [], "onKeys": ["ごう"], "kunKeys": [],
            "limits": "Exact full-list subset; pinned record has no kunyomi. Compatible curated-reading client required. No runtime offered-key/started-key acceptance claimed.",
        },
        "outsideFrozenReadingDispositions": [
            {"reading": "コウ", "evidence": "Digital Daijisen character heading listsコウ; lexical entry says古くはこう.",
             "disposition": "Different source coverage, not an invalid reading. Preserve sole frozenゴウ without appendingコウ, reordering source metadata or creating another question."},
            {"reading": "かたい・つよい; personal-name readings",
             "evidence": "字通字訓 and source nanori; JMdict剛い alias is search-only.",
             "disposition": "Do not turn descriptive native glosses, search-only spelling or nanori into new kunyomi/questions. Name-use course remains out of scope."},
        ],
        "proposedSupportMapping": [{
            "kanji": CHAR, "article": "words/剛健.md", "word": "剛健", "primaryReading": "ごうけん",
            "entryId": "1284120", "selectedSenses": [1], "newArticle": True,
            "allWrittenKanji": ["剛", "健"], "wordJlpt": None,
            "disposition": "Necessary support only, not N1 vocabulary delivery. Noun/na-adjective; explain robust body and spirit, traditional masculine association without imposing a male-only grammar restriction. Omit jlpt absent independently adopted vocabulary evidence.",
        }],
        "proposedReciprocalPairs": [[CHAR, "words/剛健.md"]],
        "proposedDirectedLinkPlan": [
            {"from": "kanji/剛.md", "to": "words/剛健.md", "reason": "Selectedゴウ row and useful common-word navigation."},
            {"from": "words/剛健.md", "to": "kanji/剛.md", "reason": "Substantive component introduction."},
        ],
        "requiredDirectionCount": 2, "alreadyExistingRequiredDirections": [], "activatedBaselinePairs": [],
        "proposedReusedChanges": [],
        "missingComponentDisposition": "健 has no card: preserve it in word metadata and explainケン/healthy from full raw record, but do not add a broken link or broaden096 into another kanji.",
        "proposedQuiz": {
            "kanjiTitle": "sturdy; unyielding strength", "distractors": ["削", "剖", "則"],
            "labels": ["shave; sharpen; pare", "dissect; split open", "rule; follow a model"],
            "rationale": "Three existing right-hand刂 visual comparisons with different left blocks. Their ordinary displayed meanings are not strength, sturdiness or rigidity. Shared indexing radical is not shared lexical meaning.",
            "unsafeComparisons": ["強", "力", "硬", "固"],
            "wordTitle": "robust; vigorous",
            "proposedDirectExclusions": [
                {"words": ["剛健", word], "entryIds": ["1284120", eid], "evidence": reason}
                for word, eid, reason in guards
            ],
            "otherInspectedComparisons": "活躍 describes activity/contribution, not robustness itself; no guard proposed. 硬い/堅い/固い describe hardness or firmness, not necessarily a robust body or spirit; no automatic clique. 頑丈 is a dictionary synonym candidate but has no article, so do not add a missing-ID guard.",
            "legacyFallbackDisposition": "Relevant existing強/力/硬/固/柔 and three proposed distractor cards already have three curated distractors. No coupled legacy fallback edit proposed; not certification of every live pool.",
            "confusableInventory": "docs/confusable-words.md used as navigation (CW035 hardness spellings; vitality comparisons); no剛健 row. Direct candidate articles/families inspected independently of inventory completeness.",
        },
        "proposedTeachingConstraints": [
            "Use structure-unclassified and a labelled modern-shape mnemonic: 岡-shaped left block with enclosing冂 and山, beside right-hand刂. Canonical radical刀18 remains; no historical/phonetic assertion from SVG phon attribute.",
            "Explain strong, sturdy or unyielding quality, physically or in character; 剛 is not an all-purpose standalone replacement for everyday強いつよい.",
            "剛健 is a noun/na-adjective: 剛健な + noun, 剛健です as polite predicate. Not an i-adjective or automatically aする verb.",
            "Attested short phrase勤勉で剛健な気風 (きんべんでごうけんなきふう), a hardworking and robust spirit, may illustrate attachment with dictionary attribution. This is phrase-level evidence, not a quotation invented to manufacture a distinction.",
            "質実剛健しつじつごうけん: plain and sincere, with fortitude/vigor, recognition context from complete1320700. Do not equate every vigorous activity or cheerful mood with剛健.",
            "Mention traditional masculine association documented by both Japanese dictionaries, without presenting it as male-only applicability or a judgment about people.",
            "剛性ごうせい rigidity and剛毛ごうもう stiff/coarse hair are optional recognition examples verified in full families; no extra articles needed for soleゴウ.",
            "Do not teach search-only剛い as normalつよい spelling. Preserve剛力's spelling-restricted carrier-guide sense as強力-only; do not silently relabel existingきょうりょく article.",
            "Selective kana/English translations; no source-frequency ranking from priorities, no invented origin, no inferred word level."
        ],
        "proposedHanText": "剛 岡 冂 山 刀 刂 削 剖 則 強 力 硬 固 柔 健 剛健 ごうけん 剛性 ごうせい 剛毛 ごうもう 質実剛健 しつじつごうけん 勤勉で剛健な気風 丈夫 健康 元気 強い 強力 体力 活気 生き生き",
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 122, "remainingAdditions": 1106,
        "nextAction": next_action, "limits": limits,
    }
    save(S / (PREFIX + "membership.json"), membership)
    save(S / (PREFIX + "progress.json"), progress)
    entries = ET.parse(S / (PREFIX + "jmdict.xml")).getroot().findall("entry")
    special = {
        "1284120": "Necessary new剛健 support; all sense1 health/vigor/sturdiness context; no inferred word level.",
        "1320700": "質実剛健 recognition phrase; full meaning includes unaffected/sincere as well as fortitude/vigor. No extra article necessary.",
        "1284130": "剛性ごうせい rigidity/stiffness recognition; technical context, not merely every English strength.",
        "1284160": "剛毛ごうもう coarse/stiff hair recognition; no claim it means vigorous health.",
        "1236070": "剛い is search-only in complete強い family; do not teach as normal spelling, change existingつよい identity or add kunyomi.",
        "1284170": "剛力ごうりき shares herculean-strength sense, but mountain carrier-guide sense is restricted to強力. Existing強力きょうりょく is a distinct family.",
        "1284050": "剛の者 aliases豪の者/強の者; こうのもの reading is outdated. Not another selected metadata reading.",
        "1284150": "剛直 has separate slang/vulgar sense2; no need to teach it as a new support or use it to imply all uprightness words are slang.",
        "1593510": "剛情 is rare spelling of強情; separate spelling flag from pronunciation. No new support.",
        "1608600": "強剛 is rare spelling of強豪; retain flags and actual whole-word reading.",
        "2574750": "剛情張 rare spelling and剛情っ張り search-only; preserve distinct flags, not invented everyday forms.",
        "2165450": "金剛鸚哥 rare spelling/usually kana; コンゴウインコ has re_nokanji. Do not pair kana-only reading mechanically to kanji.",
        "2774380": "金剛河豚 usually kana; コンゴウフグ has re_nokanji; no new animal article.",
        "2788520": "金剛穴子 usually kana; コンゴウアナゴ has re_nokanji; no new animal article.",
        "2859133": "紅金剛鸚哥 usually kana; ベニコンゴウインコ has re_nokanji; no new animal article.",
        "1933610": "金剛づえ is search-only alias; preserve杖 readingsづえ/じょう without inferring metadata from substrings.",
        "2153650": "堅剛 explicitly rare; no rarity claim inferred from missing priorities elsewhere.",
        "2228730": "金剛桜 explicitly rare Japanese bird cherry; not a generic cherry synonym or new support.",
        "2862524": "剛剣/豪剣 formal/literary great sword; ごうけん homophone is not剛健 lexical identity.",
        "5292765": "剛柔流 is organization name, not generic softness/strength adjective or a personal-name reading.",
        "2080860": "Standalone剛/豪ごう strength/toughness; not a nativeつよい adjective. No extra support needed.",
        "2637400": "柔よく剛を制す is a proverb; whole construction and fixed meaning are not a free replacement rule for every soft/strong pair.",
    }
    member_decisions = [{
        "entryIds": [e.findtext("ent_seq")],
        "decision": special.get(e.findtext("ent_seq"),
            "Complete family inspected and retained as unselected source context. No additional support article needed for soleゴウ. All aliases, reading/sense restrictions, field/register flags and priorities remain source evidence, not claims of frequency or permission to teach every specialized/religious/idiomatic use."),
    } for e in entries]
    comparison_groups = [
        (["1010960", "1012700", "1208270", "1256170", "1260720", "1409760", "1554820",
          "1580480", "1609130", "1236070", "1236600"], "Actual primary article identities and broad health/robustness/vigor/strength labels support the eleven proposed direct safeguards. Noun/adverb/register differences do not by themselves remove English-label ambiguity; no unrestricted substitution asserted."),
        (["1208450"], "Energetic activity is not a robust state; separate obsolete walking sense retained. No direct guard proposed."),
        (["1217690"], "頑丈 lexical robust/sturdy overlap; no current article, so no missing-ID guard. Outdated岩乗 spelling is not new teaching."),
        (["1223021", "1298120", "1199270"], "Actual rule/deletion/dissection example families support visual-distractor meaning inspection; not strength synonyms."),
        (["1257110"], "All eight hardness-family senses and spelling restrictions retained. These spellings are not fixed exclusive compartments; no new word guard just from shared broad character gloss."),
        (["1284120"], "Exact selected new support retained in comparison packet too; counted once in distinct-family totals."),
        (["1284170"], "Separateごうりき identity, carrier-guide restricted to強力; do not transfer to existingきょうりょく article."),
        (["1324520", "1605630"], "Weak/soft comparisons, not universal antonyms for all robust/rigid uses; retain search-only alias柔かい and all nonphysical senses."),
        (["1554830", "1554840", "1580485", "2087680"], "Same-spelling distinct primary lexical readings: 力りき/りょく, 丈夫じょうふ/ますらお and強いこわい. Respect restrictions/dialect labels; do not replace existing primary articles."),
    ]
    articles = ["kanji/" + c + ".md" for c in "削剖則強硬固力柔"]
    articles += ["words/" + w + ".md" for w in [
        "丈夫", "健康", "元気", "強い", "強力", "体力", "力", "活気", "もりもり",
        "生き生き", "活躍", "硬い", "堅い", "固い", "ぴんぴん", "弱い", "柔らかい"]]
    save(S / (PREFIX + "source-evidence.json"), {
        "schemaVersion": 1, "batch": "096", "baseCommit": BASE,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "attribution": "KANJIDIC2/JMdict: James William Breen and EDRDG, CC BY-SA4.0; KanjiVG: Ulrich Apel and contributors, CC BY-SA3.0; Unicode17.0.0. RepositoryNOTICE retains attribution. Supplemental public dictionary material is attributed in exact source receipts, not an unrestricted reproduction license.",
        "authorInspection": {
            "completeMemberFamilies": 78, "memberFamilyReturnedRanges": [[1,20],[21,40],[41,60],[61,78]],
            "memberFamilyReadingPath": str(C / "batch-096-full-family-reading.txt"),
            "comparisonFamilyReturnedRanges": "Original24 compact families returned completely in ranges1-12/13-24; supplemental complete1010960 returned separately after addingぴんぴん. Final packet25 checked mechanically against frozen originals.",
            "completeComparisonCharacterRanges": [[1,4],[5,8],[9,11]],
            "method": "Each compact line is one complete parsed/reserialized family/character with all restrictions/flags/senses. All specified ranges returned without truncation. Semantic-equivalence audit binds compact lines to original frozen entries. Author inspection, not independent review or comprehension certification.",
            "completeExistingArticlesRead": articles,
            "primaryArticleNavigation": "Full word metadata scan found zero articles whose written spelling or declared kanji contains剛. No剛健/ごうけん article. 健 and岡 kanji cards, 頑丈 word article absent; absence is inventory, not a permission denial.",
            "publicSourceScope": "Actual Digital Daijisen剛 character heading explicitly lists剛健 underゴウ and separatelyコウ. Simplified剛健 fetch omitted Digital Daijisen; exact curl HTML/article extraction includes its actual heading, masculine association, 心身が強くたくましい and attested勤勉で剛健な気風. Complete actual character/article extractions returned. No historical reconstruction adopted from gaiji-incomplete字通.",
            "toolLimits": "Character webfetch truncated only later historical compound navigation; actual full article extraction returned all52 lines in requested range1-55. All27 gouken extraction lines returned. No fresh native/rendered evidence, independent upstream reviewer lookup, actual permission denial, optional historical-session helper access, runner-lock acquisition or concurrent heavy job.",
        },
        "selectedLexicalDecisions": member_decisions,
        "comparisonDecisions": [{"entryIds": ids, "decision": reason} for ids, reason in comparison_groups],
        "phoneticAndOriginDisposition": "No historical or phonetic assertion proposed. structure-unclassified and labelled modern-shape memory aid. SVG phon attributes and gaiji-incomplete字通 are not independent phonetic verification.",
        "reviewAndAcceptance": "No reviewer, runtime draft, native test or publication claimed. All original096 gates remain pending.",
    })
    print("Explicit membership, every source reading/family disposition, support/link/quiz plan and author-inspection limits saved.")


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
    assert len(named) == len(set(named)) == 1232 and named[106] == CHAR
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
    assert len(exact_ids) == 78 and len(comparison_ids) == 25
    for stem, ids in [("", exact_ids), ("comparison-", comparison_ids)]:
        selected_ids = (comparison_selection["entryIds"] if stem
                        else load(S / (PREFIX + "lexical-selection.json"))["entryIds"])
        assert ids == selected_ids
        assert (S / (PREFIX + stem + "jmdict.xml")).read_bytes() == extract(
            inputs["n1-implementation-JMdict_e.gz"],
            snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        compact_path = C / ("batch-096-comparison-reading.txt" if stem else "batch-096-full-family-reading.txt")
        compact = compact_path.read_text(encoding="utf-8").splitlines()
        entries = ET.parse(S / (PREFIX + stem + "jmdict.xml")).getroot().findall("entry")
        assert len(compact) == len(entries) == len(ids)
        assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(compact, entries))
        (S / (PREFIX + stem + "full-family-reading.txt.gz")).write_bytes(
            gzip.compress(compact_path.read_bytes(), mtime=0))
    compact_characters = C / "batch-096-comparison-characters-reading.txt"
    raw_characters = ET.parse(S / (PREFIX + "comparison-kanjidic2.xml")).getroot().findall("character")
    assert all(canonical(ET.fromstring(a)) == canonical(b)
               for a, b in zip(compact_characters.read_text(encoding="utf-8").splitlines(), raw_characters))
    assert len(compact_characters.read_text(encoding="utf-8").splitlines()) == len(raw_characters) == 11
    (S / (PREFIX + "comparison-character-reading.txt.gz")).write_bytes(
        gzip.compress(compact_characters.read_bytes(), mtime=0))
    for field, ids in [("selectedLexicalDecisions", exact_ids), ("comparisonDecisions", comparison_ids)]:
        decisions = [i for group in evidence[field] for i in group["entryIds"]]
        assert len(decisions) == len(set(decisions)) and set(decisions) == set(ids)
    expected = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                for reading in row["metadata"][field]]
    assert [(d["kind"], d["reading"]) for d in progress["readingDispositions"]] == expected
    assert len(expected) == 1
    assert all(d["kanji"] == CHAR and d["qualification"] and d["evidence"]
               and set(d["entryIds"]) <= set(exact_ids) for d in progress["readingDispositions"])
    assert progress["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    selected = [d for d in progress["readingDispositions"] if d["proposedQuizSelection"]]
    assert [d["reading"] for d in selected] == ["ゴウ"]
    projection = progress["proposedCuratedProjection"]
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == ["ごう"]
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == []
    pairs = set()
    for mapping in progress["proposedSupportMapping"]:
        entry = families[mapping["entryId"]]
        assert lexical_pair(entry, mapping["word"], mapping["primaryReading"])
        assert mapping["entryId"] in exact_ids and mapping["newArticle"] is True
        assert not (R / mapping["article"]).exists()
        assert mapping["wordJlpt"] is None
        assert all(1 <= i <= len(entry.findall("sense")) for i in mapping["selectedSenses"])
        written = list(dict.fromkeys(c for c in mapping["word"] if 0x4E00 <= ord(c) <= 0x9FFF))
        assert mapping["allWrittenKanji"] == written == ["剛", "健"]
        for char in written:
            if char == CHAR or (R / "kanji" / (char + ".md")).exists():
                pairs.add((char, mapping["article"]))
    assert not (R / "kanji" / "健.md").exists()
    assert pairs == {tuple(p) for p in progress["proposedReciprocalPairs"]} and len(pairs) == 1
    directions = {(f"kanji/{char}.md", article) for char, article in pairs}
    directions |= {(article, f"kanji/{char}.md") for char, article in pairs}
    assert {(d["from"], d["to"]) for d in progress["proposedDirectedLinkPlan"]} == directions
    assert progress["requiredDirectionCount"] == len(directions) == 2
    assert progress["alreadyExistingRequiredDirections"] == []
    nav = load(S / (PREFIX + "source-navigation.json"))
    assert nav["baselinePairs"] == progress["activatedBaselinePairs"] == []
    assert nav["candidates"] == []
    assert progress["membership"] == load(S / (PREFIX + "membership.json"))["membership"] == [CHAR]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    assert progress["proposedReusedChanges"] == []
    quiz = progress["proposedQuiz"]
    assert quiz["labels"] == [metadata(R, f"kanji/{char}.md")["title"] for char in quiz["distractors"]]
    assert len(quiz["distractors"]) == len(set(quiz["distractors"])) == 3
    assert all(metadata(R, path.relative_to(R).as_posix())["title"] != quiz["kanjiTitle"]
               for path in (R / "kanji").glob("*.md"))
    assert all(len(metadata(R, f"kanji/{char}.md")["distractors"]) == 3 for char in "削剖則強硬固力柔")
    guards = quiz["proposedDirectExclusions"]
    assert len(guards) == len({tuple(g["words"]) for g in guards}) == 11
    assert all(g["words"][0] == "剛健" and (R / "words" / (g["words"][1] + ".md")).exists()
               and set(g["entryIds"]) <= set(exact_ids + comparison_ids) for g in guards)
    assert not (R / "words" / "頑丈.md").exists()
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8441 and manifest["contentVersion"] == "3eebfff0fdad5e28"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    baseline = load(S / "baseline-inventory.json")
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    earlier = set("保案派第策結")
    assert len(accepted) == 122 and accepted <= current - original and accepted <= set(named)
    assert len(current) == 1118 and len(set(named) & current) == 132
    assert current & set(named) == (original & set(named)) | accepted | earlier
    assert len(set(named) - current) == 1100
    assert all(metadata(R, f"kanji/{char}.md")["jlpt"] == 2 for char in earlier)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-0525b-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    svg_root = ET.fromstring(svg)
    paths = svg_root.findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 10
    assert [p.attrib["id"] for p in paths] == [f"kvg:0525b-s{i}" for i in range(1, 11)]
    variant = next(g for g in svg_root.findall(".//{http://www.w3.org/2000/svg}g")
                   if any(k.endswith("}element") and v == "刂" for k, v in g.attrib.items()))
    assert next(v for k, v in variant.attrib.items() if k.endswith("}original")) == "刀"
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "096", "revision": tree["sha"], "input": str(svg_path),
        "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/0525b.svg",
        "dictionaryStrokeCount": 10, "sourceStrokePaths": 10, "converted": False,
        "nativeDrawingAccepted": False, "converterNormalizedSha256": converter,
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repositoryNOTICE.",
        "limits": "Pinned SVG inspected and verified; no runtime geometry/native drawing acceptance. SVG phon attributes are not accepted historical evidence.",
    }
    save(S / (PREFIX + "stroke-evidence.json"), stroke)
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg)
    han = sorted({char for char in progress["proposedHanText"] if 0x2E80 <= ord(char) <= 0x2FDF
                  or 0x3400 <= ord(char) <= 0x9FFF or 0xF900 <= ord(char) <= 0xFAFF
                  or 0x20000 <= ord(char) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-095-font-preparation.json")["fonts"]:
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
        "schemaVersion": 1, "batch": "096", "proposedTextInventory": progress["proposedHanText"],
        "inventoryScope": "Proposed material only; no reused teaching change. Final draft may change inventory.",
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "unicodeRadicalCompatibility": "Frozen Unicode17.0.0 U+2F11 maps to ordinary刀 U+5200; no compatibility radical proposed. Visible岡/冂/山/刂 are ordinary BMPHan, not RareHan routing ranges.",
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
    word_text = (S / (PREFIX + "gouken-public-text.txt")).read_text(encoding="utf-8")
    assert "ごう【剛】［漢字項目］" in character_text and "剛健" in character_text
    assert "ごう‐けん" in word_text and "勤勉で剛健な気風" in word_text and "男性的" in word_text
    evidence["actualPacketLineCounts"] = {
        name: len((S / (PREFIX + name)).read_text(encoding="utf-8").splitlines())
        for name in ["jmdict.xml", "kanjidic2.xml", "comparison-jmdict.xml", "comparison-kanjidic2.xml",
                     "character-public-text.txt", "gouken-public-text.txt"]}
    evidence["familyCounts"] = {"allExactMemberFamilies": 78, "comparisonFamilies": 25,
                                "distinctCompleteFamilies": len(set(exact_ids + comparison_ids))}
    save(evidence_path, evidence)
    result = {
        "schemaVersion": 1, "execution": 700, "batch": "096", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 107,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True, "completeLexicalFamilies": 78,
        "completeComparisonFamilies": 25, "distinctCompleteFamilies": len(set(exact_ids + comparison_ids)),
        "allExtractedEntryIdsAccountedFor": True,
        "freshExactDictionaryExtractionsVerified": 2, "rawCharacterRecordsVerified": 12,
        "compactFullFamilyTextSemanticallyEqualToRawXml": True,
        "proposedMetadataReadingDispositionsVerified": 1,
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 0,
        "allMappedReciprocalPairs": 1, "requiredDirectedLinks": 2,
        "alreadyExistingDirections": 0, "activatedBaselinePairs": 0,
        "proposedNewDirectWordGuards": 11,
        "pinnedSvg": stroke, "proposedHanCount": len(han),
        "fontPreparation": PREFIX + "font-preparation.json",
        "mainFontCmapAbsences": fonts[0]["allProposedMissing"],
        "inspectedArticleHashes": {name: sha((R / name).read_bytes())
                                  for name in evidence["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "contentVersion": manifest["contentVersion"], "publishedAdditions": 122,
        "remainingAcceptanceAdditions": 1106, "actuallyAbsentNamedMembers": 1100,
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
        path = L / f"{name}-700.txt"
        text = path.read_text(encoding="utf-8-sig")
        assert "Traceback" not in text and "FAILED" not in text
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8441' in text
        archive = S / f"batch-096-{name}-700.txt.gz"
        raw = path.read_bytes()
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {"path": str(path), "sha256": sha(raw),
                        "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
                        "losslessGzip": True,
                        "provenance": "Direct redirected stdout/stderr; exit0 explicitly checked by checks-source-700.ps1."}
    helpers = []
    for name, archive_name in [
        ("source-700.py", PREFIX + "source-recipe.py"),
        ("preflight-700.ps1", PREFIX + "preflight-700.ps1.txt"),
        ("checks-source-700.ps1", PREFIX + "checks-source-700.ps1.txt"),
    ]:
        target = S / archive_name
        target.write_bytes((C / name).read_bytes())
        helpers.append({"durableControlPath": str(C / name), "archive": archive_name,
                        "sha256": sha(target.read_bytes())})
    progress = load(S / (PREFIX + "progress.json"))
    save(S / "execution-700.json", {
        "schemaVersion": 1, "execution": 700, "batch": "096", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution700StartingState"],
        "sourceAudit": PREFIX + "preparation-audit.json", "sourcePacket": PREFIX + "progress.json",
        "sourceEvidence": PREFIX + "source-evidence.json", "durableHelpers": helpers,
        "checks": checks, "runtimeChanged": False, "runtimePublished": False,
        "focusedTestsPassed": 43,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 122, "remainingAdditions": 1106,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": progress["nextAction"], "limits": progress["limits"],
    })
    print("Source evidence/checks and durable helpers archived; normal local signing next, no push.")


def seal():
    head = git("rev-parse", "HEAD")
    clean(R, head)
    clean(A, APP)
    assert head != BASE and git("rev-parse", "origin/main") == BASE
    assert git("rev-parse", "HEAD^") == BASE
    assert not git("diff", BASE, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    changed = git("diff", "--name-only", BASE, "HEAD").splitlines()
    assert changed and all(name.startswith("docs/n1-sources/batch-096-") or name == "docs/n1-sources/execution-700.json"
                           for name in changed)
    before = load(L / "progress-before-700.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert (p["checkpoint"], p["batch"]) == (699, "096")
    assert all(p.get(key) == value for key, value in before.items() if key not in allowed)
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == L.name and runner["status"] == "running"
    issue = load(L / "issue-response-700.json")
    body = (C / "execution700-issue.txt").read_text(encoding="utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body
    assert issue["issue_url"].endswith("/issues/60")
    receipt = {"id": issue["id"], "url": issue["html_url"], "author": "stop-cran",
               "bodySha256": sha(body.encode("utf-8")), "verified": True}
    source_audit = load(S / (PREFIX + "preparation-audit.json"))
    state = {
        "schemaVersion": 1, "execution": 700, "checkpoint": 700, "batch": "096",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-096-progress.json",
        "sourceAudit": "docs/n1-sources/batch-096-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-700.json",
        "membership": [CHAR], "sourceRow": 107,
        "lexicalFamilies": 78, "comparisonFamilies": 25,
        "distinctCompleteDictionaryFamilies": source_audit["distinctCompleteFamilies"],
        "completeRawCharacterRecords": 12, "completeExistingArticlesRead": 25,
        "metadataReadings": 1, "proposedOnKeys": ["ごう"], "proposedKunKeys": [],
        "proposedNewSupportArticles": 1, "proposedReusedSupportArticles": 0,
        "allMappedReciprocalPairs": 1, "proposedLinkDirections": 2, "activatedBaselinePairs": 0,
        "pinnedSvgPaths": 10, "geometryConverted": False, "proposedNewDirectWordGuards": 11,
        "proposedHanCount": source_audit["proposedHanCount"],
        "mainFontCmapAbsences": source_audit["mainFontCmapAbsences"],
        "dedicatedWorktreesClean": True, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 122, "remainingAdditions": 1106,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "runtimeHashesUnchanged": 8441, "originalHistoricalRootKeysCompared": len(before),
        "allOriginalHistoricalValuesPreserved": True,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "issueUpdate": receipt["url"],
        "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": load(S / (PREFIX + "progress.json"))["nextAction"],
    }
    p["execution700CoordinatorCheckpoint"] = state
    p["batch096SourcePreparation"] = state
    p["batch096SourcePreparationIssueReceipt"] = receipt
    p["execution700StartingState"]["status"] = "signed-local-source-preparation-checkpoint-complete"
    p.update(checkpoint=700, status="continue", stage="batch-096-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(key) == value for key, value in before.items() if key not in allowed)
    save(L / "execution-700-final-checkpoint.json", state)
    print(json.dumps(state, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "packet", "comparison", "public", "plan", "audit", "record", "seal"])
    globals()[parser.parse_args().action]()
