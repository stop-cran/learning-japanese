"""Bounded source completion; never writes learner-visible content."""
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
from html.parser import HTMLParser
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "2fe17ac2-9fd1-4657-8231-22e9510a84b9"
HEAD = "c2abec23b8feeb639b0773bd06b96022cd8ddda8"
MAIN = "047c2cef6b6a48b1738f2c5957de01be481c63e1"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
NEXT = (
    "SAME105 ONE bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; "
    "no reviewer/Android/native/publication/106 in that draft checkpoint. Source-complete row116勁 "
    "is preserved in docs/n1-sources/batch-105-source-completion-plan.json and execution-808.json. "
    "Nine member+28comparison families (36distinct), nine full raw characters,49actual full article "
    "bodies incl11legacy two-choice fallbacks, four actual public dictionary blocks retained. "
    "Preserve exact full [ケイ]/[つよ.い] source order; select[ケイ]/[] keyけい with own linked "
    "雄勁ゆうけい example. 勁い remains explicitly search-only recognition, not ordinary spelling, "
    "duplicate article or quiz question; 強い/N5/つよい stays unchanged and its navigation link "
    "is not allocation evidence. ONE necessary NEW words/雄勁.md/no inferred vocabularylevel, "
    "noun+na-adjective/style vigor, attested 雄勁な筆跡ゆうけいなひっせき; explain な, no generic "
    "strong substitution, automaticする or absolute art-only rule. 雄 plain component/fullwordmetadata; "
    "full raw+actual character ユウ/strength evidence retained, no out-of-batchcard/brokenlink. "
    "Proposed kanjititle strong;taut, wrongN1功劾剖, FOURdirectkanjiguards強剛力勢; "
    "wordtitle vigorous style(art;prose), SIXdirectwordguards強い強力力強い剛健力勢い; "
    "direct/symmetric/NONTRANSITIVE, not unproved synonym cliques. Exact allmappedONEpair/TWOdirections, "
    "ZEROactivatedbaselinepairs/ZERObaselineedits. Actual legacy11fallbacks inspected, not assumed "
    "threechoices or rewritten. Modernshape巠+力 mnemonicNOTetymology, structure-unclassified/grade9, "
    "canonical力19 onright, no phonetic claim. Convert retained pinned9pathSVG ONLY through unchanged "
    "pinnedconverter,16points/path, no handgeometry. Proposed22Han: 刂/勁/巠 absent allTHREEbundledcmaps, "
    "NOTglyphfailure; final actualHan+fresh nativeALLfourfont/defaultfallback/readability remainMANDATORY. "
    "After later freeze every original TWOserialblind differentfamilies/same snapshot/serialinternaltools/"
    "originalsessionconfirmations/non-skipped qualifiedAndroidbf30cdead HOST+finite semantic defaultN1/"
    "All/custom/productionContentSyncONCE/nativeN1/All/meaning/curatedreading/drawing/article/Back/offline/"
    "rendered acceptance remains. Then combinedcurrentmain/fullPython/vocabulary/baseline-membership-links/"
    "manifest/perfilemedia-safepaths/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/"
    "normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/verifiedownerissue. "
    "Verify whollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/exactsession. Parent13320 "
    "ownsrunner.lock; no childacquire/readprobe/delete/unlock. Approvedcontrol/committedsource/frozeninputs "
    "only, not optional historicalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. Published131/1228,1097remaining unchanged;1127kanji5078words136N1labels, "
    "129necessarysupportsNOTN1vocabulary. Six separatelyplaced保案派第策結retainN2/noacceptedcredit/"
    "duplicate/relevel. CompatibleAndroid#125+#132 required;oldclientsignore;qualifiedsignedbf30cdead "
    "guard+schemaonlyNOTlatestmain. Original806/104 finite192optionsets/live-default/native/rendered "
    "acceptance and all original source/review/readdepth/process/image/rendition/ANR/routing/permission/"
    "OOM/pending limits preserved, not retroaccepted; historical806/807nextActions intact. No forced "
    "withdrawal/modelvote/newguard from unproved hypotheses. Physicalphone/generalrelease/whole-set "
    "outstanding;projectincomplete. No106/unreviewedpush/authoragents/concurrentheavywork/secondrunner/"
    "signingretry/guardincrease."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256 as manifest_sha256
from extract_n1_jmdict import extract

sys.stdout.reconfigure(encoding="utf-8")


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def save(p, v):
    t = p.with_suffix(p.suffix + ".808.tmp")
    assert not t.exists(), t
    t.write_text(json.dumps(v, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(t) == v
    t.replace(p)


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=root)


def role():
    runner = load(C / "runner.json")
    assert runner["pid"] == 13320 and runner["status"] == "running"
    assert runner["sessionId"] == L.name
    script = r"""
$ErrorActionPreference='Stop'
$id=$PID; $chain=@()
for($i=0;$i -lt 7 -and $id;$i++){
 $x=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
 if(-not $x){break}
 $chain+=@{pid=[int]$x.ProcessId;parent=[int]$x.ParentProcessId;name=$x.Name}
 $id=$x.ParentProcessId
}
$r=Get-CimInstance Win32_Process -Filter 'ProcessId=13320'
if(-not $r){throw 'Parent absent'}
$encoded=($r.CommandLine -split '-EncodedCommand ')[1]
$decoded=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($encoded))
@{chain=$chain;decodedLauncher=$decoded}|ConvertTo-Json -Depth 5 -Compress
"""
    result = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script], encoding="utf-8"))
    assert 13320 in [x["pid"] for x in result["chain"]]
    assert str(C / "runner.ps1") in result["decodedLauncher"]
    result.update(sessionId=L.name, liveParentPid=13320, lockTouched=False,
                  role="Child inherits live parent protection; no lock acquisition/read/delete/unlock.")
    return result


def frozen():
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, rec in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert sha(raw) == rec["sha256"] and len(raw) == rec["bytes"], name
        inputs[name] = raw
    jm = gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(jm) == snapshot["jmdict"]["xmlSha256"]
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, inputs, ET.fromstring(jm), ET.fromstring(kd)


def start():
    clean(R, HEAD)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == MAIN
    assert git("branch", "--show-current") == "content/n1-kanji"
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    cp = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):",
        1)[1])
    assert cp["checkpoint"] == 807 and cp["batch"] == "105"
    p = load(C / "progress.json")
    assert p["checkpoint"] == 807 and p["status"] == "continue" and p["batch"] == "105"
    assert p["lastPublishedCommit"] == MAIN and p["remainingAdditions"] == 1097
    assert not (L / "progress-before-808.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-808.json")
    preflight = role()
    save(L / "preflight-808.json", preflight)
    state = {
        "execution": 808, "batch": "105", "startingHead": HEAD,
        "freshOriginMain": MAIN, "androidHead": APP,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE source-completion checkpoint for SAME105 only. No runtime draft, reviewer, Android/native, publication,106 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed; operative contract, approved issue and final807 inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": preflight,
        "artifactPathPreflight": "Approved control helpers, committed packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main unchanged.",
        "actualNewPermissionDenials": [],
    }
    p["execution808StartingState"] = state
    p.update(stage="batch-105-source-completion-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Source-completion scope persisted; parent ownership and clean signed heads verified.")


def packet():
    snapshot, inputs, jm, kd = frozen()
    words = ["強い", "剛健", "力強い", "強力", "力", "勢い", "活力", "活気",
             "元気", "エネルギー", "迫力", "体力", "実力", "勇ましい",
             "堅い", "固い", "硬い", "筆跡", "雄", "雄大",
             "もりもり", "ばりばり", "生き生き", "ぐいぐい"]
    entries = [e for e in jm.findall("entry") if any(
        x.text in words for x in e.findall("k_ele/keb") + e.findall("r_ele/reb"))]
    ids = [e.findtext("ent_seq") for e in entries]
    save(S / "batch-105-comparison-selection.json", {
        "schemaVersion": 1, "batch": "105", "requestedForms": words, "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "All complete frozen families with exact requested keb or reb, including homographs, alternate readings and sense restrictions.",
        "limits": "Selection and extraction do not establish reading, frequency or semantic acceptance."})
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / "batch-105-comparisons.xml").write_bytes(raw)
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in "雄強剛力勢功劾剖":
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    (S / "batch-105-support-characters.xml").write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    kanji = "強剛力勢硬固精勇永凌冒弱軽労功勉劾剖"
    article_words = ["強い", "剛健", "力強い", "強力", "力", "勢い", "活力", "活気",
                     "元気", "エネルギー", "迫力", "体力", "実力", "勇ましい", "堅い",
                     "固い", "硬い", "雄大", "もりもり", "ばりばり", "生き生き", "ぐいぐい"]
    paths = [f"kanji/{x}.md" for x in kanji]
    paths += [f"words/{x}.md" for x in article_words if (R / "words" / (x + ".md")).exists()]
    records = {name: {"sha256": sha((R / name).read_bytes()),
                      "bytes": len((R / name).read_bytes()), "metadata": metadata(R, name)}
               for name in paths}
    save(S / "batch-105-comparison-article-snapshots.json", records)
    print(f"Extracted {len(ids)} complete comparison families; {len(records)} actual article snapshots; eight complete raw comparison/support characters.")
    for e in entries:
        print(e.findtext("ent_seq"), "/".join(x.text for x in e.findall("k_ele/keb")),
              "/".join(x.text for x in e.findall("r_ele/reb")))


def public():
    class Blocks(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth = 0
            self.parts = []
            self.blocks = []

        def handle_starttag(self, tag, attrs):
            if tag == "div":
                if self.depth:
                    self.depth += 1
                elif "kijiWrp" in dict(attrs).get("class", "").split():
                    self.depth = 1
                    self.parts = []
            if self.depth and tag in {"p", "h2", "h3", "br", "li"}:
                self.parts.append("\n")

        def handle_endtag(self, tag):
            if tag == "div" and self.depth:
                self.depth -= 1
                if not self.depth:
                    self.blocks.append("\n".join(
                        x.strip() for x in "".join(self.parts).splitlines() if x.strip()))

        def handle_data(self, text):
            if self.depth:
                self.parts.append(text)

    p = C / "batch-105-yuu-808.html"
    raw = p.read_bytes()
    parser = Blocks()
    parser.feed(raw.decode("utf-8"))
    candidates = ["ゆう【雄】\n" + b for b in
                  parser.blocks[0].split("ゆう【雄】\n")[1:] if "［音］" in b]
    assert len(candidates) == 1
    text = candidates[0].rstrip() + "\n"
    assert all(x in text for x in ["ユウ", "勇ましく強い", "規模が大きい", "雄大"])
    out = S / "batch-105-yuu-public-text.txt"
    out.write_text(text, encoding="utf-8")
    archive = S / "batch-105-yuu-808.html.gz"
    archive.write_bytes(gzip.compress(raw, mtime=0))
    save(S / "batch-105-supplemental-public-receipt.json", {
        "url": "https://www.weblio.jp/content/%E9%9B%84",
        "downloadedAt": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(),
        "rawBytes": len(raw), "rawSha256": sha(raw), "archive": archive.name,
        "archiveSha256": sha(archive.read_bytes()), "losslessGzip": True,
        "extractedText": out.name, "extractedTextSha256": sha(out.read_bytes()),
        "inspectedBlock": "Actual Digital Daijisen character heading ゆう【雄】, sound ユウ, all three numbered senses and complete entry. Other readings and aggregator neighbors were returned by web_fetch but are not assigned to this compound.",
        "qualification": "Character reading/strength sense plus frozen full 雄勁 family and 勁 character listing support ユウ+ケイ. A kana substring alone is not allocation evidence. No animal-sex claim or gender restriction for 雄勁.",
        "limits": "Coordinator retrieval and author inspection, not independent upstream reviewer lookup, historical etymology or frequency evidence."})
    print(text)


def canonical(e):
    return (e.tag, tuple(sorted(e.attrib.items())), (e.text or "").strip(),
            tuple(canonical(c) for c in e))


def preparation():
    from fontTools.ttLib import TTFont
    snapshot, inputs, jm, kd = frozen()
    plan = load(S / "batch-105-source-completion-plan.json")
    text = plan["strokeAndFontPlan"]["proposedTextInventory"]
    han = sorted({c for c in text if 0x3400 <= ord(c) <= 0x9fff or ord(c) >= 0x20000})
    fonts = []
    for path in sorted((A / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            fonts.append({"path": str(path), "sha256": sha(path.read_bytes()),
                          "keyGlyphPresence": {c: ord(c) in cmap for c in han},
                          "allProposedMissing": [c for c in han if ord(c) not in cmap]})
    assert len(fonts) == 3
    save(S / "batch-105-font-preparation.json", {
        "schemaVersion": 1, "batch": "105", "proposedTextInventory": text,
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "defaultSystemFont": "Later native four-mode rendering required; not a fourth bundled file.",
        "limits": "Proposed text only. Cmap presence/absence is not rendered readability, fallback-face identity or native/phone acceptance. Recompute final actual runtime Han after drafting."})
    manifest = load(R / "manifest.json")
    all_cards = {p.stem: metadata(R, p.relative_to(R).as_posix())
                 for p in (R / "kanji").glob("*.md")}
    fewer = {k: v.get("distractors", []) for k, v in all_cards.items()
             if len(v.get("distractors", [])) < 3}
    incoming = [k for k, v in all_cards.items() if "勁" in v.get("distractors", [])]
    legacy = {k: {"distractors": v, "metadata": all_cards[k],
                  "sha256": sha((R / "kanji" / (k + ".md")).read_bytes())}
              for k, v in fewer.items()}
    save(S / "batch-105-baseline-plan.json", {
        "schemaVersion": 1, "batch": "105", "signedSourceBase": HEAD, "publishedBase": MAIN,
        "androidHead": APP, "manifestSha256": sha((R / "manifest.json").read_bytes()),
        "contentVersion": manifest["contentVersion"],
        "completeBaselineInventory": "All exact runtime paths/hashes in manifest.json at signed c2abec23; full published-base bytes unchanged. No baseline runtime edit is proposed.",
        "comparisonArticleSnapshots": "batch-105-comparison-article-snapshots.json",
        "currentKanji": len(all_cards), "currentWords": len(list((R / "words").glob("*.md"))),
        "currentN1Labels": sum(v["jlpt"] == 1 for v in all_cards.values()),
        "legacyFewerThanThreeCurated": legacy, "incomingCuratedTargetReferences": incoming,
        "allMappedPairs": [["勁", "words/雄勁.md"]], "requiredDirections": 2,
        "activatedBaselinePairs": [], "navigationOnlyReusedEdits": [],
        "allowedLaterRuntimeAdditions": ["kanji/勁.md", "strokes/勁.json", "words/雄勁.md"],
        "baselineRuntimeChangesAllowed": [],
        "limits": "Source-stage inventory only. Recheck all baseline metadata/hashes, exact new links and generated manifest on actual draft and accepted integrated tree."})
    print(json.dumps({"proposedHan": len(han), "missing": fonts[0]["allProposedMissing"],
                      "legacyFewerThanThree": len(legacy), "incomingTarget": incoming},
                     ensure_ascii=False))


def audit():
    snapshot, inputs, jm, kd = frozen()
    plan = load(S / "batch-105-source-completion-plan.json")
    ids = load(S / "batch-105-comparison-selection.json")["entryIds"]
    assert len(ids) == len(set(ids)) == 28
    assert (S / "batch-105-comparisons.xml").read_bytes() == extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    member_ids = load(S / "batch-105-lexical-selection.json")["entryIds"]
    assert len(member_ids) == 9
    assert len(set(member_ids) | set(ids)) == 36
    assert (S / "batch-105-jmdict.xml").read_bytes() == extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], member_ids)
    source_chars = {e.findtext("literal"): e for e in kd.findall("character")}
    records = ET.parse(S / "batch-105-support-characters.xml").getroot().findall("character")
    records += ET.parse(S / "batch-105-kanjidic2.xml").getroot().findall("character")
    assert len(records) == 9
    for e in records:
        assert canonical(e) == canonical(source_chars[e.findtext("literal")])
    char = source_chars["勁"]
    kp = plan["kanjiTeachingPlan"]
    assert kp["fullOnyomi"] == [x.text for x in char.findall(".//reading[@r_type='ja_on']")]
    assert kp["fullKunyomi"] == [x.text for x in char.findall(".//reading[@r_type='ja_kun']")]
    assert kp["quizOnyomi"] == ["ケイ"] and kp["quizKunyomi"] == []
    assert char.findtext("misc/stroke_count") == "9"
    assert char.findtext("radical/rad_value[@rad_type='classical']") == "19"
    assert plan["membership"] == ["勁"] and plan["sourceRows"] == [116]
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == "勁")
    assert row["sourceRow"] == 116
    nav = load(S / "batch-105-source-navigation.json")
    assert nav["candidates"] == [] and nav["baselinePairs"] == []
    assert not (R / "kanji" / "勁.md").exists()
    assert not (R / "kanji" / "雄.md").exists()
    assert not (R / "words" / "雄勁.md").exists()
    assert not (R / "strokes" / "勁.json").exists()
    snap = load(S / "batch-105-comparison-article-snapshots.json")
    assert len(snap) == 38
    for name, rec in snap.items():
        assert sha((R / name).read_bytes()) == rec["sha256"]
        assert metadata(R, name) == rec["metadata"]
    baseline = load(S / "batch-105-baseline-plan.json")
    assert baseline["currentKanji"] == 1127 and baseline["currentWords"] == 5078
    assert baseline["currentN1Labels"] == 136
    assert not baseline["incomingCuratedTargetReferences"]
    assert set(baseline["legacyFewerThanThreeCurated"]) == set("人休何入出口女日月男買")
    for k, rec in baseline["legacyFewerThanThreeCurated"].items():
        assert sha((R / "kanji" / (k + ".md")).read_bytes()) == rec["sha256"]
        assert metadata(R, f"kanji/{k}.md") == rec["metadata"]
    guards = kp["quizExclusions"]
    distractors = [r["kanji"] for r in kp["curatedDistractors"]]
    assert distractors == ["功", "劾", "剖"] and len(guards) == 4
    assert not set(guards) & set(distractors)
    for d in kp["curatedDistractors"]:
        m = metadata(R, f"kanji/{d['kanji']}.md")
        assert m["title"] == d["displayedTitle"] and m["jlpt"] == 1
        assert not set(m.get("quiz_exclusions", [])) & set(distractors)
    for g in kp["directGuardReasons"]:
        assert metadata(R, f"kanji/{g['pair'][1]}.md")["title"] == g["displayedOtherTitle"]
    sp = plan["supportTeachingPlan"]
    assert sp["kanji"] == ["雄", "勁"] and len(sp["quizExclusions"]) == 6
    assert set(sp["quizExclusions"]) == {g["word"] for g in sp["guardReasons"]}
    for g in sp["guardReasons"]:
        assert metadata(R, f"words/{g['word']}.md")["title"] == g["title"]
    assert plan["navigationAndBaselinePlan"]["proposedAllMappedPairs"] == [["勁", "words/雄勁.md"]]
    assert plan["navigationAndBaselinePlan"]["activatedBaselinePairs"] == []
    primary = [p.name for p in (R / "words").glob("*.md")
               if metadata(R, p.relative_to(R).as_posix())["reading"] == "ゆうけい"]
    assert primary == []
    for rec in load(S / "batch-105-public-source-receipts.json") + [
            load(S / "batch-105-supplemental-public-receipt.json")]:
        zipped = (S / rec["archive"]).read_bytes()
        assert sha(zipped) == rec["archiveSha256"]
        assert sha(gzip.decompress(zipped)) == rec["rawSha256"]
        assert sha((S / rec["extractedText"]).read_bytes()) == rec["extractedTextSha256"]
    svg = (S / "batch-105-kanjivg.svg").read_bytes()
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert [p.attrib["id"] for p in paths] == [f"kvg:052c1-s{i}" for i in range(1, 10)]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    unicode_rows = inputs["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines()
    radical_row = next(x.split(";") for x in unicode_rows if x.startswith("2F12;"))
    assert radical_row[5] == "<compat> 529B"
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    assert sha((R / "manifest.json").read_bytes()) == baseline["manifestSha256"]
    count = 0
    for section in ("files", "images", "scenes", "audio", "listening", "curriculum",
                    "listeningTasks", "listeningTaskAudio", "listeningTaskImages"):
        for name, digest in manifest.get(section, {}).items():
            path = R / name
            actual = sha(path.read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else manifest_sha256(path)
            assert actual == digest, name
            count += 1
    assert count == 8466
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD") == HEAD and git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    before, now = load(L / "progress-before-808.json"), load(C / "progress.json")
    mutable = {"stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    fonts = load(S / "batch-105-font-preparation.json")
    for rec in fonts["fonts"]:
        assert sha(Path(rec["path"]).read_bytes()) == rec["sha256"]
    result = {
        "schemaVersion": 1, "execution": 808, "batch": "105", "sourceBase": HEAD,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamilies": 9, "completeComparisonFamilies": 28,
        "distinctFamilyUnion": 36, "exactFreshExtractionsMatch": True,
        "completeRawCharacterRecords": 9, "rawCharacterSemanticEquality": True,
        "sourceRow": 116, "kanji": "勁", "metadataReadingEntries": 2,
        "selectedReadingEntries": 1, "newNecessarySupportWords": 1,
        "existingArticleSnapshotsVerified": len(snap) + len(baseline["legacyFewerThanThreeCurated"]),
        "legacyFallbackArticles": len(baseline["legacyFewerThanThreeCurated"]),
        "navigationOnlyReusedChanges": 0,
        "directKanjiGuards": len(guards), "directWordGuards": 6,
        "curatedWrongChoices": 3, "allMappedPairs": 1, "requiredDirections": 2,
        "activatedBaselinePairs": 0, "actualPublicPagesRetained": 4,
        "proposedHan": fonts["auditedHanCount"], "bundledFonts": 3,
        "missingFromAllBundledCmaps": sorted(set.intersection(*[
            set(r["allProposedMissing"]) for r in fonts["fonts"]])),
        "missingCmapIsRenderingFailure": False, "defaultSystemFont": "Later native rendering required",
        "geometryConverted": False, "pinnedSvgPaths": 9, "canonicalRadicalVerifiedFromUnicode": True,
        "runtimeBytesUnchanged": True, "runtimeManifestHashesVerified": count,
        "manifestBytesUnchanged": True, "contentVersion": manifest["contentVersion"],
        "originalHistoricalRootValuesPreserved": True, "sourcePreparationComplete": True,
        "limits": "Source-stage author inspection/mechanical audit, not independent linguistic review or fresh Android/native/font/phone acceptance. Initial807 historical read depth and all acceptance limits remain. Direct safeguards do not certify every unsampled quiz pool."}
    save(S / "batch-105-source-completion-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    assert git("rev-parse", "HEAD") == HEAD
    clean(A, APP)
    checks = {}
    for label in ["preparation", "source-tests", "validate", "manifest", "manifest-diff",
                  "budget", "vocabulary", "audit", "whitespace"]:
        raw = (L / f"{label}-808.txt").read_bytes()
        out = S / f"batch-105-{label}-808.txt.gz"
        out.write_bytes(gzip.compress(raw, mtime=0))
        checks[label] = {"archive": out.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(out.read_bytes())}
        assert gzip.decompress(out.read_bytes()) == raw
    tests = (L / "source-tests-808.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-808.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    audit_result = load(S / "batch-105-source-completion-audit.json")
    assert audit_result["runtimeManifestHashesVerified"] == 8466
    assert audit_result["proposedHan"] == 22
    helper_hashes = {}
    for name in ["complete-batch-105-808.py", "checks-batch-105-source-808.ps1",
                 "post-batch-105-source-808.ps1"]:
        out = S / ("batch-105-" + name)
        shutil.copyfile(C / name, out)
        helper_hashes[out.name] = sha(out.read_bytes())
    shutil.copyfile(L / "preflight-808.json", S / "batch-105-runner-role-808.json")
    progress = load(S / "batch-105-progress.json")
    progress.update(status="source-complete-not-runtime-drafted", sourcePreparationComplete=True,
                    sourceCompletionPlan="batch-105-source-completion-plan.json",
                    sourceCompletionAudit="batch-105-source-completion-audit.json",
                    sourceCompletionExecution=808, nextAction=NEXT,
                    limits="Source-complete author plan and exact evidence, not runtime drafting, independent review or acceptance. Initial member-only observations/audit remain historical807 records. All original downstream gates and outstanding phone/general-release/whole-set limits remain.")
    save(S / "batch-105-progress.json", progress)
    save(S / "execution-808.json", {
        "schemaVersion": 1, "execution": 808, "checkpoint": 808, "batch": "105",
        "stage": "batch-105-source-complete-not-runtime-drafted",
        "baseCommit": HEAD, "publishedBase": MAIN, "androidSignedHead": APP,
        "membership": ["勁"], "sourceRows": [116],
        "sourcePlan": "batch-105-source-completion-plan.json",
        "sourceCompletionAudit": audit_result,
        "validation": checks, "durableHelperHashes": helper_hashes,
        "runnerPreflight": load(L / "preflight-808.json"),
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False,
        "sourcePreparationComplete": True, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 131,
        "remainingAdditions": 1097, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "actualNewPermissionDenials": [],
        "diagnostics": [
            "Public-entry extraction first asserted because Weblio groups multiple Daijisen headings in one wrapper; selected the exact character subentry from that retained wrapper and verified complete heading/senses. No substituted neighboring dictionary.",
            "Initial source audit deliberately failed an incorrect all-three-distractor assumption: actual full metadata found11 two-choice legacy cards. All11 full bodies inspected, exact snapshots/labels retained and source plan corrected; none requires a new strength guard. No baseline runtime edits.",
            "A read-only Python probe used a non-raw Windows path string and failed Invalid argument before reading; corrected by direct view calls to the approved exact files. Not a permission denial.",
            "Staged whitespace check caught an extra final blank line in generated public text. Trimmed extractor output, regenerated its hash/receipt and reran source checks; no runtime content changed."
        ],
        "nextAction": NEXT,
        "limits": "Normally signed LOCAL source-only checkpoint; no push, independent content review, app/native acceptance or runtime publication. Source-ready is not review-closed. Vocabulary check remains2122/2431 pilot coverage, not whole-corpus annotation completion. All earlier evidence and acceptance gates remain intact."})
    print("Source-completion evidence and check logs archived for a normally signed local checkpoint.")


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("rev-parse", "HEAD^") == HEAD
    clean(R, head)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == MAIN
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    preflight = role()
    receipt = load(L / "issue-receipt-808.json")
    assert receipt["author"] == "stop-cran" and receipt["verified"] and receipt["localCommit"] == head
    before, p = load(L / "progress-before-808.json"), load(C / "progress.json")
    changed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert p["checkpoint"] == 807 and p["batch"] == "105"
    assert all(p[k] == v for k, v in before.items() if k not in changed)
    result = {
        "execution": 808, "checkpoint": 808, "batch": "105", "savedCommit": head,
        "signature": "G", "status": "continue", "stage": "batch-105-source-complete-not-runtime-drafted",
        "baseCommit": HEAD, "lastPublishedCommit": MAIN, "membership": ["勁"], "sourceRows": [116],
        "completeMemberFamilies": 9, "completeComparisonFamilies": 28, "distinctFamilyUnion": 36,
        "completeRawCharacterRecords": 9, "completeExistingArticlesRead": 49,
        "actualPublicDictionaryEntries": 4, "metadataReadingEntries": 2,
        "proposedQuizOnyomi": ["ケイ"], "proposedQuizKunyomi": [],
        "newNecessarySupportWords": 1, "directKanjiGuards": 4, "directWordGuards": 6,
        "proposedHan": 22, "missingFromAllBundledCmaps": ["刂", "勁", "巠"],
        "geometryConverted": False, "pinnedSvgPaths": 9,
        "focusedTestsPassed": 43, "validatorErrors": 0, "runtimeHashesVerified": 8466,
        "runtimeBytesUnchanged": True, "manifestBytesUnchanged": True,
        "contentVersion": "a5bc9b199c7df334", "sourcePreparationComplete": True,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "publishedAdditions": 131, "remainingAdditions": 1097,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "originalHistoricalRootValuesPreserved": True,
        "originalRootKeysCompared": len(before), "finalRunnerPreflight": preflight,
        "sourceEvidence": "docs/n1-sources/execution-808.json",
        "sourcePlan": "docs/n1-sources/batch-105-source-completion-plan.json",
        "issueUpdate": receipt["url"], "ownerIssueAuthorAndBodyVerified": True, "nextAction": NEXT}
    p["execution808CoordinatorCheckpoint"] = result
    p["batch105SourceCompletionIssueReceipt"] = receipt
    p.update(checkpoint=808, status="continue", stage=result["stage"], nextAction=NEXT, blocker=None)
    assert all(p[k] == v for k, v in before.items() if k not in changed)
    save(C / "progress.json", p)
    saved = load(C / "progress.json")
    assert all(saved[k] == v for k, v in before.items() if k not in changed)
    assert saved["execution808CoordinatorCheckpoint"] == result
    save(L / "checkpoint-808.json", result)
    print(json.dumps({"checkpoint": 808, "savedCommit": head, "status": "continue",
                      "historicalRootKeysPreserved": len(before),
                      "issueUpdate": receipt["url"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["start", "packet", "public", "preparation", "audit", "record", "checkpoint"])
    args = parser.parse_args()
    globals()[args.stage]()
