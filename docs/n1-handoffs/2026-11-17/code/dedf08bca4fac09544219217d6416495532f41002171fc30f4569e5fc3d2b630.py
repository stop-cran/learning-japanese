"""Successor to prepare_b134_source_facts.py; reuses its frozen selection logic and fixes bindings output."""
import json
import re
import sys
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
PRIOR = TOOLS / "prepare_b134_source_facts.py"
PRIOR_SHA = "dd94b7011326df7a150656867fbdf1913fabdbb86d9f3d7ad1ca6b1443988301"
frozen(PRIOR, PRIOR_SHA)

from prepare_b134_source_facts import (
    BASE, BASELINE_CARDS, FINGERPRINT, Git, HELPERS, HERE, MEMBERS, ORIGIN, OWNER, PREFIX,
    PRODUCERS, REPO, RUNNER, TRAILER, selections,
)

FAILED_ATTEMPT = "source-facts-execution-001: facts written, bindings not written (TypeError in output call)."


def main(candidate, facts_name, proof_name):
    require(re.fullmatch("[0-9a-f]{40}", candidate) is not None, "Full candidate SHA required")
    bindings_name = Path(facts_name).stem + "-bindings.json"
    require(len({facts_name, proof_name, bindings_name}) == 3, "Output filenames must differ")
    for name in (facts_name, proof_name, bindings_name):
        require(Path(name).name == name and name.endswith(".json") and not (HERE / name).exists(),
                "Use new JSON files directly in the review directory")
    guard, _ = start_guard("B134 signed source-selector preparation v2")
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
    record = freeze_json(HERE / bindings_name, {
        "batch": 134, "status": "PREPARATION_ONLY", "candidate": candidate, "base": BASE,
        "facts": facts, "signedInputs": bindings,
        "signatureOutputSha256": sha(signature), "signatureOutput": signature.decode("utf-8", "replace"),
        "helpers": HELPERS, "producers": PRODUCERS,
        "selectionLogic": {"path": str(PRIOR), "sha256": PRIOR_SHA},
        "producerSha256": sha(frozen(Path(__file__))), "memory": memory,
        "preservedFailedAttempt": FAILED_ATTEMPT,
        "scanScope": "One actual complete expanded baseline scan per member is bound in both "
                     "schema slots; not two independently produced scans.",
        "limits": "Includes the search-only variant, absent additional exact/reading queries, all "
                  "linked comparison-word spellings, the KANJIDIC2-only component/variant supplement "
                  "and complete per-family predicate provenance. Original-source re-stream, full scan "
                  "reproduction, payload, gates, semantic review and publication remain separate.",
    })
    print(json.dumps(record, ensure_ascii=False))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: prepare_b134_source_facts_v2.py CANDIDATE FACTS_NAME PROOF_NAME")
    main(*sys.argv[1:])
