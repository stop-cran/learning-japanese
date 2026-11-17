"""Freeze own-only cc374 confirmation requests and complete neutral source units.

No reviewer admission, messaging, semantic adjudication, repo writes or signing.
Original author response/receipt and four-path diff stay coordinator-only because
they disclose the opposite family's findings. Their object hashes remain bound.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
import b134_integration_confirmation_v1 as tool
from common import WS, freeze_json, frozen, sha, start_guard, write_frozen, require

HERE = Path(__file__).resolve().parent
REVIEW = WS / "scratch-134" / "review"
CANDIDATE = "cc374051efa75199212a87c9abf08d7391419055"
SCOPE = {"path": str(REVIEW / "revision002-scope-verification-001" / "verification.json"),
         "sha256": "6fa5d0d4cdfe4a8e2f9ca06f703c8e1bf7da0d9ce9576771174e818e6c636d6e"}
GATES = {"path": str(REVIEW / "revision002-gate-verification-001" / "verification.json"),
         "sha256": "8fa34d64fe16c821c8593778bd0af242c6420329cedea0c432b9f6294abe644a"}
COLLECTORS = {"claude": "fd9f3c289f6bff65af0b7119379eb350822a096e6dbd55484bfa9cd72f332162",
              "gpt": "af3c8e28b994e462882465106326c2669ceed8317fc8f1d058dc48b5c264a689"}


def small(ref):
    return {k: ref[k] for k in ("path", "sha256")}


def main():
    guard, _ = start_guard("B134 actual neutral bounded requests, not admission")
    try:
        scope, gates = (json.loads(tool.read(ref)) for ref in (SCOPE, GATES))
        require(scope["commit"] == gates["candidate"] == CANDIDATE, "Actual proof candidate differs")
        # Source bindings only: never copy the receipt's GPT review/verdict/claim analysis.
        receipt_ref = scope["bindings"]["snapshot/docs/n1-sources/batch-134-reconciliation-002/receipt.json"]
        receipt = json.loads(tool.read(receipt_ref))
        bindings = {row["source"]: row for row in receipt["sourceBindings"]}
        extras, selection = [], []
        for number in ("01", "02"):
            label = f"evidence/external-snapshots/{number}-extract.txt"
            row = bindings[label]
            source = {"path": row["localPath"], "sha256": row["sha256"]}
            raw = tool.read(source)
            require(len(raw.splitlines()) == row["lineCount"] and raw.endswith(b"\n"), "Incomplete native source")
            extras.append({"source": label, "ref": source, "audience": "neutral", "kind": "native-extract"})
        row = bindings["evidence/jmdict-families.compact-xml-v1.txt"]
        original = {"path": row["localPath"], "sha256": row["sha256"]}
        raw = tool.read(original)
        lines = raw.splitlines(keepends=True)
        require(len(lines) == row["lineCount"] and raw.endswith(b"\n"), "Incomplete original compact record file")
        for record_id in ("1311640", "1956480"):
            found = [(n, line) for n, line in enumerate(lines, 1)
                     if re.match(rb"^#=" + record_id.encode() + rb"(?:\s|$)", line)]
            require(len(found) == 1, "Complete record identity not unique")
            number, complete_line = found[0]
            label = f"evidence/jmdict-complete-record-{record_id}.txt"
            selected = small(write_frozen(HERE / "neutral-inputs" / Path(label).name, complete_line))
            extras.append({"source": label, "ref": selected, "audience": "neutral", "kind": "native-extract"})
            selection.append({"original": original, "sourceLines": len(lines), "line": number,
                              "entryId": record_id, "selected": selected, "selectedLines": 1,
                              "representation": "Entire previously validated compact-xml-v1 record line; no fields elided. Not raw XML."})
        selected = small(freeze_json(HERE / "neutral-inputs" / "complete-record-selection.json", selection))
        extras.append({"source": "evidence/complete-record-selection.json", "ref": selected,
                       "audience": "neutral", "kind": "mechanical-proof"})
        for family, digest in COLLECTORS.items():
            path = REVIEW / f"{family}-fresh003-collector-001" / "review-input.json"
            collected = json.loads(frozen(path, digest))
            prior = collected["review"]
            require(collected["status"] == "PASS_ACCEPTED_REVIEW_COLLECTION_NOT_CLOSURE"
                    and prior["spec"]["family"] == family, "Own accepted collector differs")
            spec = {"schemaVersion": 1, "mode": "revision", "scope": tool.REVISION_SCOPE,
                    "family": family, "run": f"N1-B134-{family.upper()}-REVISION-001",
                    "session": tool.OWN[family], "candidate": CANDIDATE,
                    "scopeProof": SCOPE, "gateProof": GATES,
                    "prior": {"review": prior["spec"], "preflight": prior["preflight"], "final": prior["final"]},
                    "obligations": [{"id": name, "claim": "Own unchanged FRESH003 report/adjudication obligation "
                                    + name + "; preserve that exact prior disposition and assess only this bounded revision."}
                                   for name in collected["requiredDispositionIds"]],
                    "additionalSources": extras,
                    "neutralEvidence": {"exactDeltaReadCompletely": True, "noOppositeFamilyResults": True,
                        "addedEvidenceTreatment": "private-raw-neutral-hash-inventory", "addedPaths": scope["evidencePaths"]}}
            freeze_json(HERE / ("request-" + family + ".json"), spec)
            guard.check()
    finally:
        freeze_json(HERE / "actual-request-memory.json", guard.finish())


if __name__ == "__main__":
    main()
