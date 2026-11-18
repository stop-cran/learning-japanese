"""Successor to prepare_b130_source_facts.py for B130's residual final JMdict union.

The observed author packet adds jmdict-final-families.xml: only the families matched by
the final union predicates that are absent from the two earlier JMdict outputs. The frozen
generic source verifier cannot express a residual file, so this preparer freezes the
unchanged earlier selections for it and separate facts for verify_b130_final_sources.py.
"""
import json
import re
import sys
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard
import prepare_b130_source_facts as v1
from prepare_b129_source_facts import literal_assignment
from verify_b130_payload import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, SOURCE_VERIFIER_SHA
from verify_b130_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

V1_SHA = "11b2173c11af0183a490a0be136387171425b932ba8ef72522bbb130ac1644ef"
FINAL_PRODUCER = "final_sources_b130.py"
FINAL_PRODUCER_SHA = "1700179f812d4ea3e52a56e0c61f9af219eec9e4be8e6f96f5da548d2f4d6a9c"
FINAL = {"residual": "jmdict-final-families.xml", "membership": "final-query-membership.json",
         "audit": "final-source-audit.json", "readingKeys": "reading-keys.json"}


def final_queries(jm, tested):
    require([item["mode"] for item in jm] == ["union", "union"], "Final union needs both earlier union selections")
    require(set(tested) == set(MEMBERS)
            and all(isinstance(keys, list) and keys and len(keys) == len(set(keys))
                    and all(isinstance(key, str) and key for key in keys) for keys in tested.values()),
            "Tested reading keys differ")
    return sorted(set().union(*(item["queries"] for item in jm))
                  | {"exact-reb:" + key for keys in tested.values() for key in keys})


def final_selection(source, jm, kd):
    initial = json.loads(source("source-receipt.json"))
    supplement = json.loads(source("supplemental-source-receipt.json"))
    audit = json.loads(source(FINAL["audit"]))
    producer = source("producers/" + FINAL_PRODUCER)
    require(sha(producer) == audit["producerSha256"] == FINAL_PRODUCER_SHA,
            "Final producer changed; re-inspect its actual union predicates")
    tested = json.loads(source(FINAL["readingKeys"]))["testedKeys"]
    require(literal_assignment(producer, "KEYS") == tested, "Committed reading keys differ from the producer")
    require(audit["base"] == BASE and audit["dictionaryInputs"] == initial["dictionaryInputs"],
            "Final audit lineage differs")
    comparisons = set(initial["outputs"]["kanjidic2-comparison-records.xml"]["canonicalRecordHashes"])
    require(comparisons == set(kd[1]["queries"])
            and set(supplement["predicates"]["exactSpellings"])
            == {query.split(":", 1)[1] for query in jm[1]["queries"] if query.startswith("exact-keb:")}
            and set(supplement["predicates"]["exactReadings"])
            == {query.split(":", 1)[1] for query in jm[1]["queries"] if query.startswith("exact-reb:")},
            "Final producer inputs differ from the earlier selections")
    raw = source(FINAL["residual"])
    output = audit["finalAdditionalOutput"]
    require(sha(raw) == output["sha256"] and len(raw) == output["bytes"], "Residual output binding differs")
    return {"files": [jm[0]["file"], jm[1]["file"], FINAL["residual"]], **FINAL,
            "mode": "union", "queries": final_queries(jm, tested),
            "producer": {"name": FINAL_PRODUCER, "sha256": FINAL_PRODUCER_SHA}}


def main(candidate, facts_name, proof_name, final_facts_name, final_proof_name):
    require(re.fullmatch("[0-9a-f]{40}", candidate) is not None, "Full candidate SHA required")
    bindings_name = Path(facts_name).stem + "-bindings.json"
    names = [facts_name, proof_name, bindings_name, final_facts_name, final_proof_name]
    require(len(set(names)) == len(names), "Output filenames must differ")
    for name in names:
        require(Path(name).name == name and name.endswith(".json") and not (HERE / name).exists(),
                "Use new JSON files directly in the review directory")
    frozen(Path(v1.__file__), V1_SHA)
    frozen(Path(__file__).with_name("verify_b130_sources.py"), SOURCE_VERIFIER_SHA)
    guard, _ = start_guard("B130 signed source-selector preparation v2")
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
        jm, kd = v1.selections(source)
        final = final_selection(source, jm, kd)
        xml = {name.removeprefix(PREFIX) for name in
               git("ls-tree", "-r", "--name-only", candidate, "--", PREFIX).decode().splitlines()
               if name.endswith(".xml")}
        require(xml == {item["file"] for item in jm + kd} | {final["residual"]},
                "Signed packet has unverified XML selections")
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
    final_facts = freeze_json(HERE / final_facts_name, {
        "batch": 130, "base": BASE, "candidate": candidate, "sourceFacts": facts,
        "sourceProof": str(HERE / proof_name), **final, "output": str(HERE / final_proof_name),
    })
    print(json.dumps(freeze_json(HERE / bindings_name, {
        "candidate": candidate, "base": BASE, "facts": facts, "finalFacts": final_facts,
        "signedInputs": bindings, "producerSha256": sha(Path(__file__).read_bytes()), "memory": memory,
        "limits": "Includes zero-match queries and verifies per-family predicate provenance for the earlier "
                  "selections. Preparation only: complete original-source re-streams, the residual final "
                  "union and signed payload checks remain.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 6, "Usage: prepare_b130_source_facts_v2.py CANDIDATE FACTS_NAME PROOF_NAME "
                                "FINAL_FACTS_NAME FINAL_PROOF_NAME")
    main(*sys.argv[1:])
