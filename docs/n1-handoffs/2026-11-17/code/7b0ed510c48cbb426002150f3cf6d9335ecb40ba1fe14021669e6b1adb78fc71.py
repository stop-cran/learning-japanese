"""Bind the original 29 coordinator dispositions to the signed B134 revision."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from b134_initial_records import INITIALS, actual_initial, disposition_ids
from common import WS, freeze_json, frozen, readonly, require, sha, start_guard, write_frozen
from run_b134_closure_checks import REPO, lineage
from verify_b133_reconciliation import front_matter, listing
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

SOURCE = Path(__file__).with_name("b134-coordinator-obligation-map-001.json")
SOURCE_SHA = "e317783a7c579ca13ff7d3cbe9f8a4940b6dc7cce3ae0eed791c8625dcb92b13"
OUT = WS / "scratch-134" / "review" / "coordinator-disposition-bindings-001"
PURPLE = "\u7d2b"
READBACKS = {
    "threadReadback": "\u7cf8", "fiberReadback": "\u7dad",
    "hallReadback": "\u9928", "wrapReadback": "\u5305",
}


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def check_predicate(item, text, fields, comparison):
    kind = item["kind"]
    exclusions = listing(fields.get("quiz_exclusions"))
    if kind == "exclusionPresent":
        ok = item["char"] in exclusions
    elif kind == "exclusionAbsent":
        ok = item["char"] not in exclusions
    elif kind == "pairUndeclared":
        other = front_matter(comparison(item["char"]))
        ok = item["char"] not in exclusions and PURPLE not in listing(other.get("quiz_exclusions"))
    elif kind == "tagPresent":
        ok = item["tag"] in listing(fields.get("tags"))
    elif kind == "cardContains":
        ok = item["text"] in text
    elif kind == "cardLacks":
        ok = item["text"] not in text
    else:
        raise ValueError("Unknown card predicate: " + kind)
    require(ok, "Signed card predicate failed: " + repr(item))


def check_readback(char, raw, original, index, jm, kd):
    text = raw.decode("utf-8").replace("\r\n", "\n")
    article, rest = text.split("=== COMPLETE KANJIDIC2 CHARACTER ===\n")
    require(article.startswith("=== " + char + ": COMPLETE ARTICLE ===\n"), "Wrong readback header")
    require(article.split("\n", 1)[1].strip()
            == original.decode("utf-8").replace("\r\n", "\n").strip()
            and sha(original) == index[char]["sha256"], "Readback article differs")
    character, entries = rest.split("=== COMPLETE APPLICABLE EXACT-SPELLING FAMILIES ===\n")
    require(canonical(ET.fromstring(character)) == canonical(kd[char]), "KD record differs")
    nodes = ET.fromstring("<root>" + entries + "</root>").findall("entry")
    selected = {char, *index[char]["linkedWords"]}
    expected = {identity for identity, node in jm.items()
                if {n.text for n in node.findall("k_ele/keb")} & selected}
    require(len(nodes) == len(expected) and {n.findtext("ent_seq") for n in nodes} == expected,
            "Readback family membership differs")
    for node in nodes:
        require(canonical(node) == canonical(jm[node.findtext("ent_seq")]), "JMdict record differs")
    return sorted(expected)


def main():
    require(not OUT.exists(), "Preserve existing disposition bindings")
    raw = SOURCE.read_bytes()
    require(sha(raw) == SOURCE_SHA, "Original coordinator map changed")
    value = json.loads(raw)
    guard, _ = start_guard("B134 original disposition bindings")
    try:
        git = Git(REPO, RUNNER, guard)
        reviewed = value["reviewedSnapshot"]

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == reviewed
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Reviewed candidate changed")

        def blob(name):
            return git("show", reviewed + ":" + name)

        clean()
        require(lineage(git, reviewed) > 0, "Missing owner-signed reconciliation")
        required, original_refs = set(), {}
        for family in INITIALS:
            spec, refs, _, claims = actual_initial(family)
            report = frozen(refs["report"]["path"], refs["report"]["sha256"])
            required.update((spec["run"], claim) for claim in disposition_ids(report, claims))
            original_refs[family] = {key: refs[key] for key in ("report", "adjudication")}
        actual = [(row["run"], row["id"]) for row in value["dispositions"]]
        require(len(actual) == len(set(actual)) == len(required) == 29 and set(actual) == required,
                "Original obligations were lost, duplicated or added")
        evidence = {}
        for key, ref in value["evidence"].items():
            path = Path(ref["path"]).resolve()
            require(path.is_relative_to(WS), "Evidence escaped the N1 workspace")
            data = path.read_bytes()
            require(sha(data) == ref["sha256"], "Evidence changed: " + key)
            evidence[key] = (data, readonly(path))
            guard.check()
        text_raw = blob("kanji/" + PURPLE + ".md")
        text = text_raw.decode("utf-8").replace("\r\n", "\n")
        fields = front_matter(text)

        def comparison(char):
            return blob("kanji/" + char + ".md").decode("utf-8").replace("\r\n", "\n")

        checks = []
        for row in value["dispositions"]:
            require(row["status"] in ("resolved", "withdrawn", "optional")
                    and row["reason"].strip() and row["evidenceKeys"]
                    and set(row["evidenceKeys"]) <= set(evidence), "Incomplete disposition")
            for predicate in row["predicates"]:
                check_predicate(predicate, text, fields, comparison)
            checks.append({"run": row["run"], "id": row["id"],
                           "cardPredicates": len(row["predicates"])})
        prefix = "docs/n1-sources/batch-134-reconciliation-001/"
        source_proof = json.loads(evidence["sourceProof"][0])
        signed = {}
        for name in ("comparison-index.json", "jmdict-complete-families.xml",
                     "kanjidic2-complete-characters.xml"):
            signed[name] = blob(prefix + name)
            require(sha(signed[name]) == source_proof["signedFiles"][prefix + name],
                    "Signed source differs from the independent full-source proof")
        require(sha(text_raw) == source_proof["signedFiles"]["kanji/" + PURPLE + ".md"],
                "Card differs from the source proof")
        index = json.loads(signed["comparison-index.json"])
        jm = {n.findtext("ent_seq"): n for n in ET.fromstring(
            signed["jmdict-complete-families.xml"]).findall("entry")}
        kd = {n.findtext("literal"): n for n in ET.fromstring(
            signed["kanjidic2-complete-characters.xml"]).findall("character")}
        families = {char: check_readback(char, evidence[key][0], blob("kanji/" + char + ".md"),
                                        index, jm, kd) for key, char in READBACKS.items()}
        require(SOURCE.read_bytes() == raw, "Disposition map changed during verification")
        for key, ref in value["evidence"].items():
            require(Path(ref["path"]).read_bytes() == evidence[key][0], "Evidence changed: " + key)
        clean()
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Disposition verification RAM breach")
    captures = {
        key: {**write_frozen(OUT / "local-evidence" / (key + ".txt"), data),
              "original": value["evidence"][key], "originalReadOnly": was_readonly}
        for key, (data, was_readonly) in evidence.items()
    }
    result = {
        "status": "PASS_BINDINGS_NOT_FINAL_CLOSURE", "candidate": reviewed,
        "dispositions": write_frozen(OUT / "coordinator-dispositions.json", raw),
        "originalReviews": original_refs, "completeReadbackFamilies": families,
        "cardSha256": sha(text_raw), "checks": checks, "captures": captures, "memory": memory,
        "producer": write_frozen(OUT / "producer.py", Path(__file__).read_bytes()),
        "limits": [
            "Nonblind coordinator decisions; never supply these dispositions to fresh reviewers.",
            "Predicates and record equality prove bindings, not linguistic correctness.",
            "Full copied sources and readbacks remain local; final archive requires retention scans.",
            "Fresh claims, final review closure and publication are still required.",
        ],
    }
    print(json.dumps(freeze_json(OUT / "verification.json", result)))


if __name__ == "__main__":
    main()
