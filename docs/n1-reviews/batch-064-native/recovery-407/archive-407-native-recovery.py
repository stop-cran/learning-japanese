import hashlib
import json
import re
import shutil
import struct
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace\learning-japanese")
CONTROL = ROOT.parent / "control"
START = "7c617aacb6101d3229eeb8daa3ca68abce9c2542"
NATIVE = ROOT / "docs" / "n1-reviews" / "batch-064-native"
SOURCES = ROOT / "docs" / "n1-sources"
DEST = NATIVE / "recovery-407"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(
        ["git", "--no-pager", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


assert git("rev-parse", "HEAD") == START
assert not git("diff", "--name-only", "ff6eb7893344b806bf517ebd41bf19089bed5021",
               "HEAD", "--", "kanji", "words", "strokes", "manifest.json")
index_path = NATIVE / "execution-406-artifact-index.json"
assert digest(index_path) == "83638bf17311ae74742ab9f2a12e4c95cb5938d9035f7767ac0531dc9af4bc8d"
index = load(index_path)
assert len({row["path"] for row in index["files"]}) == len(index["files"])
pngs = 0
for row in index["files"]:
    path = ROOT / row["path"]
    assert path.is_relative_to(ROOT)
    assert path.stat().st_size == row["bytes"], row["path"]
    assert digest(path) == row["sha256"], row["path"]
    if path.suffix == ".png":
        data = path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        assert list(struct.unpack(">II", data[16:24])) == row["dimensions"]
        pngs += 1
assert pngs == index["sourcePngCount"] == 55
raw_path = NATIVE / "attempt-1" / "instrumentation.txt"
assert digest(raw_path) == "a4fca3b0cbba47b2e9888612ecebdf140be12fcc47b0620d62676e464c42d97a"
raw = raw_path.read_text(encoding="utf-8")
statuses = re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", raw, re.MULTILINE)
assert statuses == ["1", "0", "1", "0"]
for name in (
    "investigationLookalikesAndRadicalVariantsAcrossFourProductionFamilies",
    "fullSingleImportOfflineInvestigationTwoPairsComparisonOnOnlyDrawingAndSystemBack",
):
    assert raw.count("INSTRUMENTATION_STATUS: test=" + name + "\n") == 2
assert "Time: 160.379\n" in raw and "OK (2 tests)" in raw
assert "INSTRUMENTATION_CODE: -1" in raw
route = load(NATIVE / "attempt-1" / "n1-064-article-route.json")
assert [route[key] for key in ("importedKanji", "importedWords", "n1Cards", "problems",
                              "archiveRequests", "acceptedReadingParserEpoch")] == [1076, 5034, 96, 0, 1, 1]
assert route["contentVersion"] == "ae05977ba66f42f5"
assert route["quizOnKeys"] == ["てい"] and route["quizKunKeys"] == []
assert route["fullOnyomi"] == ["テイ"] and route["fullKunyomi"] == []
assert route["touchInjectedReferenceStrokes"] == 11
assert route["passed"] and route["offline"] and not route["phoneEvidence"]

recovery_path = CONTROL / "batch-064-parent-cleanup-verification-recovery.json"
postrun_path = CONTROL / "execution-406-postrun-verification.json"
assert digest(recovery_path) == "c43912a5be95bbf103673eb5f3ebf80e1cb26206403000fe5a1a110f603fdb86"
assert digest(postrun_path) == "cb1ed24b7e8ad4c973fbb79a85d1c95f4c468dcffac1310afce738080ea00946"
recovery, postrun = load(recovery_path), load(postrun_path)
assert recovery["postrunVerification"] == postrun
assert recovery["parentToolExitCode"] == 0
assert postrun["contentHead"] == START and postrun["contentStatus"] == []
assert postrun["androidHead"] == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert postrun["androidStatus"] == [] and postrun["ownedProcessesRemaining"] == 0
assert "emulator-5556" in postrun["devices"] and "emulator-5580" not in postrun["devices"]
assert postrun["connections"] == [{
    "LocalAddress": "127.0.0.1", "RemoteAddress": "127.0.0.1",
    "LocalPort": 9377, "RemotePort": 5581, "State": 3, "OwningProcess": 9520,
}]
assert recovery["nativeResult"]["terminalCase0"] == 2
assert not recovery["nativeResult"]["independentVisualAcceptance"]
DEST.mkdir(exist_ok=True)
artifacts = []
for source in (recovery_path, postrun_path, Path(__file__).resolve()):
    target = DEST / source.name
    assert not target.exists(), f"Refusing to overwrite {target}"
    shutil.copyfile(source, target)
    assert source.read_bytes() == target.read_bytes()
    artifacts.append({"path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size,
                      "sha256": digest(target)})

next_action = (
    "SAME064 bounded dependent visual confirmations in ORIGINAL Claude "
    "28a561c9-9201-40a9-a3a1-c9e37c6d168a and GPT "
    "1d30e91b-c5ed-4bd0-8d74-2177b9fbb0d7 sessions, STRICTLY SERIAL; "
    "archive first process exit/report before launching second. Read execution-407.json "
    "and original406 native artifact index/attempt-1. These are dependent follow-ups, "
    "not new blind initial reviews. Preserve402 textual closure and original reports, "
    "read-depth/lookup/citation/process limits. No native or accepted404 Android rerun "
    "absent new concern; no065 or second runner. Then latest-main normal nonrewriting "
    "integration, all combined source/baseline/reading/link/font/stroke/Python/vocab/"
    "validator/fresh-manifest/original-budget checks, normal signing, owner fast-forward, "
    "public SHA/terminal green CI/every immutable public ZIP runtime hash and issue60 "
    "receipt BEFORE delivery/065. Published90/1228,1138 remain; local draft91 not delivered. "
    "Compatible Androidf9b59a2+ required; physical-phone/general-release/whole-set outstanding."
)
record = {
    "schemaVersion": 1, "execution": 407, "checkpoint": 407, "batch": "064",
    "status": "native-parent-recovery-archived-pending-original-visual",
    "startingHead": START, "reviewedTeachingSnapshot": "ff6eb7893344b806bf517ebd41bf19089bed5021",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
    "scope": "Native evidence and exact parent cleanup recovery archival only.",
    "artifactIndex": str(index_path.relative_to(ROOT)), "artifactIndexSha256": digest(index_path),
    "verifiedIndexedArtifacts": len(index["files"]), "verifiedPngHeadersAndDimensions": pngs,
    "terminalSuccessCases": 2, "durationSeconds": 160.379,
    "rawLogSha256": digest(raw_path), "actualRouteReceipt": route,
    "parentPostrunVerification": postrun, "recoveryArtifacts": artifacts,
    "original406PermissionDenialPreserved": True,
    "onlyPostrunPermissionGateParentResolved": True,
    "allPortsFreeClaim": False,
    "portQualification": recovery["portQualification"],
    "accepted404AndroidRetainedWithoutRerun": True,
    "newPngVisualReads": 0, "independentVisualAcceptance": False,
    "runtimeEditsMade": False, "nativeOrAndroidRerun": False,
    "reviewersLaunched": 0, "publicationAttempted": False,
    "publishedAdditions": 90, "remainingAdditions": 1138,
    "lastPublishedCommit": "d00bf868466437d39b0330a383de8448686b502d",
    "wholeProjectComplete": False, "nextAction": next_action,
    "limits": (
        "Fresh byte/header/terminal-result and supplied-parent-receipt verification only; "
        "not fresh native execution, independent upstream process observation or image inspection. "
        "Parent exact-command recovery is separate from original406 denial, which remains historical. "
        "Only two coordinator image reads among55 PNGs are inherited; no parent image reads. "
        "Font raster hashes do not prove readability or fallback-face identity. Textbook探偵 wraps; "
        "not all screenshots/articles visually inspected. Touch-reference tracing and recall miss "
        "are not MLKit or correct human recall. Prior049 host OOM/qualified1GiB host-only limits "
        "remain historical; native192m/576m and production guards unchanged. "
        "Connection to remote5581/PID9520 remains recorded; no all-ports-free inference. "
        "Fresh ownership guard required before any future launch. No device or process changed."
    ),
}
save(SOURCES / "execution-407.json", record)
batch_path = SOURCES / "batch-064-progress.json"
batch = load(batch_path)
batch["status"] = record["status"]
batch["nativeParentRecoveryCheckpoint"] = {
    "execution": 407, "record": "execution-407.json", "nativeTerminalCase0": 2,
    "onlyPostrunPermissionGateParentResolved": True, "original406DenialPreserved": True,
    "allPortsFreeClaim": False, "independentVisualAcceptance": False,
    "nextAction": next_action,
}
save(batch_path, batch)
progress_path = CONTROL / "progress.json"
progress = load(progress_path)
assert progress["checkpoint"] == 406 and progress["batch"] == "064"
progress["execution407StartingState"]["status"] = "verified-awaiting-normal-signed-checkpoint"
progress["execution407NativeRecoveryDraft"] = record
save(progress_path, progress)
print(json.dumps({"verifiedArtifacts": len(index["files"]), "pngHeaders": pngs,
                  "terminalCase0": 2, "parentPostrunGateResolved": True,
                  "allPortsFree": False, "record": str(SOURCES / "execution-407.json")}))
