"""Verify B120's signed direct-pair correction and its committed-tree gates."""
import difflib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, require, sha, start_guard
from confirm_v2 import binding, clean

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse

PRIOR = "c986ae49e844c08afc294d9381c7e486f2c9315d"
CARD = "kanji/\u902e.md"
PAIR = "\u62bc"
PREFIX = "docs/n1-sources/batch-120/reconciliation-002/"
REVIEW = WS / "scratch-120" / "review"
SOURCES = {
    "jmdict-records.xml": "88f5963e3895d2ff91f404e17e53d330c0c922eb792580dcb33f09c0bac6fe92",
    "kanjidic2-records.xml": "0b3e20e97aa1eeb94c4263187e21845d4b726f3843662f7f93f6287808617b57",
    "receipt.json": "f6c3900c9abc3f9fccb620939d4954ab980cdcf31b1c273e7ea9428d4fffe592",
}
RUNNER_SHA = "cc10b400cc2c1c2b7ca26acfa120c4d4e336c071b930cbbee9b01654e1f1f68a"


def verify_pair_change(before, after):
    old, old_body = parse(before.replace("\r\n", "\n"))
    new, new_body = parse(after.replace("\r\n", "\n"))
    require({k: v for k, v in old.items() if k != "quiz_exclusions"}
            == {k: v for k, v in new.items() if k != "quiz_exclusions"},
            "Preserved metadata changed")
    require(PAIR not in old["quiz_exclusions"]
            and new["quiz_exclusions"] == [*old["quiz_exclusions"], PAIR],
            "Only the direct pushing-character guard may be appended")
    old_lines, new_lines = old_body.splitlines(), new_body.splitlines()
    changes = [(tag, a, b, c, d) for tag, a, b, c, d in difflib.SequenceMatcher(
        a=old_lines, b=new_lines, autojunk=False).get_opcodes() if tag != "equal"]
    if changes:
        require(len(changes) == 1, "More than one comparison passage changed")
        tag, a, b, c, d = changes[0]
        require(tag == "insert" and a == b and d - c == 1
                and old_lines.index("## Notes") < a
                and any(line.startswith("Metadata:") for line in old_lines[a:])
                and f"[{PAIR}]({PAIR}.md)" in new_lines[c],
                "Only one new qualified Notes comparison may be inserted")
    return {"addedGuard": PAIR, "changedBodyPassages": len(changes)}


def verify(candidate, gates, output):
    config = load_batch(120)
    clean(config, candidate)
    require(config["members"] == ["\u902e"]
            and git(config, "show", "-s", "--format=%P", candidate).decode().strip() == PRIOR,
            "Correction must be the sole direct child of the prior snapshot")
    signature = git(config, "show", "-s", "--format=%G?|%GF|%ae|%ce|%B", candidate).decode()
    require(signature.startswith(
        "G|D4C9A275A218AF747B787AFA9D94B9D311BD26A7|stop-cran@list.ru|stop-cran@list.ru|")
        and "\nCo-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in signature,
        "Owner signature or required trailer differs")
    guard, _ = start_guard("B120 correction verification")
    try:
        blob = lambda commit, path: git(config, "show", f"{commit}:{path}")
        docs, runtime_changes = [], set()
        for line in git(config, "diff", "--name-status", "--no-renames", PRIOR, candidate).decode().splitlines():
            status, path = line.split("\t")
            if path.startswith(PREFIX):
                require(status == "A", "Existing source evidence changed")
                docs.append(path)
            else:
                require(status == "M" and path in (CARD, "manifest.json"), f"Unexpected change: {line}")
                runtime_changes.add(path)
        require(runtime_changes == {CARD, "manifest.json"} and docs, "Missing correction or sources")
        card = blob(candidate, CARD)
        delta = verify_pair_change(blob(PRIOR, CARD).decode(), card.decode())
        manifest_raw = blob(candidate, "manifest.json")
        manifest, previous = json.loads(manifest_raw), json.loads(blob(PRIOR, "manifest.json"))
        runtime = lambda value: {p: h for entries in value.values() if isinstance(entries, dict)
                                 for p, h in entries.items()}
        old, current = runtime(previous), runtime(manifest)
        require(old.keys() == current.keys() and len(current) == 8702
                and {path for path in old if old[path] != current[path]} == {CARD}
                and current[CARD] == sha(card.replace(b"\r\n", b"\n")), "Unexpected manifest delta")
        receipts = []
        summary_path = gates / "summary.json"
        summary = json.loads(frozen(summary_path))
        runner_path = WS / "scratch-120" / "run-reconciliation-002-checks.py"
        frozen(runner_path, RUNNER_SHA)
        require(summary["status"] == "PASS" and summary["candidate"] == candidate
                and summary["base"] == config["base"] and summary["startingHead"] == PRIOR
                and summary["manifestReproducible"]
                and summary["manifestSha256"] == summary["committedManifestSha256"] == sha(manifest_raw)
                and set(summary["checks"]) == set(CHECKS), "Gates do not bind the committed revision")
        for name in CHECKS:
            receipt_raw, log = frozen(gates / f"{name}.json"), frozen(gates / f"{name}.log")
            receipt = json.loads(receipt_raw)
            require(receipt["gate"] == name and receipt["exitCode"] == 0
                    and receipt["logSha256"] == sha(log) and receipt["cwd"] == config["repo"]
                    and not receipt["memory"]["breach"]
                    and receipt["memory"]["freeRamBeforeBytes"] > 2 * 1024**3
                    and receipt["memory"]["minimumObservedFreeRamBytes"] > 1024**3,
                    f"Failed or changed gate: {name}")
            if name in ("manifest", "manifest-rebuild"):
                require(receipt["manifestSha256"] == sha(manifest_raw), "Gate manifest differs")
            if name == "manifest-rebuild":
                require(receipt["manifestReproducible"], "Manifest is not reproducible")
            if name == "reading-exposure":
                require(all(text.encode() in log for text in ("\u902e", "\u30c0\u30a4", "\u30c6\u30a4", "\u304a\u3088\u3076")),
                        "Required supplemental readings absent")
            receipts.append({"gate": name, "receiptSha256": sha(receipt_raw), "logSha256": sha(log)})
            guard.check()
        evidence = {}
        for path in docs:
            raw = blob(candidate, path)
            require((Path(config["repo"]) / path).read_bytes() == raw, "Signed evidence differs on disk")
            evidence[path] = sha(raw)
            guard.check()
        source_paths = {}
        for name, digest in SOURCES.items():
            raw = frozen(REVIEW / "push-sources-001" / name, digest)
            matches = [path for path, value in evidence.items() if value == digest]
            require(matches and all(blob(candidate, path) == raw for path in matches),
                    f"Complete supplemental source is absent or changed: {name}")
            source_paths[name] = matches
        bindings = json.loads(blob(candidate, PREFIX + "bindings.json"))
        require(bindings["startingHead"] == PRIOR and bindings["originalBase"] == config["base"]
                and set(bindings["packetFiles"]) == {path.removeprefix(PREFIX) for path in docs}
                - {"bindings.json"}, "Signed source inventory differs")
        for name, item in bindings["packetFiles"].items():
            raw = blob(candidate, PREFIX + name)
            require(sha(raw) == item["sha256"] and len(raw) == item["bytes"],
                    f"Signed source binding differs: {name}")
        for item in bindings["reports"].values():
            require(len(frozen(Path(item["path"]), item["sha256"])) == item["bytes"],
                    "Author response names a changed report")
        require(blob(candidate, PREFIX + "comparison-cards/\u62bc.md") == blob(PRIOR, "kanji/\u62bc.md"),
                "Comparison snapshot differs from the actual prior card")
        records = ET.fromstring(frozen(REVIEW / "push-sources-001" / "jmdict-records.xml"))
        entry = next(node for node in records.findall("entry") if node.findtext("ent_seq") == "2011120")
        search_only = [node.findtext("keb") for node in entry.findall("k_ele")
                       if node.findtext("ke_inf") == "search-only kanji form"]
        require(search_only == ["\u53d6\u308a\u62bc\u3048\u308b", "\u53d6\u62bc\u3048\u308b", "\u53d6\u6291\u3048\u308b"]
                and b"other two shortened spellings" in blob(candidate, PREFIX + "pair-dispositions.md"),
                "Inspected source-summary erratum changed")
        proof_path = REVIEW / "push-pair-evidence-001.json"
        frozen(proof_path, "2325629267609b1ec972a2f1f64c76426a1bbe7ee148018aee1192ee401c227f")
        result = {
            "status": "PASS", "batch": 120, "candidate": candidate, "prior": PRIOR,
            "base": config["base"], "manifestSha256": sha(manifest_raw),
            "contentVersion": manifest["contentVersion"], "runtimeEntries": len(current),
            "boundedDelta": delta, "newEvidenceSha256": evidence, "completeSourceCopies": source_paths,
            "sourcePairProof": binding(proof_path), "gates": receipts, "summary": binding(summary_path),
            "gateRunner": binding(runner_path), "signature": signature, "tool": binding(Path(__file__)),
            "sourceSummaryErratum": {
                "path": PREFIX + "pair-dispositions.md",
                "incorrectText": "other two shortened spellings",
                "correction": "There are three search-only shortened spellings in JMdict 2011120.",
                "spellings": search_only,
                "effect": "The complete XML is correct and unchanged; the count error affects only "
                          "the author's source summary, not the direct arrest sense or runtime card.",
                "publicationRequirement": "Persist this explicit erratum alongside the original source summary.",
            },
            "scope": "Owner-signed direct child, one appended guard and optional inserted Note, "
                     "unchanged metadata and baseline, complete supplemental-source copies, "
                     "and ten committed-tree gates. Not reviewer or publication acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
