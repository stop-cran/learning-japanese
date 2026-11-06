import hashlib
import json
import shutil
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
LOG = C / "logs" / "45e618f9-8a01-4bfc-99e2-7739bc2bf9f0"
HEAD = "f6f9b9425b483ed98950c67c35610caaccd6c786"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args], text=True).strip()


state = load(C / "progress.json")
assert (state["checkpoint"], state["batch"], state["status"], state["stage"]) == (
    595, "085", "continue", "native-prepared-compiled-not-executed")
request = LOG / "request.txt"
text = request.read_text(encoding="utf-8-sig")
checkpoint = json.loads(text.split(
    "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
assert checkpoint["checkpoint"] == 595
for root, head in ((R, HEAD), (A, APP)):
    assert git(root, "rev-parse", "HEAD") == head
    assert git(root, "log", "-1", "--format=%G?") == "G"
    assert not git(root, "status", "--porcelain")
evidence = load(R / "docs" / "n1-sources" / "execution-595.json")
fixture = evidence["fixtureVerification"]
assert load(C / "batch-085-native-fixture-verification.json") == fixture
for entry in (
    {"path": fixture["archive"], "sha256": fixture["archiveSha256"]},
    {"path": fixture["fixture"], "sha256": fixture["fixtureSha256"]},
    evidence["testApk"], evidence["appApk"],
):
    assert sha(Path(entry["path"])) == entry["sha256"]
assert sha(R / evidence["committedFixture"]) == fixture["fixtureSha256"]
assert not git(A, "diff", evidence["productionBaseline"], APP, "--",
               "app/src/main", "core/src/main", "gradle.properties")
with zipfile.ZipFile(fixture["archive"]) as archive:
    names = archive.namelist()
    manifest_name, = (name for name in names if name.endswith("/manifest.json"))
    prefix = manifest_name.removesuffix("manifest.json")
    manifest_bytes = archive.read(manifest_name)
    assert manifest_bytes.replace(b"\r\n", b"\n") == (R / "manifest.json").read_bytes().replace(b"\r\n", b"\n")
    manifest = json.loads(manifest_bytes)
    assert manifest["contentVersion"] == "0c514711ae8d3212"
    assert len(names) == len(set(names)) == fixture["zipEntries"] <= 18000
    assert all(name.startswith(prefix) and "\\" not in name and ".." not in name.split("/") for name in names)
    verified = 0
    retained = len(manifest_bytes)
    for section, mapping in manifest.items():
        if not isinstance(mapping, dict):
            continue
        binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
        limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                 512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
        for name, expected in mapping.items():
            data = archive.read(prefix + name)
            current = (R / name).read_bytes()
            assert len(data) <= limit
            assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected, name
            assert hashlib.sha256(current if binary else current.replace(b"\r\n", b"\n")).hexdigest() == expected, name
            retained += len(data)
            verified += 1
    assert verified == fixture["verifiedRuntimeHashes"] == 8413
    assert retained == fixture["retainedBytes"] <= 56 * 1024 * 1024
    assert sum(entry.file_size for entry in archive.infolist()) == fixture["inflatedBytes"] <= 80 * 1024 * 1024
    assert Path(fixture["archive"]).stat().st_size == fixture["compressedBytes"] <= 42 * 1024 * 1024
before = LOG / "progress-before-596.json"
assert not before.exists()
shutil.copyfile(C / "progress.json", before)
start = {
    "execution": 596, "batch": "085", "startedAt": datetime.now(timezone.utc).isoformat(),
    "startingHead": HEAD, "androidHead": APP, "contentSnapshot": fixture["contentSnapshot"],
    "scope": "SAME085 frozen native execution and direct PNG inspection only; no reviewer, integration, publication or086.",
    "request": {"sha256": sha(request), "bytes": request.stat().st_size, "characters": len(text),
                "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                "limits": "Entire request loaded and checkpoint decoded; operative contract, entire approved issue and final595 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
    "artifactPathPreflight": "Approved workspace inputs and committed sources only; no optional historical-session helper access.",
    "parentLockRole": "Live parent19008 verified in coordinator ancestry; native wrapper rechecks ancestry without touching runner.lock.",
    "verifiedRuntimeHashes": verified, "runtimeManifestEqual": True,
    "actualNewPermissionDenials": [],
}
save(C / "execution-596-start.json", start)
state["execution596StartingState"] = start
state["stage"] = "batch-085-native-execution-in-progress"
state["nextAction"] = start["scope"]
temp = C / "progress.596.tmp"
assert not temp.exists()
save(temp, state)
assert load(temp) == state
temp.replace(C / "progress.json")
print("Preflight passed: 8413 exact runtime hashes, full archive budgets, frozen APKs/fixture, signed clean heads; starting scope persisted.")
