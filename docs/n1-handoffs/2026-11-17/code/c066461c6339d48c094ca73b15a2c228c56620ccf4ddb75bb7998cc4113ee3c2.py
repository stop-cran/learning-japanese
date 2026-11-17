"""Recover B133's complete source predicates from a clean signed candidate."""
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
    "verify_b133_payload.py": "b75726e35d93210a18fe72b953e5437b90d7f4efa0caedebcdc6c9f662b6b775",
    "verify_b133_sources.py": "84135cb99ff36f31bd6ac27fa9a82dd656c14dcf4d20c98c6852c45745cd5e71",
}
for name, digest in HELPERS.items():
    frozen(TOOLS / name, digest)

from prepare_b129_source_facts import literal_assignment, union_selection
from prepare_b130_source_facts import verify_query_membership
from prepare_b131_source_facts import verify_output
from prepare_b132_source_facts import verify_query_counts
from verify_b133_payload import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, SUPPORTS
from verify_b133_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

BASELINE_CARDS = 1258
CURATED = {
    "\u7434": ["\u53e4", "\u53f3", "\u5ddd"],
    "\u925b": ["\u53e4", "\u53f3", "\u5ddd"],
    "\u6edd": ["\u53e4", "\u53f3", "\u5bfa"],
}
PRODUCERS = {
    "sources_133.py": "84e67a0ae09642089000bc8a7e2c7f9006c2d68ec947973a986db454bed85a81",
    "sources_133_final.py": "1837d1f3cb7aace9f7cc3b26c4d130443b29c75d4ef0bfc986da279c639fc9a9",
    "supplement_133.py": "898203c48fa5c20fe4d453c13b4064dd3140c556a85a2199163bc1bd603f1646",
}


def initial_scope(source, initial, curated, readings):
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
    exact = comparisons | set(MEMBERS) | {word for words in SUPPORTS.values() for word in words}
    for char in sorted(comparisons):
        article = source(f"comparison-cards/{char}.md").decode("utf-8").replace("\r\n", "\n")
        exact.update(re.findall(r"\]\(\.\./words/([^/)]+)\.md\)", article))
    all_readings = {reading for values in readings.values() for reading in values}
    require(initial["containsKeys"] == MEMBERS + ["\u7027"]
            and initial["allExactSpellings"] == sorted(exact)
            and initial["allExactReadings"] == sorted(all_readings),
            "Initial predicates omit or alter target, variant, comparison, linked-word or reading queries")
    return comparisons, exact, all_readings


def selections(source):
    initial = json.loads(source("source-receipt.json"))
    supplemental = json.loads(source("supplemental-source-receipt.json"))
    selection = json.loads(source("selection.json"))
    pairs = [[char, word] for char in MEMBERS for word in SUPPORTS[char]]
    require(type(selection["batch"]) is int and selection["batch"] == 133
            and selection["base"] == BASE and selection["members"] == MEMBERS
            and selection["sourceRows"] == [707, 1120, 643]
            and selection["supports"] == pairs and selection["proseException"] is None,
            "B133 source scope changed; inspect before preparing a successor")
    require(initial["base"] == supplemental["base"] == BASE
            and initial["inputs"] == supplemental["inputs"], "Source inputs or bases differ")
    producers = {}
    for name, digest in PRODUCERS.items():
        raw = source("producers/" + name)
        require(sha(raw) == digest, "Inspected source producer changed: " + name)
        producers[name] = raw
    require(initial["producerSha256"] == PRODUCERS["sources_133.py"]
            and supplemental["producerSha256"] == PRODUCERS["supplement_133.py"],
            "Source receipt producer binding differs")
    require(literal_assignment(source("producers/common_133.py"), "BASE") == BASE,
            "Source helper uses another base")
    raw_supports = literal_assignment(producers["sources_133.py"], "SUPPORTS")
    require({char: raw_supports[char] for char in MEMBERS} == SUPPORTS,
            "Inspected source supports differ")
    readings = literal_assignment(producers["sources_133.py"], "READINGS")
    readings = {char: readings[char] for char in MEMBERS}
    require(json.loads(source("reading-keys.json"))["testedKeys"] == readings,
            "Complete explicit supplemental reading keys changed")
    comparisons, exact, all_readings = initial_scope(source, initial, CURATED, readings)
    variants = literal_assignment(producers["supplement_133.py"], "VARIANTS")
    components = literal_assignment(producers["supplement_133.py"], "COMPONENTS")
    extra = literal_assignment(producers["supplement_133.py"], "EXACT")
    require(supplemental["containsKeys"] == list(variants)
            and supplemental["allExactSpellings"] == extra
            and supplemental["allExactReadings"] == [],
            "Supplemental variant or lexical predicates differ")
    jm = [
        union_selection("jmdict-complete-families.xml", contains=MEMBERS + ["\u7027"],
                        spellings=exact, readings=all_readings),
        union_selection("jmdict-supplemental-families.xml", contains=variants, spellings=extra),
    ]
    kd = [{"file": name, "mode": "exact", "queries": sorted(set(queries))}
          for name, queries in (
              ("kanjidic2-targets.xml", MEMBERS),
              ("kanjidic2-comparisons.xml", comparisons),
              ("kanjidic2-variants-components.xml", variants + components),
          )]
    require(not initial["outputs"].keys() & supplemental["outputs"].keys(),
            "Duplicate source output")
    outputs = {**initial["outputs"], **supplemental["outputs"]}
    require(set(outputs) == {item["file"] for item in jm + kd}, "Unaccounted source output")
    for item in jm + kd:
        verify_output(source(item["file"]), outputs[item["file"]])
    for item, receipt, membership_name in (
        (jm[0], initial, "query-membership.json"),
        (jm[1], supplemental, "supplemental-query-membership.json"),
    ):
        membership = json.loads(source(membership_name))
        verify_query_membership(source(item["file"]), membership, item)
        queries = ["contains:" + value for value in receipt["containsKeys"]]
        queries += ["exact-spelling:" + value for value in receipt["allExactSpellings"]]
        queries += ["exact-reading:" + value for value in receipt["allExactReadings"]]
        verify_query_counts(membership, queries, receipt["queryCountsIncludingAbsences"])
    return jm, kd


def main(candidate, facts_name, proof_name):
    require(re.fullmatch("[0-9a-f]{40}", candidate) is not None, "Full candidate SHA required")
    bindings_name = Path(facts_name).stem + "-bindings.json"
    require(len({facts_name, proof_name, bindings_name}) == 3, "Output filenames must differ")
    for name in (facts_name, proof_name, bindings_name):
        require(Path(name).name == name and name.endswith(".json") and not (HERE / name).exists(),
                "Use new JSON files directly in the review directory")
    guard, _ = start_guard("B133 signed source-selector preparation")
    git = Git(REPO, RUNNER, guard)
    bindings = {}

    def source(name):
        raw = git("show", f"{candidate}:{PREFIX}{name}")
        bindings[PREFIX + name] = sha(raw)
        return raw

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
        jm, kd = selections(source)
        xml = {name.removeprefix(PREFIX) for name in
               git("ls-tree", "-r", "--name-only", candidate, "--", PREFIX).decode().splitlines()
               if name.endswith(".xml")}
        require(xml == {item["file"] for item in jm + kd}, "Signed packet has unaccounted XML")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    facts = freeze_json(HERE / facts_name, {
        "batch": 133, "repo": str(REPO), "base": BASE, "candidate": candidate,
        "prefix": PREFIX, "requireCheckout": True, "runner": RUNNER,
        "members": [{"kanji": char, "scans": {"original": f"scans/{char}.json",
                                            "expanded": f"scans/{char}.json"}} for char in MEMBERS],
        "jmdictSelections": jm, "kanjidic2Selections": kd,
        "expectedBaselineCards": BASELINE_CARDS, "output": str(HERE / proof_name),
    })
    print(json.dumps(freeze_json(HERE / bindings_name, {
        "batch": 133, "status": "PREPARATION_ONLY", "candidate": candidate, "base": BASE,
        "facts": facts, "signedInputs": bindings,
        "signatureOutputSha256": sha(signature), "signatureOutput": signature.decode("utf-8", "replace"),
        "helpers": HELPERS, "producerSha256": sha(frozen(Path(__file__))), "memory": memory,
        "scanScope": "One actual complete expanded baseline scan per member is bound in both "
                     "schema slots; not two independently produced scans.",
        "limits": "Includes absent variant/lexical queries, all linked comparison-word spellings "
                  "and complete per-family predicate provenance. Original-source re-stream, "
                  "full scan reproduction, payload, gates, semantic review and publication "
                  "remain separate requirements.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: prepare_b133_source_facts.py CANDIDATE FACTS_NAME PROOF_NAME")
    main(*sys.argv[1:])
