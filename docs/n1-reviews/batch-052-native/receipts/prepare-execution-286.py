import hashlib
import json
import re
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

c = Path(__file__).parent
r = c.parent / "learning-japanese"
reviews = r / "docs" / "n1-reviews"
head = "13e8768e0822a488f372bd94b4d6c964c08474cb"
teaching = "c7aeff7cf02165bbc1ddd33384faf645920fe2bf"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    assert not path.exists(), path
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=r, text=True).strip() == head
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=r)
assert not subprocess.check_output(["git", "diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json"], cwd=r)
p = load(c / "progress.json")
assert p["checkpoint"] == 285 and p["status"] == "continue"
if "execution286StartingState" not in p:
    (c / "execution-286-progress-before.json").write_bytes((c / "progress.json").read_bytes())
    p["execution286StartingState"] = {
    "execution": 286, "batch": "052", "startingHead": head,
    "startedAt": datetime.now().astimezone().isoformat(),
    "scope": "SAME052 original Claude then GPT dependent native visual confirmations and normally signed local evidence checkpoint only; no publication,053,repeated accepted tests/blind initials or second runner.",
    "acquisition": "Complete authorized request acquired through actual EOF13380/final285checkpoint before action;1-9050 inherited,9051-13380 returned currently. BeyondEOF13451 error not evidence. Approved issue1-129 complete including truncated tail recovery123-129; actual guidance/current signed clean dedicated heads/live scoped history/original reports/retry diff/native logs inspected.",
    "status": "starting-original-visual-confirmations",
    }
    (c / "progress.json").write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
else:
    assert p["execution286StartingState"]["startingHead"] == head
native = load(reviews / "batch-052-native-execution.json")
record = load(r / "docs" / "n1-sources" / "execution-285.json")
assert all(record[k] == v for k, v in native.items())
assert record.keys() - native.keys() == {"nativeRecord", "nativeRecordSha256"}
assert sha(reviews / "batch-052-native-execution.json") == record["nativeRecordSha256"]
for row in native["evidenceIndex"]:
    assert sha(r / row["path"]) == row["sha256"], row["path"]
for label, row in zip(["claude", "gpt"], load(reviews / "batch-052-reconciliation.json")["reviewProcesses"]):
    assert sha(reviews / f"batch-052-initial-{label}.md") == row["reportSha256"]
log = (reviews / "batch-052-native" / "attempt-3" / "instrumentation.txt").read_text()
assert [int(x) for x in re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", log, re.M)] == [1, 0, 1, 0]
assert "OK (2 tests)" in log and "Time: 69.476" in log
route = load(reviews / "batch-052-native" / "attempt-3" / "n1-052-article-route.json")
assert route == native["attempts"][2]["route"]
assert route["passed"] and route["archiveRequests"] == 1 and route["problems"] == 0
assert route["fullOnyomi"] == ["ニ", "ジ"] and route["fullKunyomi"] == ["ふた.つ", "そえ"]
assert route["quizOnKeys"] == ["に"] and route["quizKunKeys"] == []
archive = Path(native["archive"]["archive"])
assert sha(archive) == native["archive"]["archiveSha256"]
with zipfile.ZipFile(archive) as z:
    manifests = [n for n in z.namelist() if n.endswith("/manifest.json") or n == "manifest.json"]
    assert len(manifests) == 1
    prefix = manifests[0][:-len("manifest.json")]
    assert z.read(manifests[0]) == (r / "manifest.json").read_bytes()
    manifest = json.loads(z.read(manifests[0]))
    count = 0
    for kind, section in manifest.items():
        if not isinstance(section, dict):
            continue
        for name, digest in section.items():
            old, current = z.read(prefix + name), (r / name).read_bytes()
            if kind not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                old, current = old.replace(b"\r\n", b"\n"), current.replace(b"\r\n", b"\n")
            assert hashlib.sha256(old).hexdigest() == hashlib.sha256(current).hexdigest() == digest, name
            count += 1
    assert count == 8283
screens = native["coordinatorVisual"]["directReads"]
pngs = [reviews / "batch-052-native" / "attempt-3" / f"n1-052-{s}.png" for s in screens]
save(c / "batch-052-recovered-evidence-verification.json", {
    "execution": 286, "verifiedAt": datetime.now().astimezone().isoformat(),
    "contentHead": head, "reviewedTeachingSnapshot": teaching,
    "runtimeAndTeachingUnchanged": True, "nativeEvidenceHashesVerified": len(native["evidenceIndex"]),
    "archiveRuntimeHashesVerified": count, "actualNativeStatusCodes": [1, 0, 1, 0],
    "sameVisualScope": [{"path": str(p), "sha256": sha(p)} for p in pngs],
    "limits": "Mechanical re-verification of accepted285 evidence, not fresh tests or independent visual inspection. Original failures and all inherited limits retained.",
})
common = f"""SAME052 bounded ORIGINAL-session dependent visual confirmation, NOT new blind initial.
Frozen current signed HEAD {head}; teaching unchanged from original reviewed {teaching}.
Envelope22f2dfa8b370cefd8227e1cf05a730b921764ef3 differs only in contributor evidence.
Use ONLY SERIAL view calls: exactly ONE tool call per response, await completion. Never parallelize.
Read this task, YOUR COMPLETE original initial report below, NOT the other reviewer's report.
Read complete current teaching in separate calls:
{r}\\kanji\\弐.md
{r}\\words\\二.md
Read exact disposable retry diff:
{reviews}\\batch-052-native\\scroll-fixture.diff
Read accepted fixture lines210-320 and375-415 separately:
{reviews}\\batch-052-native\\N1Batch052NativeScrollTest.kt
Actually view EACH of these SIXTEEN accepted attempt3 PNGs singly, ONE PER RESPONSE:
""" + "\n".join(str(p) for p in pngs) + """
Check readability/distinction 弐式武三弋 in all four actual production rows. 弐式武三 four rasters each; 弋 one readable Gothic-like fallback, actual face unknown. No requirement for four distinct fallback designs.
Check six strokes/canonical radical弋56/modern mnemonic NOT etymology; full orderedニ,ジ/ふた.つ,そえ versus sole selectedonニ/emptykun. Obsolete pronunciationじしん does not label all弐心 readings; 弐つ is old/documentary/JMdictverified but independentJapanese wholeheading unverified; そえsource-only no invented lexicalexample/practice/弐える. Check two actual 二にN5 reuse passages/backlink and preserved identity/kanji[二].
Check visible reciprocalarticle/SystemBack, meaningquestionfeedback, curatedonquestionfeedback, trace/reference/geometryfeedback/recallmiss. Separate inherited textual judgments from newly viewed screenshots and supplied operational evidence.
Supplied operational results, NOT tests run by reviewer: accepted nativeattempt3 two terminalcase0/no skips69.476s. Exact complete Git envelope through productionContentSync ONCE perarticleattempt:1064kanji5021words84N1/contentVersion601a0fb709961e28/schema1en-ja/problems0/parserEpoch1/fullrawreadings/soleon normalizedに/emptykun. Unique disposable source; otherN1postponed/twohistoricalmeaninglogs unlockdrawing; NO drawingstate seeded/noownerprogress. Meaningfeedback, soleon question/persistedgrade, SIX exactreference-touch strokes/ungradedtraceWellDrawn/recall I do not remember/persistedDrawgrade onNext/offlinereciprocalBack/20Paintprobes. Fresh283Android3+1 exactsource/copyhashes retained, not rerun or oldbatchreuse.
Originalattempt1 glyph0/article-2 nested viewport assertion failure45.608s retained. Attempt2 outboundSynSent5581 portblock/nohelper/no native retained. Retry only separateclassidentities/threeadditionalreadingrowcaptures/explicitouterverticalscrolling nestedtablecells; assertIsDisplayed and all acceptance assertions retained. Attempt3 freshportownership/knownAPI35read-onlyhostGPU-Vulkan-disabled helper5580 owned/stopped; exactAndroidtempsremoved/appclean.2048MiBrequest auto2560MB; actualmemtotal2532900kB/guestapp192m576m unchanged. Original049512MiBHOSTTestOOM/bounded1GiBHOSTcoreTest headroom is NOT nativeauthorization; no hostinit used nativecompile.
Explicit visual limits: table rightedge initiallyclipped/leftlabels clipped afterhorizontal scroll; do not certify allcolumns simultaneously/fullarticle. Actual N1 meaningfallback labels cocoon/seedling;youngplant/turtle;tortoise differ from authored式武三; judge actual visible alternatives, not authoredtrio. Trace first-use downloading-model message/geometric-onlyfeedback/modelunavailable and recallMISS retained; not MLKit recognition/realcorrectrecall/negativegeometry/reverseorder/phone evidence. Sources1080x2400 may returnresized900x2000; do NOT claim exact originalbytes/dimensions without evidence.
Initials actual29/29calls23/23resources, ONE Claude internaloverlap/zeroGPT preserved. Both textual allfacetsCLEAN, no teachingfix; threeClaudeoptional groupsnotadopted. This supplied-evidence dependent visualfollowup is not blind, fresh source retrieval/native-speaker certification/modelbenchmark or reviewer-executed tests.
Return complete Snapshot/Scope/Verdicts(each article correctness/scopedcoverage/comprehensibility)/Findings/Optional/Limits. Enumerate actualPNGreads/textranges and process deviations honestly. No finding quota. No edits/shell/delegation/search/retries/tools beyond view. Physicalphone/generalrelease/currentmain/publication/whole-set unperformed. Return FINAL REPORT, not task_complete. ONE tool call per response.
"""
for label, model, session in [
    ("claude", "claude-opus-5.5", "78592329-26fa-4c54-aa96-e6bff3a769ec"),
    ("gpt", "gpt-6.1-sol", "0ef2bb14-7846-423b-a39d-f50d6559b9fb"),
]:
    path = c / f"batch-052-visual-{label}-prompt.txt"
    assert not path.exists()
    path.write_text(f"You are original {model}, same session {session}.\nYour original report: {reviews}\\batch-052-initial-{label}.md\n" + common, encoding="utf-8")
print("Execution286 starting scope persisted; all native evidence and8283runtimehashes reverified; bounded16PNG tasks prepared.")
