"""Check B117's signed revision, source preservation and ten bound gate receipts."""
import json
import sys
from pathlib import Path

from common import CHECKS, WS, freeze_json, git, load_batch, require, sha, start_guard
from confirm_v2 import clean

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse


def verify_gates(gates, manifest_bytes, guard):
    receipts = []
    for original_name in CHECKS:
        name = ("reading-exposure-supplemental"
                if original_name == "reading-exposure" else original_name)
        raw = (gates / f"{name}.json").read_bytes()
        record = json.loads(raw)
        log = (gates / f"{name}.log").read_bytes()
        require(record["gate"] == name and record["exitCode"] == 0
                and record["logSha256"] == sha(log)
                and not record["memory"]["breach"]
                and record["memory"]["minimumObservedFreeRamBytes"] > 1024 ** 3,
                f"Gate receipt failed: {name}")
        if original_name == "reading-exposure":
            require("Supplemental source-attested reading: 維=ゆい;".encode("utf-8") in log,
                    "Supplemental reading was not included in the revised audit")
        if name in ("manifest", "manifest-rebuild"):
            require(record["manifestSha256"] == sha(manifest_bytes), "Gate manifest mismatch")
        if name == "manifest-rebuild":
            require(record["manifestReproducible"], "Manifest is not reproducible")
        receipts.append({"gate": name, "receiptSha256": sha(raw), "logSha256": sha(log)})
        guard.check()
    return receipts


def verify(candidate, gates, output):
    config = load_batch(117)
    clean(config, candidate)
    require(candidate != config["candidate"], "The initial candidate has not been repaired")
    guard, _ = start_guard("B117 revision verification")
    try:
        blob = lambda commit, path: git(config, "show", f"{commit}:{path}")
        members = config["members"]
        declared = json.loads((WS / "scratch-117" / "selection.json").read_bytes())["declared"]
        manifest_bytes = blob(candidate, "manifest.json")
        manifest = json.loads(manifest_bytes)
        base_manifest = json.loads(blob(config["base"], "manifest.json"))
        runtime = lambda value: {p: h for entries in value.values() if isinstance(entries, dict)
                                 for p, h in entries.items()}
        current, old = runtime(manifest), runtime(base_manifest)
        additions = {f"{folder}/{c}.{ext}" for c in members
                     for folder, ext in (("kanji", "md"), ("strokes", "json"))}
        words = {f"words/{w}.md" for values in declared.values() for w in values}
        require(current.keys() - old.keys() == additions and old.keys() <= current.keys(),
                "Unexpected runtime additions/removals")
        require({p for p in old if current[p] != old[p]} == words,
                "Unrelated baseline runtime change")
        for c in members:
            path = f"kanji/{c}.md"
            original, _ = parse(blob(config["candidate"], path).decode("utf-8"))
            revised, _ = parse(blob(candidate, path).decode("utf-8"))
            mutable = {"quiz_exclusions"} | ({"distractors"} if c == "\u7dad" else set())
            require({k: v for k, v in original.items() if k not in mutable}
                    == {k: v for k, v in revised.items() if k not in mutable},
                    f"Preserved frontmatter changed: {c}")
            require(revised["quiz_exclusions"][:len(original["quiz_exclusions"])]
                    == original["quiz_exclusions"], f"Original guards changed: {c}")
            require(blob(candidate, f"strokes/{c}.json")
                    == blob(config["candidate"], f"strokes/{c}.json"), f"Stroke source changed: {c}")
        for path in words:
            before = blob(config["base"], path).decode("utf-8")
            after = blob(candidate, path).decode("utf-8")
            require(parse(before)[0] == parse(after)[0], f"Word metadata changed: {path}")
            for c, mapped in declared.items():
                if Path(path).stem in mapped:
                    wrapper = f"[{c}](../kanji/{c}.md)"
                    require(after.count(wrapper) == before.count(wrapper) + 1,
                            f"Required wrapper count changed: {path}/{c}")
                    after = after.replace(wrapper, c)
                    before = before.replace(wrapper, c)
            require(after == before, f"Non-link word text changed: {path}")
        sources = git(config, "ls-tree", "-r", "--name-only", config["candidate"], "--",
                      "docs/n1-sources/batch-117").decode("utf-8").splitlines()
        for path in sources:
            require(blob(config["candidate"], path) == blob(candidate, path),
                    f"Historical author source/receipt rewritten: {path}")
        index = json.loads(blob(candidate, "docs/n1-sources/source-index.json"))
        pending = {row["kanji"] for row in index if row["statusAtFreeze"] == "pending"}
        present = {Path(p).stem for p in current if p.startswith("kanji/")}
        prior = {Path(p).stem for p in old if p.startswith("kanji/")}
        require(len(pending) == 1228 and len(pending & prior) == 242
                and len(pending & present) == 246, "Source membership accounting mismatch")
        receipts = verify_gates(gates, manifest_bytes, guard)
        result = {"batch": 117, "candidate": candidate, "initial": config["candidate"],
                  "base": config["base"], "status": "PASS", "ownerSignature": "G",
                  "worktreeClean": True, "manifestSha256": sha(manifest_bytes),
                  "contentVersion": manifest["contentVersion"], "runtimeEntries": len(current),
                  "baselineRuntimePreservedExceptRequiredWrappers": True,
                  "originalMetadataStrokesGuardsAndSourceReceiptsPreserved": True,
                  "sourceMembersPublishedBeforeBatch": 242, "sourceMembersInCandidate": 246,
                  "publicationAccepted": False, "gates": receipts,
                  "limits": "Structural/byte evidence only; independent confirmations still required."}
        print(json.dumps(freeze_json(output, result)))
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Revision verification RAM guard breached")


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
