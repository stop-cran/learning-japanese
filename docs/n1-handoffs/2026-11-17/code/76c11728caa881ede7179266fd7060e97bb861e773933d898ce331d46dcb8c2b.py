"""Verify B131's original source binding without relabelling it to the final base."""
import json

from common import WS, frozen, require, sha

SOURCE_BASE = "6da1184b82b60553f9b65c57f53289c779f96f7c"
CANDIDATE_BASE = "cb0f5581bdda84f7e673225c19126c85e242e57b"
PREFIX = "docs/n1-sources/batch-131/"
HERE = WS / "scratch-131" / "review"
OBSERVED_SHA = "69fec25c4cdb64e13c7c45d6f01d3dc45bf3348fec549fabe928555ce19dc8b8"
INCOMING_PROOF_SHA = "0448941d3d420612eb6bc07a1c677a15c06ee72e0786d4d9e3eb1c5dcf578f3e"


def verify_baseline_trees(record, original, incoming):
    require(original == incoming, "Original and incoming baseline kanji trees differ")
    entries = [entry for entry in original.split(b"\0") if entry]
    for entry in entries:
        _, path = entry.split(b"\t", 1)
        name = path.decode("utf-8")
        require(name.startswith("kanji/") and name.endswith(".md") and len(name) == 10
                and not any(char in name for char in "\r\n\t\"\\"),
                "Unexpected baseline kanji path")
    # The author hashed `ls-tree -r`, not the NUL-delimited listing used for equality.
    listing = b"\n".join(entries) + b"\n"
    require(sha(listing) == record["baselineKanjiTreeSha256"],
            "Baseline tree does not match the observed adaptation")
    require(len(entries) == record["baselineKanjiEntries"],
            "Baseline tree entry count differs")
    return len(entries)


def verify_scan_bindings(record, scans):
    require(set(scans) == set(record["originalScans"]),
            "Original scan inventory differs")
    for path, raw in scans.items():
        require(sha(raw) == record["originalScans"][path],
                "Original scan bytes changed: " + path)
        require(json.loads(raw)["base"] == SOURCE_BASE,
                "Original scan was relabelled: " + path)
    return {path: sha(raw) for path, raw in scans.items()}


def verify_signed_binding(git, candidate):
    observed = frozen(HERE / "author-base-adaptation-observed-001.json", OBSERVED_SHA)
    incoming_proof = json.loads(frozen(
        HERE / "incoming-main-verification-001.json", INCOMING_PROOF_SHA))
    require(incoming_proof["status"] == "PASS_WORD_ONLY_BASELINE_ADAPTATION"
            and incoming_proof["originalBase"] == SOURCE_BASE
            and incoming_proof["incomingBase"] == CANDIDATE_BASE
            and incoming_proof["membershipPreservedByExactTreeEquality"] is True
            and not incoming_proof["memory"]["breach"], "Incoming baseline proof differs")
    require(git("show", "-s", "--format=%P", candidate).decode().strip() == CANDIDATE_BASE,
            "Candidate is not a direct child of the explicitly adapted base")
    signed = git("show", candidate + ":" + PREFIX + "base-adaptation.json")
    require(signed == observed, "Signed adaptation differs from the frozen observation")
    record = json.loads(signed)
    require(record["originalSourceBase"] == SOURCE_BASE
            and record["candidateBase"] == CANDIDATE_BASE
            and record["coordinatorProofSha256"] == INCOMING_PROOF_SHA,
            "Signed source/candidate base binding differs")
    count = verify_baseline_trees(
        record, git("ls-tree", "-rz", SOURCE_BASE, "--", "kanji"),
        git("ls-tree", "-rz", CANDIDATE_BASE, "--", "kanji"))
    require(count == 1254 and len(record["originalScans"]) == 6,
            "Observed baseline or original scan count differs")
    scans = {path: git("show", candidate + ":" + PREFIX + path)
             for path in record["originalScans"]}
    scan_hashes = verify_scan_bindings(record, scans)
    selection = json.loads(git("show", candidate + ":" + PREFIX + "selection.json"))
    require(selection["base"] == SOURCE_BASE, "Original selection was relabelled")
    preserved = {}
    for path in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json"):
        original = git("show", SOURCE_BASE + ":" + path)
        require(original == git("show", CANDIDATE_BASE + ":" + path)
                == git("show", candidate + ":" + path),
                "Source baseline changed: " + path)
        preserved[path] = sha(original)
    return {
        "sourceBase": SOURCE_BASE,
        "candidateBase": CANDIDATE_BASE,
        "candidate": candidate,
        "signedAdaptationSha256": sha(signed),
        "incomingProofSha256": INCOMING_PROOF_SHA,
        "baselineKanjiEntries": count,
        "originalScans": scan_hashes,
        "preservedSourceFiles": preserved,
        "limits": "Source-base bridge only; caller must verify the candidate signature and clean "
                  "checkout. Does not certify the author's historical 215-file preservation "
                  "timing, candidate semantics, final gates or publication.",
    }
