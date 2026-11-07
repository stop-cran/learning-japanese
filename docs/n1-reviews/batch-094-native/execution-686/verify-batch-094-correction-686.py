import hashlib
import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "f980cb7f-4783-4a86-9e11-fe07ed360018"
HEAD = "5f0be6677c770b2841073c0864229e49ce1e96bd"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "74b7e886a1afbd46"
WORK = C / "batch-094-corrected-native-686"
FIXTURE = C / "N1Batch094Correction686Test.kt"
ARCHIVE = C / "artifacts" / "n1-batch-094-5f0be667-corrected-envelope.zip"
VERIFICATION = WORK / "verification.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def clean(head=HEAD):
    for root, expected in [(R, head), (A, APP)]:
        assert git(root, "rev-parse", "HEAD") == expected
        assert git(root, "log", "-1", "--format=%G?") == "G"
        assert not git(root, "status", "--porcelain", "--untracked-files=all")
    assert not git(A, "diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties")


def persist(state):
    temp = C / "progress.686.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")


def start():
    clean()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["batch"], state["stage"]) == (
        685, "continue", "094", "correction-textually-confirmed-awaiting-exact-native-import")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    role = load(L / "runner-role-686.json")
    assert role["parentAncestryVerified"] and role["launcherCommandMatches"]
    assert not (L / "progress-before-686.json").exists()
    request = (L / "request.txt").read_text(encoding="utf-8-sig")
    embedded = json.loads(request[request.index("{", request.index("Current execution checkpoint")):])
    assert embedded["checkpoint"] == 685
    save(L / "progress-before-686.json", state)
    state["execution686StartingState"] = {
        "execution": 686, "batch": "094", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git(R, "rev-parse", "origin/main"),
        "scope": "SAME094 exact corrected native single import and focused direct-pair production builder checks only; signed LOCAL evidence, no publication/095/second runner.",
        "request": {"sha256": sha(L / "request.txt"), "characters": len(request),
                    "lines": len(request.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint decoded; operative contract, complete issue and final685 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role,
        "diagnostics": [
            "Read-only runner.lock probe returned expected Windows sharing violation; no acquisition, write, deletion or unlock attempted. Parent19008 live ancestry and decoded launcher separately verified; child wrappers do not open the lock.",
            "Initial console summary cp1252 error after complete request parse; rerun UTF-8 output succeeded. Two guessed workspace paths absent; actual durable workspace recipes located. No mandatory input missing or permission denial.",
        ],
        "artifactPathPreflight": "Approved control and committed packets only; no optional historical-session helpers accessed.",
        "actualNewPermissionDenials": [],
    }
    state["stage"] = "batch-094-corrected-native-in-progress"
    state["nextAction"] = state["execution686StartingState"]["scope"]
    persist(state)
    print("Starting686 persisted; complete live history preserved.")


def prepare():
    clean()
    assert not WORK.exists() and not ARCHIVE.exists()
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest and manifest["contentVersion"] == VERSION
    subprocess.run(["git", "-C", str(R), "archive", "--format=zip", "--prefix=n1-batch-094/",
                    f"--output={ARCHIVE}", HEAD], check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) <= 18000
        assert all(n.startswith("n1-batch-094/") and "\\" not in n and ".." not in n.split("/")
                   and not n.startswith("/") for n in names)
        raw = archive.read("n1-batch-094/manifest.json")
        assert raw == (R / "manifest.json").read_bytes()
        retained, verified = len(raw), 0
        for section, group in manifest.items():
            if not isinstance(group, dict):
                continue
            for name, digest in group.items():
                data = archive.read("n1-batch-094/" + name)
                assert data == R.joinpath(*name.split("/")).read_bytes(), name
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                limit = 150 * 1024 if section in {"images", "listeningTaskImages"} else (
                    512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                assert len(data) <= limit, name
                assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == digest, name
                retained += len(data)
                verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8438 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in names)
    WORK.mkdir()
    save(VERIFICATION, {
        "execution": 686, "batch": "094", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "androidSnapshot": APP, "productionBaseline": PROD,
        "contentVersion": VERSION, "runtimeHashesVerified": verified,
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE), "zipEntries": len(names),
        "compressedBytes": ARCHIVE.stat().st_size, "inflatedBytes": inflated, "retainedBytes": retained,
        "fixture": str(FIXTURE), "fixtureSha256": sha(FIXTURE),
        "allRuntimeZipBytesEqualCheckout": True, "manifestFresh": True,
        "publicGithubZipAcceptance": False, "nativeAcceptance": False,
        "previousFixturesUnchanged": True, "productionContentSyncImportCountExpected": 1,
        "expectedBuilderChecks": 128, "guardsChanged": False, "heapsChanged": False,
    })
    print("Corrected full archive prepared; all8438 runtime bytes and hashes verified.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"start": start, "prepare": prepare}[sys.argv[1]]()
