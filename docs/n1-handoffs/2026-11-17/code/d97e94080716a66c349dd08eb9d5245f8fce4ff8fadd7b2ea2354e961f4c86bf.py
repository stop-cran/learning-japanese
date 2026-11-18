"""Scan existing B134 closure inputs without inventing the pending fresh reviews."""
import copy
import json

from close_b134 import (
    AUTHOR, COORDINATOR, CORE_ROOT, CORE_SHA, FAILED_SESSION, METER_SESSIONS, PACKET_SHA,
    PROOFS, ROOT, add_chain, add_protected, load_originals, protected_source,
    publication_findings, put, read_review, retain_overlapping_chains,
)
from common import freeze_json, require, sha, start_guard

OUT = ROOT / "closure-retention-rehearsal-001"
EVIDENCE = {
    "verification/coordinator-original-dispositions.json": (
        "coordinator-disposition-bindings-001/coordinator-dispositions.json",
        "e317783a7c579ca13ff7d3cbe9f8a4940b6dc7cce3ae0eed791c8625dcb92b13"),
    "verification/coordinator-original-bindings.json": (
        "coordinator-disposition-bindings-001/verification.json",
        "d4eee7728c8cd3570096621ef38ffe68dd9ffda0346ddf6b068b38bc509ad9ac"),
    "verification/coordinator-source-checks.json": (
        "coordinator-source-checks-captures-001/coordinator-source-checks.json",
        "e044047ebe19a8f64865c462fc1e51187d3f77dad85344c4b20baa4b16511843"),
    "verification/coordinator-source-bindings.json": (
        "coordinator-source-checks-captures-001/verification.json",
        "0d6e2c85dcde9bbbc49c4176a649bf1bf6c359b5f2c78354752586b4c099d7fb"),
}


def main():
    require(not OUT.exists(), "Preserve prior retention rehearsal")
    guard, _ = start_guard("B134 actual-input publication-retention rehearsal")
    try:
        original, files = load_originals()
        retentions = copy.deepcopy(original["chainRetention"])
        retentions["fresh-core"] = add_chain(files, "fresh-core", {
            "path": str(CORE_ROOT / "fresh-independent-core-001.json"), "sha256": CORE_SHA}, guard)
        for label, (relative, digest) in PROOFS.items():
            put(files, "verification/" + label + ".json", read_review(ROOT / relative, digest))
        for name, (relative, digest) in EVIDENCE.items():
            put(files, name, read_review(ROOT / relative, digest))
        windows = set()
        sums_raw = read_review(CORE_ROOT / "packet" / "SHA256SUMS.json", PACKET_SHA)
        for name, digest in json.loads(sums_raw).items():
            raw = read_review(CORE_ROOT / "packet" / name, digest)
            if protected_source(name):
                add_protected(windows, raw, name.endswith((".html", ".htm")))
            guard.check()
        protected = []
        for name in ("verification/coordinator-original-bindings.json",
                     "verification/coordinator-source-bindings.json"):
            for key, ref in json.loads(files[name])["captures"].items():
                if not key.endswith(("Readback", "NativeCapture")):
                    continue
                raw = read_review(ref["path"], ref["sha256"])
                add_protected(windows, raw, False)
                protected.append({key: ref[key] for key in ("path", "sha256")})
                guard.check()
        require(windows, "No protected text windows")
        put(files, "packet/SHA256SUMS.json", sums_raw)
        allowed = {COORDINATOR, AUTHOR, FAILED_SESSION, *METER_SESSIONS,
                   *(entry["session"] for entry in original["reviewLineage"])}
        initial_uuids, initial_leaks = publication_findings(files, windows, allowed, guard)
        diagnostics = {"uuidFindings": initial_uuids, "externalWindowFindings": initial_leaks}
        freeze_json(OUT / "before-retention.json", diagnostics)
        adjustments = retain_overlapping_chains(files, windows, allowed, guard, retentions)
        uuids, leaks = publication_findings(files, windows, allowed, guard)
        result = {
            "status": "PASS_EXISTING_INPUTS_NOT_FINAL_PUBLICATION_SCAN",
            "files": len(files), "sha256": {name: sha(raw) for name, raw in sorted(files.items())},
            "protectedSources": protected, "adjustments": adjustments, "retentions": retentions,
            "uuidFindings": uuids, "externalWindowFindings": leaks,
            "limits": "Fresh reports, extensions, lifecycle records and final resolution do not yet "
                      "exist. This is neither review closure nor the required final whole-archive scan.",
        }
        require(not uuids and not leaks, "Unresolved publication findings")
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Retention rehearsal RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(OUT / "verification.json", result)))


if __name__ == "__main__":
    main()
