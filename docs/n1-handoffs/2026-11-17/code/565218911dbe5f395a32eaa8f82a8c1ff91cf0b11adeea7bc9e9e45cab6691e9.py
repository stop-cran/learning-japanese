"""Recover B131 selectors from its inspected, immutable signed source producers."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from b131_base_binding_v2 import CANDIDATE_BASE, SOURCE_BASE, verify_signed_binding
from prepare_b129_source_facts import literal_assignment, union_selection
from prepare_b130_source_facts import verify_query_membership
from verify_b131_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-131" / "review"
REPO = WS / "b131-worktree"
CANDIDATE = "1359b467e0edee8822c665614d6ca57e42785c4d"
PREFIX = "docs/n1-sources/batch-131/"
MEMBERS = list("\u885b\u7f8a\u971c")
SUPPORTS = {"\u885b": ["\u81ea\u885b", "\u885b\u661f"],
            "\u7f8a": ["\u7f8a\u6bdb"], "\u971c": ["\u971c"]}
RUNNER = {"path": str(HERE / "guarded-test-v3.py"),
          "sha256": "da78564efadb90ac4c174dbf13e375327b611bc5e0fc77913c8b85c22c1aaf6b"}
SOURCE_VERIFIER_SHA = "6efda73704e0ed665c540b5cba62d9de62613df5fc4c16ffe5ba52c834078e67"
FACTS = HERE / "source-facts-001.json"
PROOF = HERE / "source-verification-001.json"


def verify_output(raw, recorded):
    require(set(recorded) == {"sha256", "bytes", "canonicalRecordHashes"}
            and sha(raw) == recorded["sha256"] and len(raw) == recorded["bytes"],
            "Source output bytes differ from receipt")
    hashes = {}
    for node in ET.fromstring(raw):
        require(node.tag in {"entry", "character"}, "Unexpected source record")
        key = node.findtext("ent_seq") or node.findtext("literal")
        require(key and key not in hashes, "Missing or duplicate source identity")
        hashes[key] = sha(ET.canonicalize(ET.tostring(node, encoding="unicode"),
                                        strip_text=True).encode("utf-8"))
    require(hashes == recorded["canonicalRecordHashes"], "Source canonical hashes differ")


def selections(source):
    initial_raw = source("source-receipt.json")
    initial = json.loads(initial_raw)
    supplemental = json.loads(source("supplemental-source-receipt.json"))
    manual = json.loads(source("manual-source-receipt.json"))
    selection = json.loads(source("selection.json"))
    require(selection["batch"] == 131 and selection["base"] == SOURCE_BASE
            and selection["members"] == MEMBERS and selection["allDeclaredSupportArticles"] == SUPPORTS,
            "Signed source selection differs from inspected B131 scope")
    require(initial["batch"] == 131 and initial["base"] == supplemental["base"] == SOURCE_BASE
            and supplemental["sourceReceiptSha256"] == sha(initial_raw)
            and manual["base"] == CANDIDATE_BASE and manual["inputs"] == initial["inputs"],
            "Source receipt lineage differs")
    producers = {}
    for receipt, name in ((initial, "sources_b131.py"), (supplemental, "supplement_b131.py"),
                          (manual, "manual_sources_b131.py")):
        raw = source("producers/" + name)
        require(sha(raw) == receipt["producerSha256"], "Source producer binding differs: " + name)
        producers[name] = raw
    require(literal_assignment(source("producers/candidate_b131.py"), "BASE") == CANDIDATE_BASE,
            "Manual source producer base differs")
    extras = literal_assignment(producers["sources_b131.py"], "EXTRAS")
    require(json.loads(source("reading-keys.json"))["testedKeys"] == extras,
            "Final reading keys differ from inspected original source predicates")

    original, expanded = set("\u53e4\u53f3\u77f3"), set()
    baseline = None
    for char in MEMBERS:
        first = json.loads(source(f"scans/{char}.json"))
        second = json.loads(source(f"scans-002/{char}.json"))
        require(first["base"] == second["base"] == SOURCE_BASE
                and first["kanji"] == second["kanji"] == char, "Scan identity differs")
        rows = {row["kanji"] for row in first["rows"]}
        require(len(first["rows"]) == len(second["rows"]) == len(rows) == 1254
                and {row["kanji"] for row in second["rows"]} == rows
                and (baseline is None or rows == baseline), "Baseline scan inventory differs")
        baseline = rows
        original.update(first["matches"])
        expanded.update(second["matches"])
    added = expanded - original
    require(original | expanded <= baseline, "Comparison selection includes a nonbaseline card")
    exact = original | set(MEMBERS) | {word for words in SUPPORTS.values() for word in words}
    readings = set().union(*map(set, extras.values())) | {"\u3048\u3044", "\u3048", "\u3088\u3046", "\u305d\u3046"}
    require(initial["containsKeys"] == [*MEMBERS, "\u885e"]
            and initial["allExactSpellings"] == sorted(exact)
            and initial["allExactReadings"] == sorted(readings)
            and supplemental["allExactSpellings"] == sorted(added)
            and manual["allExactSpellings"] == ["\u5ddd"],
            "Receipt selectors omit or alter inspected producer queries")
    jm = [
        union_selection("jmdict-complete-families.xml", contains=[*MEMBERS, "\u885e"],
                        spellings=exact, readings=readings),
        union_selection("jmdict-supplemental-families.xml", spellings=added),
        union_selection("jmdict-manual-families.xml", spellings=["\u5ddd"]),
    ]
    kd = [{"file": name, "mode": "exact", "queries": sorted(queries)} for name, queries in (
        ("kanjidic2-target-records.xml", MEMBERS),
        ("kanjidic2-comparison-records.xml", original),
        ("kanjidic2-supplemental-comparisons.xml", added),
        ("kanjidic2-manual-comparisons.xml", ["\u5ddd"]),
    )]
    outputs = {}
    for receipt in (initial, supplemental, manual):
        require(not outputs.keys() & receipt["outputs"].keys(), "Duplicate declared source output")
        outputs.update(receipt["outputs"])
    require(set(outputs) == {item["file"] for item in jm + kd}, "Unaccounted source output")
    for item in jm + kd:
        verify_output(source(item["file"]), outputs[item["file"]])
    for item, name in zip(jm, ("query-membership.json", "supplemental-query-membership.json")):
        verify_query_membership(source(item["file"]), json.loads(source(name)), item)
    require(sha(source("comparison-cards/\u5ddd.md")) == manual["comparisonCardSha256"],
            "Manual comparison copy differs")
    for suffix in ("", "-002"):
        raw = source(f"jmdict-final-families{suffix}.xml")
        audit = json.loads(source(f"final-source-audit{suffix}.json"))
        verify_output(raw, audit["finalAdditionalOutput"])
        root = ET.fromstring(raw)
        require(root.tag == "JMdict" and not len(root), "Inspected residual is no longer empty")
    return jm, kd


def main():
    for path in (FACTS, PROOF, HERE / "source-facts-001-bindings.json", HERE / "signed-source-bridge-001.json"):
        require(not path.exists(), "Preserve existing source admission artifact: " + str(path))
    for name, expected in (
        ("verify_b131_sources.py", SOURCE_VERIFIER_SHA),
        ("b131_base_binding_v2.py", "76c11728caa881ede7179266fd7060e97bb861e773933d898ce331d46dcb8c2b"),
        ("prepare_b129_source_facts.py", "a1f850826848325b2566c859353f424c8476fb6de05225cd1a79476722a989ea"),
        ("prepare_b130_source_facts.py", "11b2173c11af0183a490a0be136387171425b932ba8ef72522bbb130ac1644ef"),
    ):
        frozen(TOOLS / name, expected)
    guard, _ = start_guard("B131 signed source-selector preparation")
    git = Git(REPO, RUNNER, guard)
    bindings = {}

    def source(name):
        raw = git("show", CANDIDATE + ":" + PREFIX + name)
        bindings[PREFIX + name] = sha(raw)
        return raw

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate is not the unchanged clean checkout")

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{CANDIDATE_BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Wrong owner, signature or parent")
        signature = git("verify-commit", CANDIDATE, include_stderr=True)
        require(TRAILER in git("show", "-s", "--format=%B", CANDIDATE), "Missing trailer")
        bridge = verify_signed_binding(git, CANDIDATE)
        jm, kd = selections(source)
        xml = {name.removeprefix(PREFIX) for name in
               git("ls-tree", "-r", "--name-only", CANDIDATE, "--", PREFIX).decode().splitlines()
               if name.endswith(".xml")}
        require(xml == {item["file"] for item in jm + kd}
                | {"jmdict-final-families.xml", "jmdict-final-families-002.xml"},
                "Signed packet has unaccounted XML selections")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    facts = freeze_json(FACTS, {
        "batch": 131, "repo": str(REPO), "base": CANDIDATE_BASE, "candidate": CANDIDATE,
        "prefix": PREFIX, "requireCheckout": True, "runner": RUNNER,
        "members": [{"kanji": char, "scans": {"original": f"scans/{char}.json",
                                            "expanded": f"scans-002/{char}.json"}} for char in MEMBERS],
        "jmdictSelections": jm, "kanjidic2Selections": kd, "expectedBaselineCards": 1254,
        "output": str(PROOF),
    })
    bridge_proof = freeze_json(HERE / "signed-source-bridge-001.json", {
        "status": "PASS_SIGNED_SOURCE_BASE_BRIDGE", **bridge,
        "signatureOutputSha256": sha(signature), "signatureOutput": signature.decode("utf-8", "replace"),
        "checkoutBound": True, "memory": memory,
        "producerSha256": sha(frozen(Path(__file__))),
        "limits": "Actual owner-signed candidate bridge only; source completeness, final gates, "
                  "content reviews and publication remain separate.",
    })
    print(json.dumps(freeze_json(HERE / "source-facts-001-bindings.json", {
        "status": "PREPARATION_ONLY", "candidate": CANDIDATE, "base": CANDIDATE_BASE,
        "sourceBase": SOURCE_BASE, "facts": facts, "signedBridge": bridge_proof,
        "signedInputs": bindings, "memory": memory, "producerSha256": sha(frozen(Path(__file__))),
        "limits": "Exact source selectors including absent queries and all comparison/support families. "
                  "Residual XML bytes are checked empty, not yet accepted as a complete final union. "
                  "Complete pinned-source re-stream, final-union audit and payload/gates remain pending.",
    })))


if __name__ == "__main__":
    main()
