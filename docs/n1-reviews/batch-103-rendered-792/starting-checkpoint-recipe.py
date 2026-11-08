import copy
import datetime
import hashlib
import json
import os
from pathlib import Path

C = Path(r"C:\Users\stop-\n1-kanji-workspace\control")
L = C / "logs" / "d36f9eb0-350c-445d-98cd-6c7f932c5be1"
p = C / "progress.json"
backup = L / "progress-before-792.json"
if backup.exists():
    original = json.loads(backup.read_text(encoding="utf-8-sig"))
    current = json.loads(p.read_text(encoding="utf-8-sig"))
    assert all(current[k] == v for k, v in original.items())
    state = current["execution792StartingState"]
    assert set(current) == set(original) | {"execution792StartingState"}
    (L / "starting-state-792.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Interrupted verification resumed with one parse; all original historical values unchanged.")
    raise SystemExit(0)
original = json.loads(p.read_text(encoding="utf-8-sig"))
assert original["checkpoint"] == 791 and original["batch"] == "103"
assert original["status"] == "continue"
backup.write_bytes(p.read_bytes())
request = (L / "request.txt").read_bytes()
state = {
    "execution": 792, "batch": "103",
    "startedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "startingHead": "878b65a7480d0e6a24d00789d8fd98b32d296522",
    "androidHead": "bf30cdead8515739bc0e671d57a54b9a3109dd46",
    "freshOriginMain": "a38f4cf554300ce34ee65aada79e87b7c9d0319e",
    "scope": "SAME103 bounded source-and-image packet preparation for original-family rendered confirmations; reviewers only if complete evidence and compliant serial execution can be established. No native rerun/publication/104.",
    "request": {"sha256": hashlib.sha256(request).hexdigest(), "bytes": len(request),
                "completeFileLoadedAndCheckpointParsed": True,
                "limits": "Entire request loaded and checkpoint decoded; operative contract, entire approved issue and final791 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
    "runnerPreflight": json.loads((L / "preflight-792.json").read_text(encoding="utf-8-sig")),
    "artifactPathPreflight": "Approved committed packets/frozen workspace inputs/control helpers only; optional historical-session recipes not accessed.",
    "status": "rendered-evidence-preparing",
}
updated = copy.deepcopy(original)
assert "execution792StartingState" not in updated
updated["execution792StartingState"] = state
tmp = C / "progress.json.792-start.tmp"
assert not tmp.exists()
tmp.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
os.replace(tmp, p)
reread = json.loads(p.read_text(encoding="utf-8-sig"))
assert all(reread[k] == v for k, v in original.items())
(L / "starting-state-792.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Starting scope persisted; all original historical values unchanged.")
