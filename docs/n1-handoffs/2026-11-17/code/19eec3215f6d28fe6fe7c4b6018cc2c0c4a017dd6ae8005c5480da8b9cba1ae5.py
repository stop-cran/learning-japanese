"""Recover B132's complete selectors from a clean owner-signed candidate."""
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
    "verify_b132_payload_v2.py": "af5091da5140b08e12dd1dd182f3a5db512751e808ed522f3a757d065cb6ecff",
    "verify_b132_sources.py": "43ee9a6ceaf4ae023d4c9739b0a5276bdfd0c9c8573b410f99c5c06970dfe861",
}
for name, digest in HELPERS.items():
    frozen(TOOLS / name, digest)

from prepare_b129_source_facts import literal_assignment, union_selection
from prepare_b130_source_facts import verify_query_membership
from prepare_b131_source_facts import verify_output
from verify_b132_payload_v2 import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, SUPPORTS
from verify_b132_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

READINGS = ["\u307c", "\u306f\u304b", "\u3082", "\u304a\u304f\u3064\u304d",
            "\u3064\u304b", "\u3080\u306f\u3075", "\u304f\u3055"]
CURATED = set("\u66ae\u52df\u5ddd")


def verify_query_counts(membership, queries, recorded):
    require(len(queries) == len(set(queries)), "Duplicate declared query")
    expected = {query: sum(query in values for values in membership.values()) for query in queries}
    require(recorded == expected and all(type(value) is int for value in recorded.values()),
            "Query counts omit an absent query or differ from membership")


def verify_plain_spelling_membership(raw, membership, selection):
    prefixed = {key: ["exact-spelling:" + value for value in values]
                for key, values in membership.items()}
    verify_query_membership(raw, prefixed, selection)


def selections(source):
    initial_raw = source("source-receipt.json")
    initial = json.loads(initial_raw)
    supplemental = json.loads(source("supplemental-source-receipt.json"))
    selection = json.loads(source("selection.json"))
    require(selection["batch"] == 132 and selection["base"] == BASE
            and selection["members"] == MEMBERS and selection["sourceRows"] == [197]
            and selection["supports"] == [[MEMBERS[0], MEMBERS[0]]]
            and selection["proseException"] is None, "B132 source scope changed")
    require(initial["base"] == supplemental["base"] == BASE
            and supplemental["sourceReceiptSha256"] == sha(initial_raw),
            "Source receipt lineage differs")
    producers = {}
    for receipt, name in ((initial, "sources_132.py"), (supplemental, "supplement_132.py")):
        raw = source("producers/" + name)
        require(sha(raw) == receipt["producerSha256"], "Source producer binding differs: " + name)
        producers[name] = raw
    require(literal_assignment(source("producers/common_132.py"), "BASE") == BASE,
            "Executed source helper uses another base")
    require(literal_assignment(producers["sources_132.py"], "READINGS")[MEMBERS[0]] == READINGS
            and json.loads(source("reading-keys.json"))["testedKeys"] == {MEMBERS[0]: READINGS},
            "Complete explicit supplemental reading keys changed")

    scan = json.loads(source(f"scans/{MEMBERS[0]}.json"))
    baseline = {row["kanji"] for row in scan["rows"]}
    require(scan["base"] == BASE and scan["kanji"] == MEMBERS[0]
            and len(scan["rows"]) == len(baseline) == 1257
            and set(scan["matches"]) | CURATED <= baseline, "Baseline scan inventory differs")
    comparisons = set(scan["matches"]) | CURATED
    exact = comparisons | set(MEMBERS) | {word for words in SUPPORTS.values() for word in words}
    extra_spellings = literal_assignment(producers["supplement_132.py"], "SPELLINGS")
    require(initial["containsKeys"] == MEMBERS
            and initial["allExactSpellings"] == sorted(exact)
            and initial["allExactReadings"] == sorted(READINGS)
            and supplemental["allExactSpellings"] == extra_spellings,
            "Declared source predicates differ from inspected scope")
    jm = [
        union_selection("jmdict-complete-families.xml", contains=MEMBERS,
                        spellings=exact, readings=READINGS),
        union_selection("jmdict-supplemental-families.xml", spellings=extra_spellings),
    ]
    kd = [{"file": name, "mode": "exact", "queries": sorted(queries)} for name, queries in (
        ("kanjidic2-targets.xml", MEMBERS), ("kanjidic2-comparisons.xml", comparisons))]
    require(not initial["outputs"].keys() & supplemental["outputs"].keys(),
            "Duplicate source output")
    outputs = {**initial["outputs"], **supplemental["outputs"]}
    require(set(outputs) == {item["file"] for item in jm + kd}, "Unaccounted source output")
    for item in jm + kd:
        verify_output(source(item["file"]), outputs[item["file"]])
    membership = json.loads(source("query-membership.json"))
    verify_query_membership(source(jm[0]["file"]), membership, jm[0])
    queries = ["contains:" + value for value in MEMBERS]
    queries += ["exact-spelling:" + value for value in sorted(exact)]
    queries += ["exact-reading:" + value for value in sorted(READINGS)]
    verify_query_counts(membership, queries, initial["queryCountsIncludingAbsences"])
    supplementary_membership = json.loads(source("supplemental-query-membership.json"))
    verify_plain_spelling_membership(source(jm[1]["file"]), supplementary_membership, jm[1])
    verify_query_counts(supplementary_membership, extra_spellings, supplemental["countsIncludingAbsences"])
    return jm, kd


def main(candidate, facts_name, proof_name):
    require(re.fullmatch("[0-9a-f]{40}", candidate) is not None, "Full candidate SHA required")
    bindings_name = Path(facts_name).stem + "-bindings.json"
    require(len({facts_name, proof_name, bindings_name}) == 3, "Output filenames must differ")
    for name in (facts_name, proof_name, bindings_name):
        require(Path(name).name == name and name.endswith(".json") and not (HERE / name).exists(),
                "Use new JSON files directly in the review directory")
    guard, _ = start_guard("B132 signed source-selector preparation")
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
        "batch": 132, "repo": str(REPO), "base": BASE, "candidate": candidate,
        "prefix": PREFIX, "requireCheckout": True, "runner": RUNNER,
        "members": [{"kanji": char, "scans": {"original": f"scans/{char}.json",
                                            "expanded": f"scans/{char}.json"}} for char in MEMBERS],
        "jmdictSelections": jm, "kanjidic2Selections": kd, "expectedBaselineCards": 1257,
        "output": str(HERE / proof_name),
    })
    print(json.dumps(freeze_json(HERE / bindings_name, {
        "batch": 132, "status": "PREPARATION_ONLY", "candidate": candidate, "base": BASE,
        "facts": facts, "signedInputs": bindings,
        "signatureOutputSha256": sha(signature), "signatureOutput": signature.decode("utf-8", "replace"),
        "helpers": HELPERS, "producerSha256": sha(frozen(Path(__file__))), "memory": memory,
        "scanScope": "One actual complete expanded baseline scan is bound in both schema slots. "
                     "There is no invented second scan or assertion of a second author expansion.",
        "limits": "Includes absent queries and complete per-family predicate provenance. "
                  "Original-source re-stream, full baseline scan reproduction, signed payload, "
                  "gate evidence, independent content review and publication remain pending.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: prepare_b132_source_facts.py CANDIDATE FACTS_NAME PROOF_NAME")
    main(*sys.argv[1:])
