import ast
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
LOG = C / "logs" / "2e14dd9a-69fc-43be-9850-505c7ab3da66"
HEAD = "eb7e1b3781c707ef270b8a242c343e6cf388e2b9"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
BASE = "21a5cb1328aadd437139a6b850f07298a2e2985d"
BACKUP = C / "artifacts" / "execution-575-progress-before.json"
IDS = ["1554200", "1606270", "1297050", "1297040", "1877830", "2576510",
       "1341500", "1341510", "1341520", "2178020", "1483390",
       "1536300", "1536310", "1655600"]
NEXT = (
    "SAME083 bounded original-family changed-choice confirmations NEXT, then persist/yield; "
    "no publication/084. Signed LOCAL UNREVIEWED575 changes ONLY 凌.distractors "
    "[准,冶,次]->[准,冶,冴], manifest6dfe6a1e287ce5df. Read execution-575.json, "
    "batch-083-choice-source-evidence.json/choice-correction-audit.json/choice-font-audit.json "
    "and actual signed one-line diff versus eb7e1b37. Original batch-083-reconciliation.json/"
    "both full initial reports remain historical, NOT approval of correction. Reuse original "
    "ClaudeOpus5.5 sessionce6f8ba4-518e-42b8-b0ee-bd14d3b291e9 and GPT6.1Sol "
    "session574ee3ae-411e-4a83-b00f-89b69ac61d99 serially, actualmodel/read-depth/process-exit "
    "evidence, sameboundedpacket, originalownfindings+exactdiff/14fullfamilies/4rawrecords/"
    "actualcandidatebodies/productionmechanism. No new blind initial review absent concern. "
    "次N3/easierlevel unchanged; all三curatedIDs available N1/All, no title collisions, but "
    "staticavailability is NOT liveQuizBuilder/native or independent semantic acceptance. "
    "冴える skill/excel-at secondary sense retained, not denied; assess actual clear;sharp-minded "
    "label for 凌, do not claim universal synonym disjointness. No word titles/exclusions changed; "
    "17directguards preserved. Original失败574 articleterminal-2/glyph0/63artifacts immutable. "
    "After confirmations refresh affected HOST on exact signedAndroid1c1b7bf4/G TEST-ONLY harness "
    "atop unchangedproductionf9, full signed archive/manifest/version/newfixture/APKs under NEW "
    "names. Original573/574 versions/fixtures/archives/APKs not corrected acceptance. Assert "
    "exact凌/准/冶/冴 IDs+titles N1 AND All with no randompadding; fullproductionContentSyncONCE "
    "1095kanji5052words115N1/version6dfe6a1e287ce5df/zeroProblems/acceptedepoch1; both Full/Lite "
    "and独立persisted soleりょう/しのぐ unchanged. ActualHan now30 includingnew冴; fresh "
    "120individual+8wholeword/fourfonts/Paint/directComposePNG/legibility/lookalikes "
    "凌陵准冶冴次/冫夌阝隹 required, not old29scope. Both named corrected native cases terminal0/"
    "noskips/no-2/-3; complete3articles/two reciprocalpairs/fourdirections/SystemBack/offline/"
    "selection/meaningfeedback/bothcuratedreadings/tenstroketrace/recall/persistence retained. "
    "Injectedtrace/giveup NOT humanrecognition/MLKit/phone evidence. FreshlocalANDremote5580/5581 "
    "includingTimeWait/devices/PIDs/liveparentancestry before ownedreadonlyAVD/API35/hostGPU/"
    "-Vulkan/2048MiB2cores explicitserial launch, no shareddevice interference or alternateport, "
    "owned-only cleanup; HOSTinit NEVER native. Original serial two-family dependent visual "
    "confirmations BEFORE current-main normalmerge/combinedPython/validator/vocabulary/manifest/"
    "exactguards/baseline/link/membership/originalbudgets/normal signedownerfastforward/exactremote/"
    "terminalgreenCI/EVERYimmutableZIPhash/terminalreceipts/verifiedownerissue60 BEFORE084. "
    "Full original574 nextGate preserved in execution575 evidence; all source/reviewer/process/"
    "lookup/read-depth/viewport/fallback/MLKit/OOM/denial limits remain. Parent19008 runner.lock "
    "untouched; approvedcontrolhelpers/committedsources only, no optionalhistoricalsessionhelpers. "
    "Preserve/report/yield actualnewdenial/signinghang without workaround. Published109/1228,"
    "remaining1119/latestpublic21a5cb1328aadd437139a6b850f07298a2e2985d unchanged;083 not delivered. "
    "Physicalphone/generalrelease/whole-set outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def check_clean(root, head):
    assert git(root, "rev-parse", "HEAD") == head
    assert git(root, "log", "-1", "--format=%G?") == "G"
    assert not git(root, "status", "--porcelain")


def persist(p):
    temporary = C / "progress.575.tmp"
    assert not temporary.exists()
    save(temporary, p)
    assert load(temporary) == p
    temporary.replace(C / "progress.json")


def start():
    check_clean(R, HEAD)
    check_clean(A, APP)
    assert git(R, "rev-parse", "origin/main") == BASE
    p = load(C / "progress.json")
    assert p["checkpoint"] == 574 and p["status"] == "continue" and p["batch"] == "083"
    assert not BACKUP.exists()
    shutil.copyfile(C / "progress.json", BACKUP)
    text = (LOG / "request.txt").read_text(encoding="utf-8-sig")
    snapshot = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert snapshot["checkpoint"] == 574
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    verified = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                verified += 1
    assert verified == 8376
    state = {
        "execution": 575, "batch": "083", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": BASE,
        "scope": "SAME083 source-backed N1 distractor correction and normally signed LOCAL UNREVIEWED freeze only; no reviewer/HOST/native/integration/publication/084.",
        "request": {"sha256": sha(LOG / "request.txt"), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Operative contract, complete issue and final checkpoint inspected directly; historical middle loaded/parsed, not freshly semantically re-reviewed."},
        "runtimeManifestHashesVerified": verified,
        "runnerLockRole": "Live parent PID19008 verified as coordinator ancestor; child never opens/reacquires/deletes/unlocks runner.lock.",
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
    }
    p["execution575StartingState"] = state
    p["stage"] = "batch-083-source-backed-choice-correction-in-progress"
    p["nextAction"] = state["scope"]
    persist(p)
    before = load(BACKUP)
    assert all(p[k] == v for k, v in before.items() if k not in {"stage", "nextAction"})
    save(C / "execution-575-start.json", state)
    print("Starting scope persisted; all original historical values preserved, 8376 runtime hashes verified.")


def prepare():
    assert git(R, "rev-parse", "HEAD") == HEAD and not git(R, "status", "--porcelain")
    freeze = load(R / "docs" / "n1-source-snapshot.json")
    inputs = []
    for name, info in freeze["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"]
        inputs.append({"name": name, **info})
    raw = gzip.decompress((C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes())
    assert hashlib.sha256(raw).hexdigest() == freeze["jmdict"]["xmlSha256"]
    dictionary = ET.fromstring(raw)
    families = {e.findtext("ent_seq"): e for e in dictionary.findall("entry")}
    selected = ET.Element("JMdict")
    for identity in IDS:
        selected.append(families[identity])
    ET.indent(selected, space="  ")
    lexical = S / "batch-083-choice-jmdict.xml"
    assert not lexical.exists()
    lexical.write_bytes(ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    raw = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert hashlib.sha256(raw).hexdigest() == freeze["kanjidic2"]["xmlSha256"]
    kd = ET.fromstring(raw)
    records = {e.findtext("literal"): e for e in kd.findall("character")}
    selected = ET.Element("kanjidic2")
    selected.append(kd.find("header"))
    for char in "凌准冶冴":
        selected.append(records[char])
    ET.indent(selected, space="  ")
    character = S / "batch-083-choice-kanjidic2.xml"
    assert not character.exists()
    character.write_bytes(ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    save(S / "batch-083-choice-selection.json", {
        "entryIds": IDS, "source": "docs/n1-source-snapshot.json",
        "sourceGzipSha256": freeze["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"],
        "sourceXmlSha256": freeze["jmdict"]["xmlSha256"],
        "transformation": "Complete parsed families reserialized in explicit selection order; no fields, restrictions or senses removed.",
        "attribution": "Copyright James William Breen and EDRDG; CC BY-SA 4.0; repository NOTICE.",
    })
    save(C / "execution-575-source-preparation.json", {
        "frozenInputsVerified": inputs, "completeFamilies": IDS,
        "lexicalSha256": sha(lexical), "characterSha256": sha(character),
        "characterScope": list("凌准冶冴"),
        "status": "extracted-awaiting-author-inspection",
    })
    print("Extracted 14 complete lexical families and four complete character records from verified frozen inputs.")


def canonical(element):
    return ET.canonicalize(ET.tostring(element, encoding="unicode"), strip_text=True)


def audit():
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit as batch_audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from fontTools.ttLib import TTFont

    assert git(R, "rev-parse", "HEAD") == HEAD
    check_clean(A, APP)
    freeze = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in freeze["inputs"].items():
        path = C / "inputs" / name
        assert sha(path) == info["sha256"] and path.stat().st_size == info["bytes"]
    fresh = ET.fromstring(gzip.decompress(
        (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()))
    families = {e.findtext("ent_seq"): e for e in fresh.findall("entry")}
    packet = ET.parse(S / "batch-083-choice-jmdict.xml").getroot()
    assert [e.findtext("ent_seq") for e in packet] == IDS
    assert all(canonical(e) == canonical(families[e.findtext("ent_seq")]) for e in packet)
    kd = ET.fromstring(gzip.decompress(
        (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()))
    records = {e.findtext("literal"): e for e in kd.findall("character")}
    selected = ET.parse(S / "batch-083-choice-kanjidic2.xml").getroot()
    assert canonical(selected.find("header")) == canonical(kd.find("header"))
    assert [e.findtext("literal") for e in selected.findall("character")] == list("凌准冶冴")
    assert all(canonical(e) == canonical(records[e.findtext("literal")])
               for e in selected.findall("character"))
    for name, lines in [("batch-083-choice-jmdict.xml", 412),
                        ("batch-083-choice-kanjidic2.xml", 234)]:
        assert len((S / name).read_text(encoding="utf-8").splitlines()) == lines
    old_card = subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "show", HEAD + ":kanji/凌.md"]).decode("utf-8")
    old_card = old_card.replace("\r\n", "\n")
    new_card = (R / "kanji" / "凌.md").read_text(encoding="utf-8")
    assert old_card.count("distractors: [准, 冶, 次]") == 1
    assert new_card == old_card.replace("distractors: [准, 冶, 次]", "distractors: [准, 冶, 冴]")
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    old_manifest = json.loads(subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "show", HEAD + ":manifest.json"]))
    changed = []
    checked = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        assert entries.keys() == old_manifest[section].keys()
        for name, expected in entries.items():
            assert (sha(R / name) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)) == expected
            checked += 1
            if old_manifest[section][name] != expected:
                changed.append(name)
    assert checked == 8376 and changed == ["kanji/凌.md"]
    result = batch_audit(R, "083")
    pool = {p.stem: metadata(R, f"kanji/{p.name}") for p in (R / "kanji").glob("*.md")}
    expected = {"凌": "endure; surpass", "准": "quasi-; associate rank",
                "冶": "smelt; work metals", "冴": "clear; sharp-minded"}
    assert pool["次"]["jlpt"] == 3
    availability = []
    for name, cards in [("N1", {k: v for k, v in pool.items() if v["jlpt"] == 1}),
                         ("All", pool)]:
        ids = ["凌"] + pool["凌"]["distractors"]
        labels = {c: cards[c]["title"] for c in ids}
        assert labels == expected and len(set(labels.values())) == 4
        availability.append({"stack": name, "cards": len(cards), "expectedOptions": labels,
                             "allThreeCuratedIdsAvailable": True, "distinctDisplayedTitles": True,
                             "defaultFourFallbackSlots": 0,
                             "limits": "Static availability/uniqueness only; production runtime acceptance pending."})
    ledger = load(S / "batch-083-progress.json")
    direct_pairs = set()
    for row in ledger["wordQuizAudit"]["directExclusions"]:
        assert metadata(R, f"words/{row['word']}.md")["quiz_exclusions"] == row["exclude"]
        for other in row["exclude"]:
            direct_pairs.add(tuple(sorted((row["word"], other))))
    assert len(direct_pairs) == 17
    scope = ["kanji/凌.md", "words/凌ぐ.md", "words/凌駕.md"]
    text = "".join((R / name).read_text(encoding="utf-8") for name in scope)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    old_font = load(S / "batch-083-draft-font-audit.json")
    assert set(han) - set(old_font["actualHan"]) == {"冴"} and len(han) == 30
    fonts = []
    for info in old_font["fonts"]:
        path = Path(info["path"])
        assert sha(path) == info["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        missing = [c for c in han if ord(c) not in cmap]
        assert set(missing) == set("冫夌阝隹") and ord("冴") in cmap
        fonts.append({"path": str(path), "sha256": sha(path), "missingFromCmap": missing})
    save(S / "batch-083-choice-font-audit.json", {
        "schemaVersion": 1, "batch": "083", "scope": scope,
        "articleHashes": {n: sha(R / n) for n in scope}, "actualHan": han,
        "actualHanCount": 30, "addedSinceAttempt574": ["冴"], "fonts": fonts,
        "requiredNextNative": {"individualPaintProbes": 120, "wholeWordProbes": 8,
                               "productionFontFamilies": 4,
                               "focusedLookalikes": list("凌陵准冶冴次冫夌阝隹")},
        "limits": "Cmap and inventory only; new native/Compose PNG acceptance pending. Original29Han/116probes remain historical, not corrected-snapshot acceptance.",
    })
    attempt = R / "docs" / "n1-reviews" / "batch-083-native" / "attempt-574"
    artifacts = load(attempt / "artifact-index.json")
    for info in artifacts:
        path = attempt / info["path"]
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"], info["path"]
    assert len(artifacts) == 63
    result.update({
        "schemaVersion": 1, "execution": 575, "stage": "local-unreviewed-choice-correction",
        "startingHead": HEAD, "onlyChangedRuntimePayload": changed, "runtimeHashesVerified": checked,
        "freshlyReextractedCompleteFamilies": len(IDS), "freshlyComparedCompleteCharacterRecords": 4,
        "frozenInputsVerified": 5, "lexicalSha256": sha(S / "batch-083-choice-jmdict.xml"),
        "characterSha256": sha(S / "batch-083-choice-kanjidic2.xml"),
        "poolAvailability": availability, "directWordExclusionPairsUnchanged": 17,
        "failedAttempt574ArtifactHashesPreserved": len(artifacts),
        "currentHanCount": len(han), "newNativeIndividualProbesRequired": 120,
        "guardsNeedingFreshAcceptance": [
            "Corrected N1 and All default-four exact IDs/titles; no random replacement.",
            "Corrected full signed archive/manifest/contentVersion, fixture assertions and app/test APK hashes.",
            "Updated30Han/fourfonts/Paint/ComposePNG inventory including new冴; all original routes and assertions.",
            "Fresh affected HOST/non-skipped XML and both named corrected native terminal0 cases.",
        ],
        "originalGuardsPreservedAsHistorical": [
            "batch-083-draft-recipe.py", "batch-083-draft-audit.json",
            "batch-083-draft-font-audit.json", "batch-083-reconciliation.json",
            "batch-083-native/N1Batch083NativeTest.kt", "batch-083-native/attempt-574",
            "execution573/574 full archive, frozen APKs and verification receipts",
        ],
        "runtimePublished": False, "runtimeAccepted": False, "reviewClosed": False,
        "independentReviewersLaunched": 0, "freshHostCompileOrNativeClaimed": False,
        "limits": "Static mechanical audit only. Coordinator source assessment is not original-family confirmation or runtime acceptance. Original source/reviewer/process/lookup/denial/OOM/read-depth/viewport/fallback/MLKit limits remain.",
    })
    save(S / "batch-083-choice-correction-audit.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    result = load(S / "batch-083-choice-correction-audit.json")
    assert result["contentVersion"] == "6dfe6a1e287ce5df" and not result["runtimeAccepted"]
    receipts = {}
    for stem in ["validate", "manifest", "audit", "n1-tests", "format-tests", "budget", "vocabulary"]:
        path = LOG / f"{stem}-575.txt"
        text = path.read_text(encoding="utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8376" in text and result["contentVersion"] in text
        elif stem == "audit":
            assert json.loads(text) == result
        elif stem in {"n1-tests", "format-tests"}:
            count = 43 if stem == "n1-tests" else 82
            assert f"Ran {count} tests" in text and "OK" in text
            assert "FAILED" not in text and "skipped" not in text
        elif stem == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] == 8398 and budget["retainedBytes"] < 56 * 1024**2
            assert budget["inflatedBytes"] < 80 * 1024**2 and budget["localZipBytes"] < 42 * 1024**2
        else:
            assert text.strip() == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
        receipts[stem] = {"path": str(path), "sha256": sha(path), "completeOutput": text}
    old = load(S / "execution-574.json")
    evidence = {
        "schemaVersion": 1, "execution": 575, "batch": "083",
        "stage": "corrected-choice-local-unreviewed-awaiting-original-confirmations",
        "startingState": load(C / "execution-575-start.json"),
        "correctionAudit": result, "sourcePreparation": load(C / "execution-575-source-preparation.json"),
        "sourceEvidence": "docs/n1-sources/batch-083-choice-source-evidence.json",
        "fontEvidence": "docs/n1-sources/batch-083-choice-font-audit.json",
        "receipts": receipts, "runtimePublished": False, "runtimeAccepted": False,
        "independentReviewersLaunched": 0, "freshHostCompileOrNativeClaimed": False,
        "findingDisposition": {"id": "083-NATIVE-574-CHOICE", "status": "partially resolved",
                               "reason": "Source-backed local correction and static availability fixed; original-family confirmation and corrected runtime acceptance remain mandatory."},
        "publishedAdditions": 109, "remainingAdditions": 1119, "lastPublishedCommit": BASE,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "inheritedNextGateUnchanged": old["nextGate"], "nextGate": NEXT,
        "limits": "Bounded LOCAL UNREVIEWED corrective freeze only. Source packets and receipts are not independent review or native acceptance. All original source/reviewer/process/read-depth/viewport/fallback/MLKit/OOM/denial limits preserved. No new batch or publication.",
    }
    save(S / "execution-575.json", evidence)
    shutil.copyfile(Path(__file__), S / "batch-083-choice-recipe.py")
    print("Correction evidence and exact durable recipe archived; ready for normal signed LOCAL UNREVIEWED freeze.")


def finish():
    check_clean(A, APP)
    assert not git(R, "status", "--porcelain")
    saved = git(R, "rev-parse", "HEAD")
    assert git(R, "log", "-1", "--format=%G?") == "G"
    assert git(R, "rev-parse", "HEAD^") == HEAD and saved != HEAD
    assert git(R, "rev-parse", "origin/main") == BASE
    assert (S / "batch-083-choice-recipe.py").read_bytes() == Path(__file__).read_bytes()
    before = load(BACKUP)
    p = load(C / "progress.json")
    assert p["checkpoint"] == 574 and p["batch"] == "083"
    record = {
        "schemaVersion": 1, "execution": 575, "checkpoint": 575, "batch": "083",
        "savedCommit": saved, "signature": "G", "status": "continue",
        "stage": "corrected-choice-local-unreviewed-awaiting-original-confirmations",
        "evidence": "docs/n1-sources/execution-575.json", "contentVersion": "6dfe6a1e287ce5df",
        "androidHead": APP, "runtimeChanged": ["kanji/凌.md"],
        "runtimePublished": False, "runtimeAccepted": False, "reviewClosed": False,
        "independentReviewersLaunched": 0, "freshHostCompileOrNativeClaimed": False,
        "finding": "083-NATIVE-574-CHOICE partially resolved; confirmations/native outstanding",
        "completeSourceFamilies": 14, "completeRawCharacterRecords": 4,
        "runtimeHashesVerified": 8376, "preservedAttempt574Artifacts": 63,
        "actualHanCount": 30, "newNativeIndividualProbesRequired": 120,
        "targetedTests": 125, "publishedAdditions": 109, "remainingAdditions": 1119,
        "lastPublishedCommit": BASE, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextBatchStarted": False, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "dedicatedWorktreesClean": True, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
    }
    p.update(checkpoint=575, status="continue", stage=record["stage"], nextAction=NEXT, blocker=None)
    p["execution575CoordinatorCheckpoint"] = record
    p["batch083ChoiceCorrectionCheckpoint"] = record
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in allowed)
    persist(p)
    reloaded = load(C / "progress.json")
    assert all(reloaded[k] == value for k, value in before.items() if k not in allowed)
    save(C / "execution-575-checkpoint.json", record)
    print("Checkpoint575 persisted; full historical values preserved, signed LOCAL freeze, both dedicated worktrees clean.")


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "audit": audit, "record": record, "finish": finish}[sys.argv[1]]()
