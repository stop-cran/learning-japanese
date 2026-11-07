import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("visual_base", C / "review-batch-089-visual-633.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
R, A, V = base.R, base.A, base.V
N = V / "batch-090-native" / "execution-641" / "retry1"
L = C / "logs" / "9abde9c2-6ba1-4aa8-970c-92bb2a057a53"
HEAD = "8308d49fce923789c9b2126ff71b0b581a44c849"
TEACHING = "e044e953133548dd37fdf1dba449de2f4ee7575f"
ANDROID = base.ANDROID
SESSIONS = {
    "claude": ("claude-opus-5.5", "63fa1d59-4733-497f-bc2d-b6202471619d"),
    "gpt": ("gpt-6.1-sol", "f0995652-508c-4921-a3dd-08e89e67eb46"),
}
PACKET = C / "batch-090-visual-642-packet.txt"
IMAGES = [N / "inspection" / f"contact-{i:02d}.png" for i in range(1, 12)]
IMAGES += [N / f"n1-090-font-panel-{i}.png" for i in (1, 2, 3)]
load, save, sha, git, now = base.load, base.save, base.sha, base.git, base.now


def ownership():
    command = r"""
$ErrorActionPreference='Stop'
$runner=Get-Content 'C:\Users\stop-\n1-kanji-workspace\control\runner.json' -Raw | ConvertFrom-Json
if($runner.pid -ne 19008 -or $runner.sessionId -ne '9abde9c2-6ba1-4aa8-970c-92bb2a057a53'){throw 'Runner identity uncertain'}
$p=Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
while($p -and $p.ProcessId -ne 19008){$p=Get-CimInstance Win32_Process -Filter "ProcessId=$($p.ParentProcessId)"}
if(-not $p){throw 'Expected live parent ancestry not established'}
$command=$p.CommandLine
if($command -match '(?i)-EncodedCommand\s+([A-Za-z0-9+/=]+)'){
 $command=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
}
if(-not $command.Contains('C:\Users\stop-\n1-kanji-workspace\control\runner.ps1')){throw 'Parent launcher command uncertain'}
"""
    subprocess.run(["pwsh", "-NoProfile", "-Command", command], check=True, capture_output=True)


def frozen():
    ownership()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    state = load(C / "progress.json")
    assert state["checkpoint"] == 641 and state["batch"] == "090"
    assert not git("diff", TEACHING, HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")


def prepare():
    frozen()
    assert not PACKET.exists()
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["execution641CoordinatorCheckpoint"]["savedCommit"] == HEAD
    shutil.copyfile(C / "progress.json", L / "progress-before-642.json")
    state = load(C / "progress.json")
    state["execution642StartingState"] = {
        "execution": 642, "batch": "090", "startedAt": now(),
        "startingHead": HEAD, "androidHead": ANDROID,
        "scope": "SAME090 original-session serial dependent visual confirmations; signed LOCAL evidence only; no publication/091.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request read/decoded; operative contract, complete issue and final641 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 ancestry, exact session and decoded launcher command verified; no child lock acquisition/delete/unlock.",
        "artifactPathPreflight": "Approved control helpers/inputs and committed source/evidence only; no historical session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-090-dependent-visual-confirmations"
    state["nextAction"] = "SAME090 original Claude then original GPT serial dependent visual confirmations, preserving full reports/process limits; local evidence checkpoint only."
    save(C / "progress.json", state)
    for kind, args in [("help", ["--help"]), ("config", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (C / f"batch-090-visual-cli-{kind}-642.txt").write_bytes(result.stdout)
    native = load(R / "docs" / "n1-sources" / "execution-641.json")
    for receipt in native["receipts"]:
        assert sha(R.joinpath(*receipt["archive"].split("/"))) == receipt["archiveSha256"]
    parts = [
        f"DEPENDENT VISUAL EVIDENCE: frozen signed HEAD {HEAD}; unchanged teaching {TEACHING}.",
        "Not new blind review. Native assertions below are supplied receipts, NOT reviewer-executed tests. No other reviewer's report or coordinator visual opinions are included.",
    ]
    for path in [R / "kanji" / "\u5200.md", R / "words" / "\u65e5\u672c\u5200.md",
                 N / "n1-090-article-route.json", N / "inspection" / "contact-map.json"]:
        parts.append(f"RESOURCE {path}; SHA256 {sha(path)}\n{path.read_text(encoding='utf-8-sig')}")
    parts.append("NATIVE EXECUTION RECEIPT ONLY (not coordinator visual opinions):\n" +
                 json.dumps(native["executionReceipt"], ensure_ascii=False, indent=2))
    parts.append("ONLY CHANGED REUSED PASSAGES:\n" + git(
        "-c", "core.quotepath=false", "diff", TEACHING + "^", TEACHING, "--",
        "words/\u5200.md", "words/\u5243\u5200.md", "kanji/\u65e5.md", "kanji/\u672c.md"))
    parts.append("EXACT TEACHING DIFF FROM INITIAL REVIEW TO CURRENT HEAD:\n" + git(
        "diff", TEACHING, HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json"))
    parts.append("VIEW ALL ACTUAL PNGS SERIALLY:\n" + "\n".join(map(str, IMAGES)))
    PACKET.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    save(C / "batch-090-visual-642-inputs.json", {
        "packet": {"path": str(PACKET), "sha256": sha(PACKET)},
        "images": [{"path": str(p), "sha256": sha(p)} for p in IMAGES],
        "head": HEAD, "teachingSnapshot": TEACHING,
        "baseRecipe": str(C / "review-batch-089-visual-633.py"),
        "baseRecipeSha256": sha(C / "review-batch-089-visual-633.py"),
    })
    print("Prepared", PACKET.stat().st_size, "bytes;", len(IMAGES), "images")


def make_prompt(label, model, session):
    return f"""DEPENDENT visual follow-up in your ORIGINAL session {session}, actual model {model}.
Frozen signed HEAD {HEAD}; unchanged initial teaching {TEACHING}. NOT new blind initial review.
MANDATORY: EXACTLY ONE view call PER assistant response, starting with TWO TEXT reads. Never batch text or image reads; wait for each result before requesting the next.
FIRST read ONLY your own original report {V / ('batch-090-initial-' + label + '.md')}.
In a SEPARATE subsequent response read the ENTIRE {PACKET} with forceReadLargeFiles=true.
Then view ALL FOURTEEN PNG paths at its end, ONE call per response, SERIALLY: eleven mapped whole-frame contact sheets cover all64captures; three separate original Compose font panels. Additional originals under {N} are available if legibility requires. No other reports/opinions, shell, edits, delegation or parallel calls; only view is exposed.
If vision/decoding unavailable or text truncated, disclose and recover missing ranges serially; never substitute hashes/cmap/hasGlyph for viewing.

Assess EACH new kanji\\刀.md, new words\\日本刀.md, and ONLY FOUR changed reused passages words\\刀.md:24, words\\剃刀.md:25, kanji\\日.md:48 and kanji\\本.md:37. Inherit original textual correctness/coverage unless images establish a defect; no fresh dictionary-retrieval claim.
Inspect all18 scoped Han in four production font selections Gothic/Mincho/Textbook/Brush, especially 刀 inward-starting sweep versus 力 crossing and 乃/凹/凸. 72individual+4wholewordPaint probes are recycled hashes, NOT76exported/viewedPNGs or identifiedfallbackface. Actual glyph evidence is Compose panels. No cosmetic font-uniformity requirement.
Inspect BOTH complete new article projections and ONLY four changed linked passages, not approval of unchanged legacy articles. Reading table can scroll horizontally: complementary captures expose row; assess actual readability, not static clipping alone. Raw onトウ and kunかたな,そり kept in order; onlyトウ/かたな selected, each own linked row. Source-onlyそり retained, not labelled nonexistent/archaic or independently allocated from jukujikun剃刀/かみそり. Full source and Lite equality and persisted keys are receipt evidence.
日本刀 is traditional Japanese sword noun; neutral museum/photo sentences with readings/translations. 日本 lexical country-name modifier + 刀 sword, not sun-book etymology. Both にほんとう/にっぽんとう without frequency ranking or universal sound-change/shape rule. Tool/category/subtype distinctions and modern-shape mnemonic not historical origin; source/sense correctness inherited, not new independentupstream.
FIVE mapped reciprocalpairs/TENdirections including reused刀/剃刀 and日/本, ONE direct日本刀-to-刀wordguard/SystemBack/offline. Existing刀N3/剃刀N2/鋭いguard preserved. No cutting-tool exclusion clique or rewrite of unchanged content.
Check actual pictured and supplied production N1 AND All meaning options: 刀 sword;blade versus 乃 thereupon;possessive no, 凹 concave;sunken, 凸 convex;protruding; allthreecuratedwrongcards available/zerofallback. Close own prior fallback-unverified limit ONLY for these tested configurations, not everyfuturecustompool/oldclient. All production is supplied receipt unless separately pictured.
Inspect both reading questions and alternatives: exactly onとう AND kunかたな Good/2of2done; sourceonlyそり excluded from quiz though raw reference feedback may list it. Full/Lite agreement is supplied receipt. Documented にっぽんとう is explanatory, not second primary wordquiz key.
Inspect N1selection122cards, TWO-stroke injectedtrace/practicefeedback/recallgiveup. Supplied fullarchive40bc5a55 through productionContentSyncONCE imported1113kanji5069words122N1zeroProblems/acceptedVersionceee0f79a6d394df/epoch1; BOTHnative terminalcase0/no skips. These are supplied receipts NOT your tests. Injectedtrace/giveup is NOT humanhandwriting/offlineMLKit/phone; unavailablemodel/shape-onlyfeedback explicit. Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. No new nativephone acceptance.

Return COMPLETE report: Snapshot;Scope(actual model, actual text/image reads);Verdicts(correctness/scopedcoverage/renderedcomprehensibility EACH of2newarticles plus EACH of4changedreusedpassages, identify inheritedtextual conclusions);Findings(severity;facet;file/PNG:location;claim+impact;remedy;evidence;confidence ornone);Optional;Limits.
Reconcile OWN prior limitations; preserve optional suggestions and residual uncertainty. Disclose incomplete reads, tool-resized contactsheets/originalfontpanels, not identifiedfallbackface/76PaintPNGs, API35 emulator not physicalphone/native-speaker. Preserve original textual report/provenance/readlimits; this is dependent follow-up not replacement initial review. Currentmain/combinedchecks/CI/publicZIP/publication/phone/generalrelease/whole-set remain later gates. No edits/questions/nextbatch.
"""


def run(label):
    for name in ["C", "R", "A", "V", "N", "L", "HEAD", "TEACHING", "ANDROID",
                 "SESSIONS", "PACKET", "IMAGES", "frozen", "make_prompt"]:
        setattr(base, name, globals()[name])
    source = (C / "review-batch-089-visual-633.py").read_text(encoding="utf-8")
    start = source.index("def run(label):")
    end = source.index('\n\nif __name__ == "__main__":', start)
    body = source[start:end]
    pstart = body.index('    prompt = f"""')
    pend = body.index('    prefix.with_suffix(".prompt.txt")', pstart)
    body = body[:pstart] + "    prompt = make_prompt(label, model, session)\n" + body[pend:]
    body = body.replace("batch-089-", "batch-090-").replace("-633", "-642")
    body = body.replace('"execution": 633, "batch": "089"', '"execution": 642, "batch": "090"')
    exec(compile(body, str(Path(__file__)), "exec"), base.__dict__)
    base.run(label)


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] in SESSIONS:
        run(sys.argv[1])
    else:
        raise ValueError(sys.argv[1])
