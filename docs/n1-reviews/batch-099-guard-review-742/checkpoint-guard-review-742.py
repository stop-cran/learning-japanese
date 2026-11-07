import copy
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "31a08f01-c04c-40a3-b57e-f979dcaa5fd0"
BASE = "1ff076b11b37f2280b7b976746b788a5de842f7c"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
PREFIX = "batch-099-guard-review-742"
D = R / "docs" / "n1-reviews" / PREFIX
REC = R / "docs" / "n1-reviews" / "batch-099-guard-742-reconciliation.json"


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, value):
    assert not p.exists(), p
    p.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(p) == value


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def runtime():
    result = subprocess.check_output(
        [sys.executable, "-B", str(C / "checkpoint-native-741.py"), "runtime"],
        encoding="utf-8",
    ).strip()
    assert result == "8451"
    return 8451


def audit_reviews():
    packet = (C / (PREFIX + "-packet.txt")).read_text(encoding="utf-8")
    required = load(C / (PREFIX + "-required.json"))
    assert sha(C / (PREFIX + "-packet.txt")) == required["packet"]["sha256"]
    records, audits = {}, {}
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        r = load(C / (PREFIX + f"-{label}-execution.json"))
        assert r["actualModels"] == [model] and r["usageCurrentModel"] == model
        assert r["exitCode"] == 0 and not r["unfinishedTools"] and not r["observedToolOverlaps"]
        calls = r["toolCalls"]
        assert len(calls) == 14
        assert all(x["name"] == "view" and x["success"] and not x["truncationMarker"] for x in calls)
        expected_paths = [
            str(R / "docs" / "n1-reviews" / "batch-099-rendered-734" /
                f"batch-099-rendered-734-{label}.md"),
            str(C / (PREFIX + "-packet.txt")),
            *[x["path"] for x in required["images"]],
        ]
        assert [x["arguments"]["path"] for x in calls] == expected_paths
        for i in range(1, len(calls)):
            assert calls[i]["startedAt"] >= calls[i-1]["completedAt"]
        subprocess.run(["pwsh", "-NoProfile", "-Command",
                        f"if (Get-Process -Id {r['launcherPid']} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
                       check=True)
        raw_path = C / (PREFIX + f"-{label}.jsonl")
        report_path = C / (PREFIX + f"-{label}.md")
        assert sha(raw_path) == r["rawSha256"] and sha(report_path) == r["reportSha256"]
        events = [json.loads(s) for s in raw_path.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
        packet_id = next(e["data"]["toolCallId"] for e in events
                         if e.get("type") == "tool.execution_start" and
                         e["data"]["arguments"].get("path") == str(C / (PREFIX + "-packet.txt")))
        returned = next(e["data"]["result"]["content"] for e in events
                        if e.get("type") == "tool.execution_complete" and e["data"]["toolCallId"] == packet_id)
        nonblank = lambda text: [line for line in text.splitlines() if line.strip()]
        assert nonblank(packet) == nonblank(returned)
        audits[label] = {
            "allNonblankLinesExactlyEqualAndInOrder": True,
            "packetNonblankLines": len(nonblank(packet)),
            "returnedNonblankLines": len(nonblank(returned)),
            "strictOriginalComparison": calls[1]["exactCompletePacketReturned"],
            "originalReceiptPreserved": True,
            "diagnostic": "Historical CRLF embedded in Windows text output produced blank-line-only differences; every nonblank line returned exactly. Not byte-identical tool rendering, not truncation.",
            "actualProcessExited": True,
            "toolCalls": len(calls), "toolOverlaps": 0,
            "successfulImageCalls": 12,
        }
        records[label] = r
    assert records["claude"]["completedAt"] < records["gpt"]["startedAt"]
    for image in required["images"]:
        assert sha(Path(image["path"])) == image["sha256"]
    return records, audits


def archive():
    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD", root=A) == APP and git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    assert not git("diff", BASE, "--", "manifest.json", "kanji", "words", "strokes")
    records, audits = audit_reviews()
    assert runtime() == 8451
    strokes = load(R / "strokes" / "\u5270.json")
    assert strokes["strokeCount"] == len(strokes["strokes"]) == 11
    assert [s["id"] for s in strokes["strokes"]] == list(range(1, 12))
    svg_path = R / "docs" / "n1-sources" / "batch-099-kanjivg.svg"
    raw_svg = svg_path.read_bytes()
    assert hashlib.sha256(raw_svg.replace(b"\r\n", b"\n")).hexdigest() == "f4ceeed7d030403d1fae485978b27fd31bea68a7b3dbaac2bd2f89eb2fddb852"
    svg = ET.fromstring(raw_svg)
    paths = [e for e in svg.iter("{http://www.w3.org/2000/svg}path")
             if e.attrib.get("id", "").startswith("kvg:05270-s")]
    assert len(paths) == 11
    rec = load(REC)
    assert rec["independentRenderedReviewClosed"] and rec["changedGuardSemanticReviewClosed"]
    assert not rec["runtimeAccepted"] and not rec["runtimePublished"]
    p = load(C / "progress.json")
    assert p["checkpoint"] == 741 and p["stage"] == "batch-099-original-guard-rendered-confirmations-in-progress"
    D.mkdir()
    provenance = []

    def add(source, name=None, compress=False):
        destination = D / (name or source.name)
        assert not destination.exists()
        original = source.read_bytes()
        if compress:
            destination.write_bytes(gzip.compress(original, mtime=0))
            assert gzip.decompress(destination.read_bytes()) == original
        else:
            shutil.copyfile(source, destination)
            assert destination.read_bytes() == original
        provenance.append({"source": str(source), "archive": destination.relative_to(R).as_posix(),
                           "sourceSha256": sha(source), "sha256": sha(destination),
                           "compressed": compress, "bytes": destination.stat().st_size})

    for label in ("claude", "gpt"):
        for suffix in (".md", "-execution.json", "-usage.json", "-stderr.txt", "-active.json"):
            add(C / (PREFIX + f"-{label}" + suffix))
        add(C / (PREFIX + f"-{label}.jsonl"), PREFIX + f"-{label}.jsonl.gz", True)
        add(C / (PREFIX + f"-{label}-prompt.txt"))
    add(C / (PREFIX + "-packet.txt"), PREFIX + "-packet.txt.gz", True)
    add(C / (PREFIX + "-required.json"))
    add(C / "review-batch-099-guard-742.py")
    add(C / "checkpoint-guard-review-742.py")
    add(C / "preflight-742.ps1", "preflight-742.ps1.txt")
    for name in ("preflight-742.json", "preflight-742-before-claude.json",
                 "preflight-742-before-gpt.json", "starting-state-742.json",
                 "copilot-help-742.txt", "validate-742.txt", "manifest-742.txt"):
        add(L / name)
    add(L / "copilot-config-742.txt", "copilot-config-742.txt.gz", True)
    save(D / "supplementary-return-and-exit-audit.json", audits)
    save(D / "artifact-index.json", provenance)
    evidence = {
        "schemaVersion": 1, "execution": 742, "batch": "099",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "startingState": load(L / "starting-state-742.json"),
        "snapshot": BASE, "archiveSnapshot": "749ea11b0c9a43d13577b104cd5fe33d9e864e62",
        "qualifiedAndroidHead": APP, "contentVersion": "39eb4a86902c6dec",
        "stage": "dependent-guard-and-rendered-review-closed-awaiting-publication-gates",
        "reconciliation": REC.relative_to(R).as_posix(),
        "reviewers": [{k: record[k] for k in [
            "sessionId", "requestedModel", "actualModels", "usageCurrentModel", "startedAt",
            "completedAt", "launcherPid", "exitCode", "reportSha256", "rawSha256",
            "observedToolOverlaps", "unfinishedTools"]} for record in records.values()],
        "supplementaryPacketReturnAudit": audits,
        "artifactIndex": (D / "artifact-index.json").relative_to(R).as_posix(),
        "archivedArtifacts": len(provenance),
        "processesSerial": True, "actualProcessExitsVerified": True,
        "sourceReadScope": "13 complete selected lexical families,2 character records,4 full articles, exact teaching and guard diffs; both reviewers read own prior report and same bounded packet. Supplied source excerpts/summary, not fresh upstream retrieval or raw assertion-by-assertion review.",
        "imageReadScopePerReviewer": "2 original native741 font panels and10contact sheets for39route captures;12image reads, not41fullresolution views.",
        "independentRenderedReviewClosed": True, "changedGuardSemanticReviewClosed": True,
        "original733734Retroaccepted": False, "newBlindReviewCredit": False,
        "sourceStrokeCount": len(paths), "generatedStrokeCount": 11,
        "coordinatorAdditionalImageRead": "Original native741 drawing-trace.png; visible numbered labels1..11. Resolves no proven missing-path concern without claiming reviewer geometry verification.",
        "verifiedRuntimeHashes": 8451, "runtimeChanged": False, "manifestChanged": False,
        "freshValidationAndUnchangedRegeneratedManifest": True,
        "freshHostOrNativeExecuted": False,
        "inheritedHostNative": "Fresh HOST740 six non-skipped cases and native741 two terminalcase0 retained; no unneeded rerun for docs-only evidence.",
        "runtimeAccepted": False, "runtimePublished": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [],
        "publishedAdditions": 125, "remainingAdditions": 1103,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": "Current-main nonrewriting integration/actual combined acceptance and normal signed owner fast-forward publication gates; no100 until terminal CI and exact immutable ZIP/owner issue evidence. Old clients ignore guard; compatible-client owner testing only.",
    }
    save(R / "docs" / "n1-sources" / "execution-742.json", evidence)
    print(json.dumps({"archivedArtifacts": len(provenance), "reviewsClosed": True,
                      "runtimeAccepted": False, "runtimePublished": False}))


def finish():
    before = load(L / "progress-before-742.json")
    current = load(C / "progress.json")
    assert current["checkpoint"] == before["checkpoint"] == 741
    assert current["execution742StartingState"] == load(L / "starting-state-742.json")
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    assert not git("diff", BASE, head, "--", "manifest.json", "kanji", "words", "strokes")
    assert runtime() == 8451
    evidence = load(R / "docs" / "n1-sources" / "execution-742.json")
    for row in load(D / "artifact-index.json"):
        assert sha(R / row["archive"]) == row["sha256"]
    posted = load(L / "issue-742-posted.json")
    reread = load(L / "issue-742-reread.json")
    body = C / "batch-099-guard-review-742-issue-body.txt"
    assert posted["author"] == reread["user"]["login"] == "stop-cran"
    assert posted["bodySha256"] == sha(body)
    assert body.read_bytes().decode("utf-8") == reread["body"]
    assert reread["html_url"] == posted["url"]
    next_action = (
        f"SAME099 checkpoint742: signed LOCAL dependent review evidence HEAD{head}, "
        f"qualifiedAndroid{APP}; runtime archive749ea11b/version39eb4a86902c6dec unchanged, "
        "all8451hashes/manifest equal compiled739. Original-session dependent confirmations "
        "Claude2ac79fdb opus5.5 then GPT240faa46 gpt6.1sol BOTH actualexit0,14successful calls each/"
        "zerooverlapstarts/no unfinishedtools; actualmodels+usageconfirmed. Each read own734report/"
        "same full bounded packet(13families/2characters/4articles/exactdiff/64choices/35labels)/"
        "two ORIGINAL741fontpanels+10sheets(39thumbnails). Strict packet byte-comparisonfalse "
        "preserved; supplementaryaudit all2784nonblanklinesexact/inorder, blankline-only CRLF "
        "normalization, no truncation. Read docs/n1-sources/execution-742.json and "
        "docs/n1-reviews/batch-099-guard-742-reconciliation.json; complete rawreports/JSONL.gz/"
        "prompts/packet/catalog/exit-tool audits archived batch-099-guard-review-742. "
        "N099-FALLBACK-JOU resolved for supported compatible-client direct symmetricnontransitive "
        "guard; N099-RENDERED-PROTOCOL-734 resolved by NEW compliant confirmation, original "
        "false serialclaim/nineoverlaps/max9 preserved NOTretroaccepted. Both textual3facets/"
        "sampledsemantic/glyph/renderedCLEAN bounded scope. Claude10pathlimitation reconciled "
        "by exact11sourcepaths/generatedIDs1..11/native741assertion and coordinator fullsize "
        "drawingtrace labels1..11; not reviewer fullgeometry/humanrecall. Optionalpolish not "
        "blocking; unsampled余hypothesis/actualfallbackface/phone/rawreviewlimitations retained. "
        "Fresh validate+regeneratedunchangedmanifest+8451runtimehashcheck passed; no new HOST/native "
        "needed merely for docs-onlyevidence. HOST740sixcases/native741twoterminalcase0 retain. "
        "NEXT SAME099 current-main publication gates: fetch latest origin/main(last2d3a3fa0), "
        "normal nonrewritingmerge if advanced, inspect actualdelta/independentlyreview changed "
        "substantiveteaching, actualcombinedPython/tests/vocabulary/budget/membership/baseline/"
        "links/reading/quiz/font audits and applicable justifiedAndroid checks, normal signed "
        "review-closed checkpoint then ownercommandscoped stop-cran normalfastforwardpush only "
        "if allgatespass. Verify exactremoteSHA/terminalgreenCI/EVERY immutable GitHubZIP "
        "runtimeentryhash/18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-"
        "safepath/verifiedownerissue beforecount099/start100. No unreviewedpush. "
        "Olderclientsignorekanjiguards/curation:compatible-clientownertestingonly, "
        "notuniversalsynonymdetection/exhaustivepoolcertification/phone/generalrelease/whole-set. "
        "Current runtime NOTaccepted/published yet; delivered125/1228,remaining1103,"
        "lastpublished098d5a376ee unchanged. All originalsource/review/process/denial/OOM/history "
        "and full741nextAction preserved. Parentownsrunner.lock throughoutchildlifetime: "
        "NOchildacquire/delete/unlock/readprobe; exactsignedheads/checkpoint/whollyclean/"
        "liveancestryguardsstay. Approvedcontrol/committedsource/frozeninputs only;"
        "nooptional historicalsessionhelpers. Preserve/report/yield actualnewdenial/signinghang/"
        "uncertainownership; no secondrunner/batch100."
    )
    checkpoint = {
        "schemaVersion": 1, "execution": 742, "checkpoint": 742, "batch": "099",
        "status": "continue",
        "stage": "batch-099-dependent-guard-rendered-review-closed-awaiting-publication-gates",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "savedCommit": head, "signature": "G", "qualifiedAndroidHead": APP,
        "reviewedSnapshot": BASE, "archiveSnapshot": evidence["archiveSnapshot"],
        "evidence": "docs/n1-sources/execution-742.json",
        "reconciliation": REC.relative_to(R).as_posix(),
        "issueUpdate": posted["url"], "ownerIssueAuthorAndBodyVerified": True,
        "independentRenderedReviewClosed": True, "changedGuardSemanticReviewClosed": True,
        "dependentReviewers": 2, "newBlindReviewCredit": False,
        "processesSerialAndActualExitsVerified": True, "toolCallsPerReviewer": 14,
        "toolOverlaps": 0, "verifiedRuntimeHashes": 8451,
        "runtimeChanged": False, "manifestChanged": False,
        "freshHostOrNativeExecuted": False, "runtimeAccepted": False, "runtimePublished": False,
        "original733734Retroaccepted": False, "dedicatedWorktreesClean": True,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 125, "remainingAdditions": 1103,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "historicalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "nextAction": next_action,
    }
    after = copy.deepcopy(current)
    assert "historicalExecution741Before742Review" not in after
    assert "execution742CoordinatorCheckpoint" not in after
    after["historicalExecution741Before742Review"] = {
        key: before[key] for key in ("checkpoint", "status", "stage", "nextAction", "blocker")}
    after["execution742CoordinatorCheckpoint"] = checkpoint
    after.update(checkpoint=742, status="continue", stage=checkpoint["stage"],
                 nextAction=next_action, blocker=None)
    for key, value in before.items():
        if key not in {"checkpoint", "status", "stage", "nextAction", "blocker"}:
            assert after[key] == value, key
    save(L / "checkpoint-742.json", checkpoint)
    tmp = C / "progress.json.742-final.tmp"
    save(tmp, after)
    assert load(C / "progress.json") == current
    os.replace(tmp, C / "progress.json")
    assert load(C / "progress.json") == after
    print(json.dumps({"checkpoint": 742, "savedCommit": head, "issue": posted["url"],
                      "historicalRootKeysPreserved": len(before), "status": "continue"}))


if __name__ == "__main__":
    {"archive": archive, "finish": finish}[sys.argv[1]]()
