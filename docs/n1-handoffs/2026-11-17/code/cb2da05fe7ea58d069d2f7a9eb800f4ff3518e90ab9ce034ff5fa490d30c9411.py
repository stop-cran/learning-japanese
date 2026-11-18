"""Verify the exact, additive B129 pre-review correction."""
import hashlib
import json
from pathlib import Path

from common import frozen, require, sha
from verify_b129_payload import BASE, PREFIX

ORIGINAL = "61232c2022be5cd81b26ee1fed87f788ce4a5da0"
CORRECTION = "evidence-scope-revision-003.json"
INVENTORY = "evidence-inventory-003.json"
FILES = {"docs/n1-authoring-notes.md", "words/\u8309\u8389\u82b1.md"}


def verify_formatting(revision, historical, blobs, original_blobs):
    require(set(revision["files"]) == set(historical["formatting"]) == set(blobs) == FILES,
            "Correction formatting scope differs")
    for name in sorted(FILES):
        raw, claim, prior = blobs[name], revision["files"][name], historical["formatting"][name]
        require(raw == original_blobs[name]
                and sha(raw) == claim["committedBlobSha256"] == prior["rawBeforeSha256"]
                and sha(raw.replace(b"\r\n", b"\n")) == claim["historicalTemporaryLfSha256"] == prior["rawAfterSha256"]
                and b"\r\n" in raw and b"\n" not in raw.replace(b"\r\n", b"")
                and hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
                == claim["committedBlobIdAtOriginalCandidate"]
                and claim["equalsHistoricalRawBefore"] is True
                and claim["temporaryLfNormalizationWasReverted"] is True,
                f"Corrected raw-byte disposition does not match the signed files: {name}")


def verify(git, blob, source, candidate, payload, scratch, gates_name, preservation_name, findings):
    revision = json.loads(source(CORRECTION))
    historical = json.loads(source("evidence-scope-revision-002.json"))
    require(revision["revision"] == "003" and revision["base"] == BASE
            and revision["originalSignedCandidate"] == ORIGINAL
            and revision["supersedesForFinalDisposition"] == "evidence-scope-revision-002.json"
            and revision["originalCandidatePreservedAt"] == "refs/heads/b129-candidate-001",
            "Correction identity differs")
    require(git("rev-parse", revision["originalCandidatePreservedAt"]).decode().strip() == ORIGINAL,
            "Original candidate preservation ref differs")
    changes = git("diff", "--name-status", "--no-renames", ORIGINAL, candidate).decode().splitlines()
    require(set(changes) == {f"A\t{PREFIX}{name}" for name in (CORRECTION, INVENTORY)},
            "Correction changed files outside the two additive evidence records")
    require(set(revision["preservedHistoricalFilesSha256"]) == {
        "evidence-scope-revision-002.json", "evidence-inventory.json", "evidence-inventory-002.json"},
        "Historical correction bindings incomplete")
    for name, digest in revision["preservedHistoricalFilesSha256"].items():
        require(sha(source(name)) == digest
                and source(name) == git("show", f"{ORIGINAL}:{PREFIX}{name}"),
                "Historical evidence changed")
    verify_formatting(revision, historical, {name: blob(name) for name in FILES},
                      {name: git("show", f"{ORIGINAL}:{name}") for name in FILES})
    require(len(findings) == 2 and {row["path"] for row in findings} == FILES
            and all(row["committedEqualsClaimedBefore"] and not row["committedEqualsClaimedAfter"]
                    for row in findings), "Unexpected historical findings")
    final = revision["finalSnapshotEvidence"]
    require(final["replacementCommittedGatesDirectory"] == str(scratch / gates_name)
            and final["replacementAllGroupPreservationDirectory"] == str(scratch / preservation_name)
            and revision["runtimeManifestSha256Unchanged"] == payload["manifestSha256"],
            "Replacement verification scope differs")
    for group in final["priorCommittedVerification"].values():
        directory = Path(group["directory"])
        require(directory.parent == scratch and group["snapshot"] == ORIGINAL,
                "Historical verification path or snapshot differs")
        for name, digest in group["files"].items():
            require(Path(name).name == name and sha((directory / name).read_bytes()) == digest,
                    "Historical committed receipt changed")
        require(group["summarySha256"] == group["files"]["summary.json"], "Summary binding differs")
    for local, signed, digest in (
        ("run_b129_correction_gates.py", "run_b129_gates.py", final["gateRunnerSha256"]),
        ("preserve_b129_correction.py", "preserve_b129_all.py", final["allGroupPreservationProducerSha256"]),
    ):
        raw = (scratch / local).read_bytes()
        expected = source("producers/" + signed)
        old = b"assert head == BASE"
        new = ('assert head == "' + ORIGINAL + '"').encode()
        require(expected.count(old) == 1, "Original author-admission check differs")
        expected = expected.replace(old, new)
        if local == "preserve_b129_correction.py":
            require(expected.count(b"evidence-inventory-002.json") == 2,
                    "Original inventory references differ")
            expected = expected.replace(b"evidence-inventory-002.json", b"evidence-inventory-003.json")
        require(raw == expected and sha(raw) == digest,
                "Executed correction producer differs beyond the verified bounded adaptation")
    handoff_path = scratch / "handoff-002.json"
    handoff_raw = frozen(handoff_path, "6f559a2a11f3e729424c27afa1dfcb60588a60bc98d9d07e979b40cccb3e064d")
    handoff = json.loads(handoff_raw)
    require(handoff["candidate"] == candidate and handoff["base"] == BASE
            and handoff["supersededCandidate"] == ORIGINAL
            and handoff["correction"]["sha256"] == sha(source(CORRECTION))
            and handoff["finalInventory"]["sha256"] == sha(source(INVENTORY))
            and handoff["manifestSha256"] == payload["manifestSha256"], "Handoff differs")
    for group in handoff["exactReplacementSnapshotEvidence"].values():
        directory = Path(group["directory"])
        require(directory.parent == scratch, "Unexpected handoff evidence path")
        for name, digest in group["files"].items():
            require(Path(name).name == name and sha((directory / name).read_bytes()) == digest,
                    "Handoff evidence bytes changed")
        require(group["summarySha256"] == group["files"]["summary.json"], "Handoff summary differs")
    for name, digest in handoff["producerBindings"].items():
        require(Path(name).name == name and sha((scratch / name).read_bytes()) == digest,
                "Handoff producer binding differs")
    previous = handoff["previousHandoff"]
    require(Path(previous["path"]) == scratch / "handoff-001.json"
            and sha(Path(previous["path"]).read_bytes()) == previous["sha256"], "Prior handoff changed")
    return {
        "handoff": {"path": str(handoff_path), "sha256": sha(handoff_raw)},
        "record": PREFIX + CORRECTION, "sha256": sha(source(CORRECTION)),
        "originalCandidate": ORIGINAL, "candidate": candidate, "onlyTwoAdditiveEvidenceFiles": True,
        "correctedHistoricalFindings": findings,
        "preservationInventoryScope": "Both the correction preservation producer and this verifier check final inventory 003. "
                                      "Producer changes are exactly the original-candidate author admission and two inventory references.",
    }
