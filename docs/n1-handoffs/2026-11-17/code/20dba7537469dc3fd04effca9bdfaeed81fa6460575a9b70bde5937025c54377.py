"""Verify the signed B134 reconciliation against complete pinned source streams.

The output is a mechanical provenance proof, not a linguistic adjudication.
Usage: verify_b134_reconciliation.py FULL_COMMIT NEW_OUTPUT_DIRECTORY
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from run_b134_closure_checks import CANDIDATE, HERE, REPO, lineage
from run_b134_reconciliation_checks import parse_changes, validate_scope
from verify_b134_payload import RUNNER, runtime_entries
from verify_b134_sources import Git, ORIGIN

TOOLS = Path(__file__).resolve().parent
DEPENDENCIES = {
    "verify_b133_reconciliation.py": "03852aa7499ca8e4d574e730df1f63b9fe4e9ada7f28645d0ff725a1131972f9",
    "verify_reconciliation_sources.py": "761688d05d89807478c002e3022749cc6b1cbd9ab4cb18b0805b4c19761ce7e6",
}
for name, digest in DEPENDENCIES.items():
    frozen(TOOLS / name, digest)

from verify_b133_reconciliation import front_matter, records, stream

PREFIX = "docs/n1-sources/batch-134-reconciliation-001/"
CHARS = set("絹衣服書誌紀詞層列段階冠根殿隻紅紺青町薬典料糸維綿妻花油被系濃薄稲久館包")
EXTRA = {"紫", "紫衣", "紫闥", "紫宸殿", "紫禁", "紫紺", "青紫", "紅紫",
         "赤紫", "紫根", "検校", "江戸", "源氏物語", "紫式部", "紅絹", "絹布",
         "布帛", "紫草", "醤油", "鰯"}
READINGS = {"きぬ", "ふみ", "もみ", "め", "わた", "せき"}
TARGET = "kanji/紫.md"
FILES = {
    "comparison-index.json", "dispositions.md", "jmdict-complete-families.xml",
    "kanjidic2-complete-characters.xml", "memory.json", "query-membership.json",
    "receipt.json", "reconcile_sources_001.py", "verification-memory.json",
    "verification.json", "verify_reconcile_sources_001.py",
}


def verify_membership(actual, recorded, counts, queries):
    require(len(queries) == len(set(queries)) and set(counts) == set(queries),
            "Missing, duplicate or unaccounted predicate, including zero matches")
    require(all(v and len(v) == len(set(v)) for v in recorded.values()),
            "Empty or duplicate membership predicates")
    require({k: sorted(v) for k, v in actual.items()} == {k: sorted(v) for k, v in recorded.items()},
            "Per-record query membership differs")
    computed = {q: sum(q in values for values in actual.values()) for q in queries}
    require(computed == counts and all(type(n) is int for n in counts.values()),
            "Exact predicate counts differ")
    return computed


def compare_records(selected, found):
    require(selected.keys() == found.keys(), "Source selection membership differs")
    for identity, value in selected.items():
        require(value == found[identity], f"Altered or incomplete source record: {identity}")


def main(candidate, output):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate) and candidate != CANDIDATE,
            "Use the full signed reconciliation identity")
    require(output.parent == HERE / "review" and not output.exists(), "Use a new B134 review output")
    guard, _ = start_guard("B134 independent reconciliation verification")
    evidence = {}
    try:
        git = Git(REPO, RUNNER, guard)

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == candidate
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Signed reconciliation checkout changed")

        def blob(name, commit=candidate):
            return git("show", f"{commit}:{name}")

        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        depth = lineage(git, candidate)
        require(depth > 0, "No owner-signed reconciliation descendant")
        names = validate_scope(parse_changes(git(
            "diff", "--no-renames", "--name-status", "-z", CANDIDATE, candidate, "--")))
        require(set(names) == {TARGET, "manifest.json"} | {PREFIX + name for name in FILES},
                "Unexpected reconciliation inventory")
        signed = {name: blob(name) for name in names}
        require(all((REPO / name).read_bytes() == raw for name, raw in signed.items()),
                "Working bytes differ from signed blobs")
        receipt = json.loads(signed[PREFIX + "receipt.json"])
        require(receipt["candidate"] == CANDIDATE, "Source extraction identifies another candidate")
        index_raw = signed[PREFIX + "comparison-index.json"]
        index = json.loads(index_raw)
        require(sha(index_raw) == receipt["comparisonIndexSha256"] and set(index) == CHARS
                and receipt["comparisonCharacters"] == sorted(CHARS), "Comparison inventory differs")
        exact = set(CHARS) | EXTRA
        comparison_proofs = {}
        for char, row in index.items():
            name = f"kanji/{char}.md"
            raw = blob(name, CANDIDATE)
            require(blob(name) == raw == (REPO / name).read_bytes()
                    and sha(raw) == row["sha256"], f"Comparison bytes differ: {char}")
            text = raw.decode("utf-8").replace("\r\n", "\n")
            fields = front_matter(text)
            words = sorted(set(re.findall(r"\]\(\.\./words/([^/)]+)\.md\)", text)))
            require(fields["title"] == row["title"] and words == row["linkedWords"]
                    and fields.get("quiz_exclusions") == row["existingExclusions"],
                    f"Comparison metadata differs: {char}")
            exact.update(words)
            evidence["comparisons/" + name] = raw
            comparison_proofs[char] = sha(raw)
        require(receipt["exactSpellings"] == sorted(exact)
                and receipt["exactReadings"] == sorted(READINGS), "Declared selector contract differs")
        queries = [f"exact-spelling:{s}" for s in sorted(exact)]
        queries += [f"exact-reading:{r}" for r in sorted(READINGS)]

        def jm_match(node, identity):
            spellings = {n.text for n in node.findall("k_ele/keb")} & exact
            readings = {n.text for n in node.findall("r_ele/reb")} & READINGS
            return [f"exact-spelling:{s}" for s in sorted(spellings)] + [
                f"exact-reading:{r}" for r in sorted(readings)]

        chars = CHARS | {"紫"}
        snapshot_raw = blob("docs/n1-source-snapshot.json")
        require(snapshot_raw == blob("docs/n1-source-snapshot.json", CANDIDATE), "Pinned inputs changed")
        snapshot = json.loads(snapshot_raw)
        source_results, selected, canonical = {}, {}, {}
        for kind, filename, tag, key in (
                ("jmdict", "jmdict-complete-families.xml", "entry", "ent_seq"),
                ("kanjidic2", "kanjidic2-complete-characters.xml", "character", "literal")):
            input_name, compressed, decompressed, declared_tag = receipt["inputs"][kind]
            require(declared_tag == tag and snapshot["inputs"][input_name]["sha256"] == compressed
                    and snapshot[kind]["xmlSha256"] == decompressed, "Dictionary input is not pinned")
            raw = signed[PREFIX + filename]
            info = receipt["outputs"][filename]
            require(sha(raw) == info["sha256"] and len(raw) == info["bytes"], "Source bytes differ")
            selected[kind] = records(raw, tag, key)
            canonical[kind] = {node.findtext(key): sha(ET.canonicalize(
                ET.tostring(node, encoding="unicode"), strip_text=True).encode("utf-8"))
                for node in ET.fromstring(raw).findall(tag)}
            require(canonical[kind] == info["canonicalRecordHashes"], "Canonical record hashes differ")
            match = jm_match if kind == "jmdict" else lambda node, identity: [identity] if identity in chars else []
            found = stream(WS / "control" / "inputs" / input_name, compressed, decompressed,
                           tag, key, match, guard)
            compare_records(selected[kind], {identity: value for identity, (_, value) in found.items()})
            if kind == "jmdict":
                membership_raw = signed[PREFIX + "query-membership.json"]
                require(sha(membership_raw) == receipt["membershipSha256"], "Membership hash differs")
                counts = verify_membership(
                    {identity: qs for identity, (qs, _) in found.items()}, json.loads(membership_raw),
                    receipt["countsIncludingZero"], queries)
            else:
                require(set(found) == chars, "Character selection is incomplete")
            source_results[kind] = {"records": len(found), "compressedSha256": compressed,
                                    "decompressedSha256": decompressed, "selectionSha256": sha(raw)}
        original = json.loads(blob("docs/n1-sources/batch-134/source-receipt.json", CANDIDATE))
        overlap = {}
        for name, info in original["outputs"].items():
            current = canonical["jmdict" if name.startswith("jmdict") else "kanjidic2"]
            for identity, digest in info["canonicalRecordHashes"].items():
                if identity in current:
                    require(current[identity] == digest, "Original source record changed")
                    overlap[identity] = digest
        require(overlap == receipt["originalPacketCanonicalEquality"], "Original overlap accounting differs")
        require(sha(signed[PREFIX + "reconcile_sources_001.py"]) == receipt["producerSha256"],
                "Source producer binding differs")
        verification = json.loads(signed[PREFIX + "verification.json"])
        require(verification["status"] == "PASS" and verification["candidate"] == CANDIDATE
                and verification["families"] == len(selected["jmdict"])
                and verification["characters"] == len(selected["kanjidic2"])
                and verification["sourceReceiptSha256"] == sha(signed[PREFIX + "receipt.json"])
                and verification["queryMembershipSha256"] == receipt["membershipSha256"]
                and verification["countsIncludingZero"] == counts
                and verification["producerSha256"] == sha(signed[PREFIX + "verify_reconcile_sources_001.py"]),
                "Author verification differs from independently reproduced result")
        before, manifest = (json.loads(blob("manifest.json", commit)) for commit in (CANDIDATE, candidate))
        old_runtime, runtime = runtime_entries(before), runtime_entries(manifest)
        require(runtime.keys() == old_runtime.keys()
                and {p for p in runtime if runtime[p] != old_runtime[p]} == {TARGET},
                "Runtime changes exceed the revised card")
        for name, (digest, binary) in runtime.items():
            raw = (REPO / name).read_bytes()
            require(sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest,
                    "Runtime manifest hash differs: " + name)
            guard.check()
        clean()
        evidence.update({"snapshot/" + name: raw for name, raw in signed.items()})
        bindings = {name: write_frozen(output / name, raw) for name, raw in evidence.items()}
        result = {
            "batch": 134, "status": "PASS", "initialSnapshot": CANDIDATE, "candidate": candidate,
            "lineageDepth": depth, "signedFiles": {name: sha(raw) for name, raw in signed.items()},
            "sources": source_results, "predicates": len(queries),
            "zeroMatches": [q for q, n in counts.items() if not n], "originalRecordOverlap": len(overlap),
            "comparisons": comparison_proofs, "runtimeEntries": len(runtime),
            "unchangedRuntimeEntries": len(runtime) - 1, "manifestSha256": sha(signed["manifest.json"]),
            "contentVersion": manifest["contentVersion"], "evidence": bindings,
            "dependencies": DEPENDENCIES, "verifierSha256": sha(Path(__file__).read_bytes()),
            "limits": "Complete source provenance and runtime preservation only; no semantic adjudication, "
                      "reviewer admission, native/device, arbitrary-pool or publication acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Reconciliation verification RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(output / "verification.json", result)))


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]).resolve())
