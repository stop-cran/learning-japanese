import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
SESSION = "50f27fd4-ff59-4b08-8d2f-788dfa34050a"
L = C / "logs" / SESSION
RAW = C / "artifacts" / "batch-099-native-attempt-733"
FOLDER = R / "docs" / "n1-reviews" / "batch-099-native" / "execution-733"
HEAD = "e413b33ca170f1233cde699c2a3aef2e136d593b"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
STAGE = "batch-099-native-passed-rendered-and-fallback-reconciliation-pending"
NEXT = (
    "SAME099 bounded source-backed semantic reconciliation and serial ORIGINAL-session rendered confirmations next; "
    "NO publication/100. Read docs/n1-sources/execution-733.json and committed batch-099-native/execution-733/"
    "raw/n1-099-article-route.json plus inspection.json. Native733 BOTH named terminalcase0/no skips; owned "
    "emulator5580 parent18272/qemu28876 stopped. Exact17a4bbb9 archive/version5408632b5aa1382c productionContentSync "
    "ONCE1122kanji5073words131N1/zeroProblems/acceptedRoomepoch1,8451hashes unchanged. "
    "Coordinator inspected TWO original fontpanels and TEN indexed contact sheets covering39routePNGs: all12Han/"
    "fourproductionfamilies incl fallback刂/older剩 legible/distinguishable in bounded panels; actual fallbackface "
    "unknown. 48individual+8wordPaint probes NOT56PNGreads. Article screenshots include complementary horizontal "
    "table offsets, not all columns in oneframe; retain clipping/readdepth/phone limits. "
    "N1UI exact剰/奇/剣/享 offers TWO semantically distinct observed fallbacks, not complete authored乗/剣/則 trio; "
    "All/custom64builderrecords and896existingSEVENwordguardchecks passed structurally. "
    "CONSEQUENTIAL OPEN hypothesis: randomN1Subset seeds4/7 offer冗(superfluous;redundant) against剰"
    "(remainder;surplusamount). Titles differ but meanings may overlap; inspect COMPLETE frozen character/dictionary "
    "evidence and originalreviewers before any semantic-clean/publication claim. No automatic exclusion/renaming/"
    "algorithm change is authorized by this receipt; if genuine app mechanism needed, establish narrow prerequisite. "
    "Full/Liteジョウ +あまつさえ/あま.り/あま.る preserved, explicitquizジョウ/[] ->じょうGood/Done1andNOkun. "
    "Eleven injectedpinnedstrokes trace/recallgiveup/grade1 NOT humanhandwriting/MLKit/phone. "
    "ONE complete剰projection, exact reused過剰component/過bullet, TWO pairsFOURdirectionsONEactivatedbaselinepair/"
    "SystemBack/offline passed. Reuse originalClaude2ac79fdb-83fc-485d-8f64-6c5d7b473973 THEN "
    "GPT240faa46-7797-4c93-998e-af5db5677c98 serial bounded dependent visual confirmations, oneprocess at a time/"
    "actualexit/readlimits; not newblindreviews. No fresh native rerun absent actual changed teaching/fixture/newconcern. "
    "Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOTlatestappmain. Fresh731JVM4noskips retained. "
    "Keep all original source/review/process/denial/OOM/phone limitations; parent15692 owns runner.lock; "
    "verify live ancestry/session/checkpoint/exact signed heads/whollyclean, NOchildreacquire/delete/unlock/readprobe. "
    "Approvedcontrol/committedsources only, no optionalhistoricalsessionhelper. Preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. All latest-main nonrewritingmerge/surgicalreconciliation/changedteachingreview/"
    "combinedchecks/normalsigning/ownerfastforward/exactremote/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/"
    "18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue gates remain. "
    "Published125/1228,1103remaining unchanged. Physicalphone/generalrelease/whole-set outstanding. No100/"
    "runtimepublication/secondrunner."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "-C", str(root), "--no-pager", *args], text=True, encoding="utf-8"
    ).strip()


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    before = load(L / "runtime-hashes-before.json")
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for path, digest in entries.items():
            actual = sha(R / path) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"
            } else sha256(R / path)
            assert actual == digest == before[path], path
    assert len(before) == 8451
    assert sha(R / "manifest.json") == load(C / "progress.json")["execution733StartingState"]["manifestSha256"]
    return {"verifiedRuntimeHashes": len(before), "contentVersion": manifest["contentVersion"],
            "manifestSha256": sha(R / "manifest.json"), "manifestFreshAndUnchanged": True}


def capture():
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    receipt = load(C / "batch-099-native-attempt-733-execution.json")
    route = load(RAW / "n1-099-article-route.json")
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 2
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"]
    assert route["passed"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"],
            route["acceptedReadingParserEpoch"]) == (1122, 5073, 131, 0, 1)
    assert route["quizOnKeys"] == ["じょう"] and route["quizKunKeys"] == []
    assert len(route["directGuardBuilderChecks"]) == 896
    pools = route["productionBuilderN1AndAllExactChoices"]
    assert len(pools) == 64
    concern = [row for row in pools if any(option["kanji"] == "冗" for option in row["options"])]
    assert [(row["pool"], row["seed"]) for row in concern] == [("randomN1Subset", 4), ("randomN1Subset", 7)]
    checked_runtime = runtime()
    FOLDER.mkdir(exist_ok=False)
    shutil.copytree(RAW, FOLDER / "raw")
    shutil.copytree(C / "batch-099-native-inspection-733", FOLDER / "contact-sheets")
    recipes = FOLDER / "receipts"
    recipes.mkdir()
    provenance = []
    for path in [
        C / "prepare-execution-733.py", C / "preflight-733.ps1", C / "run-733-native.ps1",
        C / "inspect-batch-099-native-733.py", Path(__file__), C / "run-724-native.ps1",
        C / "preflight-732.ps1", L / "preflight-733.json",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
    ]:
        target = recipes / path.name
        shutil.copyfile(path, target)
        provenance.append({"source": str(path), "archive": target.relative_to(R).as_posix(), "sha256": sha(target)})
    inspection = {
        "snapshot": HEAD,
        "reviewedTeachingSnapshot": "70dfe3344d167e5152a3685b09689d73fa1cdab1",
        "reviewer": "Coordinator, GPT-6.1 Sol; not independent content-review credit",
        "actualImagesViewed": {
            "originalFontPanels": ["n1-099-font-panel-1.png", "n1-099-font-panel-2.png"],
            "contactSheets": [f"sheet-{i:02}.png" for i in range(1, 11)],
            "routeOriginalsRepresented": 39,
            "totalOriginalPngs": 41,
            "readDepth": "Two original 1080x2400 font panels via image tool; ten 1000x2260 contact sheets showing 39 route originals as thumbnails. Not 41 separate full-resolution route reads.",
        },
        "glyphInspection": {
            "scope": "乗 余 刀 刂 則 剣 剩 剰 去 字 通 過; 過剰 and剰え; Gothic/Mincho/Textbook/Brush",
            "observed": "All 12 Han and two words readable in both bounded Compose panels. 剰/older剩 differ in left block; 剰/乗 distinguishable by right刂; 剣/則 distinct left blocks; 刂 visible rather than tofu in all four rows. No blank/replacement or materially misleading glyph established in this capture.",
            "cmapAbsences": ["刂", "剩"],
            "fallbackFaceIdentified": False,
            "nativePaintIndividualProbes": 48,
            "nativePaintWholeWordProbes": 8,
            "limit": "Paint hasGlyph/nonblank/hash assertions are not legibility or actual font-face identification; no physical-phone evidence.",
        },
        "routeInspection": [
            "N1 selection shows131cards, one meaning due and one reading due. Meaning question/feedback shows 剰 and the exact labels remainder;surplusamount / strange;extraordinary / sword;double-edgedblade / enjoy;receivebenefits.",
            "The two observed N1 UI fallbacks 奇/享 have distinct displayed senses from remainder/surplus; this bounded coordinator observation does not certify every possible N1 fallback.",
            "Reading screenshot offersジョウ once; リュウ/ジュウ/ケン are wrong options. Feedback selectsジョウ, Done reports1of1; raw source readings appear in feedback prose, not additional queued questions. Actual Room logs asserted by fixture.",
            "Eleven numbered reference paths and injected tracing are visible, followed by ungraded practice and give-up recall. Handwriting model unavailable offline; no human handwriting/MLKit/successful memory recall claim.",
            "Meaning, modern-shape mnemonic, all four reading rows, curation/spelling qualifications, common words, older form and source notes rendered; exact reused過剰 component links and過 commonword link captured with Back-return positions.",
            "Reading table has explicit sideways-scroll guidance and complementary horizontal offsets; some left/right cell portions are outside individual frames. Do not equate semantics existence/assertIsDisplayed or article projection count with every character visible in one screenshot.",
        ],
        "fallbackSemanticVerdict": "UNVERIFIED pending source-backed reconciliation and original-family confirmation",
        "consequentialOpenHypothesis": {
            "id": "N099-FALLBACK-JOU",
            "status": "unresolved hypothesis; not a verified linguistic defect or accepted substitution",
            "facet": "correctness / quiz comprehensibility",
            "impact": "Random N1 subset seeds4/7 can offer 冗 superfluous;redundant against 剰 remainder;surplusamount. These semantic ranges may overlap despite distinct labels, so structural uniqueness does not establish a single defensible answer.",
            "exactNativeRecords": concern,
            "additionalEvidenceInspected": "Complete current kanji/冗.md: title superfluous;redundant; body concerns superfluous/unnecessary and wordiness. No fresh upstream dictionary retrieval for this hypothesis in733.",
            "remedy": "Inspect complete applicable frozen character/dictionary evidence and both original model reviewers. Resolve by evidence, not votes or different noun/adjective wording. No silent title renaming, invented sense division, broad exclusion or algorithm edit.",
            "confidence": "High that observed native records contain冗; linguistic ambiguity remains unadjudicated.",
        },
        "independentRenderedConfirmations": "Pending; no independent reviewer launched in733.",
        "phoneAcceptance": "outstanding",
    }
    save(FOLDER / "inspection.json", inspection)
    raw_hashes = [
        {"path": path.relative_to(FOLDER).as_posix(), "sha256": sha(path), "bytes": path.stat().st_size}
        for path in sorted(FOLDER.rglob("*")) if path.is_file()
    ]
    save(FOLDER / "artifact-index.json", raw_hashes)
    evidence = {
        "schemaVersion": 1, "execution": 733, "batch": "099", "status": STAGE,
        "startingState": load(C / "progress.json")["execution733StartingState"],
        "nativeExecution": receipt, "runtime": checked_runtime,
        "nativeRoute": {
            key: value for key, value in route.items()
            if key not in {"directGuardBuilderChecks", "productionBuilderN1AndAllExactChoices"}
        },
        "productionKanjiBuilderRecords": 64,
        "existingDirectWordGuardBuilderChecks": 896,
        "preservedDirectWordGuardPairs": 7,
        "newDirectWordGuardPairs": 0,
        "inspection": inspection,
        "artifactIndex": (FOLDER / "artifact-index.json").relative_to(R).as_posix(),
        "artifactCount": len(raw_hashes),
        "provenance": provenance,
        "nativeMechanicalChecksPassed": True,
        "independentRenderedReviewClosed": False,
        "runtimeAccepted": False, "runtimeChanged": False, "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshJvmRerun": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "publishedAdditions": 125, "remainingAdditions": 1103,
        "lastPublishedCommit": "d5a376ee2b014aae3c47c58eea47b327e44be6d2",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT,
    }
    save(R / "docs" / "n1-sources" / "execution-733.json", evidence)
    packet_path = R / "docs" / "n1-sources" / "batch-099-progress.json"
    packet = load(packet_path)
    packet["status"] = STAGE
    packet["nativeExecution733"] = {
        "evidence": "docs/n1-sources/execution-733.json",
        "terminalSuccessCases": 2, "nativeMechanicalChecksPassed": True,
        "independentRenderedReviewClosed": False, "fallbackSemanticAcceptance": "UNVERIFIED",
        "openHypothesis": "N099-FALLBACK-JOU: actual randomN1Subset seeds4/7 offer冗; source-backed adjudication pending.",
        "runtimeAccepted": False, "runtimePublished": False, "nextAction": NEXT,
    }
    packet["limits"].append(
        "733 two native terminalcase0 and coordinator PNG inspection passed within recorded limits; independent rendered confirmations and source-backed冗 fallback reconciliation remain OPEN, not full acceptance."
    )
    assert packet["reviewClosed"] == packet["published"] == []
    save(packet_path, packet)
    print(json.dumps({"evidence": "docs/n1-sources/execution-733.json",
                      "artifacts": len(raw_hashes), "runtime": checked_runtime}, indent=2))


def seal():
    p = load(C / "progress.json")
    original = load(L / "progress-before-733.json")
    assert p["checkpoint"] == 732 and p["stage"] == "batch-099-native-execution-in-progress"
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    checked_runtime = runtime()
    issue = load(L / "issue-733-reread.json")
    expected_body = (C / "batch-099-native-733-issue-body.txt").read_text(encoding="utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == expected_body
    record = {
        "schemaVersion": 1, "execution": 733, "checkpoint": 733, "batch": "099",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G",
        "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-733.json",
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "nativeMechanicalChecksPassed": True, "terminalSuccessCases": 2, "skipped": 0,
        "coordinatorViewedPngs": {"originalFontPanels": 2, "contactSheets": 10, "routeOriginalsRepresented": 39},
        "independentRenderedReviewClosed": False,
        "fallbackSemanticAcceptance": "UNVERIFIED: N099-FALLBACK-JOU",
        "ownedEmulatorStopped": True, "parentLockTouched": False,
        "runtimeAccepted": False, "runtimeChanged": False, "runtimePublished": False,
        "runtime": checked_runtime, "dedicatedWorktreesClean": True,
        "actualNewPermissionDenials": [], "optionalHistoricalHelpersAccessed": False,
        "reviewClosed": [], "published": [], "publishedAdditions": 125, "remainingAdditions": 1103,
        "lastPublishedCommit": "d5a376ee2b014aae3c47c58eea47b327e44be6d2",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    }
    p.update(checkpoint=733, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution733CoordinatorCheckpoint"] = record
    p["batch099NativeExecutionCheckpoint"] = record.copy()
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in original.items():
        if key not in allowed:
            assert p[key] == value, key
    record["originalRootKeysCompared"] = len(original)
    record["allOriginalHistoricalRootValuesPreservedExactly"] = True
    p["batch099NativeExecutionCheckpoint"] = record.copy()
    temporary = C / "progress.733.tmp"
    assert not temporary.exists()
    save(temporary, p)
    assert load(temporary) == p
    temporary.replace(C / "progress.json")
    save(L / "checkpoint-733.json", record)
    print(json.dumps(record, ensure_ascii=True, indent=2))


def pack_logs():
    packed = []
    for name in ["adb-operations.txt", "emulator-stdout.txt"]:
        path = FOLDER / "raw" / name
        data = path.read_bytes()
        compressed = path.with_suffix(path.suffix + ".gz")
        with compressed.open("xb") as stream:
            stream.write(gzip.compress(data, mtime=0))
        assert gzip.decompress(compressed.read_bytes()) == data
        packed.append({"archive": compressed.relative_to(R).as_posix(), "sha256": sha(compressed),
                       "sourceSha256": hashlib.sha256(data).hexdigest(), "losslessGzipVerified": True})
        path.unlink()
    evidence_path = R / "docs" / "n1-sources" / "execution-733.json"
    evidence = load(evidence_path)
    evidence["losslessRawLogArchives"] = packed
    evidence["diagnostics"] = [
        "Staged whitespace check identified trailing spaces in verbatim adb/emulator logs. Archived these two logs as verified lossless gzip rather than editing original evidence; original control artifacts retained."
    ]
    archived_recipe = FOLDER / "receipts" / Path(__file__).name
    shutil.copyfile(Path(__file__), archived_recipe)
    for item in evidence["provenance"]:
        if item["source"] == str(Path(__file__)):
            item["sha256"] = sha(archived_recipe)
    index = FOLDER / "artifact-index.json"
    hashes = [
        {"path": path.relative_to(FOLDER).as_posix(), "sha256": sha(path), "bytes": path.stat().st_size}
        for path in sorted(FOLDER.rglob("*")) if path.is_file() and path != index
    ]
    save(index, hashes)
    evidence["artifactCount"] = len(hashes)
    save(evidence_path, evidence)
    print(json.dumps({"packed": packed, "artifactCount": len(hashes)}, indent=2))


if __name__ == "__main__":
    {"capture": capture, "seal": seal, "pack-logs": pack_logs}[sys.argv[1]]()
