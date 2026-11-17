"""Bind the five coordinator readbacks without assuming reused captures are frozen."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, readonly, require, sha, start_guard, write_frozen
from run_b134_closure_checks import REPO, lineage
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

ARTIFACT = Path(__file__).with_name("b134-coordinator-source-checks-001.json")
OUT = WS / "scratch-134" / "review" / "coordinator-source-checks-captures-001"


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def main():
    require(not OUT.exists(), "Preserve the previous capture attempt")
    raw = ARTIFACT.read_bytes()
    value = json.loads(raw)
    guard, _ = start_guard("B134 coordinator source-check bindings")
    try:
        git = Git(REPO, RUNNER, guard)
        reviewed = value["reviewedSnapshot"]

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == reviewed
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Candidate differs")

        clean()
        lineage(git, reviewed)
        evidence = {}
        for key, ref in value["evidence"].items():
            path = Path(ref["path"])
            data = path.read_bytes()
            require(sha(data) == ref["sha256"], "Source bytes differ: " + key)
            evidence[key] = (data, readonly(path))
            guard.check()
        prefix = "docs/n1-sources/batch-134-reconciliation-001/"

        def blob(name):
            return git("show", reviewed + ":" + prefix + name)

        jm = {n.findtext("ent_seq"): n for n in
              ET.fromstring(blob("jmdict-complete-families.xml")).findall("entry")}
        kd = {n.findtext("literal"): n for n in
              ET.fromstring(blob("kanjidic2-complete-characters.xml")).findall("character")}
        comparisons = json.loads(blob("comparison-index.json"))
        counts = {}
        for check in value["claimChecks"]:
            char = check["pair"][1]
            key = next(key for key in check["evidenceKeys"] if key.endswith("Readback"))
            text = evidence[key][0].decode("utf-8").replace("\r\n", "\n")
            article, rest = text.split("=== COMPLETE KANJIDIC2 CHARACTER ===\n")
            require(article.startswith("=== " + char + ": COMPLETE ARTICLE ===\n"),
                    "Readback header differs")
            article = article.split("\n", 1)[1].strip()
            original = git("show", reviewed + ":kanji/" + char + ".md")
            require(sha(original) == comparisons[char]["sha256"]
                    and article == original.decode("utf-8").replace("\r\n", "\n").strip(),
                    "Readback article differs")
            character, entries = rest.split("=== COMPLETE APPLICABLE EXACT-SPELLING FAMILIES ===\n")
            require(canonical(ET.fromstring(character)) == canonical(kd[char]),
                    "Readback KD record differs")
            nodes = ET.fromstring("<root>" + entries + "</root>").findall("entry")
            selected = {char, *comparisons[char]["linkedWords"]}
            expected = {identity for identity, node in jm.items()
                        if {n.text for n in node.findall("k_ele/keb")} & selected}
            require(len(nodes) == len(expected)
                    and {n.findtext("ent_seq") for n in nodes} == expected,
                    "Readback family membership differs")
            for node in nodes:
                require(canonical(node) == canonical(jm[node.findtext("ent_seq")]),
                        "Readback JMdict record differs")
            counts[char] = len(nodes)
            guard.check()
        require(ARTIFACT.read_bytes() == raw, "Coordinator artifact changed")
        for key, ref in value["evidence"].items():
            require(Path(ref["path"]).read_bytes() == evidence[key][0], "Source changed: " + key)
        clean()
    finally:
        memory = guard.finish()
        require(not memory["breach"], "RAM breach")
    captures = {
        key: {**write_frozen(OUT / (key + ".txt"), data), "originalReadOnly": was_readonly,
              "original": value["evidence"][key]}
        for key, (data, was_readonly) in evidence.items()
    }
    result = {
        "status": "PASS_SOURCE_BINDINGS_NOT_LINGUISTIC_PROOF",
        "artifact": write_frozen(OUT / "coordinator-source-checks.json", raw),
        "candidate": reviewed, "completeReadbackFamilies": counts, "captures": captures,
        "producer": write_frozen(OUT / "producer.py", Path(__file__).read_bytes()),
        "memory": memory,
        "preservedFailure": "coordinator-source-checks-execution-001 rejected a false ReadOnly "
                            "assumption about reused local captures. Their original bytes and "
                            "attributes were not changed; hash-verified immutable copies are here.",
        "limits": "Complete signed-record/article equality for five readbacks only. The coordinator "
                  "decisions remain partial, nonblind and not replacement-review or publication acceptance.",
    }
    print(json.dumps(freeze_json(OUT / "verification.json", result)))


if __name__ == "__main__":
    main()
