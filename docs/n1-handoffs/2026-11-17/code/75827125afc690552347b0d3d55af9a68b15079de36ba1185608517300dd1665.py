"""Verify a signed B119 reconciliation without treating host checks as content approval."""
import gzip
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, require, sha, start_guard
from confirm_v2 import clean
from verify_b118_revision import verify_sources
from verify_reconciliation_sources import element_value

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse

SUPPORT = {"妥": "妥当", "循": "循環"}
READINGS = {"妥": ("た", "やす", "やすい", "おだやか"), "循": ("しゅん", "したがう")}
REQUIRED = {"妥": {"了", "定", "済", "決", "寧", "応", "優"}, "循": {"則", "倣", "準", "応", "転", "復"}}
COMPONENTS = {"妥": "爪", "循": "盾"}
INTERMEDIATE = "5e1cb22194aefd348cb229a743615253ce35166b"


def verify_card(before, after, required):
    original, original_body = parse(before)
    revised, revised_body = parse(after)
    require({k: v for k, v in original.items() if k != "quiz_exclusions"}
            == {k: v for k, v in revised.items() if k != "quiz_exclusions"},
            "Preserved metadata changed")
    old, new = original["quiz_exclusions"], revised["quiz_exclusions"]
    require(isinstance(new, list) and new[:len(old)] == old
            and len(new) == len(set(new)) and required <= set(new),
            "Original guards or required direct pairs missing")
    for text in (before, after):
        require(text.count("## Notes\n") == 1 and text.count("\nMetadata:") == 1,
                "Card section boundaries changed")
    mnemonic_prefix = "**Modern-shape mnemonic, not etymology:**"
    before_notes, after_notes = (body.split("## Notes\n")[0] for body in (original_body, revised_body))
    mnemonics = [[line for line in body.splitlines() if line.startswith(mnemonic_prefix)]
                 for body in (before_notes, after_notes)]
    require(all(len(lines) == 1 for lines in mnemonics), "Qualified mnemonic boundary changed")
    old_mnemonic, new_mnemonic = (lines[0] for lines in mnemonics)
    require(COMPONENTS[original["kanji"]] in new_mnemonic, "Accepted component identification is missing")
    require(before_notes == after_notes.replace(new_mnemonic, old_mnemonic, 1),
            "Teaching outside the accepted mnemonic and comparison notes changed")
    first_note = before.split("## Notes\n", 1)[1].strip().splitlines()[0]
    require(first_note in after.splitlines(), "Source-only reading disclosure changed")
    require(before.split("\nMetadata:", 1)[1] == after.split("\nMetadata:", 1)[1],
            "Original source attribution changed")
    return set(new) - set(old)


def verify_gates(gates, manifest_bytes, config, guard):
    receipts = []
    for original in CHECKS:
        name = config.get("gateNames", {}).get(original, original)
        raw, log = frozen(gates / f"{name}.json"), frozen(gates / f"{name}.log")
        receipt = json.loads(raw)
        require(receipt["gate"] == name and receipt["exitCode"] == 0
                and receipt["logSha256"] == sha(log) and not receipt["memory"]["breach"]
                and receipt["memory"]["freeRamBeforeBytes"] > 2 * 1024 ** 3
                and receipt["memory"]["minimumObservedFreeRamBytes"] > 1024 ** 3,
                f"Failed or changed gate: {name}")
        if original == "reading-exposure":
            require(all(text.encode("utf-8") in log
                        for character, readings in READINGS.items() for text in (character, *readings)),
                    "A target or supplemental reading is missing from the audit")
        if original in ("manifest", "manifest-rebuild"):
            require(receipt["manifestSha256"] == sha(manifest_bytes), "Gate manifest mismatch")
        if original == "manifest-rebuild":
            require(receipt["manifestReproducible"], "Manifest is not reproducible")
        receipts.append({"gate": name, "receiptSha256": sha(raw), "logSha256": sha(log)})
        guard.check()
    return receipts


def verify_supplemental_sources(config, candidate, directory, receipt, guard):
    digest = "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d"
    source = WS / "control" / "inputs" / "n1-implementation-JMdict_e.gz"
    require(receipt["jmdictInputSha256"] == digest, "JMdict input pin changed")
    computed = hashlib.sha256()
    with source.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            computed.update(chunk)
            guard.check()
    require(computed.hexdigest() == digest, "Pinned JMdict bytes changed")
    raw = frozen(directory / "jmdict-records.xml", receipt["jmdictXmlSha256"])
    rows = ET.fromstring(raw).findall("entry")
    expected = {node.findtext("ent_seq"): element_value(node) for node in rows}
    require(len(expected) == len(rows) == len(receipt["jmdictEntryIds"])
            and set(expected) == set(receipt["jmdictEntryIds"]), "JMdict extraction membership differs")
    queries = set(receipt["jmdictQueries"])
    found, matches = set(), set()
    with gzip.open(source, "rb") as stream:
        for _, node in ET.iterparse(stream, events=("end",)):
            if node.tag != "entry":
                continue
            identifier = node.findtext("ent_seq")
            if queries & {item.text for path in ("k_ele/keb", "r_ele/reb") for item in node.findall(path)}:
                matches.add(identifier)
            if identifier in expected:
                require(identifier not in found and element_value(node) == expected[identifier],
                        f"Changed or incomplete JMdict entry: {identifier}")
                found.add(identifier)
            node.clear()
            guard.check()
    require(found == set(expected) and matches <= found, "JMdict family missing an applicable matching entry")
    community = receipt["community"]
    raw_members = frozen(directory / "n1-kanji-source-20261102.json",
                         "889faaefbec573e806f298766d2eee1300674c7b229bd973a35169cd2652cd73")
    members = json.loads(raw_members)
    require(isinstance(members, list) and len(members) == len(set(members)) == community["members"] == 1232
            and set(SUPPORT) <= set(members) and community["sha256"] == sha(raw_members),
            "Modern community membership differs")
    original_index = git(config, "show", f"{config['candidate']}:docs/n1-sources/source-index.json")
    require(sha(original_index) == community["sourceIndexSha256"], "Source-index binding changed")
    selected = json.loads(frozen(directory / "source-index-rows.json", community["rowsSha256"]))
    require(selected == [row for row in json.loads(original_index) if row["kanji"] in SUPPORT],
            "Selected modern source rows differ")
    return {"completeJmdictRecordsVerified": len(found), "matchedFamilyEntriesVerified": len(matches),
            "jmdictXmlSha256": sha(raw), "modernSourceSha256": sha(raw_members),
            "modernSourceMembers": len(members), "sourceRows": [row["sourceRow"] for row in selected]}


def verify(candidate, gates, output):
    config = load_batch(119)
    clean(config, candidate)
    require(config["members"] == list(SUPPORT), "Unexpected batch membership")
    require(git(config, "rev-parse", f"{candidate}^").decode().strip() == INTERMEDIATE
            and git(config, "rev-parse", f"{INTERMEDIATE}^").decode().strip() == config["candidate"]
            and git(config, "show", "-s", "--format=%G?|%ae|%ce", INTERMEDIATE).decode().strip()
            == "G|stop-cran@list.ru|stop-cran@list.ru",
            "Correction must preserve the signed two-commit reconciliation lineage")
    guard, _ = start_guard("B119 revision and source verification")
    try:
        blob = lambda commit, path: git(config, "show", f"{commit}:{path}")
        raw_manifest = blob(candidate, "manifest.json")
        manifest = json.loads(raw_manifest)
        base_manifest = json.loads(blob(config["base"], "manifest.json"))
        runtime = lambda value: {p: h for entries in value.values() if isinstance(entries, dict)
                                 for p, h in entries.items()}
        current, old = runtime(manifest), runtime(base_manifest)
        additions = {f"{kind}/{c}.{extension}" for c in SUPPORT
                     for kind, extension in (("kanji", "md"), ("strokes", "json"))}
        require(current.keys() - old.keys() == additions and old.keys() <= current.keys()
                and {p for p in old if current[p] != old[p]} == {f"words/{w}.md" for w in SUPPORT.values()},
                "Unexpected baseline runtime change")
        added_guards = {}
        for character, word in SUPPORT.items():
            path = f"kanji/{character}.md"
            added_guards[character] = verify_card(blob(config["candidate"], path).decode("utf-8"),
                                                 blob(candidate, path).decode("utf-8"), REQUIRED[character])
            require(current[path] == sha(blob(candidate, path)), "Card manifest binding differs")
            path = f"strokes/{character}.json"
            require(blob(candidate, path) == blob(config["candidate"], path), "Stroke source changed")
            before = blob(config["base"], f"words/{word}.md").decode("utf-8")
            after = blob(candidate, f"words/{word}.md").decode("utf-8")
            wrapper = f"[{character}](../kanji/{character}.md)"
            require(parse(before)[0] == parse(after)[0]
                    and after.count(wrapper) == before.count(wrapper) + 1
                    and after.replace(wrapper, character) == before.replace(wrapper, character),
                    f"Required wrapper or unrelated word text changed: {word}")
            guard.check()
        source_prefix = "docs/n1-sources/batch-119"
        sources = git(config, "ls-tree", "-r", "--name-only", INTERMEDIATE, "--",
                      source_prefix).decode("utf-8").splitlines()
        for path in sources:
            require(blob(INTERMEDIATE, path) == blob(candidate, path),
                    f"Original source or receipt rewritten: {path}")
            guard.check()
        changed = git(config, "diff", "--name-only", config["candidate"], candidate).decode("utf-8").splitlines()
        require(all(path in {"manifest.json", *(f"kanji/{c}.md" for c in SUPPORT)}
                    or any(path.startswith(f"{source_prefix}/reconciliation-{number:03d}/")
                           for number in (1, 2)) for path in changed),
                "Unexpected correction scope")
        index = json.loads(blob(candidate, "docs/n1-sources/source-index.json"))
        pending = {row["kanji"] for row in index if row["statusAtFreeze"] == "pending"}
        present = {Path(p).stem for p in current if p.startswith("kanji/")}
        prior = {Path(p).stem for p in old if p.startswith("kanji/")}
        require(len(pending) == 1228 and len(pending & prior) == 247 and len(pending & present) == 249,
                "Source accounting differs")
        receipts = verify_gates(gates, raw_manifest, config, guard)
        directory = WS / "scratch-119" / "review" / "reconciliation-002"
        source_proof = verify_sources(config, candidate, directory, guard)
        extraction = json.loads(frozen(directory / "source-extraction.json"))
        source_proof.update(verify_supplemental_sources(config, candidate, directory, extraction, guard))
        require(set(SUPPORT) | set().union(*added_guards.values()) <= set(extraction["members"]),
                "A new guard lacks complete dictionary evidence")
        for name in ("source-extraction.json", "kanjidic2-records.xml", "pair-dispositions.json",
                     "jmdict-records.xml", "n1-kanji-source-20261102.json", "source-index-rows.json"):
            require(frozen(directory / name) == blob(candidate, f"{source_prefix}/reconciliation-002/{name}"),
                    f"Committed reconciliation evidence differs: {name}")
        result = {
            "batch": 119, "candidate": candidate, "initial": config["candidate"], "prior": INTERMEDIATE,
            "base": config["base"],
            "status": "PASS", "ownerSignature": "G", "worktreeClean": True,
            "manifestSha256": sha(raw_manifest), "contentVersion": manifest["contentVersion"],
            "runtimeEntries": len(current), "gates": receipts, "sourceProof": source_proof,
            "addedGuards": {c: sorted(values) for c, values in added_guards.items()},
            "baselineRuntimePreservedExceptRequiredWrappers": True,
            "originalMetadataStrokesGuardsAndSourceReceiptsPreserved": True,
            "sourceMembersPublishedBeforeBatch": 247, "sourceMembersInCandidate": 249,
            "linguisticAcceptance": False, "publicationAccepted": False,
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Verification RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
