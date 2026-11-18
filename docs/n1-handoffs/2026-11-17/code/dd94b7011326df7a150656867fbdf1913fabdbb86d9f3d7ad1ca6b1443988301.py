"""Recover B134's complete source predicates from a clean signed candidate."""
import ast
import json
import re
import sys
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
HELPERS = {
    "prepare_b129_source_facts.py": "a1f850826848325b2566c859353f424c8476fb6de05225cd1a79476722a989ea",
    "prepare_b130_source_facts.py": "11b2173c11af0183a490a0be136387171425b932ba8ef72522bbb130ac1644ef",
    "prepare_b131_source_facts.py": "565218911dbe5f395a32eaa8f82a8c1ff91cf0b11adeea7bc9e9e45cab6691e9",
    "prepare_b132_source_facts.py": "19eec3215f6d28fe6fe7c4b6018cc2c0c4a017dd6ae8005c5480da8b9cba1ae5",
    "verify_b134_payload.py": "422a44461c37f5478d8ab2e6f52da82ce6fa76405391c6305baeecb7013b2a5f",
    "verify_b134_sources.py": "794a75b0a4d0f89bd7ec1066d9d917a262148c95159f18a20a71cc4e1d926aee",
}
for name, digest in HELPERS.items():
    frozen(TOOLS / name, digest)

from prepare_b129_source_facts import literal_assignment, union_selection
from prepare_b130_source_facts import verify_query_membership
from prepare_b131_source_facts import verify_output
from prepare_b132_source_facts import verify_query_counts
from verify_b134_payload import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, SUPPORTS
from verify_b134_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

BASELINE_CARDS = 1261
SOURCE_ROWS = [831]
VARIANT = "\u8308"
CURATED = {"\u7d2b": ["\u53e4", "\u53f3", "\u5ddd"]}
SUPPLEMENT = "supplement/kanjidic2-components-variant.xml"
PRODUCERS = {
    "sources_134.py": "437bfcd037ee87ca0129dd073fdd970b1dcc14b4213da8bb31aeb941c91a6b27",
    "sources_134_final.py": "8713abef42b5d75ab71594931f6f0bd4bf1fe2affb8fc695175205c47afd67f0",
    "supplement_134.py": "c3b66236adabd54bdf7e1b802b01bcf4b1d50de338848c0a064688d8ef25a87a",
}


def curated_assignment(raw, name="CURATED"):
    """Read a dict whose values are list literals or list(<string literal>) calls only."""
    nodes = [node.value for node in ast.parse(raw).body if isinstance(node, ast.Assign)
             and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)]
    require(len(nodes) == 1 and isinstance(nodes[0], ast.Dict), f"Expected one dict assignment: {name}")
    result = {}
    for key, value in zip(nodes[0].keys, nodes[0].values):
        key = ast.literal_eval(key)
        if (isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "list"
                and len(value.args) == 1 and not value.keywords
                and isinstance(value.args[0], ast.Constant) and isinstance(value.args[0].value, str)):
            items = list(value.args[0].value)
        else:
            items = ast.literal_eval(value)
        require(isinstance(key, str) and isinstance(items, list) and key not in result,
                f"Unsupported {name} entry")
        result[key] = items
    return result


def initial_scope(source, initial, curated, readings, additional):
    require(set(curated) == set(readings) == set(MEMBERS),
            "Source member reading or distractor inventory differs")
    comparisons = set().union(*(set(values) for values in curated.values()))
    baseline = None
    for char in MEMBERS:
        scan = json.loads(source(f"scans/{char}.json"))
        rows = {row["kanji"] for row in scan["rows"]}
        require(scan["base"] == BASE and scan["kanji"] == char
                and len(scan["rows"]) == len(rows) == BASELINE_CARDS
                and (baseline is None or rows == baseline),
                "Incomplete, inconsistent or wrong-base member scan")
        baseline = rows
        comparisons.update(scan["matches"])
    require(comparisons <= baseline, "Comparison selectors include nonbaseline cards")
    require(isinstance(additional, set) and all(isinstance(value, str) and value for value in additional),
            "Additional exact queries must be a literal set of spellings")
    exact = comparisons | set(MEMBERS) | set(additional) \
        | {word for words in SUPPORTS.values() for word in words}
    for char in sorted(comparisons):
        article = source(f"comparison-cards/{char}.md").decode("utf-8").replace("\r\n", "\n")
        exact.update(re.findall(r"\]\(\.\./words/([^/)]+)\.md\)", article))
    all_readings = {reading for values in readings.values() for reading in values}
    require(initial["containsKeys"] == MEMBERS + [VARIANT]
            and initial["allExactSpellings"] == sorted(exact)
            and initial["allExactReadings"] == sorted(all_readings),
            "Initial predicates omit or alter target, variant, comparison, additional, "
            "linked-word or reading queries")
    return comparisons, exact, all_readings


def selections(source, baseline_word):
    initial = json.loads(source("source-receipt.json"))
    supplemental = json.loads(source("supplement/receipt.json"))
    selection = json.loads(source("selection.json"))
    pairs = [[char, word] for char in MEMBERS for word in SUPPORTS[char]]
    require(type(selection["batch"]) is int and selection["batch"] == 134
            and selection["base"] == BASE and selection["members"] == MEMBERS
            and selection["sourceRows"] == SOURCE_ROWS
            and selection["supports"] == pairs and selection["proseException"] is None,
            "B134 source scope changed; inspect before preparing a successor")
    require(initial["base"] == supplemental["base"] == BASE, "Source bases differ")
    producers = {}
    for name, digest in PRODUCERS.items():
        raw = source("producers/" + name)
        require(sha(raw) == digest, "Inspected source producer changed: " + name)
        producers[name] = raw
    final = producers["sources_134_final.py"]
    require(initial["producerSha256"] == PRODUCERS["sources_134_final.py"]
            and supplemental["producerSha256"] == PRODUCERS["supplement_134.py"],
            "Source receipt producer binding differs")
    require(literal_assignment(source("producers/common_134.py"), "BASE") == BASE,
            "Source helper uses another base")
    require(literal_assignment(final, "CHARS") == "".join(MEMBERS), "Inspected source members differ")
    raw_supports = literal_assignment(final, "SUPPORTS")
    require(raw_supports == SUPPORTS, "Inspected source supports differ")
    require(curated_assignment(final) == CURATED, "Inspected curated comparisons differ")
    contains = literal_assignment(final, "CONTAINS")
    require(contains == MEMBERS + [VARIANT], "Inspected containing queries differ")
    readings = literal_assignment(final, "READINGS")
    require(set(readings) == set(MEMBERS), "Inspected reading keys cover other characters")
    require(json.loads(source("reading-keys.json"))["testedKeys"] == readings,
            "Complete explicit supplemental reading keys changed")
    additional = literal_assignment(final, "ADDITIONAL_EXACT")
    comparisons, exact, all_readings = initial_scope(source, initial, CURATED, readings, additional)
    for word in sorted({word for words in SUPPORTS.values() for word in words}):
        require(source(f"baseline-words/{word}.md") == baseline_word(word),
                f"Packet support baseline differs from signed base: {word}")
    wanted = list(literal_assignment(producers["supplement_134.py"], "WANTED"))
    require(len(wanted) == len(set(wanted)) and set(MEMBERS) | {VARIANT} <= set(wanted)
            and supplemental["selection"] == wanted,
            "Supplemental component/variant selection differs")
    jm = [union_selection("jmdict-complete-families.xml", contains=contains,
                          spellings=exact, readings=all_readings)]
    kd = [{"file": name, "mode": "exact", "queries": sorted(set(queries))}
          for name, queries in (
              ("kanjidic2-targets.xml", MEMBERS),
              ("kanjidic2-comparisons.xml", comparisons),
              (SUPPLEMENT, wanted),
          )]
    require(SUPPLEMENT not in initial["outputs"], "Duplicate source output")
    outputs = {**initial["outputs"], SUPPLEMENT: supplemental["output"]}
    require(set(outputs) == {item["file"] for item in jm + kd}, "Unaccounted source output")
    for item in jm + kd:
        verify_output(source(item["file"]), outputs[item["file"]])
    membership = json.loads(source("query-membership.json"))
    verify_query_membership(source(jm[0]["file"]), membership, jm[0])
    queries = ["contains:" + value for value in initial["containsKeys"]]
    queries += ["exact-spelling:" + value for value in initial["allExactSpellings"]]
    queries += ["exact-reading:" + value for value in initial["allExactReadings"]]
    verify_query_counts(membership, queries, initial["queryCountsIncludingAbsences"])
    return jm, kd


def main(candidate, facts_name, proof_name):
    require(re.fullmatch("[0-9a-f]{40}", candidate) is not None, "Full candidate SHA required")
    bindings_name = Path(facts_name).stem + "-bindings.json"
    require(len({facts_name, proof_name, bindings_name}) == 3, "Output filenames must differ")
    for name in (facts_name, proof_name, bindings_name):
        require(Path(name).name == name and name.endswith(".json") and not (HERE / name).exists(),
                "Use new JSON files directly in the review directory")
    guard, _ = start_guard("B134 signed source-selector preparation")
    git = Git(REPO, RUNNER, guard)
    bindings = {}

    def source(name):
        raw = git("show", f"{candidate}:{PREFIX}{name}")
        bindings[PREFIX + name] = sha(raw)
        return raw

    def baseline_word(word):
        return git("show", f"{BASE}:words/{word}.md")

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate is not the unchanged clean checkout")

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Wrong owner, signature or parent")
        signature = git("verify-commit", candidate, include_stderr=True)
        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing trailer")
        jm, kd = selections(source, baseline_word)
        xml = {name.removeprefix(PREFIX) for name in
               git("ls-tree", "-r", "--name-only", candidate, "--", PREFIX).decode().splitlines()
               if name.endswith(".xml")}
        require(xml == {item["file"] for item in jm + kd}, "Signed packet has unaccounted XML")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    facts = freeze_json(HERE / facts_name, {
        "batch": 134, "repo": str(REPO), "base": BASE, "candidate": candidate,
        "prefix": PREFIX, "requireCheckout": True, "runner": RUNNER,
        "members": [{"kanji": char, "scans": {"original": f"scans/{char}.json",
                                            "expanded": f"scans/{char}.json"}} for char in MEMBERS],
        "jmdictSelections": jm, "kanjidic2Selections": kd,
        "expectedBaselineCards": BASELINE_CARDS, "output": str(HERE / proof_name),
    })
    print(json.dumps(freeze_json(HERE / bindings_name, {
        "batch": 134, "status": "PREPARATION_ONLY", "candidate": candidate, "base": BASE,
        "facts": facts, "signedInputs": bindings,
        "signatureOutputSha256": sha(signature), "signatureOutput": signature.decode("utf-8", "replace"),
        "helpers": HELPERS, "producers": PRODUCERS, "producerSha256": sha(frozen(Path(__file__))),
        "memory": memory,
        "scanScope": "One actual complete expanded baseline scan per member is bound in both "
                     "schema slots; not two independently produced scans.",
        "limits": "Includes the search-only variant, absent additional exact/reading queries, all "
                  "linked comparison-word spellings, the KANJIDIC2-only component/variant supplement "
                  "and complete per-family predicate provenance. Original-source re-stream, full scan "
                  "reproduction, payload, gates, semantic review and publication remain separate.",
    }, ensure_ascii=False)))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: prepare_b134_source_facts.py CANDIDATE FACTS_NAME PROOF_NAME")
    main(*sys.argv[1:])
