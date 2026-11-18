"""Independently verify the signed B125 reconciliation-002 successor before original-family confirmations."""
import datetime
import difflib
import html
import json
import re

from common import GUARD_SHA, SIGNER, WS, freeze_json, git, load_batch, require, sha, start_guard
from verify_b123_revision_v2 import runtime

CANDIDATE = "dbca5192a4308dc6e8d954af37775e0fcd1986ea"
PARENT = "49d0b00d438969b157e739360f8639c6a9b0d950"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
TRAILER = "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
PREFIX = "docs/n1-sources/batch-125-reconciliation-002/"
PRIOR = "docs/n1-sources/batch-125-reconciliation/"
COMPARISONS = set("損略戦凌患病毒破占触違突徹討痛")
OLD_GUARDS = list("犯冒害攻撃入損痛討略戦患病毒破触違突徹")
EXPECTED_DELTA = {
    ("M", "kanji/侵.md"), ("M", "manifest.json"),
    ("A", "docs/n1-sources/batch-125-progress-003.json"),
    ("A", "docs/n1-sources/batch-125/selection-003.json"),
    ("A", "docs/n1-sources/batch-125/author-audit-003.md"),
    *{("A", PREFIX + name) for name in ("source-receipt.json", "dispositions.json",
                                        "claude-response-002.md", "gpt-response-002.md")},
}
# Values transmitted in the author's handoff before coordinator inspection.
DECLARED = {
    "dispositions": "cd2c2b9c1ef24724aa9dd4354753d6e2bfa547e9d4549fb2f1679e4e3803a3af",
    "sourceReceipt": "12f9e91e36ce611e20347f5c64d697b36f17f1cd7279acae02ee83207344bc6a",
    "claude": "bc99cdfa06643a617979666980b9c19f7eab2a7bb67ddddf7c2e9cd38ba43569",
    "gpt": "9e4f67a18b49d9d68c714b577284e83412062fd5f03f6e2e2c07861cf32130f0",
    "previousDispositions": "db59648976ec2f8f54e526c4b90929c7168006b3200e564d5d0da3712ae649b6",
    "previousSourceReceipt": "b7a96deea5a41555e14eb7ae71585d6c94dbf20bbe8038be3579e76b4ce1bbd7",
    "manifest": "0fa06c4813e212809de92787f1e227045bb00531a6d13eafe5732c0368ebb977",
    "captureReceipt": "22806123d130640b2b1b771a399195191a2287cc560fb67e644d76c85c68832e",
    "captureGate": "531ff5de92d632c5671f7fe7c65e90203eb367e1d189a1af4a7dc2a5b326067e",
    "authorIntegrity": "8b7ecfbfadb1a4f133c0dabd0e7cda9cdaecd228a72794e35f210200937a813e",
    "committedIntegrity": "63e469d38dff457a9b4d048d616d74a4be1dc17d57b8317ed5517350dfe205ad",
}
CAPTURES = {
    "ryo": ("凌", "https://www.kanjipedia.jp/kanji/0007160400",
            "dc93ba0376f96389ccc268e4282d4953c2e76fd171ec67dd585fa7c31b176e9b",
            ["①しのぐ。こえる。", "②おかす。あなどる。「凌辱」"]),
    "sen": ("占", "https://www.kanjipedia.jp/kanji/0004038500",
            "35e5f68e21a4aa81dd6b84c217018df76376b5234780f41f12b36dc5a208d0e2",
            ["①うらなう。うらない。", "②しめる。自分のものにする。「占領」「占有」"]),
    "shin": ("侵", "https://www.kanjipedia.jp/kanji/0003603100",
             "710735ff84146a52d67432006836576b54e3bf4b329daadd86ec46dc447252e4",
             ["①おかす。他人の領分に入りこむ。", "②みにくい。背が低くて容姿がみすぼらしい。"]),
}
GATE_HASHES = {
    "author": {
        "summary": "8a43196afff5a4aa52a1177b7c002424a27dfd1fcfb97650e2f9e97484a845e3",
        "lint": "29dfbe1aac25a2ecf63567c30c0b17a5c4e8c2dc27f2a1068df1f91c724ac919",
        "quiz-safety": "0a29fe5650788fa777305653a2a578477e1fd1ba7d4ac4a19fb921449281d03a",
        "linkplan": "44b68d7bbb2611c311416e07a6104a49c5d2af988f809f50464b188082fbd5a9",
        "reading-exposure": "f38b4ae23b1a0a4a151d44e2eacd4e9f10758430ea91ed69b6dcd0f848706037",
        "validate": "8e2cc32a4016e5eabbb389ab09d60b4493222f41c6c86a25e56ad6badd2cc6a2",
        "manifest": "c98ab31fd419f6078a27247e6664544bd3db4f5ae028464c4a85268201ea3b4c",
        "unittest": "e124071676e76391c39e2e3ea477fe71b058b1380ca99c588f31fdeade0d864f",
        "budget": "92ba7d64052e4aa290202d27792785529a75700b64194544447a0b6d7665948c",
        "vocabulary": "61ecaae5c06d34503a4be83fe89c1aa8976461d9c64a297ee055796d1403858f",
        "manifest-rebuild": "44fee03019a923668ddeff46ee505789be6bf841363b87b9deec4e305d3191c8",
    },
    "committed": {
        "summary": "f79fef485ccd994ab77d720d03c9a444a54f9c23354e129df3e48d9035837aba",
        "lint": "578adb3d9ce30feed29add1da91d8e9a5cff336fcdae0d9d758b2af81092d753",
        "quiz-safety": "8bd52496867ab020f69b2f395aa35083abce8be44a00f6eb923c8f4cce5598b9",
        "linkplan": "c8a07b4aae4c0ce1e80d10bbf74c6bae8ba4f62dc2e6030b7ceefb85f20ce909",
        "reading-exposure": "f6eacd09fc6a420889d9d967d89e5d4eab807a870c76c5b90f619bd05c67d91b",
        "validate": "dae1d6dd7c96da478cb7a5afb258da3060062ad96c82357cb01a9f44787dd564",
        "manifest": "bb361db3e3ff29018bab0f5bbb4627ef16f03bff164b50fd6c0f270c47d76eb7",
        "unittest": "b38dff4334353ebe63c03408db6e2e41be1e7216eb4c8abada62396f8d190b50",
        "budget": "a45d96a57ea0e47839bbe908bb9956ffa9476823b5eac89c0c08479dd22aef08",
        "vocabulary": "61dbe3d433dd159a58d212eb727167419385973085055c47832b41808a4f5f1c",
        "manifest-rebuild": "6cfeffb9b14156910869906f66c886ce536c96dd1a47c4bf8f20118d6e769195",
    },
}
DRIVER_SHA = "8c920515129eeb59ff1b71e47edde23f3a78f688f39e922c9d7199c3901cb065"
RUNNER_SHA = "ecccdbaa897600e9842865d335ab4b73a5d51b33c64c250f2c3ae60d715ba299"
CAPTURE_PRODUCER_SHA = "d53e13f23ad91c355e851a71021e25908b0ba0b9f6500bd75a52616ee2db65e1"


def frontmatter(text):
    front = text.replace("\r\n", "\n").split("---", 2)[1]
    return {line.split(":", 1)[0]: line.split(":", 1)[1].strip()
            for line in front.strip("\n").split("\n") if ":" in line}


def listed(value):
    return [item.strip() for item in value.strip("[]").split(",") if item.strip()]


def visible(data):
    text = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", data.decode("utf-8"))
    text = html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"<br\s*/?>", "", text)))
    return re.sub(r"\s+", "", text)


def stamp(value):
    return datetime.datetime.fromisoformat(value)


def receipt(path, expected_sha, command_tail, repo):
    raw = path.read_bytes()
    record = json.loads(raw)
    log = path.with_suffix(".log").read_bytes()
    require(sha(raw) == expected_sha, f"Receipt differs from handoff: {path}")
    require(record["command"][1:] == ["-B", *command_tail] and record["cwd"] == str(repo)
            and record["exitCode"] == 0 and record["childExitCodeAfterCleanup"] == 0
            and record["waitTimeoutSeconds"] <= 1 and record["runnerSha256"] == RUNNER_SHA
            and record["guardSha256"] == GUARD_SHA and record["logSha256"] == sha(log)
            and record["logBytes"] == len(log) and record["memory"]["breach"] is None
            and record["memory"]["freeRamBeforeBytes"] > 2 * 1024 ** 3
            and record["memory"]["minimumObservedFreeRamBytes"] >= 1024 ** 3
            and stamp(record["completedAt"]) >= stamp(record["startedAt"]),
            f"Command, execution, log or resource binding differs: {path}")
    return record, log


def main():
    config = load_batch(125)
    original = config["candidate"]
    blob = lambda rev, path: git(config, "show", f"{rev}:{path}")
    guard, _ = start_guard("B125 reconciliation-002 independent verification")
    try:
        meta = git(config, "log", "-1", "--format=%G?%n%GF%n%ae%n%ce%n%P%n%cI", CANDIDATE).decode().split("\n")
        require(meta[:5] == ["G", FINGERPRINT, SIGNER, SIGNER, PARENT], "Signature, identity or parent differs")
        committed_at = stamp(meta[5])
        require(TRAILER in git(config, "log", "-1", "--format=%B", CANDIDATE).decode(), "Required trailer missing")
        delta = {tuple(line.split("\t", 1)) for line in
                 git(config, "diff", "--no-renames", "--name-status", PARENT, CANDIDATE).decode().splitlines()}
        require(delta == EXPECTED_DELTA, f"Changed-file inventory differs: {sorted(delta)}")

        old_card, new_card = blob(PARENT, "kanji/侵.md").decode(), blob(CANDIDATE, "kanji/侵.md").decode()
        old_front, new_front = frontmatter(old_card), frontmatter(new_card)
        require(old_front.keys() == new_front.keys()
                and all(old_front[k] == new_front[k] for k in old_front if k != "quiz_exclusions")
                and listed(old_front["quiz_exclusions"]) == OLD_GUARDS
                and listed(new_front["quiz_exclusions"]) == OLD_GUARDS + ["凌", "占"],
                "Card metadata changed beyond the two direct guards")
        ops = [op for op in difflib.SequenceMatcher(a=old_card.splitlines(), b=new_card.splitlines(),
                                                    autojunk=False).get_opcodes() if op[0] != "equal"]
        added = new_card.splitlines()[ops[1][3]:ops[1][4]] if len(ops) == 2 else []
        require(len(ops) == 2 and ops[0][0] == "replace" and ops[0][2] - ops[0][1] == 1
                and old_card.splitlines()[ops[0][1]].startswith("quiz_exclusions:")
                and ops[1][0] == "insert" and len(added) == 1
                and "[凌](凌.md)" in added[0] and "[占](占.md)" in added[0]
                and "occupation need not involve invasion" in added[0],
                "Card prose changed beyond one bounded comparison line")
        for character in COMPARISONS:
            path = f"kanji/{character}.md"
            require(blob(CANDIDATE, path) == blob(PARENT, path) == blob(original, path),
                    f"Comparison card changed: {character}")
            guard.check()
        for path in ("words/侵入.md", "strokes/侵.json"):
            require(blob(CANDIDATE, path) == blob(original, path), f"Preserved runtime bytes changed: {path}")

        prior_dispositions = blob(PARENT, PRIOR + "dispositions.json")
        prior_receipt = blob(PARENT, PRIOR + "source-receipt.json")
        require(sha(prior_dispositions) == DECLARED["previousDispositions"]
                and sha(prior_receipt) == DECLARED["previousSourceReceipt"]
                and blob(CANDIDATE, PRIOR + "dispositions.json") == prior_dispositions
                and blob(CANDIDATE, PRIOR + "source-receipt.json") == prior_receipt,
                "Previous evidence changed")
        dispositions_raw = blob(CANDIDATE, PREFIX + "dispositions.json")
        require(sha(dispositions_raw) == DECLARED["dispositions"], "Dispositions differ from handoff")
        dispositions = json.loads(dispositions_raw)
        old_rows = {row["id"]: row for row in json.loads(prior_dispositions)["dispositions"]}
        rows = dispositions["unchanged"] + dispositions["revisions"]
        require(dispositions["parent"] == PARENT and dispositions["target"] == "侵"
                and dispositions["previousDispositionsSha256"] == DECLARED["previousDispositions"]
                and len(rows) == 15 and {row["id"] for row in rows} == set(old_rows)
                and {row["other"] for row in rows} == COMPARISONS
                and {row["id"] for row in dispositions["revisions"]} == {"Q4", "Q9"},
                "Finite inventory differs")
        for row in rows:
            old = old_rows[row["id"]]
            require(row["other"] == old["other"] and row["status"] == "direct_guard" and row["endpoint"] == "侵"
                    and row["other"] in listed(new_front["quiz_exclusions"]), f"Disposition differs: {row['id']}")
            if row["id"] in ("Q4", "Q9"):
                require(old["status"] == row["priorStatus"] == "open" and "Kanji Pedia" in row["evidence"],
                        f"Revision provenance differs: {row['id']}")
            else:
                require(old["status"] == "direct_guard" and old.get("endpoint") == "侵",
                        f"Previously settled row changed: {row['id']}")

        repo, scratch = WS / "b125-worktree", WS / "scratch-125"
        source_raw = blob(CANDIDATE, PREFIX + "source-receipt.json")
        require(sha(source_raw) == DECLARED["sourceReceipt"], "Source receipt differs from handoff")
        source = json.loads(source_raw)
        capture_dir = scratch / "reconciliation-002-source-captures-001"
        local_raw = (capture_dir / "capture-receipt.json").read_bytes()
        local = json.loads(local_raw)
        require(source["parent"] == PARENT and source["batch"] == 125
                and source["previousSourceReceipt"]["sha256"] == DECLARED["previousSourceReceipt"]
                and source["previousDispositions"]["sha256"] == DECLARED["previousDispositions"]
                and source["localCaptureReceiptSha256"] == sha(local_raw) == DECLARED["captureReceipt"]
                and source["captureGateReceiptSha256"] == DECLARED["captureGate"]
                and local["producerSha256"] == CAPTURE_PRODUCER_SHA and local["guardSha256"] == GUARD_SHA
                and sha((scratch / "reconciliation-002-capture.py").read_bytes()) == CAPTURE_PRODUCER_SHA
                and len(source["captures"]) == len(local["captures"]) == 3,
                "Capture receipt bindings differ")
        capture_record, capture_log = receipt(scratch / "reconciliation-002-capture-gate-001" / "capture.json",
                                              DECLARED["captureGate"],
                                              [str(scratch / "reconciliation-002-capture.py")], repo)
        tail = capture_log.decode("utf-8").strip().splitlines()[-4:]
        require([json.loads(line) for line in tail[:3]] == local["captures"]
                and json.loads(tail[3])["memory"]["breach"] is None, "Capture log does not bind the captures")
        identities = []
        for (stem, (character, url, digest, senses)), declared, raw in zip(
                CAPTURES.items(), source["captures"], local["captures"], strict=True):
            data = (capture_dir / f"{stem}.html").read_bytes()
            text = visible(data)
            require(declared["character"] == character and declared["url"] == raw["url"] == raw["finalUrl"] == url
                    and declared["sha256"] == raw["sha256"] == sha(data) == digest
                    and declared["bytes"] == raw["bytes"] == len(data) and raw["status"] == 200
                    and raw["contentType"].startswith("text/html") and declared["capturedAt"] == raw["capturedAt"]
                    and stamp(capture_record["startedAt"]) <= stamp(raw["capturedAt"])
                    <= stamp(capture_record["completedAt"])
                    and text.startswith(f"{character}|漢字一字|漢字ペディア")
                    and all(sense in text for sense in senses) and "角川新字源改訂新版" in text,
                    f"Capture identity or content differs: {character}")
            identities.append({"character": character, "url": url, "sha256": digest, "bytes": len(data),
                               "verifiedSenses": senses})
        shadow = scratch / "select.py"
        shadow_prefix = capture_log.decode("utf-8").split('{"url": ', 1)[0]
        shadow_memory = json.loads(shadow_prefix.strip().splitlines()[-1])["memory"]
        require(shadow_prefix.lstrip().startswith("[") and shadow_memory["breach"] is None,
                "Unexpected pre-capture output")

        claude_raw, gpt_raw = blob(CANDIDATE, PREFIX + "claude-response-002.md"), blob(CANDIDATE, PREFIX + "gpt-response-002.md")
        claude, gpt = claude_raw.decode(), gpt_raw.decode()
        require(sha(claude_raw) == DECLARED["claude"] and sha(gpt_raw) == DECLARED["gpt"], "Responses differ")
        require("gpt" not in claude.lower() and "claude" not in gpt.lower()
                and "3c3f058db413dca590555a303cd4eae704624c08f8097b45b9a01dcc15e50a7c" in claude
                and "4944978fd809b4322fe3196562b20149a3dcafd43250bc757c315b83e40822d4" in gpt
                and "kanji/撃.md:23" in claude and "1359830" in claude and "not 侵撃" in claude
                and "4944978f" not in claude and "3c3f058d" not in gpt,
                "Response isolation or E5 correction differs")
        for name in ("claude-response.md", "gpt-response.md"):
            require(blob(CANDIDATE, PRIOR + name) == blob(PARENT, PRIOR + name), f"Prior response changed: {name}")
        reports = {name: sha((WS / "reports-125" / name).read_bytes())
                   for name in ("initial-claude-001.md", "initial-gpt-002.md")}
        require(reports == {"initial-claude-001.md": "3c3f058db413dca590555a303cd4eae704624c08f8097b45b9a01dcc15e50a7c",
                            "initial-gpt-002.md": "4944978fd809b4322fe3196562b20149a3dcafd43250bc757c315b83e40822d4"},
                "Raw reports changed")

        selection = json.loads(blob(CANDIDATE, "docs/n1-sources/batch-125/selection-003.json"))
        progress = json.loads(blob(CANDIDATE, "docs/n1-sources/batch-125-progress-003.json"))
        require(selection["parent"] == progress["parent"] == PARENT
                and selection["membership"] == [{"kanji": "侵", "sourceRow": 48}]
                and selection["distractors"] == ["寝", "進", "掃"] and selection["addedDirectGuards"] == ["凌", "占"]
                and progress["membership"] == ["侵"] and progress["published"] == []
                and progress["runtimePublished"] is False and progress["reviewClosed"] == []
                and progress["accounting"] == {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 254,
                                               "publishedN1Additions": 248, "n2Placements": 6,
                                               "undelivered": 974, "overallN1TaskComplete": False},
                "Selection or progress accounting differs")

        manifest_raw = blob(CANDIDATE, "manifest.json")
        manifest_sha = sha(manifest_raw)
        manifest = json.loads(manifest_raw)
        current = runtime(manifest)
        for rev in (PARENT, original):
            before = runtime(json.loads(blob(rev, "manifest.json")))
            require(current.keys() == before.keys() and len(current) == 8712
                    and {path for path in before if before[path] != current[path]} == {"kanji/侵.md"},
                    f"Runtime scope changed relative to {rev}")
        require(manifest_sha == DECLARED["manifest"] and manifest["contentVersion"] == "e285f40167018ee4",
                "Manifest differs from handoff")

        lean = WS / "lean"
        commands = {
            "lint": [str(lean / "n1_batch_tool.py"), "lint", "--base", config["base"], "--no-jmdict", "侵"],
            "quiz-safety": [str(lean / "quiz_safety.py"), "侵"],
            "linkplan": [str(lean / "n1_linkplan.py"), "verify", config["base"], "侵"],
            "reading-exposure": [str(scratch / "reading.py")],
            "validate": [str(repo / "tools" / "validate.py")],
            "manifest": [str(repo / "tools" / "build_manifest.py")],
            "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
            "budget": [str(repo / "tools" / "check_content_budget.py")],
            "vocabulary": [str(repo / "tools" / "grammar_vocabulary.py"), "check"],
            "manifest-rebuild": [str(repo / "tools" / "build_manifest.py")],
        }
        require(sha((scratch / "reconciliation-002-gates.py").read_bytes()) == DRIVER_SHA
                and sha((WS / "scratch-124" / "run-reconciliation-002-checks.py").read_bytes()) == RUNNER_SHA,
                "Executed gate producer changed")
        gates, windows = {}, {}
        integrity_script = scratch / "reconciliation-002-integrity.py"
        for mode in ("author", "committed"):
            directory = scratch / f"reconciliation-002-{mode}-gates-001"
            summary_raw = (directory / "summary.json").read_bytes()
            summary = json.loads(summary_raw)
            require(sha(summary_raw) == GATE_HASHES[mode]["summary"] and summary["status"] == "PASS"
                    and summary["batch"] == 125 and summary["reconciliation"] == 2 and summary["mode"] == mode
                    and summary["publishedBase"] == config["base"] and summary["parent"] == PARENT
                    and summary["head"] == (PARENT if mode == "author" else CANDIDATE)
                    and summary["checks"] == list(commands) and summary["manifestSha256"] == manifest_sha
                    and summary["runnerSha256"] == DRIVER_SHA and summary["boundedRunnerSha256"] == RUNNER_SHA,
                    f"{mode} summary binding differs")
            gates[mode], latest, first = [], None, None
            for name, arguments in commands.items():
                record, log = receipt(directory / f"{name}.json", GATE_HASHES[mode][name], arguments, repo)
                started = stamp(record["startedAt"])
                require(record["gate"] == name and (latest is None or started >= latest),
                        f"{mode}/{name}: ordering differs")
                first, latest = first or started, stamp(record["completedAt"])
                if name == "unittest":
                    require(re.search(rb"(?m)^Ran 431 tests in [0-9.]+s\r?\n\r?\nOK\r?$", log),
                            "Expected test run did not pass")
                if name == "manifest-rebuild":
                    require(record["manifestReproducible"] is True and record["manifestSha256"] == manifest_sha,
                            "Manifest was not reproduced")
                gates[mode].append({"gate": name, "receiptSha256": GATE_HASHES[mode][name], "logSha256": sha(log)})
                guard.check()
            integrity, log = receipt(scratch / f"reconciliation-002-{mode}-integrity-001" / "integrity.json",
                                     DECLARED[f"{mode}Integrity"], [str(integrity_script)], repo)
            result = json.loads(log)
            require(result["parent"] == PARENT and result["head"] == (PARENT if mode == "author" else CANDIDATE)
                    and set(result["changedFiles"]) == {path for _, path in EXPECTED_DELTA}
                    and result["runtimeChangedSinceParent"] == ["kanji/侵.md"]
                    and result["manifestSha256"] == manifest_sha and result["contentVersion"] == "e285f40167018ee4"
                    and result["priorSourceFilesVerified"] == 20 and result["captureFilesVerified"] == 3
                    and result["openPairsInPredecessorNowGuarded"] == ["凌", "占"], f"{mode} integrity differs")
            windows[mode] = (first, latest, stamp(integrity["startedAt"]), stamp(integrity["completedAt"]))
        require(stamp(capture_record["completedAt"]) <= windows["author"][0]
                and windows["author"][1] <= windows["author"][2]
                and windows["author"][3] <= committed_at <= windows["committed"][0]
                and windows["committed"][1] <= windows["committed"][2],
                "Capture, author, signing and committed execution order differs")

        print(freeze_json(scratch / "review" / "reconciliation-002-independent-proof.json", {
            "batch": 125, "candidate": CANDIDATE, "parent": PARENT, "originalCandidate": original,
            "status": "PASS", "signature": {"status": "G", "fingerprint": FINGERPRINT, "signer": SIGNER},
            "changedFiles": sorted(path for _, path in EXPECTED_DELTA),
            "addedDirectGuards": ["凌", "占"], "dispositionsSha256": DECLARED["dispositions"],
            "sourceReceiptSha256": DECLARED["sourceReceipt"], "captures": identities,
            "responses": {"claude": DECLARED["claude"], "gpt": DECLARED["gpt"]},
            "manifestSha256": manifest_sha, "contentVersion": "e285f40167018ee4", "runtimeEntries": len(current),
            "gates": gates, "integrityReceipts": [DECLARED["authorIntegrity"], DECLARED["committedIntegrity"]],
            "observations": {
                "captureLogPreamble": {
                    "finding": "The capture child imported urllib.request -> socket -> selectors; selectors' "
                               "`import select` resolved to the author's scratch-125/select.py (script directory "
                               "precedes the standard library), which ran its read-only candidate scan and printed "
                               "rows before the capture code. Capture bytes, URLs and receipt lines are verified "
                               "independently; no other gate or integrity log contains that output.",
                    "shadowingScriptSha256": sha(shadow.read_bytes()),
                    "preambleSha256": sha(shadow_prefix.encode("utf-8")),
                    "integrityScriptSha256ObservedAfterRun": sha(integrity_script.read_bytes()),
                },
                "disclosedUnassessedSense": "Kanji Pedia 侵 ② みにくい (outside standard readings) is absent from "
                                            "frozen KANJIDIC2 and card metadata; the author added nothing for it.",
            },
            "reviewAccepted": False, "confirmationAccepted": False,
            "limits": "Immutable Git objects plus local author receipts and captures. Verifies exact deltas, "
                      "bindings, captured senses and twenty gate receipts; not semantic harmlessness, reviewer "
                      "confirmation, archive acceptance or publication.",
        }))
    finally:
        require(not guard.finish()["breach"], "Independent verification RAM guard breached")


if __name__ == "__main__":
    main()
