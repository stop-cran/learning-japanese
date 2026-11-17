"""Freeze the byte-verified handoff without hiding its initially writable state."""
import json
import stat
from pathlib import Path

from common import freeze_json, require, sha, start_guard
from verify_b132_reconciliation import HERE, INVENTORY_SHA, PACKET


def main():
    output = HERE / "review" / "source-reconciliation-freeze-001.json"
    require(not output.exists(), "Preserve the previous freeze receipt")
    guard, _ = start_guard("B132 source handoff freeze")
    try:
        inventory_path = PACKET / "inventory.json"
        raw = inventory_path.read_bytes()
        require(sha(raw) == INVENTORY_SHA, "Handoff inventory changed")
        inventory = json.loads(raw)
        bindings = [(inventory_path, INVENTORY_SHA)]
        for name, binding in inventory["files"].items():
            path = PACKET / name
            require(path.resolve().is_relative_to(PACKET.resolve()), "Handoff path escapes")
            bindings.append((path, binding["sha256"]))
        verification = json.loads((PACKET / "verification.json").read_bytes())
        require(sha((PACKET / "verification.json").read_bytes())
                == inventory["files"]["verification.json"]["sha256"], "Verification record changed")
        for item in verification["external"]["reusedOriginalCapturesVerified"]:
            path = Path(item["localRawCapture"])
            require(path.parent == HERE / "survey-001" / "external"
                    and path.name in ("\u5893-kotobank.html", "\u5893-weblio.html"),
                    "Unexpected reused capture")
            bindings.extend([(path, item["rawSha256"]), (path.with_suffix(".txt"), item["textSha256"])])
        before = []
        for path, digest in bindings:
            guard.check()
            require(sha(path.read_bytes()) == digest, "Handoff content changed: " + str(path))
            before.append({"path": str(path), "sha256": digest,
                           "wasReadOnly": not bool(path.stat().st_mode & stat.S_IWRITE)})
        for path, digest in bindings:
            path.chmod(stat.S_IREAD)
            require(not path.stat().st_mode & stat.S_IWRITE and sha(path.read_bytes()) == digest,
                    "Could not freeze unchanged source")
        print(json.dumps(freeze_json(output, {
            "status": "UNCHANGED_BYTES_FROZEN", "files": before,
            "initiallyWritable": sum(not row["wasReadOnly"] for row in before),
            "preservedFailure": "source-reconciliation-verification-execution-001",
            "limits": "The original handoff was not fully ReadOnly. This records the actual later "
                      "freeze, not retroactive immutability or source/semantic acceptance.",
        })))
    finally:
        require(not guard.finish()["breach"], "Source handoff freeze RAM breach")


if __name__ == "__main__":
    main()
