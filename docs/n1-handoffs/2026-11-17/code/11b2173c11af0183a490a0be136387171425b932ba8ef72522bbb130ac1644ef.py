"""Recover all B130 source predicates, including queries with no matches."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard
from prepare_b129_source_facts import literal_assignment, union_selection
from verify_b130_payload import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, SOURCE_VERIFIER_SHA, SUPPORTS
from verify_b130_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

HELPER_SHA = "a1f850826848325b2566c859353f424c8476fb6de05225cd1a79476722a989ea"
PRODUCERS = {
    "survey_b130.py": "4636bbf4fd73b03aa2b3fc51cd6caf56df582b784d07d8604e97980748385489",
    "supplement_b130.py": "199ebf60e0495c4b146b5ed09b84417259264aa4e89df2637615c51c45cfab26",
}


def verify_query_membership(raw, membership, selection):
    seen = set()
    for node in ET.fromstring(raw):
        require(node.tag == "entry", "Unexpected JMdict packet element")
        identity = node.findtext("ent_seq")
        require(identity and identity not in seen, "Missing or duplicate entry identity")
        seen.add(identity)
        spellings = {item.text for item in node.findall("k_ele/keb")}
        readings = {item.text for item in node.findall("r_ele/reb")}
        expected = set()
        for query in selection["queries"]:
            kind, value = query.split(":", 1)
            if kind == "contains-keb" and any(value in spelling for spelling in spellings):
                expected.add("contains:" + value)
            elif kind == "exact-keb" and value in spellings:
                expected.add("exact-spelling:" + value)
            elif kind == "exact-reb" and value in readings:
                expected.add("exact-reading:" + value)
        recorded = membership.get(identity, [])
        require(expected and len(recorded) == len(set(recorded)) and set(recorded) == expected,
                f"Per-family selection predicates differ: {identity}")
    require(seen == set(membership), "Query membership has missing or extra families")


def selections(source):
    frozen(Path(__file__).with_name("prepare_b129_source_facts.py"), HELPER_SHA)
    initial = json.loads(source("source-receipt.json"))
    supplement = json.loads(source("supplemental-source-receipt.json"))
    selection = json.loads(source("selection.json"))
    require(selection["batch"] == 130 and selection["base"] == BASE
            and selection["members"] == MEMBERS and selection["allDeclaredSupportArticles"] == SUPPORTS,
            "Observed B130 membership or support schema changed; re-inspect before deriving selectors")
    require(initial["batch"] == 130 and initial["base"] == supplement["base"] == BASE
            and initial["dictionaryInputs"] == supplement["originalInputs"],
            "Source receipt lineage or inputs differ")
    producers = {}
    for receipt, name in ((initial, "survey_b130.py"), (supplement, "supplement_b130.py")):
        raw = source("producers/" + name)
        require(sha(raw) == receipt["producerSha256"] == PRODUCERS[name],
                f"Producer changed; re-inspect its actual selection predicates: {name}")
        producers[name] = raw

    original = set("\u53e4\u53f3\u77f3")
    expanded = set()
    baseline = None
    for char in MEMBERS:
        first = json.loads(source(f"scans/{char}.json"))
        second = json.loads(source(f"scans-002/{char}.json"))
        require(first["base"] == second["base"] == BASE and first["kanji"] == second["kanji"] == char,
                f"Wrong scan identity: {char}")
        rows = {row["kanji"] for row in first["rows"]}
        require(len(first["rows"]) == len(rows) == 1251
                and {row["kanji"] for row in second["rows"]} == rows,
                "Incomplete or inconsistent baseline scan membership")
        require(baseline is None or rows == baseline, "Members use different baseline inventories")
        baseline = rows
        original.update(first["matches"])
        expanded.update(second["matches"])
    extra = literal_assignment(producers["supplement_b130.py"], "EXACT")
    extra_readings = literal_assignment(producers["supplement_b130.py"], "READINGS")
    expanded.update(extra & baseline)
    require(original <= baseline and expanded <= baseline, "Comparison selectors include nonbaseline cards")
    require(supplement["predicates"] == {
        "exactSpellings": sorted(expanded | extra), "exactReadings": sorted(extra_readings),
    }, "Supplemental receipt omits or changes producer queries")
    jm = [
        union_selection("jmdict-complete-families.xml", contains=[*MEMBERS, "\u5c4f"],
                        spellings=original | set(MEMBERS) | {word for words in SUPPORTS.values() for word in words},
                        readings=literal_assignment(producers["survey_b130.py"], "EXACT_READINGS")),
        union_selection("jmdict-supplemental-families.xml", spellings=expanded | extra,
                        readings=extra_readings),
    ]
    kd = [{"file": name, "mode": "exact", "queries": sorted(queries)} for name, queries in (
        ("kanjidic2-target-records.xml", MEMBERS),
        ("kanjidic2-comparison-records.xml", original),
        ("kanjidic2-supplemental-comparisons.xml", expanded),
    )]
    declared = {}
    for receipt in (initial, supplement):
        require(not declared.keys() & receipt["outputs"].keys(), "Duplicate declared source output")
        declared.update(receipt["outputs"])
    require(set(declared) == {item["file"] for item in jm + kd}, "Unaccounted source output")
    for item in jm + kd:
        raw = source(item["file"])
        require(sha(raw) == declared[item["file"]]["sha256"]
                and len(raw) == declared[item["file"]]["bytes"], "Source output binding differs")
    for item, name in zip(jm, ("query-membership.json", "supplemental-query-membership.json")):
        verify_query_membership(source(item["file"]), json.loads(source(name)), item)
    return jm, kd


def main(candidate, facts_name, proof_name):
    require(re.fullmatch("[0-9a-f]{40}", candidate) is not None, "Full candidate SHA required")
    bindings_name = Path(facts_name).stem + "-bindings.json"
    require(len({facts_name, proof_name, bindings_name}) == 3, "Output filenames must differ")
    for name in (facts_name, proof_name, bindings_name):
        require(Path(name).name == name and name.endswith(".json") and not (HERE / name).exists(),
                "Use new JSON files directly in the review directory")
    frozen(Path(__file__).with_name("verify_b130_sources.py"), SOURCE_VERIFIER_SHA)
    guard, _ = start_guard("B130 signed source-selector preparation")
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
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate owner/signature/parent differs")
        git("verify-commit", candidate, include_stderr=True)
        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing trailer")
        jm, kd = selections(source)
        xml = {name.removeprefix(PREFIX) for name in
               git("ls-tree", "-r", "--name-only", candidate, "--", PREFIX).decode().splitlines()
               if name.endswith(".xml")}
        require(xml == {item["file"] for item in jm + kd}, "Signed packet has unverified XML selections")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source preparation RAM breach")
    facts = freeze_json(HERE / facts_name, {
        "batch": 130, "repo": str(REPO), "base": BASE, "candidate": candidate, "prefix": PREFIX,
        "requireCheckout": True, "runner": RUNNER,
        "members": [{"kanji": char, "scans": {"original": f"scans/{char}.json",
                                            "expanded": f"scans-002/{char}.json"}} for char in MEMBERS],
        "jmdictSelections": jm, "kanjidic2Selections": kd, "expectedBaselineCards": 1251,
        "output": str(HERE / proof_name),
    })
    print(json.dumps(freeze_json(HERE / bindings_name, {
        "candidate": candidate, "base": BASE, "facts": facts, "signedInputs": bindings,
        "producerSha256": sha(Path(__file__).read_bytes()), "memory": memory,
        "limits": "Includes zero-match queries and verifies per-family predicate provenance. "
                  "Preparation only: complete original-source re-stream and signed payload checks remain.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: prepare_b130_source_facts.py CANDIDATE FACTS_NAME PROOF_NAME")
    main(*sys.argv[1:])
