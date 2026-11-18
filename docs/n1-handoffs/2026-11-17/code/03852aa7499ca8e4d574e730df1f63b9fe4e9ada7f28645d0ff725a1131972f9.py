"""Independently recheck the B133 source-only reconciliation packet.

Streams the complete pinned dictionaries with its own exact predicates, compares every selected
record recursively, rechecks inventory/captures/articles, and validates every pair-row binding.
Mechanical provenance only: no semantic adjudication, teaching change or reviewer admission.
"""
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from run_b133_closure_checks import BASE, CANDIDATE, HERE, MEMBERS, REPO
from verify_b133_packet import RUNNER
from verify_b133_sources import FINGERPRINT, ORIGIN, OWNER, TRAILER, Git
from verify_reconciliation_sources import element_value

PACKET = HERE / "source-reconciliation-001"
INVENTORY_SHA = "771407a30005890503babae922f454e672f1d92ee504111bd83a7974960d4eb7"
PAIRS_SHA = "186a32810d754df0a53b1555f20a66a3a0fc33514b2a8654c394e3a4c72feb92"
ORIGINAL_PAIRS_SHA = "f74263f0aded22b873f368a52b6aee3dbdc3edc286e516406959daae43d9d372"
VERIFICATION_SHA = "48b255392c68f897d9db3d1d90ddd1b9215ebb37230fbd3dcb703997d92ea6b8"
FREEZE_RUN = HERE / "review" / "source-reconciliation-freeze-001"
FREEZE_LOG_SHA = "7fa475f3738db7cbb7dc5648c98fcc2e4051e2e1c6e6a59317f31252b89da516"
FREEZE_RECEIPT_SHA = "adbec263058e9b9a0df8b64b91d7f7c26ce0d3a6df856a26f11b21a4b19713cb"
RUNNER_SHA = "03260517d250b9d8071e2e70ec76fdb3ffda906d4f947e4a049375ebb249e5eb"
GUARD_SHA = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"
OUTPUT = HERE / "review" / "source-reconciliation-verification-001.json"
COMPARISONS = "\u9271\u9244\u901f\u4f3c\u5177\u5ca9\u6a5f\u7cf8\u7dd2\u7dda\u7d22\u9045\u5186\u5023\u58f0\u967a\u6fc0\u6db2"
RATIONALE = "\u6025\u5668\u91d1"
EXPECTED_PAIRS = {
    ("\u925b", "\u9271"): ["Claude C1"], ("\u925b", "\u9244"): ["Claude C2"],
    ("\u6edd", "\u901f"): ["Claude C3", "GPT Q3/D8"], ("\u925b", "\u4f3c"): ["GPT Q1/D1"],
    ("\u7434", "\u5177"): ["GPT Q2/D9"], ("\u6edd", "\u5ca9"): ["GPT Q4/D10"],
    **{("\u7434", c): ["GPT coordinator C4"] for c in "\u6a5f\u7cf8\u7dd2\u7dda\u7d22"},
    **{("\u925b", c): ["GPT coordinator C5"] for c in "\u9045\u5186\u5023"},
    **{("\u6edd", c): ["GPT coordinator C6"] for c in "\u58f0\u967a\u6fc0\u6db2"},
}


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        data = self.stream.read(size)
        self.digest.update(data)
        return data


def front_matter(text):
    lines = text.split("\n")
    require(lines[0].strip() == "---", "Article lacks front matter")
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    raise ValueError("Unterminated front matter")


def listing(value):
    value = (value or "[]").strip()
    require(value.startswith("[") and value.endswith("]"), f"Unexpected list syntax: {value}")
    return [item.strip() for item in value[1:-1].split(",") if item.strip()]


def records(data, tag, key):
    found = {}
    for node in ET.fromstring(data).findall(tag):
        identity = node.findtext(key)
        require(identity and identity not in found, f"Duplicate/missing selected identity: {identity}")
        found[identity] = element_value(node)
    return found


def stream(path, compressed, decompressed, tag, key, apply, guard):
    with path.open("rb") as raw:
        reader = HashReader(raw, guard)
        while reader.read(1024 * 1024):
            pass
    require(reader.digest.hexdigest() == compressed, f"Compressed input differs: {path.name}")
    seen = {}
    with gzip.open(path, "rb") as raw:
        reader = HashReader(raw, guard)
        parser = ET.iterparse(reader, events=("start", "end"))
        _, root = next(parser)
        for event, node in parser:
            if event != "end" or node.tag != tag:
                continue
            identity = node.findtext(key)
            matched = apply(node, identity)
            if matched:
                require(identity not in seen, f"Duplicate pinned identity: {identity}")
                seen[identity] = (matched, element_value(node))
            node.clear()
            root.clear()
        while reader.read(1024 * 1024):
            pass
    require(reader.digest.hexdigest() == decompressed, f"Decompressed input differs: {path.name}")
    return seen


def jmdict_queries(receipt_spellings, receipt_readings):
    return ([f"exact-spelling:{q}" for q in receipt_spellings]
            + [f"exact-reading:{q}" for q in receipt_readings])


def main():
    require(not OUTPUT.exists(), "Preserve the previous reconciliation verification")
    issues = []
    guard, _ = start_guard("B133 source reconciliation verification")
    try:
        inventory = json.loads(frozen(PACKET / "inventory.json", INVENTORY_SHA))
        require(inventory["fileCount"] == len(inventory["files"]) == 243
                and inventory["externalFinalGuardLogsInventoried"] is False, "Unexpected inventory")
        total = 0
        listed = set()
        for item in inventory["files"]:
            path = PACKET / item["relativePath"]
            require(path.resolve().is_relative_to(PACKET.resolve()), "Inventory path escapes packet")
            data = frozen(path, item["sha256"])
            require(len(data) == item["bytes"] and item["readOnly"] is True, f"Binding differs: {path}")
            total += len(data)
            listed.add(path.relative_to(PACKET).as_posix())
            guard.check()
        actual = {p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file()}
        require(actual == listed | {"inventory.json"} and total == inventory["totalBytes"] == 11627784,
                "Inventory coverage differs")
        log = frozen(FREEZE_RUN / "output.log", FREEZE_LOG_SHA)
        receipt = json.loads(frozen(FREEZE_RUN / "receipt.json", FREEZE_RECEIPT_SHA))
        require(receipt["exitCode"] == 0 and receipt["memory"]["breach"] is None
                and receipt["logSha256"] == sha(log) and receipt["runnerSha256"] == RUNNER_SHA
                and receipt["guardSha256"] == GUARD_SHA, "Final freeze launcher differs")
        require({p.name for p in FREEZE_RUN.iterdir()} == {"output.log", "receipt.json"},
                "Unexpected final freeze run files")

        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and git("show", "-s", "--format=%P", CANDIDATE).decode().strip() == BASE
                and not git("status", "--porcelain=v1", "--untracked-files=all")
                and git("remote", "get-url", "origin").decode().strip() == ORIGIN,
                "Candidate is changed, dirty or has another origin")
        require(git("show", "-s", "--format=%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"G|{FINGERPRINT}|{OWNER}|{OWNER}"
                and TRAILER in git("show", "-s", "--format=%B", CANDIDATE), "Candidate identity differs")

        expected_cards = set("".join(MEMBERS) + COMPARISONS + RATIONALE)
        cards = {p.stem: p for p in (PACKET / "cards").glob("*.md")}
        require(set(cards) == expected_cards and len(cards) == 24, "Candidate article coverage differs")
        articles = {}
        for char, path in cards.items():
            data = frozen(path)
            require(data == git("show", f"{CANDIDATE}:kanji/{char}.md"), f"Article differs: {char}")
            fields = front_matter(data.decode("utf-8"))
            articles[char] = {"sha256": sha(data), "title": fields["title"],
                              "exclusions": listing(fields.get("quiz_exclusions"))}

        snapshot = json.loads(git("show", f"{CANDIDATE}:docs/n1-source-snapshot.json"))
        main_receipt = json.loads(frozen(PACKET / "dictionary-receipt.json"))
        supplement = json.loads(frozen(PACKET / "supplement-receipt.json"))
        require(main_receipt["candidate"] == CANDIDATE and main_receipt["base"] == BASE
                and main_receipt["absentCharacters"] == [], "Dictionary receipt identity differs")
        main_q = jmdict_queries(main_receipt["allExactSpellings"], main_receipt["allExactReadings"])
        supp_q = jmdict_queries(supplement["spellingQueries"], supplement["readingQueries"])
        require(len(main_q) == len(set(main_q)) == 135 and len(supp_q) == len(set(supp_q)) == 17
                and set(main_receipt["queryCountsIncludingAbsences"]) == set(main_q)
                and set(supplement["queryCountsIncludingAbsences"]) == set(supp_q),
                "Query declarations differ")
        main_c, supp_c = main_receipt["allCharacterQueries"], supplement["characterQueries"]
        require(len(main_c) == len(set(main_c)) == 41 and len(supp_c) == len(set(supp_c)) == 2
                and not set(main_c) & set(supp_c), "Character query declarations differ")
        outputs = {
            "jmdict-complete-families.xml": main_receipt["outputs"]["jmdict-complete-families.xml"],
            "kanjidic2-complete-records.xml": main_receipt["outputs"]["kanjidic2-complete-records.xml"],
            "jmdict-supplement-complete-families.xml": supplement["jmdict"],
            "kanjidic2-supplement-complete-records.xml": supplement["kanjidic2"],
        }
        selected = {}
        for name, binding in outputs.items():
            data = frozen(PACKET / name, binding["sha256"])
            require(len(data) == binding["bytes"], f"Selection size differs: {name}")
            tag, key = ("entry", "ent_seq") if name.startswith("jmdict") else ("character", "literal")
            selected[name] = records(data, tag, key)
            require(set(selected[name]) == set(binding["canonicalRecordHashes"]),
                    f"Selection identities differ from receipt: {name}")

        all_q = main_q + supp_q
        spellings = {q[len("exact-spelling:"):] for q in all_q if q.startswith("exact-spelling:")}
        readings = {q[len("exact-reading:"):] for q in all_q if q.startswith("exact-reading:")}

        def jm_apply(node, identity):
            kebs = {k.text for k in node.findall("k_ele/keb") if k.text} & spellings
            rebs = {r.text for r in node.findall("r_ele/reb") if r.text} & readings
            if not kebs and not rebs:
                return []
            return sorted({f"exact-spelling:{k}" for k in kebs} | {f"exact-reading:{r}" for r in rebs})

        characters = set(main_c) | set(supp_c)

        def kd_apply(node, identity):
            return [identity] if identity in characters else []

        dictionary = {}
        for kind, (filename, compressed, decompressed, tag) in main_receipt["inputs"].items():
            require(snapshot["inputs"][filename]["sha256"] == compressed, f"Unpinned input: {filename}")
            key = "ent_seq" if tag == "entry" else "literal"
            dictionary[kind] = stream(WS / "control" / "inputs" / filename, compressed, decompressed,
                                      tag, key, jm_apply if tag == "entry" else kd_apply, guard)
        jm, kd = dictionary["jmdict"], dictionary["kanjidic2"]

        def membership(seen, queries):
            return {i: [q for q in qs if q in queries] for i, (qs, _) in seen.items()
                    if any(q in queries for q in qs)}

        main_members = membership(jm, set(main_q))
        supp_members = membership(jm, set(supp_q))
        recorded_main = json.loads(frozen(PACKET / "query-membership.json"))
        if {i: sorted(v) for i, v in main_members.items()} != {i: sorted(v) for i, v in recorded_main.items()}:
            issues.append("Main JMdict per-identity query membership differs from query-membership.json")
        if ({i: sorted(v) for i, v in supp_members.items()}
                != {i: sorted(v) for i, v in supplement["membership"].items()}):
            issues.append("Supplement JMdict per-identity query membership differs from receipt")
        counts = {q: sum(q in qs for qs, _ in jm.values()) for q in all_q}
        for q in main_q:
            if counts[q] != main_receipt["queryCountsIncludingAbsences"][q]:
                issues.append(f"Main query count differs: {q}")
        for q in supp_q:
            if counts[q] != supplement["queryCountsIncludingAbsences"][q]:
                issues.append(f"Supplement query count differs: {q}")
        for name, members in (("jmdict-complete-families.xml", main_members),
                              ("jmdict-supplement-complete-families.xml", supp_members)):
            require(set(members) == set(selected[name]), f"Complete selection membership differs: {name}")
            for identity in members:
                require(jm[identity][1] == selected[name][identity], f"Incomplete or altered record: {identity}")
        for name, queries in (("kanjidic2-complete-records.xml", main_c),
                              ("kanjidic2-supplement-complete-records.xml", supp_c)):
            require(set(queries) == set(selected[name]) and set(queries) <= set(kd),
                    f"Complete KD membership differs: {name}")
            for literal in queries:
                require(kd[literal][1] == selected[name][literal], f"Incomplete or altered KD record: {literal}")
        overlap = sorted(set(selected["jmdict-complete-families.xml"])
                         & set(selected["jmdict-supplement-complete-families.xml"]))
        unique_jm = set(main_members) | set(supp_members)
        unique_kd = set(main_c) | set(supp_c)
        zero = [q for q in all_q if counts[q] == 0]
        require(len(main_members) == 113 and len(supp_members) == 4 and overlap == ["1314560", "1438010"]
                and len(unique_jm) == 115 and len(unique_kd) == 43 and len(all_q) == 152
                and len(set(all_q)) == 150 and len(zero) == 35, "Selection counts differ from handoff")

        receipts = sorted((PACKET / "captures").glob("*.receipt.json"))
        complete, failed = [], []
        for path in receipts:
            item = json.loads(frozen(path))
            stem = path.name[: -len(".receipt.json")]
            if item["status"] == "complete-capture":
                html = frozen(PACKET / "captures" / f"{stem}.html", item["htmlSha256"])
                sizes = [item[k] for k in ("htmlBytes", "bytes") if k in item]
                require(sizes == [len(html)], f"Capture size differs: {stem}")
                frozen(PACKET / "captures" / f"{stem}.txt", item["textSha256"])
                frozen(PACKET / "captures" / f"{stem}.images.json")
                require(item["httpStatus"] == 200 and item["finalUrl"].startswith("https://"),
                        f"Capture receipt differs: {stem}")
                complete.append(stem)
            else:
                require(item["status"] == "FAILED" and "404" in item["error"], f"Unexpected failure: {stem}")
                frozen(PACKET / "captures" / f"{stem}.failed-response.html", item["failedResponseSha256"])
                failed.append(stem)
        require(len(receipts) == 31 and len(complete) == 29
                and failed == ["\u3042\u3089\u304c\u306d-kotobank", "\u901f\u3044-kotobank"],
                "Capture attempt inventory differs")
        reused = json.loads(frozen(PACKET / "reused-target-capture-bindings.json"))["captures"]
        require(len(reused) == 6 and {(r["character"], r["provider"]) for r in reused}
                == {(c, p) for c in MEMBERS for p in ("kotobank", "weblio")}, "Reused capture set differs")
        for item in reused:
            stem = f"{item['character']}-{item['provider']}"
            original = Path(item["localRawCapture"])
            raw = original.read_bytes()
            require(sha(raw) == item["rawSha256"] and len(raw) == item["rawBytes"]
                    and frozen(PACKET / "reused-captures" / f"{stem}.html") == raw
                    and sha(original.with_suffix(".txt").read_bytes()) == item["textSha256"]
                    and sha(frozen(PACKET / "reused-captures" / f"{stem}.legacy.txt")) == item["textSha256"],
                    f"Reused capture differs: {stem}")

        final = json.loads(frozen(PACKET / "pair-dispositions-final.json", PAIRS_SHA))
        original_pairs = json.loads(frozen(PACKET / "pair-dispositions.json", ORIGINAL_PAIRS_SHA))
        require(final["candidate"] == CANDIDATE and final["finitePairCount"] == 18
                and final["pairRows"] == original_pairs["pairRows"], "Pair rows changed or misbound")
        require(json.loads(frozen(PACKET / "final-preparation.json"))["sourceVerificationSha256"]
                == sha(frozen(PACKET / "verification.json")) == VERIFICATION_SHA, "Verification binding differs")
        pairs = {tuple(row["pair"]): row for row in final["pairRows"]}
        require(len(pairs) == 18 and {k: pairs[k]["claimIds"] for k in pairs} == EXPECTED_PAIRS,
                "Pair/claim coverage differs from the assignment")
        proposals = {}
        locator_checks = 0

        def check_binding(binding, where):
            nonlocal locator_checks
            path = PACKET / binding["path"]
            require(path.resolve().is_relative_to(PACKET.resolve()), f"Binding escapes packet: {where}")
            text = frozen(path, binding["sha256"]).decode("utf-8").split("\n")
            cited = [text[n - 1] for n in binding["lines"] if 0 < n <= len(text)]
            if len(cited) != len(binding["lines"]) or not any(binding["locator"] in line for line in cited):
                issues.append(f"Locator not found on cited lines: {where}: {binding['path']} "
                              f"{binding['lines']} {binding['locator']!r}")
            locator_checks += 1

        for pair, row in pairs.items():
            proposals[row["proposal"]] = proposals.get(row["proposal"], 0) + 1
            for endpoint in row["actualCandidateEndpoints"]:
                article = articles[endpoint["kanji"]]
                require(endpoint["path"] == f"cards/{endpoint['kanji']}.md"
                        and endpoint["sha256"] == article["sha256"] and endpoint["title"] == article["title"]
                        and endpoint["quiz_exclusions"] == article["exclusions"],
                        f"Endpoint differs from committed article: {endpoint['kanji']}")
            a, b = pair
            require(row["existingDirectExclusions"] == {"aExcludesB": b in articles[a]["exclusions"],
                                                        "bExcludesA": a in articles[b]["exclusions"]},
                    f"Direct-exclusion facts differ: {a}-{b}")
            require(set(row["completeJMdictFamilyIds"]) <= unique_jm
                    and set(row["completeCharacterRecordKeys"]) <= unique_kd,
                    f"Pair cites unselected records: {a}-{b}")
            for binding in row["exactSourceBindings"]:
                check_binding(binding, f"{a}-{b}")
        require(proposals == {"qualified-precaution-proposed": 13, "retain-distinction-proposed": 5},
                "Proposal counts differ")
        cross = final["consequentialOutOfAssignedPairObservation"]
        require(cross["pair"] == ["\u925b", "\u5177"] and len(final["unresolved"]) == 5, "Cross-pair report differs")
        for binding in cross["sourceBindings"]:
            check_binding(binding, "cross \u925b-\u5177")
        require(not git("status", "--porcelain=v1", "--untracked-files=all")
                and git("rev-parse", "HEAD").decode().strip() == CANDIDATE, "Candidate changed during check")
        result = {
            "status": "PASS" if not issues else "FAIL", "issues": issues,
            "candidate": CANDIDATE, "base": BASE,
            "inventory": {"path": str(PACKET / "inventory.json"), "sha256": INVENTORY_SHA,
                          "files": 243, "bytes": total, "allReadOnly": True},
            "finalFreezeRun": {"output.log": FREEZE_LOG_SHA, "receipt.json": FREEZE_RECEIPT_SHA},
            "jmdict": {"main": len(main_members), "supplement": len(supp_members),
                       "equalOverlap": overlap, "unique": len(unique_jm)},
            "kanjidic2": {"main": len(main_c), "supplement": len(supp_c), "unique": len(unique_kd)},
            "queryApplications": len(all_q), "distinctQueries": len(set(all_q)), "zeroMatch": len(zero),
            "zeroMatchQueries": zero, "articles": 24, "newCaptureAttempts": 31,
            "completeNewCaptures": 29, "failedCaptures": failed, "reusedCaptures": 6,
            "pairRows": 18, "proposalCounts": proposals, "locatorChecks": locator_checks,
            "authoritativePairs": {"sha256": PAIRS_SHA, "rowsEqualOriginal": True},
            "producerSha256": sha(Path(__file__).read_bytes()),
            "precedingFailedAttempt": {
                "run": str(HERE / "review" / "source-reconciliation-verification-run-001"),
                "producerCopySha256": "557acd4099e6a63421b62769738d2a70df26eaf71a471c9aca3efb36a6e66b47",
                "logSha256": "f13be3a3a3cad59ec81634839c1b9deb76192e6ac11234d815e9c0a42f939c92",
                "failure": "KeyError htmlBytes: the 似-weblio receipt records its size as bytes; "
                           "successor accepts exactly one of htmlBytes/bytes. No output was written."},
            "limits": "Mechanical provenance/completeness only, using a separate streaming predicate and "
                      "recursive record equality. Captures are not refetched; extraction text is hash-bound, "
                      "not re-extracted. Locators are substring checks on cited lines. Original B132 survey "
                      "captures are hash-equal but not ReadOnly. No semantic adjudication, teaching change, "
                      "reviewer confirmation or publication.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Reconciliation verification RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(OUTPUT, result), ensure_ascii=False))
    require(not issues, f"Verification issues: {issues}")


if __name__ == "__main__":
    main()
