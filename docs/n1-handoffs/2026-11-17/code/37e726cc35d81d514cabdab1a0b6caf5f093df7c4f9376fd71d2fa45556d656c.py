"""Bind the signed B131 correction, isolated responses and exact gate executions."""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from common import GUARD_SHA, WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen
from verify_b131_gate_evidence_v2 import ORDER, commands, memory_ok
from verify_b131_payload import LINK_HELPER, LINK_HELPER_SHA, REPO, RUNNER, runtime_entries
from verify_b131_revision_runtime_001 import BASE, INITIALS, PARENT, ROOT
from verify_b131_revision_sources_001 import ORIGINAL, PREFIX
from verify_b131_sources import Git

SCRATCH = ROOT.parent
EXECUTION_SHA = "23228af0051d8e87a5ce1864671c668587c1554591cee6a841cb8a2ea303737f"
FAMILIES = {
    "claude": re.compile(r"\b(?:claude|anthropic|opus|sonnet|haiku)\b", re.I),
    "gpt": re.compile(r"\b(?:gpt|openai|codex)\b", re.I),
}


def additive_body(before, after):
    before, after = (raw.decode("utf-8").replace("\r\n", "\n") for raw in (before, after))
    guard_line = re.search(r"^quiz_exclusions:.*$", before, re.M)
    require(guard_line is not None, "Original exclusions missing")
    restored, count = re.subn(r"^quiz_exclusions:.*$", lambda _: guard_line.group(), after, flags=re.M)
    require(count == 1, "Ambiguous exclusion metadata")
    old_body, old_tail = before.split("\nMetadata:", 1)
    new_body, new_tail = restored.split("\nMetadata:", 1)
    require(new_tail == old_tail and new_body.startswith(old_body), "Existing prose or metadata changed")
    added = new_body[len(old_body):]
    require(added.startswith("- ") and "## " not in added, "Unexpected additive Notes scope")
    return added


def pair_checks(table, cards, receipt, comparison):
    rows = table["rows"]
    require(table["parent"] == PARENT and table["publishedBase"] == BASE
            and [r["id"] for r in rows] == [f"R{i}" for i in range(1, 5)] + [f"Q{i}" for i in range(1, 14)]
            and len({tuple(r["pair"]) for r in rows}) == 17, "Incomplete or duplicate pair inventory")
    declared = {char: [] for char in cards}
    for row in rows:
        char, other = row["pair"]
        require(char in cards and other in comparison
                and row["displayedLabels"] == [cards[char]["title"], comparison[other][0]["title"]]
                and all(isinstance(row[k], str) and row[k].strip() for k in (
                    "comparisonLabelOnTarget", "targetLabelOnComparison", "qualificationAndResidualLimits"))
                and row["openQuizHold"] is False, "Unbound or unresolved directional pair")
        guarded = other in cards[char]["quiz_exclusions"]
        require(row["directExclusionOnNewEndpoint"] is guarded
                and row["decision"] == ("qualified-direct-precaution" if guarded else "bounded-non-collision"),
                "Pair disposition differs from actual direct guard")
        sources = row["sources"]
        ids = [str(identity) for identity in sources["completeJmdictEntryIds"]]
        require(sources["comparisonCardSha256"] == sha(comparison[other][1])
                and sources["completeComparisonCard"] == f"comparison-cards/{other}.md"
                and sources["completeKanjidicRecords"] == [char, other]
                and len(ids) == len(set(ids)) and sources["frozenExtractLines"]
                and sources["canonicalFamilyHashes"] == {
                    identity: receipt["outputs"]["jmdict-families.xml"]["canonicalRecordHashes"][identity]
                    for identity in ids}, "Pair source bindings differ")
        if guarded:
            declared[char].append(other)
    return declared


def check_gate_context(summary, admission, mode, candidate, manifest_sha, wrapper_sha, implementation_sha):
    head = PARENT if mode == "author" else candidate
    require(summary["batch"] == 131 and summary["revision"] == "reconciliation-001"
            and summary["mode"] == mode and summary["status"] == "PASS"
            and summary["parent"] == PARENT and summary["publishedBase"] == BASE
            and summary["startingHead"] == head and summary["serial"] is True
            and summary["checks"] == list(ORDER) and summary["manifestSha256"] == manifest_sha
            and summary["runnerSha256"] == wrapper_sha
            and summary["implementation"]["sha256"] == implementation_sha
            and Path(summary["implementation"]["path"]) == SCRATCH / "run_b131_gates.py"
            and summary["guardSha256"] == GUARD_SHA and summary["waitTimeoutSeconds"] == 0.1
            and summary["cleanupTimeoutSecondsPerStage"] == 10, "Reconciliation gate summary differs")
    require(admission["head"] == head and admission["parent"] == PARENT
            and admission["base"] == BASE and admission["mode"] == mode, "Gate admission differs")
    memory_ok(summary["finalMemory"])
    memory_ok(admission["memory"])


def main(runtime_path, source_path, handoff_path, output):
    paths = [Path(p).resolve() for p in (runtime_path, source_path, handoff_path)]
    output = Path(output).resolve()
    require(output.parent == ROOT and not output.exists(), "Use a new B131 evidence directory")
    runtime, source, handoff = [json.loads(frozen(path)) for path in paths]
    candidate = runtime["candidate"]
    require(runtime["status"] == "PASS_RUNTIME_ONLY" and source["status"] == "PASS_COMPLETE_SOURCES_ONLY"
            and candidate == source["candidate"] == handoff["candidate"]
            and runtime["parent"] == source["parent"] == handoff["parent"] == PARENT
            and source["runtimeProof"] == {"path": str(paths[0]), "sha256": sha(frozen(paths[0]))}
            and not source["reviewAccepted"] and not source["publicationAccepted"],
            "Proofs do not bind the same unaccepted successor")
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b131_revision_gate_bindings", LINK_HELPER)
    execution_path = Path(__file__).with_name("verify_b130_evidence_v3.py")
    frozen(execution_path, EXECUTION_SHA)
    execution = load_module("b131_revision_serial_execution", execution_path)
    guard, _ = start_guard("B131 signed reconciliation evidence")
    git = Git(REPO, RUNNER, guard)
    cache, captured, gate_sets = {}, {}, {}

    def blob(path, revision=candidate):
        key = (revision, path)
        if key not in cache:
            cache[key] = git("show", f"{revision}:{path}")
        raw = cache[key]
        if revision == candidate:
            require(raw == (REPO / path).read_bytes(), "Signed checkout differs: " + path)
        guard.check()
        return raw

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Candidate changed")

    try:
        clean()
        require(len(handoff["changedFiles"]) == len(set(handoff["changedFiles"]))
                == len(runtime["changedPaths"]) and set(handoff["changedFiles"]) == set(runtime["changedPaths"]),
                "Handoff changed-file inventory differs")
        for path, digest in runtime["signedArtifacts"].items():
            require(sha(blob(path)) == digest, "Signed runtime proof artifact differs")
        for path, digest in source["signedBindings"].items():
            require(sha(blob(path)) == digest, "Signed source proof artifact differs")
        inventory = json.loads(blob(PREFIX + "evidence-inventory-001.json"))
        require({path[len(PREFIX):] for path in runtime["changedPaths"] if path.startswith(PREFIX)}
                == set(inventory["files"]) | {"evidence-inventory-001.json"}, "Packet inventory differs")
        for name, digest in inventory["files"].items():
            require(sha(blob(PREFIX + name)) == digest, "Packet inventory hash differs")
        dependencies = json.loads(blob(PREFIX + "tool-bindings.json"))
        require(dependencies["guardSha256"] == GUARD_SHA, "Author resource guard changed")
        for name, digest in dependencies["originalImmutableProducerDependencies"].items():
            require(sha(blob(ORIGINAL + "producers/" + name)) == digest
                    and blob(ORIGINAL + "producers/" + name) == (SCRATCH / name).read_bytes(),
                    "Executed original producer differs")
        for name in dependencies["newProducerNames"]:
            require(blob(PREFIX + "producers/" + name) == (SCRATCH / name).read_bytes(),
                    "Executed reconciliation producer differs")
        notes = {char: additive_body(blob(f"kanji/{char}.md", PARENT), blob(f"kanji/{char}.md"))
                 for char in runtime["cardMetadata"]}
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        parse_card = lambda raw: parse(raw.decode("utf-8").replace("\r\n", "\n"))[0]
        table_raw = blob(PREFIX + "pair-dispositions-001.json")
        table = json.loads(table_raw)
        comparisons = {row["pair"][1] for row in table["rows"]}
        comparisons = {char: (parse_card(blob(f"kanji/{char}.md")),
                              blob(PREFIX + f"comparison-cards/{char}.md")) for char in comparisons}
        cards = {char: parse_card(blob(f"kanji/{char}.md")) for char in runtime["cardMetadata"]}
        receipt = json.loads(blob(PREFIX + "source-receipt.json"))
        declared = pair_checks(table, cards, receipt, comparisons)
        require(all(set(declared[char]) == set(runtime["cardMetadata"][char]["addedGuards"])
                    for char in declared), "Added guards and source table differ")
        require(not any(pattern.search(table_raw.decode("utf-8")) for pattern in FAMILIES.values()),
                "Neutral pair table contains review-family attribution")
        responses = {}
        for family, (directory, run) in INITIALS.items():
            accepted = json.loads(frozen(ROOT / directory / f"{run}-acceptance.json"))
            mapping_raw = blob(PREFIX + f"responses/{family}-mapping-001.json")
            response_raw = blob(PREFIX + f"responses/{family}-response-001.md")
            mapping = json.loads(mapping_raw)
            opposite = "gpt" if family == "claude" else "claude"
            require(not FAMILIES[opposite].search((mapping_raw + response_raw).decode("utf-8"))
                    and mapping["run"] == run and mapping["parent"] == PARENT
                    and mapping["neutralTableSha256"] == sha(table_raw)
                    and mapping["independentConfirmation"] is False and mapping["publicationAccepted"] is False,
                    "Response lineage, isolation or acceptance boundary differs")
            required = [accepted["report"], accepted["adjudication"], {
                "path": str(ROOT / directory / f"{run}-acceptance.json"),
                "sha256": sha(frozen(ROOT / directory / f"{run}-acceptance.json"))}]
            require(mapping["originalBindings"] == required, "Response original bindings differ")
            for binding in required:
                frozen(binding["path"], binding["sha256"])
            responses[family] = {"mappingSha256": sha(mapping_raw), "responseSha256": sha(response_raw)}
        implementation_sha = dependencies["originalImmutableProducerDependencies"]["run_b131_gates.py"]
        common_sha = dependencies["originalImmutableProducerDependencies"]["b131_common.py"]
        wrapper_sha = sha(blob(PREFIX + "producers/r131_gates.py"))
        for mode in ("author", "committed"):
            directory = SCRATCH / "reconciliation-001" / f"{mode}-gates-001"
            files = {path.name: path.read_bytes() for path in directory.iterdir()}
            require(set(files) == {"admission.json", "summary.json",
                                    *(f"{name}.{suffix}" for name in ORDER for suffix in ("json", "log"))},
                    "Incomplete gate directory")
            summary, admission = [json.loads(files[name]) for name in ("summary.json", "admission.json")]
            check_gate_context(summary, admission, mode, candidate, runtime["manifestSha256"],
                               wrapper_sha, implementation_sha)
            records = helper.gate_bindings(directory, {"repo": str(REPO)}, runtime["manifestSha256"],
                                           implementation_sha, guard)
            receipts = {}
            for record in records:
                name = record["gate"]
                require(record["receiptSha256"] == summary["logs"][name]["receiptSha256"] == sha(files[name + ".json"])
                        and record["logSha256"] == summary["logs"][name]["logSha256"] == sha(files[name + ".log"]),
                        "Gate execution binding differs")
                receipts[name] = json.loads(files[name + ".json"])
                memory_ok(receipts[name]["memory"])
            execution.verify_execution(receipts, commands(), common_sha)
            if mode == "author":
                require(all(raw == blob(PREFIX + f"author-evidence/{directory.name}/{name}")
                            for name, raw in files.items()), "Signed author execution copy differs")
            require(sha(files["summary.json"]) == handoff["proof"][directory.name]["summarySha256"],
                    "Gate handoff hash differs")
            require(all(raw == (directory / name).read_bytes() for name, raw in files.items()),
                    "Gate files changed while being checked")
            captured.update({directory.name + "/" + name: raw for name, raw in files.items()})
            gate_sets[mode] = {"summarySha256": sha(files["summary.json"]), "gates": records,
                              "firstStartedAt": receipts[ORDER[0]]["startedAt"],
                              "lastCompletedAt": receipts[ORDER[-1]]["completedAt"]}
        require(datetime.fromisoformat(gate_sets["committed"]["firstStartedAt"]) >=
                datetime.fromisoformat(gate_sets["author"]["lastCompletedAt"]), "Gate groups overlap")
        original_log = blob(ORIGINAL + "author-evidence/author-gates-003/quiz-safety.log")
        warnings = [line for line in original_log.splitlines() if line.startswith(b"WARN")]
        for mode in ("author", "committed"):
            group = mode + "-gates-001/"
            require([line for line in captured[group + "quiz-safety.log"].splitlines() if line.startswith(b"WARN")]
                    == warnings, "Historical quiz warnings were dropped or changed")
            reading = captured[group + "reading-exposure.log"].decode("utf-8")
            require("0 production hit(s)" in reading and "0 padded-session hit(s)" in reading
                    and "6 latent collision(s)" in reading, "Reading evidence or limits differ")
            lines = [line.partition(": ")[2] for line in reading.splitlines()
                     if line.startswith("Explicit supplemental reading keys: ")]
            require(len(lines) == 1 and json.loads(lines[0]) ==
                    json.loads(blob(ORIGINAL + "reading-keys.json"))["testedKeys"], "Supplemental keys differ")
            require(re.search(rb"(?m)^Ran [1-9]\d* tests in .+\r?$", captured[group + "unittest.log"])
                    and re.search(rb"(?m)^OK\r?$", captured[group + "unittest.log"]), "Unit suite did not pass")
        progress = json.loads(blob("docs/n1-sources/batch-131-progress-reconciliation-001.json"))
        require((progress["publishedDelivered"], progress["undelivered"], progress["frozenTotal"]) == (264, 964, 1228)
                and progress["deliveryNotIncremented"] is True
                and progress["manifestSha256"] == runtime["manifestSha256"]
                and progress["contentVersion"] == runtime["contentVersion"], "Progress accounting differs")
        for mode in ("author", "committed"):
            directory = SCRATCH / "reconciliation-001" / f"{mode}-preservation-001"
            summary_raw = (directory / "summary.json").read_bytes()
            summary = json.loads(summary_raw)
            hashes_raw = (directory / "runtime-hashes.json").read_bytes()
            require(summary["status"] == "PASS" and summary["parent"] == PARENT
                    and summary["head"] == (PARENT if mode == "author" else candidate)
                    and summary["manifestSha256"] == runtime["manifestSha256"]
                    and sha(summary_raw) == handoff["proof"][directory.name]["summarySha256"]
                    and sha(hashes_raw) == handoff["proof"][directory.name]["runtimeHashesSha256"]
                    and json.loads(hashes_raw) == {name: digest for name, (digest, _) in
                                                   runtime_entries(json.loads(blob("manifest.json"))).items()},
                    "Preservation evidence differs")
            memory_ok(summary["memory"])
            captured[directory.name + "/summary.json"] = summary_raw
            captured[directory.name + "/runtime-hashes.json"] = hashes_raw
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Reconciliation evidence RAM breach")
    captured_files = {name: write_frozen(output / name, raw) for name, raw in captured.items()}
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 131, "status": "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY",
        "candidate": candidate, "parent": PARENT, "base": BASE,
        "proofs": {name: {"path": str(path), "sha256": sha(frozen(path))}
                   for name, path in zip(("runtime", "sources", "handoff"), paths)},
        "pairCount": 17, "addedGuards": declared, "notesAdditions": notes, "isolatedResponses": responses,
        "gateSets": gate_sets, "warningCount": len(warnings), "capturedExecutionFiles": captured_files,
        "memory": memory, "producerSha256": sha(frozen(Path(__file__))),
        "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Mechanical signed-source, guard, additive-prose, isolated-response and host-execution "
                  "bindings only. The directional semantic claims require substantive adjudication "
                  "and both independent confirmations; no native, device or publication acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 5, "Usage: verify_b131_revision_evidence_001.py RUNTIME SOURCES HANDOFF OUTPUT")
    main(*sys.argv[1:])
