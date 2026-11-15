"""Fail closed on the attested 維/ゆい wrong option in four bounded shipped pools."""
import argparse
import hashlib
import importlib.util
import json
import os
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT / "b117-worktree"
PARENT = "5100ec3e8580ba03e6e6dcaa378cb92492f1d13f"
SOURCES = REPO / "docs" / "n1-sources" / "batch-117" / "reconciliation-004"
os.environ["N1_REPO"] = str(REPO)
sys.path.insert(0, str(ROOT / "lean"))
import n1lib
import reading_exposure as exposure
import reading_options as options


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inspect(target, pool):
    excluded = options.excluded_keys(target)
    require("ゆい" not in excluded, "The test must not hide ゆい by injecting an exclusion.")
    reach = exposure.reach(target, "on", "い", pool, excluded)
    by_kanji = {card.kanji: card for card in pool}
    require(len(by_kanji) == len(pool), "Duplicate pool members.")
    witness = None
    seen = set()
    invalid = []
    for seed in range(1000):
        wrong = options.question(target, "on", pool, by_kanji, random.Random(seed), "い", excluded)
        if "ゆい" in wrong and witness is None:
            witness = {"seed": seed, "wrongOptions": wrong}
        seen.update(wrong)
        if len(wrong) != 3 or len(set(wrong)) != 3 or not set(wrong) <= reach["reachable"]:
            invalid.append(seed)
    return {
        "cards": len(pool),
        "membershipSha256": hashlib.sha256(
            "\n".join(sorted(by_kanji)).encode("utf-8")).hexdigest(),
        "curatedCards": reach["curated_cards"], "outcomes": reach["outcomes"],
        "deficits": reach["deficits"], "reachable": sorted(reach["reachable"]),
        "fallback": {key: sorted(value) for key, value in reach["fallback"].items()},
        "yuiReachable": "ゆい" in reach["reachable"],
        "seedRange": [0, 999], "seedsChecked": 1000, "seededWitness": witness,
        "sampledWrongOptions": sorted(seen), "invalidSampleSeeds": invalid,
    }


def main(output):
    index = json.loads((SOURCES / "source-evidence-index.json").read_bytes())
    model_hashes = {}
    for module in (n1lib, exposure, options):
        name = Path(module.__file__).name
        row = index["models"][name]
        require(sha(module.__file__) == row["sha256"] == sha(REPO / row["snapshot"]),
                f"Frozen model mismatch: {name}")
        model_hashes[name] = row["sha256"]
    source = index["characterSources"][0]
    require(source["source"] == "維", "Missing target source.")
    require(sha(source["extract"]["path"]) == source["extract"]["sha256"], "Source changed.")
    require("ユイ（呉）" in Path(source["extract"]["path"]).read_text(encoding="utf-8"),
            "The independently attested on-reading must be present.")
    cards, metadata = [], {}
    for path in sorted((REPO / "kanji").glob("*.md")):
        fm, _ = n1lib.parse(path.read_text(encoding="utf-8"))
        require(fm is not None, f"Unparsed card: {path}")
        metadata[path.stem] = fm
        cards.append(exposure.PCard(path.stem, fm))
    by_kanji = {card.kanji: card for card in cards}
    target = by_kanji["維"]
    require(target.on == ["イ"] and target.kun == []
            and target.quiz_readings("on") == ["イ"] and target.quiz_readings("kun") == [],
            "The repair must preserve full metadata and イ-only practice.")
    require("ゆい" in {key for _, key in by_kanji["由"].usable("on")},
            "The attested reading holder must still offer ゆい.")
    starter = [card for card in cards if "starter" in card.tags]
    require(by_kanji["由"] not in starter and target not in starter,
            "The pinned borrowed-target/holder scenario changed.")
    old_text = subprocess.check_output(
        ["git", "show", f"{PARENT}:kanji/維.md"], cwd=REPO).decode("utf-8").replace("\r\n", "\n")
    old_fm, _ = n1lib.parse(old_text)
    old_target = exposure.PCard("維", old_fm)
    require(old_target.distractors == ["録", "催", "集"], "Unexpected parent choices.")
    before = inspect(old_target, exposure.starter_pool(starter, old_target) + [by_kanji["由"]])
    require(before["curatedCards"] == [] and before["deficits"] == {3: 1}
            and before["yuiReachable"] and before["seededWitness"]
            and before["seededWitness"]["seed"] == 1, "The positive parent regression no longer reproduces.")
    pools = exposure.pools_of(cards) + [
        ("Starter+target", exposure.starter_pool(starter, target)),
        ("Starter+target+由", exposure.starter_pool(starter, target) + [by_kanji["由"]]),
    ]
    results = {name: inspect(target, pool) for name, pool in pools}
    expected = {"ぎん", "ご", "きゅう"}
    problems = []
    for name, result in results.items():
        if not (
            target.distractors == ["銀", "語", "休"]
            and result["curatedCards"] == ["銀", "語", "休"]
            and result["deficits"] == {0: 1} and result["outcomes"] == 1
            and set(result["reachable"]) == expected and not result["fallback"]
            and not result["yuiReachable"] and result["seededWitness"] is None
            and set(result["sampledWrongOptions"]) == expected and not result["invalidSampleSeeds"]
        ):
            problems.append(name)
    return {
        "status": "FAIL" if problems else "PASS", "failedPools": problems,
        "parent": PARENT, "models": model_hashes,
        "sourceExtractSha256": source["extract"]["sha256"], "starterCards": len(starter),
        "currentTargetMetadata": metadata["維"], "parentPositiveControl": before, "pools": results,
        "limits": "Unchanged Python model, exactly these four pools and the イ prompt. "
                  "No exclusion of ゆい was injected. Not arbitrary/multiple-borrow pools, "
                  "other readings, Kotlin/JVM/native/device or publication acceptance.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "Preserve existing check output.")
    guard_path = ROOT / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py"
    require(sha(guard_path) == "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84",
            "RAM guard changed.")
    spec = importlib.util.spec_from_file_location("b117_r4_yui_ram", guard_path)
    support = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(support)
    require(support.available_ram() > 2 * 1024**3, "Admission requires more than 2 GiB available RAM.")
    guard = support.RamGuard()
    guard.start()
    started = datetime.now(timezone.utc).isoformat()
    try:
        result = main(args.output)
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "The 1 GiB continuous RAM floor was breached.")
    result.update(startedAt=started, completedAt=datetime.now(timezone.utc).isoformat(), memory=memory)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "failedPools": result["failedPools"],
                      "parentWitness": result["parentPositiveControl"]["seededWitness"],
                      "output": str(args.output)}, ensure_ascii=False))
    sys.exit(0 if result["status"] == "PASS" else 1)
