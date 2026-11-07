import importlib.util
import inspect
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
BASE = R / "docs" / "n1-reviews" / "review-batch-092-visual-664.py"
spec = importlib.util.spec_from_file_location("visual_base", BASE)
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
review.C = C
review.R = R
review.A = C.parent / "kanji-cards-android"
review.V = R / "docs" / "n1-reviews"
review.N = review.V / "batch-093-native" / "execution-672"
review.L = C / "logs" / "54bb8274-f41a-4a34-b5dc-095999ca2c5a"
review.HEAD = "66aea026e511368a236c0b427c880aa80ea7f02f"
review.TEACHING = "27663944c7217a19e7de2f363e1b31a5f13452b6"
review.PACKET = C / "batch-093-visual-673-packet.txt"
review.SESSIONS = {
    "claude": ("claude-opus-5.5", "c8c0a762-a31b-4dca-a1a0-bc010350ec18"),
    "gpt": ("gpt-6.1-sol", "feee7268-db4e-48e3-b7d6-f3568c7173b6"),
}
review.git.__kwdefaults__["root"] = R
load, save, sha, git = review.load, review.save, review.sha, review.git


def ownership():
    source = inspect.getsource(review.ownership_original).replace(
        "263029da-d7c3-4b2a-a042-b89f35767592",
        "54bb8274-f41a-4a34-b5dc-095999ca2c5a",
    )
    namespace = {"subprocess": subprocess}
    exec(compile(source, str(BASE), "exec"), namespace)
    namespace["ownership"]()


def frozen():
    ownership()
    for root, expected in [(R, review.HEAD), (review.A, review.ANDROID)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 672 and state["batch"] == "093"
    assert not git("diff", review.TEACHING, review.HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")


def prepare():
    frozen()
    assert not review.PACKET.exists()
    backup = review.L / "progress-before-673.json"
    assert not backup.exists()
    shutil.copyfile(C / "progress.json", backup)
    request = review.L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):",
        1,
    )[1])
    assert checkpoint["execution672CoordinatorCheckpoint"]["savedCommit"] == review.HEAD
    state = load(C / "progress.json")
    state["execution673StartingState"] = {
        "execution": 673, "batch": "093", "startedAt": review.now(),
        "startingHead": review.HEAD, "androidHead": review.ANDROID,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME093 original Claude then original GPT serial dependent visual confirmations; signed LOCAL evidence only; no publication/094.",
        "request": {
            "sha256": sha(request), "bytes": request.stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/JSON decoded; operative contract, complete issue and final672 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": "Live parent19008 ancestry, exact session and decoded launcher verified; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers/inputs and committed source/evidence only; no optional historical session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    state.update(
        stage="batch-093-original-session-dependent-visual-confirmations",
        nextAction="SAME093 serial original Claude then original GPT rendered follow-ups; preserve actual reports, model identity, image returns and process/tool serialization before local reconciliation. No publication/094.",
    )
    save(C / "progress.json", state)
    for name, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-093-visual-cli-{name}-673.txt").write_bytes(result.stdout)
    catalog = (C / "batch-093-visual-cli-config-673.txt").read_text(encoding="utf-8-sig")
    assert all(f'"{model}"' in catalog for model, _ in review.SESSIONS.values())
    help_text = (C / "batch-093-visual-cli-help-673.txt").read_text(encoding="utf-8-sig")
    assert "--available-tools" in help_text and "--resume" in help_text
    evidence = load(R / "docs" / "n1-sources" / "execution-672.json")
    for item in evidence["artifacts"]:
        assert sha(R.joinpath(*item["path"].split("/"))) == item["sha256"]
    images = [
        review.N / item["file"]
        for item in evidence["visualInspection"]["inspectedOriginalPngs"]
    ]
    assert len(images) == 32
    parts = [
        f"DEPENDENT VISUAL FOLLOW-UP: signed HEAD {review.HEAD}; unchanged teaching {review.TEACHING}.",
        "Not new blind initial review. No other reviewer's report or coordinator visual opinions included. Native assertions are supplied receipts, NOT reviewer-executed tests.",
    ]
    for path in [
        R / "kanji" / "\u5211.md", R / "words" / "\u5211\u4e8b.md",
        R / "kanji" / "\u4e8b.md", review.N / "n1-093-article-route.json",
    ]:
        parts.append(f"RESOURCE {path}; SHA256 {sha(path)}\n{path.read_text(encoding='utf-8-sig')}")
    parts.append("NATIVE EXECUTION RECEIPT ONLY:\n" +
                 json.dumps(evidence["executionReceipt"], ensure_ascii=False, indent=2))
    parts.append("EXACT TEACHING DIFF:\n" + git(
        "-c", "core.quotepath=false", "diff",
        "52e706b56b7fb04c134ea6894666c52f301491ba", review.TEACHING,
        "--", "kanji", "words"))
    parts.append("TEACHING DIFF BETWEEN INITIAL REVIEW AND CURRENT HEAD (empty):\n" +
                 git("diff", review.TEACHING, review.HEAD, "--",
                     "kanji", "words", "articles", "strokes", "manifest.json"))
    parts.append(
        "BASELINE LINK ACCOUNTING: original published base fe9e1a37 already had the "
        "word \u5211\u4e8b with kanji [\u5211,\u4e8b], and the \u4e8b card, but NO \u5211 card. "
        "Therefore the one activated baseline pair is \u5211/\u5211\u4e8b, NOT \u4e8b/\u5211\u4e8b. "
        "There are TWO all-mapped pairs and FOUR directions. This accounting does not change teaching."
    )
    parts.append("VIEW THESE 32 ORIGINAL PNGS IN THIS ORDER, ONE AT A TIME:\n" +
                 "\n".join(map(str, images)))
    review.PACKET.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    save(C / "batch-093-visual-673-inputs.json", {
        "packet": {"path": str(review.PACKET), "sha256": sha(review.PACKET)},
        "images": [{"path": str(p), "sha256": sha(p)} for p in images],
        "capturedPngs": 63, "assignedOriginalPngViews": 32,
        "remainingPngsNotAssigned": 31,
        "head": review.HEAD, "teachingSnapshot": review.TEACHING,
        "sourceEvidence": "docs/n1-sources/execution-672.json",
        "sourceEvidenceSha256": sha(R / "docs" / "n1-sources" / "execution-672.json"),
        "baseRecipe": str(BASE), "baseRecipeSha256": sha(BASE),
    })
    print("Prepared", review.PACKET.stat().st_size, "bytes; 32 original PNGs; historical state retained.")


def make_prompt(label, model, session):
    return f"""Resource-constrained SERIAL visual-inspection operation in your ORIGINAL session {session}, actual model {model}.
DEPENDENT follow-up, NOT a new blind initial review. Signed evidence HEAD {review.HEAD}; unchanged teaching {review.TEACHING}.
Task acceptance requires EXACTLY ONE view call per assistant message. Interpret each image before deciding to read the next; that dependency forbids batching. Do not use parallel tool calls or a wrapper. An otherwise successful report with overlapping calls is NOT accepted.
FIRST read ONLY your own original report {review.V / ('batch-093-initial-' + label + '.md')}.
In a SEPARATE subsequent assistant message read ENTIRE {review.PACKET}, forceReadLargeFiles=true, no range.
Then view ALL32 ORIGINAL PNGs listed at its end IN ORDER, ONE tool call per message, waiting for each result. No edits, shell, delegation, other reports or coordinator opinions; only view is exposed.
If vision unavailable or text truncated, disclose and recover missing ranges serially, never substitute hash/cmap/hasGlyph for viewing.

Assess EACH complete kanji\\刑.md and reused words\\刑事.md, plus ONLY added kanji\\事.md:37 reciprocal-navigation passage (whole article supplied as context, NOT fresh linguistic review of unchanged legacy prose). Inherit your own textual correctness/coverage unless images establish a defect. Reused N3刑事 identity/primaryけいじ/title/level/inbound探偵guard preserved; componentlink/four DIRECT police-label guards only. No new wordarticle. Criminalpunishment/legal sentence NOT grammaticalsentence; police-detective person vs criminalmatters modifier NOT offender. Natural witness/criminalcase/trial examples. Fullrawonケイ/emptykun, explicit[ケイ]/[]; own linked刑事 readingrow. Specialwholewordでか NOT constituentkun; publicギョウ/historical刑部省 outsidefrozenonmetadata distinguished, no undocumented *ぎょうじ. Shape mnemonic NOT history; 刀18/right刂/sixstrokes.

Inspect all46 scopedHan in FIVE actualCompose panels across FOUR production fontselections Gothic/Mincho/Textbook/Brush, especially fallbackU+4E85亅/U+5202刂/U+5F61彡, 刑/形/型 and 刀/刂/乃/凹/凸 distinction; threewholewords. 184individual+12wholewordPaint probes are NOT196exported/viewedPNGs or identifiedfallbackface. Readability/distinguishability, not uniformfontcosmetics, is the gate.
Inspect complete刑/刑事 projections and added事line using complementary original views and supplied fulltext/native-scrollassertions. Readingtable is horizontally scrollable; complementary views, not simultaneousfullcolumnvisibility, are intended. If assignedviews do not establish something, state the limitation; additional originals in {review.N} available only if needed. Selected32of63 images are NOT63freshviews; remaining31 not separately assigned. Some routeimages may be exactduplicates, not independentrenderings.
Inspect N1selection125cards, actual pictured meaningoption labels criminal punishment versus concave;sunken/convex;protruding/thereupon;possessive no. Production N1 AND All exactthreecuratedwrongcards/zerofallback are suppliedreceipt evidence unless pictured. Close ownpriorunverifiedfallbacklimit ONLY testedconfigurations, not everyfuturecustompool/oldclient; 文 uncertainty in broaderpools not universalcertification.
Inspect onlyonけい question/correctfeedback/1of1Done; NOkunkey offered. Fullrawreference readings in feedback are NOTextraofferedkeys; full/Lite equality/persistedGood keys are suppliedreceipt. Inspect sixpinnedstrokes/injectedtrace/practicefeedback/recallgiveup. ActualUI explicitlymodelunavailable/shape-onlygrading: NOThumanhandwriting/successfulMLKit/phone.
TWOallmappedpairs刑/刑事 AND事/刑事, FOURdirections; ONEactivatedbaseline刑/刑事pair (NOT事/刑事). Forward/backlink/SystemBack/offlineroute; fourdirectpolicelabelguards and inbound探偵guard are suppliedassertions, NOT a synonymclique.
Supplied fullarchive324b0bd9 through productionContentSyncONCE imported1116kanji5070words125N1zeroProblems/contentVersionbf4cc85592bb9727/acceptedRoomreadingEpoch1. TWOcases terminalpercase0/noskips; own helper5580 stopped. These are supplied receipts, not your tests. QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOTlatestappmain. No newphysicalphone acceptance.

Return COMPLETE report: Snapshot;Scope(actualmodel, actualtext/image reads);Verdicts(correctness/scopedcoverage/renderedcomprehensibility EACHarticle/passage, identify inheritedtextualconclusions);Findings(severity;facet;file/PNG:location;preciseclaim+impact;remedy;evidence;confidence ornone);Optional;Limits.
Reconcile OWN prior limitations; preserve optional suggestions/residualuncertainty. Disclose tool-resizedimages, unviewed31originals, sourceandmodelreadlimits, unverifiedfallbackface/Paintimages. API35emulator is notphysicalphone/native-speaker/measuredlearning. No newblindinitialcredit. Currentmain/combinedchecks/CI/publicZIP/publication/phone/generalrelease/whole-set remain latergates. No edits/questions/nextbatch.
"""


review.ownership_original = review.ownership
review.ownership = ownership
review.frozen = frozen
review.make_prompt = make_prompt
source = inspect.getsource(review.run).replace("batch-092", "batch-093").replace("664", "673")
source = source.replace("25 of42 original PNGs assigned", "32 of63 original PNGs assigned")
exec(compile(source, str(BASE), "exec"), review.__dict__)

if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] in review.SESSIONS:
        review.run(sys.argv[1])
    else:
        raise ValueError(sys.argv[1])
