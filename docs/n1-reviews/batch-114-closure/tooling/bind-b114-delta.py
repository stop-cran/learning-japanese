"""Verify and freeze one pre-delivery record; does not send a message."""
import hashlib
import json
import stat
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-114\delta")
SESSIONS = {"claude": "98c7bbce-f756-4954-8263-66f20c421c8c",
            "gpt": "c4b8c183-4098-4614-ad40-537b1d9dccad"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    family = sys.argv[1]
    assert family in SESSIONS
    run = next(r for r in json.loads((ROOT / "preflight.json").read_bytes())["runs"]
               if r["run"] == f"N1-B114-{family.upper()}-DELTA-001")
    config_path = Path(run["config"]["path"])
    assert sha(config_path.read_bytes()) == run["config"]["sha256"]
    config = json.loads(config_path.read_bytes())
    chain = json.loads(Path(config["chainManifest"]).read_bytes())
    for item in config["files"] + chain["segments"]:
        path = Path(item["path"])
        assert not path.stat().st_mode & stat.S_IWRITE, path
        assert sha(path.read_bytes()) == item["sha256"], path
    for source in chain["sources"]:
        data = b""
        for segment in chain["segments"]:
            lines = Path(segment["path"]).read_bytes().splitlines(keepends=True)
            for part in segment["parts"]:
                if part["source"] == source["source"]:
                    data += b"".join(lines[part["segmentStart"] - 1:part["segmentEnd"]])
        assert sha(data) == source["selectedSha256"], source["source"]
        assert source["selectedLines"] == source["sourceLines"]
    assert not Path(config["report"]).exists()
    session = SESSIONS[family]
    record = Path.home() / ".copilot/session-state" / session / "events.jsonl"
    raw = record.read_bytes()
    assert raw.endswith(b"\n")
    last = json.loads(raw.splitlines()[-1])
    data = {"run": run["run"], "session": session, "offset": len(raw),
            "prefixSha256": sha(raw), "lastEventType": last["type"],
            "lastEventTimestamp": last["timestamp"], "kickoffSha256": run["kickoff"]["sha256"],
            "configSha256": run["config"]["sha256"], "reportAbsent": True,
            "sourceReassemblyVerified": True, "verifiedInputs": len(config["files"]) + len(chain["segments"])}
    target = ROOT / f"predelivery-{family}.json"
    with target.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")
    target.chmod(stat.S_IREAD)
    print(json.dumps(data))


if __name__ == "__main__":
    main()
