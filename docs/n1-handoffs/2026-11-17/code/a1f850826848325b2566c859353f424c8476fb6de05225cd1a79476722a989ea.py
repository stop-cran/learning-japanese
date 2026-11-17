"""Freeze all eight B129 source selections from the signed author snapshot."""
import ast
import json
import re
import sys
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard
from verify_b129_payload import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, SOURCE_VERIFIER_SHA
from verify_b129_sources import FINGERPRINT, Git, OWNER


def literal_assignment(raw, name):
    nodes = [node.value for node in ast.parse(raw).body if isinstance(node, ast.Assign)
             and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)]
    require(len(nodes) == 1, f"Expected one literal assignment: {name}")
    return ast.literal_eval(nodes[0])


def union_selection(filename, contains=(), spellings=(), readings=()):
    queries = sorted({f"{kind}:{value}" for kind, values in (
        ("contains-keb", contains), ("exact-keb", spellings), ("exact-reb", readings))
        for value in values})
    require(bool(queries), f"Empty source selection: {filename}")
    return {"file": filename, "mode": "union", "queries": queries}


def selections(source):
    initial = json.loads(source("source-receipt.json"))
    supplement = json.loads(source("supplement-receipt-002.json"))
    final = json.loads(source("final-source-receipt.json"))
    additional = json.loads(source("additional-source-receipt.json"))
    extract = source("producers/extract_b129.py")
    require(sha(extract) == initial["producerSha256"], "Initial producer binding differs")
    for receipt, name in (
        (supplement, "supplement_b129.py"), (final, "final_sources_b129.py"),
        (additional, "additional_sources_b129.py"),
    ):
        require(sha(source("producers/" + name)) == receipt["producerSha256"],
                f"Producer binding differs: {name}")
    comparisons = set("\u53e4\u53f3\u77f3")
    expanded = set()
    for char in MEMBERS:
        comparisons.update(json.loads(source(f"scans/{char}.json"))["matches"])
        expanded.update(json.loads(source(f"scans-003/{char}.json"))["matches"])
        expanded.update(supplement["distractors"][char])
    explicit = {"\u7f82", "\u7f60", "\u7db2", "\u639b\u3051\u308b", "\u304b\u3068\u308a",
                "\u8679", "\u9713", "\u8309", "\u7d79"}
    extra_readings = {reading for char in MEMBERS
                      for reading in supplement["conservativeExternalReadingKeys"][char]}
    jm = [
        union_selection("jmdict-complete-families.xml", contains=[*MEMBERS, "\u9713"],
                        spellings=literal_assignment(extract, "EXACT"),
                        readings=literal_assignment(extract, "READINGS")),
        union_selection("jmdict-supplemental-comparisons-002.xml",
                        spellings=expanded | explicit, readings=extra_readings),
        {"file": "jmdict-final-comparisons.xml", "mode": "exact", "queries": final["comparisons"]},
        union_selection("jmdict-additional-families.xml", spellings=["\u6728\u7dbf"],
                        readings=["\u304d\u304e\u306c", "\u304e\u306c"]),
    ]
    kd = [{"file": filename, "mode": "exact", "queries": sorted(queries)} for filename, queries in (
        ("kanjidic2-target-records.xml", MEMBERS),
        ("kanjidic2-comparison-records.xml", comparisons),
        ("kanjidic2-comparison-records-003.xml", expanded),
        ("kanjidic2-final-comparisons.xml", final["comparisons"]),
    )]
    declared = {name for receipt in (initial, supplement, final) for name in receipt["outputs"]}
    declared.add(additional["output"]["filename"])
    require(declared == {item["file"] for item in jm + kd}, "Unaccounted source output")
    return jm, kd


def main(candidate, facts_name, proof_name):
    require(re.fullmatch("[0-9a-f]{40}", candidate) is not None, "Full candidate SHA required")
    for name in (facts_name, proof_name):
        require(Path(name).name == name and name.endswith(".json") and not (HERE / name).exists(),
                "Use new JSON files directly in the review directory")
    frozen(Path(__file__).with_name("verify_b129_sources.py"), SOURCE_VERIFIER_SHA)
    guard, _ = start_guard("B129 signed source-selector preparation")
    git = Git(REPO, RUNNER, guard)
    bindings = {}

    def source(name):
        raw = git("show", f"{candidate}:{PREFIX}{name}")
        bindings[PREFIX + name] = sha(raw)
        return raw

    try:
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Candidate is not clean")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate owner/signature/parent differs")
        jm, kd = selections(source)
        xml = {name.removeprefix(PREFIX) for name in
               git("ls-tree", "-r", "--name-only", candidate, "--", PREFIX).decode().splitlines()
               if name.endswith(".xml")}
        require(xml == {item["file"] for item in jm + kd}, "Signed packet has unverified XML selections")
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Candidate changed")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source preparation RAM breach")
    facts = freeze_json(HERE / facts_name, {
        "batch": 129, "repo": str(REPO), "base": BASE, "candidate": candidate, "prefix": PREFIX,
        "requireCheckout": True, "runner": RUNNER,
        "members": [{"kanji": char, "scans": {"original": f"scans/{char}.json",
                                            "expanded": f"scans-004/{char}.json"}} for char in MEMBERS],
        "jmdictSelections": jm, "kanjidic2Selections": kd, "expectedBaselineCards": 1248,
        "output": str(HERE / proof_name),
    })
    print(json.dumps(freeze_json(HERE / (Path(facts_name).stem + "-bindings.json"), {
        "candidate": candidate, "base": BASE, "facts": facts, "signedInputs": bindings,
        "producerSha256": sha(Path(__file__).read_bytes()), "memory": memory,
        "limits": "Selectors include zero-match queries. Preparation only; original-source re-stream "
                  "and signed payload verification must still pass.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: prepare_b129_source_facts.py CANDIDATE FACTS_NAME PROOF_NAME")
    main(*sys.argv[1:])
