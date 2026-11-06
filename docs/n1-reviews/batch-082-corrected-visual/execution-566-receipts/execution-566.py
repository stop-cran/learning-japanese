import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("visual", C / "review-batch-082-visual.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
N = R / "docs" / "n1-reviews" / "batch-082-native-corrected"
V = R / "docs" / "n1-reviews" / "batch-082-corrected-visual"
WORK = C / "batch-082-corrected-visual-execution-566"
REQUEST = C / "logs" / "123437d1-7825-4f8e-8097-41b2f2d3d57e" / "request.txt"
HEAD = "86c77107638e0adf2aa2752c50533124c389b371"
TEACHING = "9ce870d190d5c519d65ed20b118de64371350c0c"
AH = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
E = R / "docs" / "n1-sources" / "execution-566.json"
load, save, sha, now = v.load, v.save, v.sha, v.now
STAGE = "batch-082-corrected-visual-confirmed-awaiting-combined-publication"
NEXT = (
    "SAME082 combined-current-main acceptance and authorized publication NEXT, then persist/yield "
    "before083. Start signed execution566 and docs/n1-reviews/batch-082-corrected-visual/"
    "reconciliation.json. Two serial original-family dependent corrected-runtime visual confirmations "
    "ClaudeOpus5.5 session1c5aebb9-9903-4567-a88a-5da4b472781d then GPT6.1Sol "
    "sessionfd9a447c-6e9f-4874-a043-4851de97c996; complete original reports, per-turn observations, "
    "actual returned image bytes/model/process exits preserved. No new blind initial or upstream "
    "dictionary review. Source082-V1 resolved9ce870d1; corrected runtime d82e7fefe3898a70 "
    "native565 two cases terminal0/no skips, exact default four准/冴/冶/隼/no倣/no fallback and "
    "both-family changed-runtime visual closure. Scope defaultfour N1/All allvalidcandidates only; "
    "custom/partial/larger/futurepools not certified; rare准える not invalidated. "
    "Preserve old559/560/561 uncorrected reports and all original source/lookup/citation/readdepth/"
    "denial/OOM/process/viewport/fallback/MLKit limits. Inherit563HOST3+1+5/no skips/564compile/"
    "565native honestly; no redundant HOST/native/blindinitial rerun absent new concern. "
    "Full productionContentSync ONCE1094kanji5050words114N1/zeroProblems/acceptedepoch1; "
    "Full+Lite soleジュン/kun[] andじゅん key;34Han/fourfamilies136individual+4wholewordrasters/"
    "3Composepanels. Complete准/准教授 plus exact教bullet/助教授successor paragraph/"
    "sixlinkdirections/SystemBack/offline/N1selection/meaning/singleon/10stroke injectedtrace/"
    "giveuprecall NOT humanmemory/recognition/MLKitdownload/phone. QualifiedTESTONLYAndroid"
    "1c1b7bf4/G preserves productionf9b59a2, not latestappmain; HOSTonly2g init NEVERnative; "
    "noapp/guestheap/guard increase. Required NEXT latestmain/nonrewritingintegration/"
    "combinedPython368/validator/vocabulary/freshmanifest/exact虎猿/baseline/link/membership/"
    "original18000entries42MiBcompressed80MiBinflated56MiBretainedguards/normal signedowner"
    "fastforward/remoteSHA/terminalgreenCI/EVERYimmutableZIPhash/verifiedownerissue60 BEFORE083. "
    "Published108/1228,remaining1120,lastPublished1f317f0762513720709ab0ca215f19ff021ca596;"
    "082NOTdelivered. Phone/generalrelease/whole-setoutstanding. Full live history, approvedworkspace/"
    "committedsources/controlhelpers only; no optionalhistoricalsessionrecipe access. "
    "Onecoordinator/oneactive reviewer/no secondrunner. Actualnewdenial/signinghang "
    "preserve/report/yield withoutworkaround."
)


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def runtime():
    m = load(R / "manifest.json")
    assert m["contentVersion"] == "d82e7fefe3898a70"
    count = 0
    for section, entries in m.items():
        if not isinstance(entries, dict):
            continue
        for name, digest in entries.items():
            raw = (R / name).read_bytes()
            if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                raw = raw.replace(b"\r\n", b"\n")
            import hashlib
            assert hashlib.sha256(raw).hexdigest() == digest, name
            count += 1
    assert count == 8372
    return {"contentVersion": m["contentVersion"], "runtimeHashesVerified": count,
            "manifestSha256": sha(R / "manifest.json")}


def frozen():
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "tools")
    f = load(V / "batch-082-visual-freeze.json")
    assert sha(Path(f["packet"])) == f["packetSha256"]
    for s in f["sources"]:
        assert sha(Path(s["path"])) == s["sha256"]
    for g in f["imageGroups"]:
        assert all(sha(N / "attempt-565" / name) == g["sha256"] for name in g["originals"])
    return f


def start():
    p = load(C / "progress.json")
    assert p["checkpoint"] == 565 and p["status"] == "continue" and p["batch"] == "082"
    assert not WORK.exists() and not V.exists()
    for root, head in [(R, HEAD), (A, AH)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)
    text = REQUEST.read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 565
    WORK.mkdir()
    V.mkdir()
    save(WORK / "progress-before.json", p)
    state = {
        "execution": 566, "batch": "082", "startedAt": now(), "startingHead": HEAD,
        "androidHead": AH, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME082 two serial original-family dependent corrected-runtime visual confirmations and normally signed local evidence checkpoint only; no native rerun, integration/publication/083 or second runner.",
        "authorization": {"requestSha256": sha(REQUEST), "bytes": REQUEST.stat().st_size,
                          "characters": len(text), "lines": len(text.splitlines()),
                          "completeFileLoadedAndCheckpointParsed": True,
                          "limits": "Entire request loaded and checkpoint decoded; operative contract, complete issue and final565 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial output-only cp1252 error occurred after complete successful decode; final checkpoint subsequently read directly."},
        "artifactPathPreflight": str(C / "authoring-artifact-path-notes.txt"),
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "dedicatedWorktreesInitiallyClean": True, **runtime(),
        "status": "corrected-dependent-visual-confirmations-in-progress",
    }
    save(WORK / "starting-state.json", state)
    p["execution566StartingState"] = state
    p.update(stage="batch-082-corrected-independent-visual-confirmations",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    for command, name in [(["--help"], "help"), (["help", "config"], "catalog")]:
        r = subprocess.run([shutil.which("copilot"), *command], capture_output=True)
        (V / f"cli-{name}-execution-566.txt").write_bytes(r.stdout)
        (WORK / f"cli-{name}-stderr.txt").write_bytes(r.stderr)
        assert r.returncode == 0
    catalog = (V / "cli-catalog-execution-566.txt").read_text(encoding="utf-8-sig")
    assert all(f'"{m}"' in catalog for m, _ in v.SESSIONS.values())
    parts = [
        f"COMMON CORRECTED-RUNTIME DEPENDENT VISUAL CONFIRMATION. Evidence HEAD {HEAD}; "
        f"corrected teaching {TEACHING}; native archivee108bbeb0fcd4fda3837d955a652f662f72fdac1; "
        "contentVersiond82e7fefe3898a70. Exact actual teaching diff and complete corrected articles "
        "below. Original source082-V1 correction has YOUR OWN prior source confirmation; "
        "runtime visual acceptance is a NEW bounded question, not presumed by that confirmation. "
        "No other report or coordinator verdict provided. Supplied fixture/terminal/route are "
        "execution evidence, not tests independently run by you."
    ]
    sources = []
    paths = [
        R / "docs" / "n1-reviews" / "batch-082-choice-actual-runtime.diff",
        *[R / "kanji" / (s + ".md") for s in ["准", "冴", "冶", "隼", "教"]],
        R / "words" / "准教授.md", R / "words" / "助教授.md",
        N / "N1Batch082CorrectedNativeTest.kt",
        N / "attempt-565" / "instrumentation.txt",
        N / "attempt-565" / "n1-082-corrected-article-route.json",
        N / "attempt-565" / "n1-082-corrected-article-tree.txt",
        N / "attempt-565" / "n1-082-corrected-font-raster.json",
        N / "attempt-565" / "execution.json",
    ]
    for path in paths:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        parts.append(f"SOURCE {path}; all {len(lines)} lines; SHA256 {sha(path)}\n" +
                     "\n".join(f"{i}: {s}" for i, s in enumerate(lines, 1)))
        sources.append({"path": str(path), "sha256": sha(path), "lines": len(lines)})
    packet = V / "batch-082-visual-source-packet.txt"
    packet.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    groups = load(N / "image-index-execution-565.json")["groups"]
    assert len(groups) == 28 and sum(len(g["originals"]) for g in groups) == 51
    save(V / "batch-082-visual-freeze.json", {
        "evidenceHead": HEAD, "reviewedTeachingSnapshot": TEACHING,
        "packet": str(packet), "packetSha256": sha(packet), "sources": sources,
        "imageGroups": groups, "originalPngs": 51, "distinctAssignedPngs": 28,
        "limits": "Exact byte aliases, not omitted distinct screenshots. Hashes establish bytes, not comprehension."
    })
    task = f"""SAME082 CORRECTED-RUNTIME dependent ORIGINAL-SESSION visual confirmation.
Evidence HEAD {HEAD}; corrected teaching{TEACHING}; corrected native archivee108bbeb/versiond82e7fefe3898a70.
This follows YOUR OWN original textual/visual/source-correction reports and findings; carry those forward. No other review/coordinator visual verdict supplied. NOT new blind linguistic initials, fresh dictionary retrieval or independently executed native tests.

Host dispatches EXACTLY ONE resource per exited CLI process/turn: complete common source packet, then28 ORIGINALPNG byte-group representatives covering51captures, then zero-tool final report. Only view is exposed; exactly ONE view each resource turn. No parallel tools, shell, delegation, edits or unassigned reads/rereads. Report denial/missing/unreadable evidence and stop.

Assess EACH new kanji准.md and word准教授.md, correctness/scopedcoverage/boundedvisualcomprehensibility, plus ONLY changed Common words准教授 bullet in reused教.md and successor-name paragraph/link in助教授.md. Four complete contextual comparison cards冴/冶/隼/教 supplied, not a new whole-card blind review. Actual source-approved diff replaces curated集/進/難 with N1available冴/冶/隼 and explains default N1/All four-choice scope; original readings/titles/meaning unchanged. Your own source082-V1 correction verdict is inherited. NEW runtime check: actual labels exactly 'quasi-; associate rank' / 'clear; sharp-minded' / 'smelt; work metals' / 'falcon' mapped to准/冴/冶/隼, NO倣/imitate/tagfallback, no label truncation, no defensible competing meaning established from existing source scope. Native exact-options assertions are supplied, not pixels alone. Old uncorrected559/560/561 artifacts remain historical; do not treat them as corrected acceptance. Rare准えるなぞらえる imitation is recognized; rarity NOT disproof, ordinary standalone frequency/learnerimpact not newly established. Defaultfour N1/All with allvalidcandidates only; custom/partial/larger/future pools remain uncertified, including prior準largerpool hypothesis.

Complete articles across scrollstates: onジュン full/selected; full/selectedkun[]; sole linkedジュン example. Rank and approval branches/批准ひじゅん; source metadata no kun, no universal denial of other dictionaries. 准 versus準 shape and nonfree spelling interchange, recognized準教授. Modifier准 + head教授;教teaching/授imparting. Associateprofessor/currentJapan versus former助教授/April2007; separate助教/助手/broader先生; not helper/halfprofessor/trainee/automaticpromotion/universalrankequivalence or准教授する. Qualified modern-shape mnemonic not etymology;10strokes/grade8/冫15 versus氵; communityN1 not official syllabus, no inferred wordlevel.

Inspect ALL34Han in three actualCompose panels/fourfamilies Gothic/Mincho/Textbook/Brush, particularly NEW冴/冶/隼 plus准/準/集/進/難 and冫/氵/辶/隹; whole准教授. 冴right牙 versus冶right台;隼lower十 versus隹. Two冫marks versus three氵;准no lower十 versus準with十. Blank/replacementboxes or misleading collapsed lookalikes matter, typeface change alone not defect. Cmapabsence NOT glyphfailure; pixels/Paint.hasGlyph/raster hashes NOT fallback-face identification.136individual+4wholewordPaint assertions are NOT140PNGreads. Prior all40font evidence inherited, not freshly reviewed.

Inspect Japanese/English/kana/examples/translations and complete text through scrollstates; signposted horizontal table left/shifted states collectively, not simultaneousallcolumns. Bothmappedpairs准↔准教授 and教↔准教授/fourdirections plus助教授↔准教授comparison/twodirections, exact教bullet/successorparagraph, SystemBack/offline supplied assertions versus actualpixels distinguished. N1selection114cards/meaningquestionandfeedback/solecuratedon/1of1Done. Full+Lite/key/persistedgoodlog come from fixture/terminal/route, not stillpixels alone.

Production ContentSync exactFULLcorrectedarchiveONCE yields1094kanji5050words114N1/versiond82e7fefe3898a70/zeroProblems/acceptedepoch1. Disposable synthetic source/postponedotherquestions/twohistoricalgoodmeaninglogs, noownerprogress/no drawingstate seeded. Both N1Batch082CorrectedGlyphTest and N1Batch082CorrectedArticleTest terminalstatus0/no skips. API35readonlyemulator5580 only, not physicalphone; ownedhelper stopped. QualifiedTESTONLYAndroid1c1b7bf4 preserves productionf9b59a2, not latestappmain.563HOST3+1+5/no skips/564compile inherited, no rerun. No HOSTonly2GiBinit in native, no heap/guard increases. Preserve originalOOM/denial/source/citation/lookup/readdepth/processlimits.

Drawing:10reference-injectedtouchstrokes, shapeonlycomparison, giveuprecall/gradepersistedonNext. NOT humanhandwriting/successfulrecall/MLKitrecognition/modeldownload; offline model unavailable displayed. No native-speaker certification/learningeffectiveness. Final combinedmain integration/publication/CI/immutableZIP and phone/generalrelease/whole-set outstanding.

Final COMPLETE report: Snapshot;Scope;Verdicts;Findings;Optional;Limits. Actual exposedmodel and exact source/imagecoverage. EACH new准/new准教授 and changed教bullet/助教授successor paragraph gets separate correctness/scopedcoverage/boundedvisualcomprehensibility CLEAN/NEEDS FIX/UNVERIFIED; unchanged source conclusions inherited. CLEAN=no established actionable scoped defect, not exhaustivecertification. Findings severity;facet;sourcefile:lines;claim/impact;remedy;evidence;confidence or none. Reconcile YOUR082-V1 runtimevisual claim against corrected evidence as resolved/partiallyresolved/unresolved; retain original reports/disagreements/optional. Distinguish pixels/suppliedexecution/phone unknowns and compressedhistory observations if any. No manufactured finding, edits, questions or nextbatch.
"""
    (V / "batch-082-visual-task.txt").write_text(task, encoding="utf-8")
    frozen()
    print("Execution566 early state and corrected source/image freeze persisted.", flush=True)


def run(family):
    v.C, v.R, v.V, v.N, v.HEAD, v.TEACHING, v.frozen = WORK, R, V, N, HEAD, TEACHING, frozen
    v.run(family, attempt="attempt-565")


if __name__ == "__main__":
    if sys.argv[1] == "start":
        start()
    elif sys.argv[1] == "run":
        run(sys.argv[2])
