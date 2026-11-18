"""Verify B123's signed reconciliation without accepting its linguistic decisions."""
import gzip
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import CHECKS, GUARD_SHA, WS, freeze_json, frozen, git, load_batch, require, sha, start_guard
from confirm_v2 import clean
from verify_reconciliation_sources import element_value

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse

CARD = "kanji/\u7bc4.md"
STROKES = "strokes/\u7bc4.json"
WORD = "words/\u7bc4\u56f2.md"
SOURCE = "docs/n1-sources/batch-123/reconciliation-001/"
SIGNER = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
INPUTS = {
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz",
                 "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed",
                 "character", "literal"),
    "jmdict": ("n1-implementation-JMdict_e.gz",
              "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d",
              "entry", "ent_seq"),
}


def runtime(manifest):
    return {path: digest for entries in manifest.values() if isinstance(entries, dict)
            for path, digest in entries.items()}


def check_runtime(before, after):
    old, new = runtime(before), runtime(after)
    require(new.keys() - old.keys() == {CARD, STROKES} and old.keys() <= new.keys()
            and {path for path in old if old[path] != new[path]} == {WORD},
            "Unexpected baseline runtime change")
    return new


def check_metadata(original, revised):
    allowed = {"quiz_exclusions"}
    require({k: v for k, v in original.items() if k not in allowed}
            == {k: v for k, v in revised.items() if k not in allowed},
            "Reading, title, identity or other preserved metadata changed")
    old_guards, new_guards = original["quiz_exclusions"], revised["quiz_exclusions"]
    require(new_guards[:len(old_guards)] == old_guards
            and len(new_guards) == len(set(new_guards))
            and set("\u6a19\u7d00\u93e1\u69d8\u683c") <= set(new_guards), "Required or original guards changed")
    options = revised["distractors"]
    require(len(options) == len(set(options)) == 3
            and not set(options) & (set(new_guards) | {"\u7bc4"}),
            "Three distinct, non-excluded wrong-answer identities required")


def check_gate(receipt, log, name, manifest_sha, repo, runner_sha):
    memory = receipt["memory"]
    require(receipt["gate"] == name and receipt["exitCode"] == 0
            and receipt["childExitCodeAfterCleanup"] == 0
            and receipt["cwd"] == repo and receipt["logSha256"] == sha(log)
            and receipt["logBytes"] == len(log)
            and receipt["runnerSha256"] == runner_sha
            and receipt["guardSha256"] == GUARD_SHA
            and 0 < receipt["waitTimeoutSeconds"] <= 0.1
            and not memory["breach"] and memory["freeRamBeforeBytes"] > 2 * 1024**3
            and memory["minimumObservedFreeRamBytes"] >= 1024**3
            and memory["abortThresholdBytes"] == 1024**3
            and memory["samplingIntervalSeconds"] == 0.25,
            f"Failed, weakened or changed gate: {name}")
    if name in ("manifest", "manifest-rebuild"):
        require(receipt["manifestSha256"] == manifest_sha, "Gate manifest differs")
    if name == "manifest-rebuild":
        require(receipt["manifestReproducible"] is True, "Manifest rebuild differs")
    if name == "reading-exposure":
        require(all(value.encode("utf-8") in log for value in
                    ("\u7bc4", "\u30cf\u30f3", "\u306e\u308a", "\u3059\u3059\u3080")),
                "Target or supplemental readings missing from exposure evidence")


def verify_sources(config, candidate, paths, guard):
    expected, copies = {"kanjidic2": {}, "jmdict": {}}, {}
    artifacts = {}
    for path in paths:
        raw = git(config, "show", f"{candidate}:{path}")
        artifacts[path] = sha(raw)
        if path.endswith(".xml"):
            root = ET.fromstring(raw)
            kind = root.tag.lower()
            require(kind in INPUTS, f"Unknown dictionary extraction: {path}")
            _, _, tag, key = INPUTS[kind]
            nodes = root.findall(tag)
            require(nodes, f"Empty dictionary extraction: {path}")
            identifiers = [node.findtext(key) for node in nodes]
            require(all(identifiers) and len(identifiers) == len(set(identifiers)),
                    f"Missing or duplicate dictionary identities: {path}")
            for identifier, node in zip(identifiers, nodes):
                value = element_value(node)
                require(identifier not in expected[kind] or expected[kind][identifier] == value,
                        f"Conflicting extracted record: {kind}/{identifier}")
                expected[kind][identifier] = value
        if "/comparison-cards/" in path and path.endswith(".md"):
            character = Path(path).stem
            baseline = git(config, "show", f"{config['candidate']}:kanji/{character}.md")
            current = git(config, "show", f"{candidate}:kanji/{character}.md")
            require(raw == baseline == current, f"Comparison copy changed: {character}")
            copies[character] = sha(raw)
        guard.check()
    results = []
    for kind, (filename, digest, tag, key) in INPUTS.items():
        require(expected[kind], f"No complete {kind} reconciliation evidence")
        source = WS / "control" / "inputs" / filename
        computed = hashlib.sha256()
        with source.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                computed.update(chunk)
                guard.check()
        require(computed.hexdigest() == digest, f"Pinned input changed: {kind}")
        found = set()
        with gzip.open(source, "rb") as stream:
            for _, node in ET.iterparse(stream, events=("end",)):
                if node.tag != tag:
                    continue
                identifier = node.findtext(key)
                if identifier in expected[kind]:
                    require(identifier not in found and element_value(node) == expected[kind][identifier],
                            f"Incomplete or altered {kind} record: {identifier}")
                    found.add(identifier)
                node.clear()
                guard.check()
        require(found == set(expected[kind]), f"Missing source record: {kind}")
        results.append({"source": kind, "inputSha256": digest, "completeRecordsVerified": len(found),
                        "identifiers": sorted(found)})
    return {"dictionaryRecords": results, "comparisonCards": copies, "signedArtifacts": artifacts}



def check_summary(summary, config, candidate, manifest_sha, runner_sha):
    require(str(summary["batch"]) == "123"
            and summary["status"] == "PASS" and summary["mode"] == "committed"
            and summary["base"] == config["base"] and summary["startingHead"] == candidate
            and set(summary["checks"]) == set(CHECKS) and len(summary["checks"]) == len(CHECKS)
            and summary["manifestSha256"] == manifest_sha
            and summary["runnerSha256"] == runner_sha,
            "Gate summary is not for the exact committed revision")
    if "parent" in summary:
        require(summary["parent"] == config["candidate"], "Summary parent differs")
    if "manifestReproducible" in summary:
        require(summary["manifestReproducible"] is True, "Summary rebuild differs")


def verify(candidate, gates, runner, output):
    config = load_batch(123)
    runner_sha = sha(frozen(runner))
    clean(config, candidate)
    require(config["members"] == ["\u7bc4"], "Batch membership changed")
    require(git(config, "show", "-s", "--format=%P", candidate).decode().strip() == config["candidate"],
            "Expected the first direct signed reconciliation child")
    identity = git(config, "show", "-s", "--format=%GF%n%B", candidate).decode("utf-8").splitlines()
    require(identity[0] == SIGNER and
            "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in identity,
            "Signing fingerprint or trailer differs")
    guard, _ = start_guard("B123 signed reconciliation verification")
    try:
        blob = lambda commit, path: git(config, "show", f"{commit}:{path}")
        raw_manifest = blob(candidate, "manifest.json")
        manifest, before = json.loads(raw_manifest), json.loads(blob(config["base"], "manifest.json"))
        current = check_runtime(before, manifest)
        require(len(current) == 8708, "Unexpected runtime count")
        original, _ = parse(blob(config["candidate"], CARD).decode("utf-8").replace("\r\n", "\n"))
        revised, _ = parse(blob(candidate, CARD).decode("utf-8").replace("\r\n", "\n"))
        check_metadata(original, revised)
        for character in [*revised["distractors"], *revised["quiz_exclusions"]]:
            require(f"kanji/{character}.md" in current, f"Unresolved comparison ID: {character}")
        for path in (STROKES, WORD):
            require(blob(candidate, path) == blob(config["candidate"], path), f"Frozen runtime changed: {path}")
        for path in (CARD, STROKES, WORD):
            require(sha(blob(candidate, path).replace(b"\r\n", b"\n")) == current[path],
                    f"Manifest hash differs: {path}")
        changes = git(config, "diff", "--name-status", "--no-renames", config["candidate"], candidate).decode("utf-8")
        source_paths = []
        for line in changes.splitlines():
            status, path = line.split("\t")
            require((status == "M" and path in (CARD, "manifest.json"))
                    or (status == "A" and path.startswith(SOURCE)),
                    f"Unexpected or non-additive reconciliation delta: {line}")
            if path.startswith(SOURCE):
                source_paths.append(path)
        require(source_paths, "No additive reconciliation sources")
        source_proof = verify_sources(config, candidate, source_paths, guard)
        index = json.loads(blob(candidate, "docs/n1-sources/source-index.json"))
        pending = {row["kanji"] for row in index if row["statusAtFreeze"] == "pending"}
        count = lambda entries: len(pending & {Path(p).stem for p in entries if p.startswith("kanji/")})
        require(len(pending) == 1228 and count(runtime(before)) == 252 and count(current) == 253,
                "Source membership accounting differs")
        summary_raw = frozen(gates / "summary.json")
        summary = json.loads(summary_raw)
        check_summary(summary, config, candidate, sha(raw_manifest), runner_sha)
        receipts = []
        for name in CHECKS:
            raw, log = frozen(gates / f"{name}.json"), frozen(gates / f"{name}.log")
            check_gate(json.loads(raw), log, name, sha(raw_manifest), config["repo"], runner_sha)
            receipts.append({"gate": name, "receiptSha256": sha(raw), "logSha256": sha(log)})
            guard.check()
        result = {
            "batch": 123, "status": "PASS", "candidate": candidate, "initial": config["candidate"],
            "base": config["base"], "manifestSha256": sha(raw_manifest),
            "runner": {"path": str(runner), "sha256": runner_sha},
            "contentVersion": manifest["contentVersion"], "runtimeEntries": len(current),
            "changedPaths": changes.splitlines(), "sourceProof": source_proof, "gates": receipts,
            "gateSummary": {"path": str(gates / "summary.json"), "sha256": sha(summary_raw)},
            "baselineRuntimePreservedExceptRequiredWrappers": True,
            "originalMetadataStrokesGuardsAndSourceReceiptsPreserved": True,
            "sourceMembersPublishedBeforeBatch": 252, "sourceMembersInCandidate": 253,
            "signature": {"fingerprint": SIGNER, "ownerVerified": True}, "worktreeClean": True,
            "linguisticAcceptance": False, "publicationAccepted": False,
            "limits": "Exact signed delta, complete selected source records and host gates verified; "
                      "source selection, pair decisions and visual suitability still need substantive review. "
                      "No arbitrary-pool, whole-set, native/device or publication acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Reconciliation verification RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
