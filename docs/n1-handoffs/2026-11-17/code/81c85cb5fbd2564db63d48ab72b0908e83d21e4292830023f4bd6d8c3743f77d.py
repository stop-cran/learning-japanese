"""Include the actual six-card supplemental source selection without replacing prior evidence."""
import json
import re
import sys
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
PRIOR_SHA = "c066461c6339d48c094ca73b15a2c228c56620ccf4ddb75bb7998cc4113ee3c2"
ADDITIONAL_SHA = "d30cf03e186bac21233f181df76f8f915952dd7a1ae89348a309a525f0a04115"
frozen(TOOLS / "prepare_b133_source_facts.py", PRIOR_SHA)

from prepare_b133_source_facts import (
    BASE, BASELINE_CARDS, HERE, MEMBERS, PREFIX, REPO, RUNNER,
    FINGERPRINT, Git, ORIGIN, OWNER, TRAILER, literal_assignment, selections,
    union_selection, verify_output, verify_query_counts)
from prepare_b132_source_facts import verify_plain_spelling_membership


def additional_scope(source, receipt, comparisons, baseline):
    require(len(comparisons) == len(set(comparisons)) == 6 and set(comparisons) <= baseline,
            "Additional comparisons must be six distinct baseline cards")
    exact = set(comparisons)
    for char in comparisons:
        raw = source(f"additional/comparison-cards/{char}.md")
        exact.update(re.findall(r"\]\(\.\./words/([^/)]+)\.md\)", raw.decode("utf-8")))
    require(receipt["allExactSpellings"] == sorted(exact),
            "Additional selector omits or changes a comparison-linked spelling")
    return exact


def all_selections(source):
    jm, kd = selections(source)
    initial = json.loads(source("source-receipt.json"))
    receipt = json.loads(source("additional/source-receipt.json"))
    producer = source("producers/additional_133.py")
    require(sha(producer) == receipt["producerSha256"] == ADDITIONAL_SHA,
            "Inspected additional producer changed")
    require(receipt["base"] == BASE and receipt["inputs"] == initial["inputs"],
            "Additional selection uses another base or original input")
    comparisons = literal_assignment(producer, "CHARS")
    require(comparisons == "\u4e18\u5316\u9280\u767d\u7b46\u70ad",
            "Additional comparison scope differs")
    scan = json.loads(source(f"scans/{MEMBERS[0]}.json"))
    baseline = {row["kanji"] for row in scan["rows"]}
    require(scan["base"] == BASE and len(scan["rows"]) == len(baseline) == BASELINE_CARDS,
            "Incomplete additional-comparison baseline")
    exact = additional_scope(source, receipt, comparisons, baseline)
    jm_item = union_selection("additional/jmdict-additional-families.xml", spellings=exact)
    kd_item = {"file": "additional/kanjidic2-additional-comparisons.xml",
               "mode": "exact", "queries": sorted(comparisons)}
    require(set(receipt["outputs"]) == {Path(item["file"]).name for item in (jm_item, kd_item)},
            "Unaccounted additional source output")
    for item in (jm_item, kd_item):
        verify_output(source(item["file"]), receipt["outputs"][Path(item["file"]).name])
    membership = json.loads(source("additional/query-membership.json"))
    verify_plain_spelling_membership(source(jm_item["file"]), membership, jm_item)
    verify_query_counts(membership, sorted(exact), receipt["queryCountsIncludingAbsences"])
    return jm + [jm_item], kd + [kd_item], comparisons


def main(candidate, facts_name, proof_name):
    require(re.fullmatch("[0-9a-f]{40}", candidate) is not None, "Full candidate SHA required")
    bindings_name = Path(facts_name).stem + "-bindings.json"
    require(len({facts_name, proof_name, bindings_name}) == 3, "Output filenames must differ")
    for name in (facts_name, proof_name, bindings_name):
        require(Path(name).name == name and name.endswith(".json") and not (HERE / name).exists(),
                "Use new JSON files directly in the review directory")
    guard, _ = start_guard("B133 complete signed source-selector preparation")
    git = Git(REPO, RUNNER, guard)
    bindings, comparison_bindings = {}, {}

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
        jm, kd, comparisons = all_selections(source)
        for char in comparisons:
            path = f"kanji/{char}.md"
            raw = source(f"additional/comparison-cards/{char}.md")
            require(raw == git("show", f"{BASE}:{path}"), "Additional comparison differs from signed baseline")
            comparison_bindings[char] = sha(raw)
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
        "facts": facts, "signedInputs": bindings, "additionalBaselineComparisons": comparison_bindings,
        "signatureOutputSha256": sha(signature), "signatureOutput": signature.decode("utf-8", "replace"),
        "priorProducerSha256": PRIOR_SHA, "additionalProducerSha256": ADDITIONAL_SHA,
        "producerSha256": sha(frozen(Path(__file__))), "memory": memory,
        "scanScope": "One actual complete expanded baseline scan per member is bound in both schema slots.",
        "limits": "Includes original, variant and six-card supplemental predicates, including absent "
                  "queries and complete linked-word spellings. Original-dictionary re-stream, full "
                  "scan reproduction, payload, gates, semantic review and publication remain separate.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: prepare_b133_source_facts_v2.py CANDIDATE FACTS_NAME PROOF_NAME")
    main(*sys.argv[1:])
