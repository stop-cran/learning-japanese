"""Verify the signed B118 correction, preserved runtime and hash-bound author gates."""
import gzip
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, require, sha, start_guard
from confirm_v2 import clean
from verify_reconciliation_sources import element_value

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse


def verify_gates(gates, manifest_bytes, config, guard):
    receipts = []
    for original in CHECKS:
        name = config.get("gateNames", {}).get(original, original)
        raw, log = frozen(gates / f"{name}.json"), frozen(gates / f"{name}.log")
        receipt = json.loads(raw)
        require(receipt["gate"] == name and receipt["exitCode"] == 0
                and receipt["logSha256"] == sha(log)
                and not receipt["memory"]["breach"]
                and receipt["memory"]["freeRamBeforeBytes"] > 2 * 1024 ** 3
                and receipt["memory"]["minimumObservedFreeRamBytes"] > 1024 ** 3,
                f"Failed or changed gate: {name}")
        if original == "reading-exposure":
            require("析".encode("utf-8") in log
                    and all(reading.encode("utf-8") in log for reading in ("しゃく", "さく", "へぎ")),
                    "Supplemental source-only readings absent from the audit")
        if name in ("manifest", "manifest-rebuild"):
            require(receipt["manifestSha256"] == sha(manifest_bytes), "Gate manifest mismatch")
        if name == "manifest-rebuild":
            require(receipt["manifestReproducible"], "Manifest is not reproducible")
        receipts.append({"gate": name, "receiptSha256": sha(raw), "logSha256": sha(log)})
        guard.check()
    return receipts


def verify_sources(config, candidate, directory, guard):
    receipt_raw = frozen(directory / "source-extraction.json")
    receipt = json.loads(receipt_raw)
    raw = frozen(directory / "kanjidic2-records.xml", receipt["xmlSha256"])
    require(receipt["base"] == config["candidate"], "Correction sources use another base")
    digest = "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed"
    require(receipt["kanjidicInputSha256"] == digest, "Correction changed the pinned dictionary")
    source = WS / "control" / "inputs" / "n1-planning-kanjidic2.xml.gz"
    computed = hashlib.sha256()
    with source.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            computed.update(chunk)
            guard.check()
    require(computed.hexdigest() == digest, "Pinned dictionary bytes changed")
    rows = ET.fromstring(raw).findall("character")
    expected = {node.findtext("literal"): element_value(node) for node in rows}
    require(len(expected) == len(rows) == len(receipt["members"])
            and set(expected) == set(receipt["members"]), "Extracted record membership differs")
    found = set()
    with gzip.open(source, "rb") as stream:
        for _, node in ET.iterparse(stream, events=("end",)):
            if node.tag == "character":
                character = node.findtext("literal")
                if character in expected:
                    require(character not in found and element_value(node) == expected[character],
                            f"Changed or incomplete dictionary record: {character}")
                    found.add(character)
                node.clear()
                guard.check()
    require(found == set(expected), "Missing dictionary records")
    require(set(receipt["comparisonCardSha256"]) == set(expected) - set(config["members"]),
            "Comparison source inventory is incomplete")
    for character, digest in receipt["comparisonCardSha256"].items():
        raw_card = frozen(directory / "comparison-cards" / f"{character}.md", digest)
        for revision in (config["candidate"], candidate):
            require(raw_card == git(config, "show", f"{revision}:kanji/{character}.md"),
                    f"Comparison source changed: {character}")
        guard.check()
    return {"receiptSha256": sha(receipt_raw), "xmlSha256": receipt["xmlSha256"],
            "completeRecordsVerified": len(found),
            "comparisonCardsVerified": len(receipt["comparisonCardSha256"])}


def verify(candidate, gates, output):
    config = load_batch(118)
    clean(config, candidate)
    require(git(config, "rev-parse", f"{candidate}^").decode().strip() == config["candidate"],
            "Correction must directly descend from the frozen initial")
    guard, _ = start_guard("B118 revision and source verification")
    try:
        blob = lambda commit, path: git(config, "show", f"{commit}:{path}")
        raw_manifest = blob(candidate, "manifest.json")
        manifest, base_manifest = json.loads(raw_manifest), json.loads(blob(config["base"], "manifest.json"))
        runtime = lambda value: {p: h for entries in value.values() if isinstance(entries, dict)
                                 for p, h in entries.items()}
        current, old = runtime(manifest), runtime(base_manifest)
        require(current.keys() - old.keys() == {"kanji/析.md", "strokes/析.json"}
                and old.keys() <= current.keys()
                and {path for path in old if current[path] != old[path]} == {"words/分析.md"},
                "Unexpected baseline runtime change")
        original, _ = parse(blob(config["candidate"], "kanji/析.md").decode("utf-8"))
        revised, _ = parse(blob(candidate, "kanji/析.md").decode("utf-8"))
        require({k: v for k, v in original.items() if k != "quiz_exclusions"}
                == {k: v for k, v in revised.items() if k != "quiz_exclusions"}
                and revised["quiz_exclusions"] == [*original["quiz_exclusions"], "別", "離", "刻", "盤"],
                "Correction changed preserved metadata or omitted a direct exclusion")
        require(blob(candidate, "strokes/析.json") == blob(config["candidate"], "strokes/析.json"),
                "Stroke source changed")
        before = blob(config["base"], "words/分析.md").decode("utf-8")
        after = blob(candidate, "words/分析.md").decode("utf-8")
        wrapper = "[析](../kanji/析.md)"
        require(parse(before)[0] == parse(after)[0]
                and after.count(wrapper) == before.count(wrapper) + 1
                and after.replace(wrapper, "析") == before.replace(wrapper, "析"),
                "Required word wrapper differs or unrelated word text changed")
        sources = git(config, "ls-tree", "-r", "--name-only", config["candidate"], "--",
                      "docs/n1-sources/batch-118").decode("utf-8").splitlines()
        for path in sources:
            require(blob(config["candidate"], path) == blob(candidate, path),
                    f"Original source or receipt rewritten: {path}")
        changed = git(config, "diff", "--name-only", config["candidate"], candidate).decode("utf-8").splitlines()
        require(all(path in ("kanji/析.md", "manifest.json")
                    or path.startswith("docs/n1-sources/batch-118/reconciliation-001/") for path in changed),
                "Unexpected correction scope")
        index = json.loads(blob(candidate, "docs/n1-sources/source-index.json"))
        pending = {row["kanji"] for row in index if row["statusAtFreeze"] == "pending"}
        present = {Path(path).stem for path in current if path.startswith("kanji/")}
        prior = {Path(path).stem for path in old if path.startswith("kanji/")}
        require(len(pending) == 1228 and len(pending & prior) == 246 and len(pending & present) == 247,
                "Source accounting differs")
        receipts = verify_gates(gates, raw_manifest, config, guard)
        source_proof = verify_sources(config, candidate,
                                     WS / "scratch-118" / "review" / "reconciliation-001", guard)
        result = {"batch": 118, "candidate": candidate, "initial": config["candidate"], "base": config["base"],
                  "status": "PASS", "ownerSignature": "G", "worktreeClean": True,
                  "manifestSha256": sha(raw_manifest), "contentVersion": manifest["contentVersion"],
                  "runtimeEntries": len(current), "gates": receipts, "sourceProof": source_proof,
                  "baselineRuntimePreservedExceptRequiredWrappers": True,
                  "originalMetadataStrokesGuardsAndSourceReceiptsPreserved": True,
                  "sourceMembersPublishedBeforeBatch": 246, "sourceMembersInCandidate": 247,
                  "publicationAccepted": False}
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Verification RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
