from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import zipfile

CONTROL = Path(__file__).parent
ROOT = CONTROL.parent / "learning-japanese"
progress_path = CONTROL / "progress.json"
progress = json.loads(progress_path.read_text(encoding="utf-8-sig"))
assert (progress["checkpoint"], progress["batch"], progress["stage"]) == (
    586, "084", "native-prepared-compiled-awaiting-execution"
)
request = CONTROL / "logs" / "beea3b0e-c8ab-47ae-b801-f7e33fa093ae" / "request.txt"
text = request.read_text(encoding="utf-8-sig")
checkpoint = json.loads(text.split(
    "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
)[1])
assert checkpoint["checkpoint"] == 586
evidence = json.loads((ROOT / "docs" / "n1-sources" / "execution-586.json").read_text())
fixture = evidence["fixtureVerification"]
with zipfile.ZipFile(fixture["archive"]) as archive:
    names = archive.namelist()
    manifest_name = next(name for name in names if name.endswith("/manifest.json"))
    prefix = manifest_name.removesuffix("manifest.json")
    manifest_bytes = archive.read(manifest_name)
    assert manifest_bytes.replace(b"\r\n", b"\n") == (ROOT / "manifest.json").read_bytes().replace(b"\r\n", b"\n")
    manifest = json.loads(manifest_bytes)
    assert manifest["contentVersion"] == fixture["contentVersion"]
    verified = 0
    retained = len(manifest_bytes)
    assert len(names) == len(set(names)) <= 18000
    assert all(name.startswith(prefix) and "\\" not in name and ".." not in name.split("/") for name in names)
    for section, mapping in manifest.items():
        if not isinstance(mapping, dict):
            continue
        binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
        limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                 512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
        for name, expected in mapping.items():
            data = archive.read(prefix + name)
            current = (ROOT / name).read_bytes()
            assert len(data) <= limit
            assert hashlib.sha256(data if binary else data.replace(b"\r\n", b"\n")).hexdigest() == expected, name
            assert hashlib.sha256(current if binary else current.replace(b"\r\n", b"\n")).hexdigest() == expected, name
            retained += len(data)
            verified += 1
    assert verified == 8379
    assert retained <= 56 * 1024 * 1024
    assert fixture["inflatedBytes"] <= 80 * 1024 * 1024
    assert Path(fixture["archive"]).stat().st_size <= 42 * 1024 * 1024
    assert len(names) == fixture["zipEntries"]
    assert sum(entry.file_size for entry in archive.infolist()) == fixture["inflatedBytes"]
for entry in (
    {"path": fixture["archive"], "sha256": fixture["archiveSha256"]},
    {"path": fixture["fixture"], "sha256": fixture["fixtureSha256"]},
    evidence["testApk"], evidence["appApk"],
):
    assert hashlib.sha256(Path(entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
for root, head in (
    (ROOT, "8a4a70e70d51487ae0c58979e8166b2186a6ee91"),
    (CONTROL.parent / "kanji-cards-android", evidence["androidHead"]),
):
    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), "--no-pager", *args], text=True).strip()
    assert git("rev-parse", "HEAD") == head
    assert git("status", "--porcelain") == ""
    assert git("log", "-1", "--format=%G?") == "G"
start = {
    "execution": 587, "batch": "084", "startedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "startingHead": "8a4a70e70d51487ae0c58979e8166b2186a6ee91",
    "contentSnapshot": fixture["contentSnapshot"], "androidHead": evidence["androidHead"],
    "scope": "SAME084 owned native execution and direct PNG inspection; no reviewer, integration, publication or085.",
    "request": {"sha256": hashlib.sha256(request.read_bytes()).hexdigest(), "bytes": request.stat().st_size,
                "characters": len(text), "lines": len(text.splitlines()),
                "completeFileLoadedAndCheckpointParsed": True,
                "limits": "Entire request loaded and checkpoint decoded; operative task and final checkpoint inspected. Historical middle not freshly semantically re-reviewed."},
    "verifiedRuntimeHashes": 8379, "runtimeManifestEqual": True,
    "parentLockReadDiagnostic": "An initial read of runner.lock returned an expected sharing violation; no acquisition, deletion or unlock attempted. Live parent19008 verified in child ancestry.",
    "optionalHistoricalSessionHelpersAccessed": False,
}
(CONTROL / "execution-587-start.json").write_text(json.dumps(start, indent=2) + "\n", encoding="utf-8")
progress["execution587StartingState"] = start
progress["stage"] = "batch-084-native-execution-in-progress"
progress["nextAction"] = "Execute frozen084 Retry1 native cases and inspect resulting PNGs; preserve evidence and checkpoint before dependent visual reviews."
progress_path.write_text(json.dumps(progress, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
print("Preflight passed: exact8379 runtime hashes, frozen APKs/fixture, signed heads and clean worktrees.")
