import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
ROOT = C.parent / "learning-japanese"
SESSION = "50f27fd4-ff59-4b08-8d2f-788dfa34050a"
LOG = C / "logs" / SESSION
HEAD = "e413b33ca170f1233cde699c2a3aef2e136d593b"


def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "--no-pager", *args], text=True, encoding="utf-8"
    ).strip()


def replace_once(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)


def write_new(path, text):
    if path.exists():
        assert path.read_text(encoding="utf-8-sig") == text.replace("\r\n", "\n"), str(path)
        return
    with path.open("x", encoding="utf-8", newline="\n") as f:
        f.write(text)


request_bytes = (LOG / "request.txt").read_bytes()
request = request_bytes.decode("utf-8-sig")
marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
checkpoint = json.loads(request.split(marker, 1)[1])
progress_path = C / "progress.json"
original = progress_path.read_bytes()
p = json.loads(original)
assert p["checkpoint"] == checkpoint["checkpoint"] == 732
assert p["batch"] == "099" and p["status"] == "continue"
assert p["stage"] == "batch-099-native-prepared-compiled-not-executed"
assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
assert not git("status", "--porcelain", "--untracked-files=all")
write_new(LOG / "progress-before-733.json", original.decode("utf-8-sig"))

preflight = (C / "preflight-732.ps1").read_text(encoding="utf-8-sig")
preflight = preflight.replace("e18b3bce-9dbb-464d-8dbc-bc6c53b6bec5", SESSION)
preflight = preflight.replace("732", "733")
write_new(C / "preflight-733.ps1", preflight)

run = (C / "run-724-native.ps1").read_text(encoding="utf-8-sig")
run = run.replace("2be12432-54ac-4d75-82ab-630ff0541205", SESSION)
run = run.replace("724", "733").replace("098", "099")
run = replace_once(
    run,
    '$compiled = Get-Content "$content\\docs\\n1-sources\\execution-723.json" -Raw | ConvertFrom-Json\n'
    '$prior = Get-Content "$content\\docs\\n1-sources\\execution-722.json" -Raw | ConvertFrom-Json\n'
    "$preparation = $prior.fixtureVerification",
    '$compiled = Get-Content "$content\\docs\\n1-sources\\execution-732.json" -Raw | ConvertFrom-Json\n'
    "$preparation = $compiled.fixtureVerification",
)
run = run.replace("4a652e4e6ca3c28a7d24e9720cf278347ab85f2e", HEAD)
run = replace_once(run, "$checkpoint.checkpoint -ne 723", "$checkpoint.checkpoint -ne 732")
write_new(C / "run-733-native.ps1", run)

manifest_bytes = (ROOT / "manifest.json").read_bytes()
manifest = json.loads(manifest_bytes)
sys.path.insert(0, str(ROOT / "tools"))
from build_manifest import build_manifest, sha256

assert build_manifest(ROOT) == manifest
verified = {}
for section, values in manifest.items():
    if not isinstance(values, dict):
        continue
    for path, digest in values.items():
        if not isinstance(digest, str) or len(digest) != 64:
            continue
        actual = (
            hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            if section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
            else sha256(ROOT / path)
        )
        assert actual == digest, path
        verified[path] = actual
assert len(verified) == 8451, len(verified)
write_new(LOG / "runtime-hashes-before.json", json.dumps(verified, ensure_ascii=True, indent=2) + "\n")
starting = {
    "execution": 733,
    "batch": "099",
    "startedAt": datetime.now(timezone.utc).isoformat(),
    "startingHead": HEAD,
    "androidHead": "1c1b7bf42cc91d820a93169f1088dc647ac51c0d",
    "freshOriginMain": git("rev-parse", "origin/main"),
    "scope": "SAME099 frozen native execution, actual PNG inspection and normally signed LOCAL evidence; no reviewer/publication/100.",
    "request": {
        "sha256": hashlib.sha256(request_bytes).hexdigest(),
        "bytes": len(request_bytes),
        "characters": len(request),
        "lines": len(request.splitlines()),
        "completeFileLoadedAndCheckpointParsed": True,
        "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed; operative contract, complete approved issue and final732 directly inspected. Historical middle parsed, not freshly semantically re-reviewed.",
    },
    "runtimeManifestHashesVerified": len(verified),
    "manifestSha256": hashlib.sha256(manifest_bytes).hexdigest(),
    "artifactPathPreflight": "Approved control helpers, frozen inputs and committed evidence only; no optional historical session helper access.",
    "actualNewPermissionDenials": [],
    "diagnostics": [
        "Initial preflight hash loop used raw bytes for text and stopped at CRLF curriculum/grammar.json before updating progress or launching native. Corrected to repository-standard normalized text hashes and verified full manifest freshness; runtime unchanged."
    ],
}
assert "execution733StartingState" not in p
p["execution733StartingState"] = starting
p["stage"] = "batch-099-native-execution-in-progress"
p["nextAction"] = "SAME099 execute exact frozen compiled fixture under live parent launcher, inspect actual screenshots, preserve terminal per-case status and yield a normally signed local evidence checkpoint; no reviewer, publication or100."
assert progress_path.read_bytes() == original
progress_path.write_text(json.dumps(p, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
print(json.dumps(starting, ensure_ascii=True, indent=2))
