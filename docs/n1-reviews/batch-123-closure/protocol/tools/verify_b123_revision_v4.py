"""Verify the signed held-comparison delta without accepting its semantics."""
import json
import sys
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, require, sha, start_guard
from confirm_v2 import clean
from verify_b123_revision_v2 import (
    CARD, SIGNER, STROKES, WORD, check_gate, check_metadata, check_runtime,
    check_summary, verify_sources,
)

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse

PARENT = "047970a055903c0337d73823288695938648dd1d"
PREFIX = "docs/n1-sources/batch-123/reconciliation-003/"
PRIOR_PROOF = WS / "scratch-123" / "review" / "coordinator-reconciliation-verification-002.json"
PRIOR_SHA = "c7a9b6721556e4db4d7619d4f677a75957c834c6ce31cc03d40b8ce86ea11713"
CAPTURE = WS / "scratch-123" / "review" / "open-pair-sources-001" / "provenance.json"
CAPTURE_SHA = "e0ae19c482922dab9076bb08768b6395e55fb0cef4d83773b0dce0febe612996"
REQUIRED = ["\u672c", "\u5ea6"]
OPTIONAL = set("\u50cf\u56f2\u65b9\u8a08\u6e2c\u91cf\u7406")


def check_followup_metadata(before, after):
    check_metadata(before, after)
    added = after["quiz_exclusions"][len(before["quiz_exclusions"]):]
    require(added[:2] == REQUIRED and set(added[2:]) <= OPTIONAL,
            "Expected the two required guards followed only by scoped source-based decisions")
    return added


def check_delta(changes):
    sources, runtime = [], set()
    for line in changes.splitlines():
        status, path = line.split("\t")
        require((status == "M" and path in (CARD, "manifest.json"))
                or (status == "A" and path.startswith(PREFIX)),
                f"Unexpected or non-additive reconciliation delta: {line}")
        if status == "A":
            sources.append(path)
        else:
            runtime.add(path)
    require(runtime == {CARD, "manifest.json"} and sources, "Incomplete reconciliation delta")
    return sources


def check_source_reference(reference, source, extract):
    require(reference["character"] == source["character"] and reference["url"] == source["url"]
            and reference["rawSha256"] == source["raw"]["sha256"]
            and reference["extractSha256"] == source["extract"]["sha256"],
            "Source reference differs from the frozen acquisition")
    require(isinstance(reference["summary"], str) and reference["summary"].strip()
            and isinstance(reference["limitations"], str) and reference["limitations"].strip(),
            "Missing original source summary or limitations")
    quotes = reference["quotes"]
    require(isinstance(quotes, list), "Quotes must be explicit")
    lines = extract.decode("utf-8").splitlines()
    require(sum(len(quote["text"]) for quote in quotes) <= 80, "Overlong source quotation")
    for quote in quotes:
        first, last = quote["lines"]
        require(isinstance(first, int) and isinstance(last, int)
                and 1 <= first <= last <= len(lines) and quote["text"]
                and quote["text"] in "\n".join(lines[first - 1:last]),
                "Quotation or source-line reference differs")


def verify(candidate, gates, runner, output):
    config = load_batch(123)
    prior = json.loads(frozen(PRIOR_PROOF, PRIOR_SHA))
    require(prior["status"] == "PASS" and prior["candidate"] == PARENT
            and prior["initial"] == config["candidate"] and prior["base"] == config["base"],
            "Prior revision proof binding differs")
    clean(config, candidate)
    require(git(config, "show", "-s", "--format=%P", candidate).decode().strip() == PARENT,
            "Expected a non-rewriting direct child of reconciliation 002")
    identity = git(config, "show", "-s", "--format=%GF%n%B", candidate).decode("utf-8").splitlines()
    require(identity[0] == SIGNER
            and "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in identity,
            "Signing fingerprint or trailer differs")
    runner_sha = sha(frozen(runner))
    guard, _ = start_guard("B123 signed held-comparison delta verification")
    try:
        blob = lambda commit, path: git(config, "show", f"{commit}:{path}")
        raw_manifest = blob(candidate, "manifest.json")
        manifest = json.loads(raw_manifest)
        current = check_runtime(json.loads(blob(config["base"], "manifest.json")), manifest)
        require(len(current) == prior["runtimeEntries"] == 8708, "Runtime membership differs")
        before, old_body = parse(blob(PARENT, CARD).decode("utf-8").replace("\r\n", "\n"))
        after, new_body = parse(blob(candidate, CARD).decode("utf-8").replace("\r\n", "\n"))
        added = check_followup_metadata(before, after)
        require("## Notes" in old_body and "## Notes" in new_body
                and old_body.split("## Notes", 1)[0] == new_body.split("## Notes", 1)[0],
                "Teaching outside the scoped notes changed")
        for character in [*after["distractors"], *after["quiz_exclusions"]]:
            require(f"kanji/{character}.md" in current, f"Unresolved counterpart: {character}")
        for path in (STROKES, WORD):
            require(blob(candidate, path) == blob(PARENT, path), f"Preserved runtime changed: {path}")
        for path in (CARD, STROKES, WORD):
            require(sha(blob(candidate, path).replace(b"\r\n", b"\n")) == current[path],
                    f"Manifest hash differs: {path}")
        delta = git(config, "diff", "--name-status", "--no-renames", PARENT, candidate).decode("utf-8")
        source_paths = check_delta(delta)
        artifacts = {path: sha(blob(candidate, path)) for path in source_paths}
        capture = json.loads(frozen(CAPTURE, CAPTURE_SHA))
        require(capture["candidate"] == PARENT
                and {s["character"] for s in capture["sources"]} == set(REQUIRED) | OPTIONAL,
                "Captured comparison scope differs")
        manifest_path = PREFIX + "source-manifest.json"
        require(manifest_path in source_paths, "Missing source-reference manifest")
        references = json.loads(blob(candidate, manifest_path))
        require(references["schemaVersion"] == 1 and references["candidateParent"] == PARENT
                and references["captureProvenanceSha256"] == CAPTURE_SHA,
                "Source-reference provenance differs")
        refs = references["sources"]
        require(len(refs) == 9 and {r["character"] for r in refs} == set(REQUIRED) | OPTIONAL,
                "Source references missing or duplicated")
        verified_refs = []
        for source in capture["sources"]:
            raw = frozen(Path(source["raw"]["path"]), source["raw"]["sha256"])
            extract = frozen(Path(source["extract"]["path"]), source["extract"]["sha256"])
            require(source["raw"]["sha256"] not in artifacts.values()
                    and source["extract"]["sha256"] not in artifacts.values(),
                    "Complete newly captured third-party source must stay local")
            reference = next(r for r in refs if r["character"] == source["character"])
            check_source_reference(reference, source, extract)
            verified_refs.append({"character": source["character"],
                                  "rawSha256": sha(raw), "extractSha256": sha(extract),
                                  "quotedCharacters": sum(len(q["text"]) for q in reference["quotes"])})
            guard.check()
        xml_proof = None
        if any(path.endswith(".xml") for path in source_paths):
            existing = ["docs/n1-sources/batch-123/reconciliation-001/" + name
                        for name in ("kanjidic2-records.xml", "jmdict-records.xml")]
            xml_proof = verify_sources(config, candidate, [*source_paths, *existing], guard)
        summary_raw = frozen(gates / "summary.json")
        summary = json.loads(summary_raw)
        check_summary(summary, {**config, "candidate": PARENT}, candidate,
                      sha(raw_manifest), runner_sha)
        require(summary.get("requiredParent", summary.get("parent")) == PARENT,
                "Committed runner must bind the immediate parent")
        receipts = []
        for name in CHECKS:
            raw, log = frozen(gates / f"{name}.json"), frozen(gates / f"{name}.log")
            check_gate(json.loads(raw), log, name, sha(raw_manifest), config["repo"], runner_sha)
            receipts.append({"gate": name, "receiptSha256": sha(raw), "logSha256": sha(log)})
            guard.check()
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Revision verification RAM breach")
    print(json.dumps(freeze_json(output, {
        "batch": 123, "status": "PASS", "candidate": candidate, "parent": PARENT,
        "initial": config["candidate"], "base": config["base"],
        "priorRevisionProof": {"path": str(PRIOR_PROOF), "sha256": PRIOR_SHA},
        "manifestSha256": sha(raw_manifest), "contentVersion": manifest["contentVersion"],
        "runtimeEntries": len(current), "newGuards": added,
        "changedPathsFromParent": delta.splitlines(), "signedSourceArtifacts": artifacts,
        "newCapture": {"path": str(CAPTURE), "sha256": CAPTURE_SHA},
        "verifiedSourceReferences": verified_refs, "newXmlRecordProof": xml_proof,
        "gates": receipts,
        "gateSummary": {"path": str(gates / "summary.json"), "sha256": sha(summary_raw)},
        "runner": {"path": str(runner), "sha256": runner_sha},
        "signature": {"fingerprint": SIGNER, "ownerVerified": True}, "worktreeClean": True,
        "earlierSignedSourcesAndNonScopedRuntimePreserved": True,
        "sourceMembersPublishedBeforeBatch": 252, "sourceMembersInCandidate": 253,
        "memory": memory, "linguisticAcceptance": False, "publicationAccepted": False,
        "limits": "Exact signed additive delta, source references, bounded quote identities and ten host gates only. "
                  "Prior unchanged dictionary records inherit the frozen earlier proof; newly added "
                  "XML records, if any, are independently rechecked. Source decisions, claim closure "
                  "and reviewer confirmations remain separate. Complete new third-party captures stay local; "
                  "the byte cap alone is not a license or copyright determination. No native or whole-set acceptance.",
    })))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
