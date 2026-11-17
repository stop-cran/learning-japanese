"""Recheck the frozen replacement core against signed blobs and the original source packet."""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from b134_token_meter import verify_core
from common import WS, freeze_json, frozen, require, sha, start_guard
from verify_b133_reconciliation import records
from verify_b134_packet import RUNNER
from verify_b134_sources import FINGERPRINT, Git, OWNER

ROOT = WS / "scratch-134" / "review"
PREP = ROOT / "fresh-independent-002" / "projected-successor-008"
PACKET = PREP / "packet"
OLD = ROOT / "neutral-preparation-001" / "projected-successor-001" / "packet"
CANDIDATE = "355cccb840d22e7313e79f234eb93d1367e00352"
PARENT = "ba80afffc20a72d31be68b355b6f90aab36a5726"
BASE = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
PACKET_SHA = "6f774ec7906cbe8279e972959507d8ccbbea8541273f8cfa51a405dc34fcc5f6"
CORE_SHA = "b6e49cbbcb6ebab5886dc87b9cf9557a4b213fda5d3c3b0c7c6ff3f7c18c76b8"


def main(output):
    require(output.parent == ROOT and not output.exists(), "Use a new direct review output")
    guard, _ = start_guard("B134 independent exact frozen-core verification")
    try:
        sums = json.loads(frozen(PACKET / "SHA256SUMS.json", PACKET_SHA))
        require(len(sums) == 1461, "Packet inventory differs")
        for name, digest in sums.items():
            frozen(PACKET / name, digest)
            guard.check()
        actual = {p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file()}
        require(actual == set(sums) | {"SHA256SUMS.json"}, "Unlisted packet file")
        core = json.loads(frozen(PREP / "fresh-independent-core-001.json", CORE_SHA))
        sources = {row["source"]: frozen(PACKET / row["source"], sums[row["source"]])
                   for row in core["sources"]}
        chain_bytes = verify_core(core, sources, frozen)
        git = Git(WS / "b134-worktree", RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all")
                and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{PARENT}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Signed candidate changed")
        names = git("ls-tree", "-r", "--name-only", CANDIDATE, "--", "kanji").decode().splitlines()
        names = [name for name in names if name.endswith(".md")]
        require(len(names) == 1262 and {name[5:] for name in sums if name.startswith("repo/kanji/")}
                == set(names), "Candidate article pool differs from signed tree")
        for start in range(0, len(names), 100):
            batch = names[start:start + 100]
            blobs = git.objects([f"{CANDIDATE}:{name}" for name in batch])
            for name, (_, raw) in zip(batch, blobs):
                require(frozen(PACKET / "repo" / name) == raw, "Candidate article bytes differ: " + name)
            guard.check()
        bindings = {
            "baseline/manifest.json": (BASE, "manifest.json"),
            "parent/manifest.json": (PARENT, "manifest.json"),
            "repo/manifest.json": (CANDIDATE, "manifest.json"),
            "baseline/words/紫.md": (BASE, "words/紫.md"),
            "parent/words/紫.md": (PARENT, "words/紫.md"),
            "snapshot/words/紫.md": (CANDIDATE, "words/紫.md"),
            "parent/kanji/紫.md": (PARENT, "kanji/紫.md"),
            "snapshot/kanji/紫.md": (CANDIDATE, "kanji/紫.md"),
            "snapshot/strokes/紫.json": (CANDIDATE, "strokes/紫.json"),
        }
        for name, (commit, path) in bindings.items():
            require(frozen(PACKET / name) == git("show", f"{commit}:{path}"),
                    "Published, parent or candidate binding differs: " + name)
        old_sums = json.loads(frozen(OLD / "SHA256SUMS.json",
                                    "12cabfd9f51797c02f77c9513ad5ae6fe7f57aeceb6d180bf3cf24baf6c5c13e"))
        unions = {}
        for kind, original_name, supplement, union_name, tag, key, counts in (
            ("jmdict", "jmdict-families.xml", "jmdict-complete-families.xml",
             "jmdict-families.xml", "entry", "ent_seq", (399, 194, 522)),
            ("kanjidic2", "kanjidic2-records.xml", "kanjidic2-complete-characters.xml",
             "kanjidic2-complete-union.xml", "character", "literal", (59, 37, 85)),
        ):
            original_raw = frozen(OLD / "evidence" / original_name, old_sums["evidence/" + original_name])
            supplement_raw = git("show", f"{CANDIDATE}:docs/n1-sources/batch-134-reconciliation-001/{supplement}")
            original = records(original_raw, tag, key)
            added = records(supplement_raw, tag, key)
            union = records(frozen(PACKET / "evidence" / union_name), tag, key)
            require((len(original), len(added), len(union)) == counts, "Source record counts differ")
            for identity in original.keys() & added.keys():
                require(original[identity] == added[identity], "Unequal overlapping complete record")
            require(union == original | added, "A complete source field or record was lost or changed")
            unions[kind] = {"original": len(original), "supplemental": len(added), "union": len(union),
                            "originalSha256": sha(original_raw), "supplementalSignedSha256": sha(supplement_raw)}
        for packet_name, original_name in (
            ("evidence/title-index.txt", "evidence/title-index.txt"),
            ("evidence/parent-title-index-ba80.txt", "evidence/title-index.txt"),
            ("evidence/published-title-index-e17.txt", "evidence/baseline-title-index.txt"),
        ):
            require(frozen(PACKET / packet_name) == frozen(OLD / original_name, old_sums[original_name]),
                    "Full title index differs from the verified original snapshot")
        delta = json.loads(frozen(PACKET / "evidence" / "baseline-title-delta.json"))
        require(delta["baselineCommit"] == BASE, "Published title delta names the wrong baseline")
        sys.path.insert(0, str(OLD.parent / "tools"))
        from capacity004 import project, xml_bytes
        full_kd = frozen(PACKET / "evidence" / "kanjidic2-complete-union.xml")
        require(xml_bytes(project(full_kd)) == frozen(PACKET / "evidence" / "kanjidic2-review-projection.xml"),
                "KD projection is not the prescribed full-record derivation")
        require(len(ET.fromstring(full_kd)) == 85, "Full KD units are incomplete")
        result = {
            "status": "PASS_EXACT_SIGNED_ARTICLES_BASELINES_AND_COMPLETE_SOURCE_UNIONS",
            "candidate": CANDIDATE, "parent": PARENT, "publishedBaseline": BASE,
            "packetSha256": PACKET_SHA, "coreManifestSha256": CORE_SHA,
            "packetFiles": len(sums), "exactSignedCandidateArticles": len(names),
            "exactAdditionalSignedBindings": list(bindings), "completeSourceUnions": unions,
            "coreSources": len(sources), "segments": len(core["segments"]), "chainBytes": chain_bytes,
            "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "Mechanical integrity and source preservation only; no semantic review, model "
                      "capacity measurement, reviewer admission, publication or delivery credit.",
        }
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Frozen-core verification RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(output / "verification.json", result)))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "verify_b134_fresh_core.py NEW_OUTPUT_DIRECTORY")
    main(Path(sys.argv[1]).resolve())
