"""Batch-generic complete-record and baseline-scan verifier driven by a frozen facts file.

Reuses the pinned B124 record verifier and B126 scan helper unchanged. Card titles,
distractors and source rows are read from the signed candidate rather than supplied.
"""
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, start_guard

VERIFIER = WS / "scratch-124" / "review" / "verify-source-records.py"
VERIFIER_SHA = "21842b6d2d6040d2deb4a9f8c6d15f2c28c17386a443da52780a7ef7cc169c62"
SCAN_HELPER = Path(__file__).with_name("verify_b126_sources.py")
SCAN_SHA = "6fc5f09b2c4ed04de40f9aec2502b2e560c3b577a836b1ae7f59f587e83b20e3"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
OWNER = "stop-cran@list.ru"
ORIGIN = "https://github.com/stop-cran/learning-japanese.git"
TRAILER = b"Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
FACT_KEYS = {"batch", "repo", "base", "candidate", "prefix", "requireCheckout", "runner", "members",
             "jmdictSelections", "kanjidic2Selections", "expectedBaselineCards", "output"}
MODES = {"contains-member", "contains-any", "exact", "union"}
import source_query_union
import b130_source_schema as schema
SCHEMA_SHA = "91df923ee8ed6750b079a7ef35d0231560591fa699df15c6274e9919b9260ffa"
QUERY_SHA = "789e47df47a54d7ae260ae491e965e02921b57a39436d1bf4712ad5e289b6c12"


class Git:
    def __init__(self, repo, runner, guard):
        self.repo, self.guard = Path(repo), guard
        frozen(runner["path"], runner["sha256"])
        self.cleanup = load_module("batch_source_cleanup", Path(runner["path"]))

    def wait(self, process, data=None):
        try:
            while True:
                try:
                    out, err = process.communicate(data, timeout=0.1)
                    return out, err
                except subprocess.TimeoutExpired:
                    data = None
                    self.guard.check()
        finally:
            self.cleanup.stop_child(process)

    def __call__(self, *args, include_stderr=False):
        process = subprocess.Popen(["git", "--no-pager", "-c", "core.quotepath=false", *args], cwd=self.repo,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = self.wait(process)
        require(process.returncode == 0, f"Git failed: {args}: {err.decode('utf-8', 'replace')}")
        return out + err if include_stderr else out

    def objects(self, names):
        process = subprocess.Popen(["git", "--no-pager", "cat-file", "--batch"], cwd=self.repo,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = self.wait(process, ("\n".join(names) + "\n").encode("utf-8"))
        require(process.returncode == 0, f"Git object read failed: {err.decode('utf-8', 'replace')}")
        result, offset = [], 0
        for name in names:
            end = out.index(b"\n", offset)
            header = out[offset:end].decode("utf-8").split(" ")
            require(len(header) == 3 and header[1] == "blob", f"Missing or non-blob object: {name}")
            size = int(header[2])
            raw = out[end + 1:end + 1 + size]
            require(len(raw) == size and out[end + 1 + size:end + 2 + size] == b"\n", f"Truncated object: {name}")
            result.append((header[0], raw))
            offset = end + 2 + size
        require(offset == len(out), "Unexpected trailing object output")
        return result


def load_facts(path):
    frozen(Path(source_query_union.__file__), QUERY_SHA)
    frozen(Path(schema.__file__), SCHEMA_SHA)
    raw = frozen(path)
    facts = json.loads(raw)
    require(facts["batch"] == 130 and facts["requireCheckout"] is True,
            "B130 verifier requires batch 130 and its clean signed checkout")
    require(set(facts) == FACT_KEYS, f"Facts keys differ: {sorted(set(facts) ^ FACT_KEYS)}")
    require(all(len(facts[key]) == 40 and int(facts[key], 16) >= 0 for key in ("base", "candidate")),
            "Full commit SHAs required")
    require(facts["prefix"] == f"docs/n1-sources/batch-{facts['batch']}/", "Packet prefix differs from batch")
    require(facts["members"] and len({item["kanji"] for item in facts["members"]}) == len(facts["members"])
            and all(len(item["kanji"]) == 1 for item in facts["members"]), "Members must be distinct characters")
    for kind in ("jmdictSelections", "kanjidic2Selections"):
        for item in facts[kind]:
            require(item["mode"] in MODES and isinstance(item["queries"], list) and item["queries"]
                    and all(isinstance(query, str) and query for query in item["queries"]),
                    f"Invalid {kind} selection: {item.get('file')}")
            source_query_union.validate(item)
            require(item["mode"] != "contains-member" or len(facts["members"]) == 1,
                    "contains-member supports a single-member batch only; use contains-any")
    require(not Path(facts["output"]).exists(), "Preserve existing verification output")
    return facts, raw


verify_scan = schema.verify_scan


def main(facts_path):
    facts, facts_raw = load_facts(Path(facts_path))
    base, candidate, prefix = facts["base"], facts["candidate"], facts["prefix"]
    frozen(VERIFIER, VERIFIER_SHA)
    frozen(SCAN_HELPER, SCAN_SHA)
    verifier = load_module("batch_pinned_source_verifier", VERIFIER)
    helper = load_module("batch_pinned_scan_helper", SCAN_HELPER)
    members = [item["kanji"] for item in facts["members"]]
    if len(members) == 1:
        verifier.MEMBER = helper.MEMBER = members[0]
    guard, _ = start_guard(f"B{facts['batch']} generic signed source verification")
    git = Git(facts["repo"], facts["runner"], guard)

    def blob(path, commit=candidate):
        return git("show", f"{commit}:{path}")

    def checkout():
        if facts["requireCheckout"]:
            require(git("rev-parse", "HEAD").decode().strip() == candidate, "Candidate HEAD changed")
            require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Worktree is not clean")

    inputs, results, member_proofs = {}, [], []
    try:
        checkout()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{base}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Wrong parent, signature or owner identity")
        signature = git("verify-commit", candidate, include_stderr=True)
        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing trailer")
        snapshot_raw = blob("docs/n1-source-snapshot.json")
        require(snapshot_raw == blob("docs/n1-source-snapshot.json", base), "Source snapshot changed")
        snapshot = json.loads(snapshot_raw)
        index_raw = blob("docs/n1-sources/source-index.json")
        require(index_raw == blob("docs/n1-sources/source-index.json", base), "Source index changed")
        index = {item["kanji"]: item for item in json.loads(index_raw)}
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse

        tree = {}
        for entry in git("ls-tree", "-rz", base, "--", "kanji").decode("utf-8").split("\0"):
            if entry:
                header, name = entry.split("\t", 1)
                mode, kind, identity = header.split(" ")
                require(mode == "100644" and kind == "blob" and name.endswith(".md"), "Unexpected kanji tree entry")
                tree[name] = identity
        baseline = json.loads(blob("manifest.json", base))["files"]
        cards = {}
        for (name, identity), (actual_id, raw) in zip(tree.items(), git.objects(list(tree.values()))):
            require(actual_id == identity == hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
                    and sha(raw.replace(b"\r\n", b"\n")) == baseline[name], f"Baseline card differs: {name}")
            metadata, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
            require(metadata is not None, f"Missing metadata: {name}")
            char = Path(name).stem
            working = (Path(facts["repo"]) / name).read_bytes()
            require(working.replace(b"\r\n", b"\n") == raw.replace(b"\r\n", b"\n"),
                    f"Baseline working content differs: {name}")
            cards[char] = {"kanji": char, "path": name, "baselineGitBytesSha256": sha(raw),
                           "baselineWorkingBytesSha256": sha(working),
                           "baselineNormalizedSha256": baseline[name], "title": metadata["title"]}
            guard.check()
        require(len(cards) == facts["expectedBaselineCards"] and not set(members) & set(cards),
                "Wrong baseline membership")

        source_rows_raw = blob(prefix + "source-rows.json")
        signed_rows = json.loads(source_rows_raw)
        selection_raw = blob(prefix + "selection.json")
        selection = json.loads(selection_raw)
        membership = schema.verify_selection(selection, signed_rows, index, members, base)
        cards_new, scans = {}, {}
        for position, item in enumerate(facts["members"]):
            char = item["kanji"]
            row = index[char]
            require(row["statusAtFreeze"] == "pending"
                    and membership[position]["sourceRow"] == row["sourceRow"]
                    and signed_rows[position] == row, f"Wrong source row: {char}")
            metadata, _ = parse(blob(f"kanji/{char}.md").decode("utf-8").replace("\r\n", "\n"))
            cards_new[char] = metadata
            scans[char] = {name: json.loads(blob(prefix + item["scans"][name])) for name in ("original", "expanded")}
            require(all(scan["kanji"] == char for scan in scans[char].values()), f"Scan member differs: {char}")

        required_kd = set(members)
        for char in members:
            required_kd |= set(cards_new[char]["distractors"]) | set(scans[char]["original"]["matches"]) \
                | set(scans[char]["expanded"]["matches"])
        exact_kd = {query for item in facts["kanjidic2Selections"] if item["mode"] == "exact" for query in item["queries"]}
        require(required_kd <= exact_kd, f"KANJIDIC2 selections omit: {sorted(required_kd - exact_kd)}")
        jm_member = [item for item in facts["jmdictSelections"] if item["mode"] in {"contains-member", "contains-any"}]
        jm_member += [{"queries": [q.split(":", 1)[1] for q in item["queries"] if q.startswith("contains-keb:")]}
                      for item in facts["jmdictSelections"] if item["mode"] == "union"]
        require(all(any(char in query for item in jm_member for query in item["queries"]) for char in members),
                "Every member needs a containing JMdict family selection")

        specs = {"jmdict": facts["jmdictSelections"], "kanjidic2": facts["kanjidic2Selections"]}
        for kind, (filename, compressed_sha, tag, key) in verifier.INPUTS.items():
            path = WS / "control" / "inputs" / filename
            with path.open("rb") as stream:
                reader = helper.HashedReader(stream, guard)
                while reader.read(65536):
                    pass
            require(reader.digest.hexdigest() == compressed_sha == snapshot["inputs"][filename]["sha256"],
                    f"Compressed source differs: {kind}")
            selections = []
            for item in specs[kind]:
                raw = blob(prefix + item["file"])
                selections.append({"name": prefix + item["file"], "sha256": sha(raw), "mode": item["mode"],
                                   "queries": set(item["queries"]), "expected": verifier.records(raw, tag, key)})
            with gzip.open(path, "rb") as stream:
                reader = helper.HashedReader(stream, guard)
                identities = source_query_union.verify_stream(reader, tag, key, selections, guard)
            require(reader.digest.hexdigest() == snapshot[kind]["xmlSha256"], "Decompressed source differs")
            inputs[kind] = {"filename": filename, "compressedSha256": compressed_sha,
                            "decompressedXmlSha256": reader.digest.hexdigest()}
            for selected, matched in zip(selections, identities):
                results.append({"path": selected["name"], "sha256": selected["sha256"], "input": filename,
                                "inputSha256": compressed_sha, "mode": selected["mode"],
                                "queries": sorted(selected["queries"]), "completeMatchingRecords": len(matched),
                                "identities": matched})

        with gzip.open(WS / "control" / "inputs" / verifier.INPUTS["kanjidic2"][0], "rb") as stream:
            reader = helper.HashedReader(stream, guard)
            rows = helper.scan_baseline(reader, cards, guard)
        require(reader.digest.hexdigest() == inputs["kanjidic2"]["decompressedXmlSha256"], "Baseline scan input changed")
        comparisons = set()
        for item in facts["members"]:
            char = item["kanji"]
            meanings, title = index[char]["metadata"]["meanings"], cards_new[char]["title"]
            original = verify_scan(scans[char]["original"], rows, meanings, title, base, helper)
            expanded = verify_scan(scans[char]["expanded"], rows, meanings, title, base, helper,
                                   scans[char]["original"])
            comparisons |= set(cards_new[char]["distractors"]) | set(original["matches"]) | set(expanded["matches"])
            member_proofs.append({"kanji": char, "sourceRow": index[char]["sourceRow"], "title": title,
                                  "distractors": cards_new[char]["distractors"],
                                  "scanFiles": {name: {"path": prefix + file, "sha256": sha(blob(prefix + file))}
                                                for name, file in item["scans"].items()},
                                  "originalScan": original, "expandedScan": expanded})
        packet_cards = {}
        for entry in git("ls-tree", "-rz", candidate, "--", prefix + "comparison-cards").decode("utf-8").split("\0"):
            if entry:
                header, name = entry.split("\t", 1)
                packet_cards[Path(name).stem] = header.split(" ")[2]
        require(comparisons <= set(packet_cards), f"Comparison cards missing: {sorted(comparisons - set(packet_cards))}")
        for char, identity in packet_cards.items():
            require(identity == tree.get(f"kanji/{char}.md"), f"Comparison differs from actual baseline: {char}")
        checkout()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(Path(facts["output"]), {
        "batch": facts["batch"], "candidate": candidate, "base": base, "status": "PASS",
        "facts": {"path": str(Path(facts_path)), "sha256": sha(facts_raw)},
        "checkoutBound": facts["requireCheckout"],
        "authorSchema": {"path": str(Path(schema.__file__)), "sha256": SCHEMA_SHA},
        "selectionSha256": sha(selection_raw),
        "sourceRowsSha256": sha(source_rows_raw),
        "signatureOutputSha256": sha(signature), "signatureOutput": signature.decode("utf-8", "replace"),
        "snapshotSha256": sha(snapshot_raw), "sourceIndexSha256": sha(index_raw), "inputs": inputs,
        "sourceRecords": results, "members": member_proofs, "baselineCards": len(rows),
        "requiredComparisonCards": sorted(comparisons), "packetComparisonCards": sorted(packet_cards),
        "memory": memory, "verifierSha256": sha(Path(__file__).read_bytes()),
        "selectionVerifier": {"path": str(Path(source_query_union.__file__)), "sha256": QUERY_SHA},
        "reusedVerifier": {"path": str(VERIFIER), "sha256": VERIFIER_SHA},
        "reusedScanHelper": {"path": str(SCAN_HELPER), "sha256": SCAN_SHA},
        "limits": "Complete pinned-record membership/equality for the declared selections, coverage of members, "
                  "distractors and every scan match, and actual whole-baseline scan reproduction. Keyword adequacy, "
                  "linguistic judgments, quiz pools, native/device, review and publication remain separate.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "Usage: verify_b130_sources.py <frozen-facts.json>")
    main(sys.argv[1])
