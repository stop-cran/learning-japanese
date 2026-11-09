"""Persist and audit the bounded, unpublished batch 108 runtime draft."""
import argparse
import base64
import copy
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "rollout-recovered" / "learning-japanese"
A = R.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "68a0ce7a-9dab-430c-b0ad-8a474a9c56fa"
HEAD = "64b30465652a60d891291a64ca075aa107a2d01a"
PUBLIC = "e766221c2a9c5ada2314805c307e534ccf4537ec"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
PREFIX = "batch-108-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from audit_n1_batch import (
    activated_baseline_pairs, audit_pinned_strokes, base_file,
    reused_changes, runtime_delta, teachable_lexical_pair,
)
from build_manifest import build_manifest
from freeze_n1_sources import metadata_record
from generate_strokes import convert


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def save(path, value):
    temp = path.with_name(path.name + ".861.tmp")
    if temp.exists():
        raise FileExistsError(temp)
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def current():
    runner = load(C / "runner.json")
    assert runner["status"] == "running" and runner["sessionId"] == L.name
    assert runner["pid"] == 27864
    p = load(C / "progress.json")
    assert p["checkpoint"] == 860 and p["status"] == "continue" and p["batch"] == "108"
    assert p["lastPublishedCommit"] == PUBLIC and p["remainingAdditions"] == 1094
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    return p


def start():
    p = current()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert load(L / "checkpoint-full.json") == p
    assert git("rev-parse", "origin/main") == PUBLIC
    assert p["execution792HistoryCorrection"]["ownerReportCorrection"].startswith("https://github.com/")
    probe = (
        f"$c=Get-CimInstance Win32_Process -Filter 'ProcessId={os.getpid()}';"
        "$shell=Get-CimInstance Win32_Process -Filter \"ProcessId=$($c.ParentProcessId)\";"
        "$cli=Get-CimInstance Win32_Process -Filter \"ProcessId=$($shell.ParentProcessId)\";"
        "$runner=Get-CimInstance Win32_Process -Filter \"ProcessId=$($cli.ParentProcessId)\";"
        "@{shell=$shell.ProcessId;coordinator=$cli.ProcessId;runner=$runner.ProcessId;"
        "runnerCommand=$runner.CommandLine}|ConvertTo-Json -Compress"
    )
    ancestry = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-Command", probe], encoding="utf-8"
    ))
    assert ancestry["coordinator"] == 29460 and ancestry["runner"] == 27864, ancestry
    command = ancestry["runnerCommand"]
    if " -EncodedCommand " in command:
        command = base64.b64decode(command.split(" -EncodedCommand ", 1)[1]).decode("utf-16-le")
    assert str(C / "runner.ps1") in command, ancestry
    ancestry["decodedRunnerCommandSha256"] = sha(command.encode("utf-8"))
    ancestry.pop("runnerCommand")
    before = L / "progress-before-861.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    p["execution861StartingState"] = {
        "execution": 861, "batch": "108", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "publishedBase": PUBLIC, "androidHead": APP,
        "scope": "One local UNREVIEWED runtime draft and exact-current mechanical audit; no reviewers/native/publication.",
        "ancestry": ancestry, "runnerScriptSha256": sha((C / "runner.ps1").read_bytes()),
        "parentLockTouched": False, "completeRequestReadIncludingFinalCheckpoint": True,
        "fullHistoryBefore": str(before), "fullHistoryBeforeSha256": sha(before.read_bytes()),
        "status": "local-unreviewed-runtime-draft-in-progress",
    }
    p.update(stage="batch-108-local-unreviewed-runtime-draft-in-progress",
             nextAction="Draft SAME108 from signed source plan; retain all source/review/signing/native/publication gates.")
    save(C / "progress.json", p)
    print("Full-history starting scope persisted; live parent ancestry authenticated.")


def geometry():
    current()
    assert git("rev-parse", "HEAD") == HEAD
    target = R / "strokes" / "\u52e7.json"
    assert not target.exists()
    svg = (S / (PREFIX + "kanjivg.svg")).read_text(encoding="utf-8")
    data = convert("\u52e7", svg)
    assert data["strokeCount"] == 13
    assert "\u52e7" not in load(R / "tools" / "order_variants.json")
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    print("Generated thirteen strokes using unchanged pinned converter and retained SVG.")


def xml_bytes(root):
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def verify_link_directions(root, mapping, pairs):
    directions = {(f"kanji/{k}.md", w) for k, w in pairs} | {(w, f"kanji/{k}.md") for k, w in pairs}
    assert directions == {(d["from"], d["to"]) for d in mapping["requiredDirections"]}
    assert len(mapping["requiredDirections"]) == len(directions)
    for d in mapping["requiredDirections"]:
        origin = root / d["from"]
        target = (origin.parent / d["relative"]).resolve()
        assert target == (root / d["to"]).resolve() and target.is_file(), d
        text = origin.read_text(encoding="utf-8")
        assert f"]({d['relative']})" in text and d["reading"] in text, d
    return len(directions)


def audit():
    current()
    assert git("rev-parse", "HEAD") == HEAD
    plan = load(S / (PREFIX + "source-completion-plan.json"))
    baseline = load(S / (PREFIX + "baseline-plan.json"))
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    assert baseline["baseCommit"] == plan["baseCommit"]
    before_manifest = json.loads(base_file(R, plan["baseCommit"], "manifest.json"))
    assert baseline["runtimeManifest"] == before_manifest
    assert git("merge-base", "--is-ancestor", PUBLIC, HEAD) == ""
    frozen = {}
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert sha(raw) == info["sha256"] and len(raw) == info["bytes"], name
        frozen[name] = raw
    for name, field in (("n1-implementation-JMdict_e.gz", "jmdict"),
                        ("n1-planning-kanjidic2.xml.gz", "kanjidic2")):
        assert sha(gzip.decompress(frozen[name])) == snapshot[field]["xmlSha256"]
    selections = [
        load(S / (PREFIX + "lexical-selection.json")),
        load(S / (PREFIX + "comparison-selection.json")),
    ]
    packets = [ET.Element("JMdict"), ET.Element("JMdict")]
    comparisons = set(selections[1]["comparisonSpellings"])
    with gzip.open(C / "inputs" / "n1-implementation-JMdict_e.gz", "rb") as stream:
        for _, entry in ET.iterparse(stream, events=("end",)):
            if entry.tag != "entry":
                continue
            spellings = [e.text for e in entry.findall("k_ele/keb")]
            if any("\u52e7" in s for s in spellings):
                packets[0].append(copy.deepcopy(entry))
            if comparisons.intersection(spellings):
                packets[1].append(copy.deepcopy(entry))
            entry.clear()
    for packet, name, selection, count in zip(
        packets, ["jmdict.xml", "comparison-jmdict.xml"], selections, [46, 18]
    ):
        assert xml_bytes(packet) == (S / (PREFIX + name)).read_bytes(), name
        assert len(packet) == count
        assert [e.findtext("ent_seq") for e in packet] == selection["entryIds"]
    families = {e.findtext("ent_seq"): e for packet in packets for e in packet}
    assert len(families) == 64
    characters = ET.fromstring(gzip.decompress(frozen["n1-planning-kanjidic2.xml.gz"]))
    for name, wanted in (
        ("kanjidic2.xml", "\u52e7"),
        ("comparison-kanjidic2.xml", "\u52e7\u544a\u52b1\u52df\u62db\u8b66\u652f\u89b3\u78ba\u6a29"),
        ("overlap-kanjidic2.xml", "\u4f9b\u796d\u52c9\u8a2a"),
    ):
        packet = ET.Element("kanjidic2")
        packet.append(copy.deepcopy(characters.find("header")))
        for entry in characters.findall("character"):
            if entry.findtext("literal") in wanted:
                packet.append(copy.deepcopy(entry))
        assert xml_bytes(packet) == (S / (PREFIX + name)).read_bytes(), name
    radicals = {}
    for line in frozen["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines():
        fields = line.split(";")
        cp = int(fields[0], 16)
        if 0x2F00 <= cp <= 0x2FD5:
            radicals[cp - 0x2F00 + 1] = chr(int(fields[5].split()[-1], 16))
    source_row = next(e for e in load(S / "source-index.json") if e["sourceRow"] == 119)
    assert source_row["kanji"] == json.loads(frozen["n1-kanji-source-20261102.json"])[118] == "\u52e7"
    character = next(e for e in characters if e.findtext("literal") == "\u52e7")
    assert metadata_record(character, radicals) == source_row["metadata"]
    additions = plan["linkPlan"]["runtimePathsToAddLater"]
    changes = plan["linkPlan"]["exactReusedChanges"]
    changed = {edit["article"] for edit in changes}
    expected_articles = set(baseline["inventory"]) | {n for n in additions if n.endswith(".md")}
    actual_articles = {p.relative_to(R).as_posix() for folder in ("kanji", "words")
                       for p in (R / folder).glob("*.md")}
    assert actual_articles == expected_articles
    for name, item in baseline["inventory"].items():
        if name in changed:
            continue
        assert sha((R / name).read_bytes()) == item["sha256"], name
        assert metadata(R, name) == item["metadata"], name
    for name in changed:
        old = base_file(R, plan["baseCommit"], name)
        edits = [edit for edit in changes if edit["article"] == name]
        exclusions = ["\u63a8\u85a6", "\u63d0\u6848"] if name.startswith("words/") else None
        reused_changes(old, (R / name).read_text(encoding="utf-8"), edits, exclusions)
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    runtime_delta(before_manifest, manifest, additions, changed)
    raw_changed = set(git("diff", "--name-only", HEAD).splitlines())
    tracked_runtime = {n for n in raw_changed if not n.startswith("docs/")}
    assert tracked_runtime == changed | {"manifest.json"}, tracked_runtime
    new_runtime = {p.relative_to(R).as_posix() for p in [R / n for n in additions] if p.exists()}
    assert new_runtime == set(additions)
    meta = metadata(R, "kanji/\u52e7.md")
    kp = plan["kanjiPlan"]
    for key in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
        assert meta[key] == source_row["metadata"][key], key
    for key in ("title", "jlpt", "tags", "quizOnyomi", "quizKunyomi", "quiz_exclusions"):
        expected = kp["quizExclusions"] if key == "quiz_exclusions" else kp[key]
        assert meta[key] == expected, key
    assert "phonetic" not in meta
    assert meta["distractors"] == [d["kanji"] for d in kp["curatedDistractors"]]
    assert len(set(meta["distractors"])) == 3
    assert not set(meta["distractors"]).intersection(meta["quiz_exclusions"])
    assert not any(item["metadata"]["title"] == meta["title"]
                   for name, item in baseline["inventory"].items() if name.startswith("kanji/"))
    for choice in kp["curatedDistractors"] + kp["directGuardRationale"] + kp["otherComparedLabels"]:
        assert metadata(R, f"kanji/{choice['kanji']}.md")["title"] == choice["actualTitle"]
    body = (R / "kanji" / "\u52e7.md").read_text(encoding="utf-8")
    reading_table = body.split("## Readings\n", 1)[1].split("## Common words\n", 1)[0]
    rows = {}
    for line in reading_table.splitlines():
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells[1] in ("on", "kun"):
                assert cells[0] not in rows
                rows[cells[0]] = cells
    assert list(rows) == meta["onyomi"] + meta["kunyomi"]
    assert len(kp["readingRows"]) == 3
    from audit_n1_pilot import offered_keys
    assert {"on": offered_keys(meta["quizOnyomi"]), "kun": offered_keys(meta["quizKunyomi"])} == kp["offeredKeys"]
    for row in kp["readingRows"]:
        if row["selected"]:
            relative = "../" + row["article"]
            assert f"]({relative})" in rows[row["raw"]][2] and row["reading"] in rows[row["raw"]][2]
            assert row["raw"] in meta["quizOnyomi" if row["kind"] == "on" else "quizKunyomi"]
            for sense in row.get("selectedSenses", [1]):
                assert teachable_lexical_pair(families[row["entryIds"][0]],
                                              row["example"], row["reading"], sense)
        else:
            assert row["disposition"] and row["qualification"]
            assert "Source-only" in rows[row["raw"]][2]
            assert row["raw"] not in meta["quizOnyomi"] + meta["quizKunyomi"]
    support = plan["supportPlan"]["reused"] + plan["supportPlan"]["newNecessary"]
    all_pairs = set()
    for word in support:
        wm = metadata(R, word["article"])
        for key in ("word", "reading", "title", "type"):
            assert wm[key] == word[key], (word["article"], key)
        assert wm["kanji"] == list(dict.fromkeys(c for c in wm["word"] if "\u4e00" <= c <= "\u9fff"))
        for sense in word["selectedSenses"]:
            assert teachable_lexical_pair(families[word["entryId"]], wm["word"], wm["reading"], sense)
        if word in plan["supportPlan"]["newNecessary"]:
            assert "jlpt" not in wm and wm["tags"] == word["tags"]
            assert wm["quiz_exclusions"] == word["quizExclusions"]
        else:
            assert wm["jlpt"] == word["jlpt"] == 3
        all_pairs.update((c, word["article"]) for c in wm["kanji"]
                         if (R / "kanji" / (c + ".md")).exists())
    assert all_pairs == {tuple(p) for p in plan["linkPlan"]["allMappedPairs"]}
    activated = activated_baseline_pairs(before_manifest, ["\u52e7"], load(S / "baseline-word-candidates.json"))
    assert activated == {tuple(p) for p in plan["linkPlan"]["activatedBaselinePairs"]} <= all_pairs
    direction_count = verify_link_directions(R, plan["linkPlan"], all_pairs)
    for row in plan["supportPlan"]["wordQuizAudit"]["newDirectPairs"]:
        a, b = row["pair"]
        am, bm = [metadata(R, f"words/{w}.md") for w in (a, b)]
        assert b in am.get("quiz_exclusions", []) or a in bm.get("quiz_exclusions", []), row
    for a, b in plan["supportPlan"]["wordQuizAudit"]["preservedIncomingPairs"]:
        assert a in metadata(R, f"words/{b}.md").get("quiz_exclusions", [])
    for name in additions:
        if not name.endswith(".md"):
            continue
        text = (R / name).read_text(encoding="utf-8")
        for relative in re.findall(r"\]\(([^)]+)\)", text):
            if relative.startswith("https://"):
                continue
            target = ((R / name).parent / relative).resolve()
            assert target.is_relative_to(R) and target.is_file(), (name, relative)
    audit_pinned_strokes(R, S, "108", "\u52e7", meta, source_row, snapshot, plan,
                         {"strokePaths": 13, "pointsPerPath": 16,
                          "exactPinnedConverterOutput": True}, "current", plan["baseCommit"])
    for receipt in load(S / (PREFIX + "public-source-receipts.json")) + [
        load(S / (PREFIX + "support-public-source-receipt.json"))
    ]:
        archive = (S / receipt["archive"]).read_bytes()
        raw = gzip.decompress(archive)
        assert sha(archive) == receipt["archiveSha256"]
        assert sha(raw) == receipt["rawSha256"] and len(raw) == receipt["rawBytes"]
        assert sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"]
    result = {
        "schemaVersion": 1, "batch": "108", "execution": 861,
        "auditKind": "equivalent-exact-current-reused-support-audit-not-generic-CLI",
        "sourcePreparationHead": HEAD, "baseCommit": plan["baseCommit"],
        "allFiveFrozenInputsAndBothXmlHashesVerified": True,
        "exactCompleteFamiliesReproduced": 64, "distinctCompleteRawCharactersReproduced": 14,
        "exactSourceRowMetadataAndUnicodeRadicalVerified": True,
        "baselineArticlesUnchanged": len(baseline["inventory"]) - len(changed),
        "baselineArticlesExactlyEdited": sorted(changed),
        "runtimeAdditions": additions, "noOtherRuntimeChanges": True,
        "fullReadingsAudited": 3, "selectedKeys": 2, "sourceOnlyKeysOffered": 0,
        "sourceSenseRestrictionsChecked": True, "allMappedPairs": len(all_pairs),
        "requiredLinkDirectionsPresent": direction_count, "activatedBaselinePairs": len(activated),
        "directWordPairsVerified": 8, "directKanjiPairsVerified": 4,
        "pinned13StrokeConversionExact": True, "manifestFresh": True,
        "contentVersion": manifest["contentVersion"],
        "independentReviewersLaunched": 0, "androidOrNativeExecuted": False,
        "limits": "Mechanical unpublished draft audit. No independent linguistic, production-option, rendered, native, physical-phone, handwriting-model, general-release or publication acceptance.",
    }
    save(S / (PREFIX + "runtime-draft-audit-861.json"), result)
    print(json.dumps(result, ensure_ascii=True))


def fonts():
    from fontTools.ttLib import TTFont

    current()
    paths = ["kanji/\u52e7.md", "words/\u52e7\u544a.md", "words/\u52e7\u3081\u308b.md", "kanji/\u544a.md"]
    han = sorted({c for name in paths for c in (R / name).read_text(encoding="utf-8")
                  if "\u4e00" <= c <= "\u9fff"})
    prepared = load(S / (PREFIX + "font-preparation.json"))
    results = []
    for row in prepared["bundledFonts"]:
        path = A / "app" / "src" / "main" / "res" / "font" / row["font"]
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        assert missing == ["\u96b9"], missing
        results.append({"font": row["font"], "sha256": row["sha256"], "missing": missing})
    result = {
        "schemaVersion": 1, "batch": "108", "execution": 861,
        "scope": paths, "han": han, "distinctHan": len(han), "bundledFonts": results,
        "nativeInspectionModes": ["default/system", "all three bundled production fonts"],
        "fallbackInspectionTargets": ["\u96b9"],
        "actualNativeInspection": False,
        "limits": "Cmap coverage only, not readability, fallback-face identification or phone/native acceptance. Recompute inventory if teaching changes.",
    }
    save(S / (PREFIX + "runtime-font-audit-861.json"), result)
    print(json.dumps(result, ensure_ascii=True))


def selftest():
    import unittest
    from unittest.mock import patch

    plan = load(S / (PREFIX + "source-completion-plan.json"))
    pairs = {tuple(p) for p in plan["linkPlan"]["allMappedPairs"]}
    before_manifest = json.loads(base_file(R, plan["baseCommit"], "manifest.json"))
    manifest = load(R / "manifest.json")
    additions = plan["linkPlan"]["runtimePathsToAddLater"]
    edits = plan["linkPlan"]["exactReusedChanges"]
    changed = {row["article"] for row in edits}
    original_read = Path.read_text

    class DraftInvariants(unittest.TestCase):
        def test_actual_reused_and_new_support_all_six_directions(self):
            self.assertEqual(verify_link_directions(R, plan["linkPlan"], pairs), 6)

        def test_missing_reused_backlink_rejected(self):
            def read(path, *args, **kwargs):
                text = original_read(path, *args, **kwargs)
                if path == R / "words" / "\u52e7\u3081\u308b.md":
                    text = text.replace("](../kanji/\u52e7.md)", "]")
                return text
            with patch.object(Path, "read_text", read), self.assertRaises(AssertionError):
                verify_link_directions(R, plan["linkPlan"], pairs)

        def test_existing_component_direction_cannot_be_omitted(self):
            mapping = copy.deepcopy(plan["linkPlan"])
            mapping["requiredDirections"] = [
                row for row in mapping["requiredDirections"] if row["from"] != "kanji/\u544a.md"
            ]
            with self.assertRaises(AssertionError):
                verify_link_directions(R, mapping, pairs)

        def test_exact_additive_reused_edits_only(self):
            name = "words/\u52e7\u3081\u308b.md"
            old = base_file(R, plan["baseCommit"], name)
            new = (R / name).read_text(encoding="utf-8")
            rows = [r for r in edits if r["article"] == name]
            guards = ["\u63a8\u85a6", "\u63d0\u6848"]
            reused_changes(old, new, rows, guards)
            with self.assertRaises(ValueError):
                reused_changes(old, new.replace("jlpt: 3", "jlpt: 1"), rows, guards)
            with self.assertRaises(ValueError):
                reused_changes(old, new + "\nUnrecorded teaching edit.\n", rows, guards)

        def test_unrecorded_baseline_or_extra_support_changes_rejected(self):
            runtime_delta(before_manifest, manifest, additions, changed)
            for name in ("words/\u63a8\u85a6.md", "strokes/\u544a.json"):
                altered = copy.deepcopy(manifest)
                altered["files"][name] = "0" * 64
                with self.assertRaises(ValueError):
                    runtime_delta(before_manifest, altered, additions, changed)
            altered = copy.deepcopy(manifest)
            altered["files"]["words/unplanned.md"] = "0" * 64
            with self.assertRaises(ValueError):
                runtime_delta(before_manifest, altered, additions, changed)

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DraftInvariants))
    assert result.wasSuccessful()


NEXT = (
    "SAME108 next bounded independent TEXTUAL content review checkpoint on the normally signed clean "
    "LOCAL UNREVIEWED draft recorded in execution-861.json; no publication/109. New kanji 勧, necessary "
    "勧告かんこく, reused N3 勧める componentlink plus additive 推薦/提案 wordguards, and sourced N3告 "
    "Commonwords backlink. Read all four articles and exact diff; include all metadata/quiz labels, "
    "source restrictions and full readings in both independent reviewers' scope. Preserve fullon[カン,ケン]/"
    "fullkun[すす.める], selectedカン/すす.める; ケン source-only for lack of established usable example, NOT "
    "invalid/obsolete/rare. Source64completefamilies/14rawcharacters/fivefrozeninputs/bothXMLhashes "
    "reproduced; ALL3mappedpairs6directions/1activatedbaselinepair; thirteenpinnedstrokes exact. "
    "Equivalent exact-current runtime audit and five bounded regressions passed, NOT generic CLI acceptance; "
    "generic empty-reused restriction preserved without fake legacy ledger/tooling change. 431Python tests, "
    "validator/freshmanifest/vocabularyconsistency/originalbudgets passed; coverage2122/2431pilot remains "
    "incomplete. Actual fourarticle48Han/threebundledcmaps: 隹 absent each; explicit fourmode nativefallback "
    "target, not glyphfailure/waiver. No reviewers/HOST/native/rendered/publication at861. "
    "Select actual available models from currentCLIcatalog, two DIFFERENT families with blind common "
    "snapshot/scope/sourceaccess, one isolated headless read-only reviewer at a time, actual exit before "
    "next, SERIAL internal tools/complete original reports/actualmodels/session and returnedrange audits. "
    "Use explicit approved control --add-dir and narrow owner metadata-read grant only; no broad "
    "approvals/permissions inherited into reviewer shells. Preserve/report/yield actual newdenial, no "
    "reroute/bypass. Reconcile evidence, bounded originalsession changedpassage confirmations as needed. "
    "Then qualified signed whollyclean bf30Android non-skippedHOST, actual production option samples "
    "All/N1/custom/reduced/guarded older orientations/shortpools; native full ContentSync ONCE/meaning/"
    "curatedreading/drawing/articles/Back/offline/fourfonts and both serial originalfamily rendered gates. "
    "Latestmain nonrewriting integration/changedteaching rereview/combined exactsource-membership-baseline-"
    "readings-quiz-ALLlinks-strokes-fonts/Python-vocab-validator-freshmanifest-budgets; normal signing/"
    "ownerfastforward/exactterminalgreenCI/EVERYimmutableZIP runtimehash/perfile-media-safepath/"
    "18000entries42MiBcompressed80MiBinflated56MiBretained/verifiedownerissue before delivery or109. "
    "Preserve FULLlivehistory/792correction/all prior denials/OOMs/accepted publications and unresolved "
    "定/違,支払う/支払,勘/識,勅/訓. Recovered siblings only; committedsources/approvedinputs/controlhelpers, "
    "no optional historicalsessionrecipes. Authenticate live launcher ancestry/session/currentcheckpoint/"
    "exactsignedheads/clean-accountedstate. Parent owns runner.lock; NOchildreacquire/delete/unlock/readprobe. "
    "Preserve/report/yield signinghang/uncertainownership; no signingretry/guardchanges/concurrentheavywork/"
    "authoragents/secondrunner. Published134/1228,remaining1094 unchanged; six earlier-level dispositions "
    "are not issue60acceptancecredit. Compatible clients125/132 required; physicalphone/handwritingmodel/"
    "generalrelease/whole-setacceptance outstanding; project incomplete."
)


def seal():
    current()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    tests = (L / "python-tests-861.txt").read_text(encoding="utf-8-sig")
    selftests = (L / "audit-selftests-861.txt").read_text(encoding="utf-8-sig")
    assert "Ran 431 tests" in tests and "\nOK\n" in tests
    assert "Ran 5 tests" in selftests and selftests.rstrip().endswith("OK")
    assert "0 error(s)" in (L / "validate-861.txt").read_text(encoding="utf-8-sig")
    budget = (L / "budget-861.txt").read_text(encoding="utf-8-sig")
    assert "'entries': 8499" in budget
    audit_result = load(S / (PREFIX + "runtime-draft-audit-861.json"))
    assert audit_result["manifestFresh"] and audit_result["noOtherRuntimeChanges"]
    assert audit_result["contentVersion"] == build_manifest(R)["contentVersion"]
    font = load(S / (PREFIX + "runtime-font-audit-861.json"))
    assert font["distinctHan"] == 48 and not font["actualNativeInspection"]
    plan = load(S / (PREFIX + "source-completion-plan.json"))
    for suffix in ("membership.json", "progress.json"):
        state = load(S / (PREFIX + suffix))
        state.update(
            status="local-unreviewed-runtime-draft",
            drafted=["\u52e7"], reviewClosed=[], published=[],
            runtimeChanged=True, runtimePublished=False,
            runtimeDraftAudit=PREFIX + "runtime-draft-audit-861.json",
            runtimeFontAudit=PREFIX + "runtime-font-audit-861.json",
            draftRecord=PREFIX + "runtime-draft-861.json",
            limits="Local unreviewed draft only. Both independent families, HOST/native/rendered/integration/publication gates remain; no accepted coverage.",
        )
        save(S / (PREFIX + suffix), state)
    draft = {
        "schemaVersion": 1, "batch": "108", "execution": 861,
        "status": "local-unreviewed-runtime-draft",
        "baseCommit": plan["baseCommit"], "sourcePreparationCommit": HEAD,
        "membership": ["\u52e7"], "sourceRows": [119],
        "runtimeAdditions": plan["linkPlan"]["runtimePathsToAddLater"],
        "baselineRuntimeEdits": plan["linkPlan"]["exactReusedChanges"],
        "sourceCompletionPlan": PREFIX + "source-completion-plan.json",
        "sourceCompletionAudit": PREFIX + "source-completion-audit.json",
        "runtimeAudit": PREFIX + "runtime-draft-audit-861.json",
        "genericAuditDisposition": "Not claimed: legitimate reused support is outside its supported empty-reused schema. Exact-current equivalent audit uses shared proven checks plus complete pinned-source reproduction and five bounded regressions.",
        "sourceFullReadings": {"onyomi": ["\u30ab\u30f3", "\u30b1\u30f3"], "kunyomi": ["\u3059\u3059.\u3081\u308b"]},
        "curatedReadings": {"quizOnyomi": ["\u30ab\u30f3"], "quizKunyomi": ["\u3059\u3059.\u3081\u308b"]},
        "readingDispositions": plan["kanjiPlan"]["readingRows"],
        "allMappedPairs": plan["linkPlan"]["allMappedPairs"],
        "activatedBaselinePairs": plan["linkPlan"]["activatedBaselinePairs"],
        "strokePaths": 13, "pointsPerPath": 16, "exactPinnedConverterOutput": True,
        "contentVersion": audit_result["contentVersion"],
        "manifestRawSha256": sha((R / "manifest.json").read_bytes()),
        "runtimeFiles": [
            {"path": name, "sha256": sha((R / name).read_bytes())}
            for name in sorted(set(plan["linkPlan"]["runtimePathsToAddLater"])
                               | {e["article"] for e in plan["linkPlan"]["exactReusedChanges"]}
                               | {"manifest.json"})
        ],
        "reviewScope": {
            "wholeArticles": ["kanji/\u52e7.md", "words/\u52e7\u544a.md", "words/\u52e7\u3081\u308b.md", "kanji/\u544a.md"],
            "changedReusedPassages": plan["linkPlan"]["exactReusedChanges"],
            "facets": ["correctness", "scoped coverage", "phone comprehensibility"],
            "include": "All new teaching, complete relevant lexical restrictions, full/selected reading dispositions, displayed labels and direct word/kanji guards; preserved reused identity and easier levels.",
            "independentReviewsStarted": 0,
        },
        "fontAudit": PREFIX + "runtime-font-audit-861.json",
        "runtimePublished": False, "pushed": False,
        "limits": "Unreviewed source-backed draft, not independent review or production-option/native/rendered/phone/handwriting-model/general-release/publication acceptance.",
    }
    save(S / (PREFIX + "runtime-draft-861.json"), draft)
    for suffix, source_path in (
        ("draft-861.py", Path(__file__)),
        ("draft-checks-861.ps1", C / "checks-batch-108-draft-861.ps1"),
        ("draft-post-861.ps1", C / "post-batch-108-draft-861.ps1"),
        ("draft-issue-template-861.txt", C / "batch-108-draft-861-issue-template.txt"),
    ):
        destination = S / (PREFIX + suffix)
        assert not destination.exists()
        shutil.copyfile(source_path, destination)
    for name in ("preflight", "audit-selftests", "python-tests", "validate", "manifest",
                 "budget", "vocabulary", "fonts", "audit", "whitespace"):
        extension = "json" if name == "preflight" else "txt"
        path = L / f"{name}-861.{extension}"
        destination = S / (PREFIX + f"checks-861-{name}.{extension}.gz")
        assert path.exists() and not destination.exists()
        destination.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        assert gzip.decompress(destination.read_bytes()) == path.read_bytes()
    evidence = [
        {"path": path.relative_to(R).as_posix(), "sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}
        for path in sorted(S.glob(PREFIX + "*"))
    ]
    record = {
        "schemaVersion": 1, "execution": 861, "batch": "108",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "startingCommit": HEAD, "publishedBaseCommit": PUBLIC, "androidHead": APP,
        "status": "local-unreviewed-runtime-draft-awaiting-independent-two-family-review",
        "membership": ["\u52e7"], "sourceRows": [119],
        "draftRecord": PREFIX + "runtime-draft-861.json",
        "runtimeAudit": PREFIX + "runtime-draft-audit-861.json",
        "sourcePreparationComplete": True, "sourceFamiliesReproduced": 64,
        "rawCharacterRecordsReproduced": 14, "fullReadingsAudited": 3,
        "selectedReadingKeys": 2, "sourceOnlyKeysOffered": 0,
        "allMappedPairs": 3, "requiredDirectionsPresent": 6, "activatedBaselinePairs": 1,
        "pinned13StrokeConversionExact": True, "actualRuntimeHan": 48,
        "bundledFontsChecked": 3, "cmapAbsentNativeTarget": ["\u96b9"],
        "pythonTests": 431, "equivalentAuditRegressionTests": 5,
        "validatorManifestBudgetVocabularyPassed": True,
        "vocabularyCoverageLimit": "Existing pilot coverage2122/2431, not complete coverage or a claim that unrelated baseline gaps were fixed.",
        "publishingBudget": {
            "entries": 8499, "retainedBytes": 44874747, "inflatedBytes": 45146057,
            "localZipBytes": 30400092, "allOriginalLimitsPreserved": True,
            "immutablePublicArchiveVerified": False,
        },
        "preflightGuardCorrection": "First start assertion expected clear-text runner.ps1 in the actual EncodedCommand. It failed before saving/authoring; decoding UTF-16LE authenticated the same expected parent and script. No denial, lock access, permission or launcher change; original failed tool output preserved in this execution log.",
        "helpersLocation": "Approved control; exact helper/wrapper copies archived in this source packet.",
        "runtimeChanged": True, "runtimePublished": False, "pushed": False,
        "independentReviewersLaunched": 0, "androidOrNativeExecuted": False,
        "publishedAdditions": 134, "remainingAdditions": 1094,
        "parentLockTouched": False, "fullHistoryBefore": str(L / "progress-before-861.json"),
        "evidence": evidence, "nextAction": NEXT,
        "limits": draft["limits"],
    }
    assert not (S / "execution-861.json").exists()
    save(S / "execution-861.json", record)
    print("Local UNREVIEWED draft evidence sealed for normal signing; no push or review acceptance.")


def finish():
    p = current()
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert build_manifest(R) == load(R / "manifest.json")
    record = load(S / "execution-861.json")
    for item in record["evidence"]:
        assert sha((R / item["path"]).read_bytes()) == item["sha256"], item["path"]
    draft = load(S / (PREFIX + "runtime-draft-861.json"))
    for item in draft["runtimeFiles"]:
        assert sha((R / item["path"]).read_bytes()) == item["sha256"], item["path"]
    expected_runtime = {item["path"] for item in draft["runtimeFiles"]}
    changed = git("diff", "--name-only", HEAD, head).splitlines()
    assert {name for name in changed if not name.startswith("docs/")} == expected_runtime
    assert all(name in expected_runtime or name.startswith("docs/n1-sources/batch-108-")
               or name == "docs/n1-sources/execution-861.json" for name in changed)
    assert sha((S / (PREFIX + "draft-861.py")).read_bytes()) == sha(Path(__file__).read_bytes())
    issue = load(L / "issue-receipt-861.json")
    assert issue["verified"] and issue["author"] == "stop-cran" and issue["localCommit"] == head
    before = copy.deepcopy(p)
    p["execution861StartingState"]["status"] = "signed-local-unreviewed-runtime-draft-checkpoint-complete"
    checkpoint = {
        "execution": 861, "batch": "108", "status": "continue",
        "signedLocalCommit": head, "signature": "G", "record": "docs/n1-sources/execution-861.json",
        "recordSha256": sha((S / "execution-861.json").read_bytes()),
        "membership": ["\u52e7"], "sourcePreparationComplete": True,
        "localRuntimeDrafted": True, "independentReviewsStarted": 0,
        "exactEquivalentSourceAndRuntimeAuditPassed": True, "genericCliPassClaimed": False,
        "pythonTests": 431, "auditRegressionTests": 5, "runtimeChanged": True,
        "runtimePublished": False, "pushed": False, "publishedAdditions": 134, "remainingAdditions": 1094,
        "issueUpdate": issue["url"], "ownerAuthorAndBodyAndUrlVerified": True,
        "parentLockTouched": False, "nextAction": NEXT,
    }
    p["execution861CoordinatorCheckpoint"] = checkpoint
    p.update(checkpoint=861, status="continue",
             stage="batch-108-local-unreviewed-draft-awaiting-independent-two-family-textual-review",
             nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker", "execution861StartingState"}
    for key in before:
        if key not in allowed:
            assert p[key] == before[key], key
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p and len(p) == len(before) + 1
    print(json.dumps(checkpoint, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["start", "geometry", "audit", "fonts", "selftest", "seal", "finish"])
    args = parser.parse_args()
    globals()[args.mode]()
