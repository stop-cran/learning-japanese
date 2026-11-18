"""Bind the coordinator's draft dispositions for all original B134 obligations to the signed tree."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, readonly, require, sha, start_guard, write_frozen
from run_b134_closure_checks import REPO, lineage
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

ARTIFACT = Path(__file__).with_name("b134-coordinator-obligation-map-001.json")
OUT = WS / "scratch-134" / "review" / "coordinator-obligation-map-001"
READBACKS = {"threadReadback": "糸", "fiberReadback": "維", "hallReadback": "館", "wrapReadback": "包"}
RUNS = {"claude": "N1-B134-CLAUDE-001", "gpt": "N1-B134-GPT-001"}


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def front_list(text, key):
    head = text.split("\n---\n", 1)[0]
    lines = [line for line in head.split("\n") if line.startswith(key + ": ")]
    if not lines:
        return []
    require(len(lines) == 1, "Duplicate front-matter key " + key)
    value = lines[0][len(key) + 2:].strip()
    require(value.startswith("[") and value.endswith("]"), "Unexpected list syntax for " + key)
    return [item.strip() for item in value[1:-1].split(",") if item.strip()]


def main():
    require(not OUT.exists(), "Preserve the previous obligation-map attempt")
    raw = ARTIFACT.read_bytes()
    value = json.loads(raw)
    guard, _ = start_guard("B134 coordinator obligation map")
    try:
        git = Git(REPO, RUNNER, guard)
        reviewed = value["reviewedSnapshot"]

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == reviewed
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Candidate differs")

        clean()
        lineage(git, reviewed)
        inventory_ref = value["obligationInventory"]
        inventory_bytes = Path(inventory_ref["path"]).read_bytes()
        require(sha(inventory_bytes) == inventory_ref["sha256"], "Obligation inventory differs")
        inventory = json.loads(inventory_bytes)
        require(inventory["initialSnapshot"] == value["initialSnapshot"]
                and inventory["status"] == "PREPARED_NOT_REVIEW_CLOSURE", "Inventory is unbound")
        required = {(RUNS[family], claim) for family, original in inventory["originals"].items()
                    for claim in original["requiredDispositionIds"]}
        require(len(required) == 29, "Expected 29 original obligations")
        evidence = {}
        for key, ref in value["evidence"].items():
            path = Path(ref["path"])
            data = path.read_bytes()
            require(sha(data) == ref["sha256"], "Evidence bytes differ: " + key)
            evidence[key] = (data, readonly(path))
            guard.check()

        def card(char):
            return git("show", reviewed + ":kanji/" + char + ".md").decode("utf-8").replace("\r\n", "\n")

        purple = card("紫")
        exclusions = front_list(purple, "quiz_exclusions")
        tags = front_list(purple, "tags")
        require(len(exclusions) == 56 and len(set(exclusions)) == 56, "Unexpected 紫 exclusion count")
        seen, checked = set(), []
        for item in value["dispositions"]:
            identity = (item["run"], item["id"])
            require(identity in required and identity not in seen, "Unexpected or duplicate obligation")
            require(item["status"] in ("resolved", "withdrawn", "optional")
                    and item["reason"].strip() and item["evidenceKeys"]
                    and all(key in evidence for key in item["evidenceKeys"]) and item["predicates"],
                    "Unsupported disposition " + item["id"])
            for predicate in item["predicates"]:
                kind = predicate["kind"]
                if kind == "exclusionPresent":
                    ok = predicate["char"] in exclusions
                elif kind == "exclusionAbsent":
                    ok = predicate["char"] not in exclusions
                elif kind == "pairUndeclared":
                    ok = (predicate["char"] not in exclusions
                          and "紫" not in front_list(card(predicate["char"]), "quiz_exclusions"))
                elif kind == "cardContains":
                    ok = predicate["text"] in purple
                elif kind == "cardLacks":
                    ok = predicate["text"].lower() not in purple.lower()
                elif kind == "tagPresent":
                    ok = predicate["tag"] in tags
                else:
                    ok = False
                require(ok, "Predicate failed: " + item["run"] + " " + item["id"] + " " + json.dumps(
                    predicate, ensure_ascii=False))
                checked.append(kind)
            seen.add(identity)
            guard.check()
        require(seen == required, "An original obligation lacks a draft disposition")

        prefix = "docs/n1-sources/batch-134-reconciliation-001/"

        def blob(name):
            return git("show", reviewed + ":" + prefix + name)

        jm = {n.findtext("ent_seq"): n for n in
              ET.fromstring(blob("jmdict-complete-families.xml")).findall("entry")}
        kd = {n.findtext("literal"): n for n in
              ET.fromstring(blob("kanjidic2-complete-characters.xml")).findall("character")}
        comparisons = json.loads(blob("comparison-index.json"))
        counts = {}
        for key, char in READBACKS.items():
            text = evidence[key][0].decode("utf-8").replace("\r\n", "\n")
            article, rest = text.split("=== COMPLETE KANJIDIC2 CHARACTER ===\n")
            require(article.startswith("=== " + char + ": COMPLETE ARTICLE ===\n"), "Readback header differs")
            article = article.split("\n", 1)[1].strip()
            original = git("show", reviewed + ":kanji/" + char + ".md")
            require(sha(original) == comparisons[char]["sha256"]
                    and article == original.decode("utf-8").replace("\r\n", "\n").strip(),
                    "Readback article differs: " + char)
            character, entries = rest.split("=== COMPLETE APPLICABLE EXACT-SPELLING FAMILIES ===\n")
            require(canonical(ET.fromstring(character)) == canonical(kd[char]), "Readback KD differs: " + char)
            nodes = ET.fromstring("<root>" + entries + "</root>").findall("entry")
            selected = {char, *comparisons[char]["linkedWords"]}
            expected = {identity for identity, node in jm.items()
                        if {n.text for n in node.findall("k_ele/keb")} & selected}
            require({n.findtext("ent_seq") for n in nodes} == expected and len(nodes) == len(expected),
                    "Readback family membership differs: " + char)
            for node in nodes:
                require(canonical(node) == canonical(jm[node.findtext("ent_seq")]),
                        "Readback JMdict record differs: " + char)
            counts[char] = len(nodes)
            guard.check()
        require(ARTIFACT.read_bytes() == raw, "Coordinator artifact changed")
        require(Path(inventory_ref["path"]).read_bytes() == inventory_bytes, "Inventory changed")
        for key, ref in value["evidence"].items():
            require(Path(ref["path"]).read_bytes() == evidence[key][0], "Evidence changed: " + key)
        clean()
    finally:
        memory = guard.finish()
        require(not memory["breach"], "RAM breach")
    copies = {
        key: {**write_frozen(OUT / "evidence" / (key + Path(ref["path"]).suffix), evidence[key][0]),
              "originalReadOnly": evidence[key][1], "original": ref}
        for key, ref in value["evidence"].items()
    }
    result = {
        "status": "PASS_MECHANICAL_BINDINGS_NOT_REVIEW_CLOSURE",
        "artifact": write_frozen(OUT / "obligation-map.json", raw),
        "candidate": reviewed, "obligations": len(seen),
        "statusCounts": {status: sum(1 for item in value["dispositions"] if item["status"] == status)
                         for status in ("resolved", "withdrawn", "optional")},
        "predicatesChecked": len(checked), "purpleExclusions": len(exclusions),
        "completeReadbackFamilies": counts, "evidence": copies,
        "producer": write_frozen(OUT / "producer.py", Path(__file__).read_bytes()),
        "memory": memory,
        "limits": "Signed-state predicates, evidence hashes and four complete readback equalities only. "
                  "Nonblind coordinator drafts; fresh independent claims still need dispositions. "
                  "Not replacement-review acceptance, teaching approval or publication.",
    }
    print(json.dumps(freeze_json(OUT / "verification.json", result), ensure_ascii=False))


if __name__ == "__main__":
    main()
