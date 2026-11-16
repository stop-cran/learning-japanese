"""Bind B128's signed reconciliation successor, complete sources, preserved bytes and gates.

Usage:
  verify_b128_reconciliation.py CANDIDATE HANDOFF_JSON HANDOFF_SHA256
  verify_b128_reconciliation.py --staged-preflight NEW_OUTPUT_JSON
"""
import datetime
import difflib
import json
import os
import re
import stat
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import (CHECKS, GUARD_SHA, WS, freeze_json, git, load_batch, readonly, require,
                    sha, start_guard)
from verify_b123_revision_v2 import runtime
import b128_source_restream as restream

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse

PARENT = "fb3c98d86881bbc6a4b61f94bce44d0947a0c808"
BASE = "bd0f4b842c588e581ccb31ad946eecedb63d32b8"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
EMAIL = "stop-cran@list.ru"
TRAILER = b"Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
SUBJECT = b"Reconcile B128 direct meaning choices"
SCRATCH = WS / "scratch-128"
REVIEW = SCRATCH / "review"
PRODUCERS = SCRATCH / "reconciliation-001-producers"
INDEX_VERIFICATION = SCRATCH / "reconciliation-stage-001" / "index-verification.json"
AUTHOR_GATES = SCRATCH / "reconciliation-author-gates-001"
COMMITTED_GATES = SCRATCH / "reconciliation-committed-gates-001"
AUTHOR_PRESERVATION = SCRATCH / "reconciliation-preservation-author-001"
COMMITTED_PRESERVATION = SCRATCH / "reconciliation-preservation-committed-001"
PREFIX = "docs/n1-sources/batch-128-reconciliation/"
ORIGINAL = "docs/n1-sources/batch-128/"
MEMBER = "\u5507"
CARD = f"kanji/{MEMBER}.md"
NOTES = "docs/n1-authoring-notes.md"
OLD_LEDGER = "docs/n1-sources/batch-128-progress.json"
NEW_LEDGER = "docs/n1-sources/batch-128-progress-reconciliation-001.json"
OTHERS = "\u5203\u58f0\u5dee\u623f\u6848\u6a2a\u92ed\u97ff\u9cf4\u5371\u5728\u90ca\u9a12\u53eb\u54b2"
OLD_GUARDS = list("\u53e3\u82b1\u9707\u52d5\u6050\u6016\u5074\u8fba\u969b\u5883\u754c\u5cb8\u7554\u97f3")
ADDED_GUARDS = list("\u54b2\u5203\u90ca")
DISTRACTORS = list("\u53e4\u53f3\u77f3")
GUARDED_IDS = ("Q1", "Q12", "Q15")
MANIFEST_SHA = "e41a903461a713df12ef9dfea2e7b4b1d3d567db6c505048e1126e5336b8d971"
CONTENT_VERSION = "31aa657d61cdfe9e"
RUNTIME_ENTRIES = 8718
PACKET_FILES_SHA = "b13e71b2a8b77f19904db672366383c03828f1bd203d0dfdc8eec6299c4379e3"
INDEX_SHA = "da05cdf84730a24de5c48cb4da2d7548e85188e407f6120b1f96598862425d50"
AUTHOR_GATES_SHA = "ce373afe7350b0b68aa8f464a94dc022a36d3f53bdab535e3df03913b5780663"
AUTHOR_PRESERVATION_SHA = "e837eac318ea6685a96dcf807bcebe1571d1f4cc1ab27a99ce058230ef95f509"
READING_SHA = "968d51fb88ef4e575d1da84f2cdfccaf18dec1cd56b5f34ce2704171d4370a8c"
ORIGINAL_RECEIPT_SHA = "796fc4ca8dbd438df830266b847c61e61a87fa6660b2b209dae7cac7145a51ef"
PRODUCER_SHAS = {
    "author_reconciliation.py": "8ec50ef3699ee2b46daadb18bf50ef2063aa4831d639fc1800148f9259255209",
    "extract_reconciliation.py": "d673b2f138a864cefb855955d53d94557b31ad0e202038db31e9c7dc14cb23fe",
    "finalize_reconciliation.py": "5e9385fbfd5e6ca6727007615c8b6bcef7cd5e69fc43c0da6baafc369d2adc76",
    "finish_reconciliation.py": "bff7b960ddbd074e3cbd547e70a1ea5f09d8fd53d08acbaefef9b92e4628ee39",
    "preserve_reconciliation.py": "ea118560c811c16dd291170563b274ee48c846eba5a052f3738ab5d0347a9b21",
    "recon_common.py": "46984032f589f77dcdbb5a06d92cae5db12f3d5d447355000068c25892a7057f",
    "run_reconciliation_gates.py": "2344a80d79cb67d5684ba55b2c5029a148a0c0052eb4be65038af1b4748e0710",
}
RUNNER_SHA = PRODUCER_SHAS["run_reconciliation_gates.py"]
COMMON_SHA = PRODUCER_SHAS["recon_common.py"]
ADMISSION_SHAS = {
    "instruction": "548297884774eaf14a295cb4feda9d15238c6fdee2c9a3663ee3317d941efc7c",
    "reportA": "a5cfe6db7186cd3b614ef953269d69acd47a7a825db41d0aa2846098d3d50226",
    "reportB": "1c7bd0e8c4b4071a1e75175b2d5477b53b68265fbb3c8342f47a0ab37e5d2456",
    "adjudicationA": "526d2921c29529dd14572f3f57461feabfe0d1a95176fea6ee30f24dd4f60001",
    "adjudicationB": "a28bf3e78f4257e00a268c6a519bc3aa530d2cf7438856bf21389d6f0b7ff067",
}
CARD_EDITS = [
    ("replace", 13, 14, 13, 14, "107c5528a22945c7ba1b6f431b52dcce5def0d53235b8cc450d7477e09adb015"),
    ("insert", 65, 65, 65, 68, "1f74fee94e25c501f1e666bc8ee6f62dc6bd49ff9882417f2c6048b31db486d8"),
    ("insert", 78, 78, 81, 86, "2312b19d5f708a142a2fbf19d55d3c6a1b2bbfc92d5f6059e29ef79638dffd2e"),
]
NOTES_EDITS = [
    ("insert", 82, 82, 82, 95, "b6bad87dd9cedb032b5ba6a8812f7b0255dfaff5deb217151bf2afb480db072b"),
]
BINDINGS = ("pair-dispositions.json", "source-receipt.json", "source-receipt-002.json",
            "selector-membership.json", "source-verification-002.json", "response-a.md",
            "response-b.md", "preserved-history.json", "author-evidence.json", "packet-files.json")
GATES = ["lint", "quiz-safety", "linkplan", "reading-exposure", "validate", "manifest",
         "unittest", "budget", "vocabulary", "manifest-rebuild"]
GATE_FILES = {"admission.json", "summary.json", *(f"{n}.{e}" for n in GATES for e in ("json", "log"))}
CLEANUP_SCOPE = "Immediate child PID only; not descendant-process acceptance."
FAMILY = {"claude": re.compile(r"claude|anthropic|opus|sonnet|haiku", re.I),
          "gpt": re.compile(r"\bgpt|openai|codex", re.I)}
LINKPLAN = ("changed word files: 1; expected pairs: 1; added link pairs: 1; total added links: 1; "
            "declared remark edits: 1; problems: 0")
EXPOSURE = ("== \u5507 (lips)", "curated option cards: \u53e4 \u53f3 \u77f3", "kun prompt \u304f\u3061\u3073\u308b",
            "\u304a\u3069\u308d\u304f", "\u307b\u3068\u308a", "\u3075\u308b\u3048\u308b", "\u3057\u3093",
            "0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice "
            "session only); 2 latent collision(s)")


def pin(path, expected=None):
    """Read exact bytes, compare a pinned digest, then make the evidence read-only."""
    path = Path(path)
    data = path.read_bytes()
    require(expected is None or sha(data) == expected, f"Changed evidence: {path}")
    if not readonly(path):
        os.chmod(path, stat.S_IREAD)
    return data


def memory_ok(memory):
    return (memory["breach"] is None and memory["freeRamBeforeBytes"] > 2 * 1024 ** 3
            and memory["minimumObservedFreeRamBytes"] >= 1024 ** 3
            and memory["abortThresholdBytes"] == 1024 ** 3
            and memory["samplingIntervalSeconds"] == 0.25)


def breaches(value):
    if isinstance(value, dict):
        own = [value["breach"]] if "breach" in value else []
        return own + [item for child in value.values() for item in breaches(child)]
    if isinstance(value, list):
        return [item for child in value for item in breaches(child)]
    return []


def metadata(raw):
    result, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
    require(result is not None, "Missing card metadata")
    return result


def tree_ids(config, rev):
    raw = git(config, *(("ls-tree", "-r", "-z", rev) if rev else ("ls-files", "-s", "-z")))
    result = {}
    for entry in raw.decode("utf-8").split("\0"):
        if entry:
            meta, path = entry.split("\t", 1)
            result[path] = meta.split()[2 if rev else 1]
    return result


def changed(config, candidate):
    revs = ("--cached",) if candidate is None else (PARENT, candidate)
    parts = [part for part in git(config, "diff", "--name-status", "--no-renames", "-z", *revs)
             .decode("utf-8").split("\0") if part]
    require(len(parts) % 2 == 0, "Unparseable diff status")
    return dict(zip(parts[1::2], parts[0::2]))


def check_edits(old, new, edits, label):
    a, b = old.splitlines(keepends=True), new.splitlines(keepends=True)
    ops = [op for op in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
           if op[0] != "equal"]
    require([(tag, i1, i2, j1, j2, sha(b"".join(b[j1:j2]))) for tag, i1, i2, j1, j2 in ops] == edits,
            f"Unexpected {label} edit")
    return a


def check_metadata(old, new):
    require({k: v for k, v in old.items() if k != "quiz_exclusions"}
            == {k: v for k, v in new.items() if k != "quiz_exclusions"},
            "Non-exclusion metadata changed")
    require(old["quiz_exclusions"] == OLD_GUARDS
            and new["quiz_exclusions"] == OLD_GUARDS + ADDED_GUARDS
            and len(set(new["quiz_exclusions"])) == 17
            and new["distractors"] == DISTRACTORS and new["title"] == "lips"
            and not set(new["distractors"]) & set(new["quiz_exclusions"]),
            "Original/required guards or curated options changed")


def check_claims(table, old, new, cards, identities, kanjidic_raw):
    claims = table["claims"]
    require(table["parentCommit"] == PARENT and table["publishedBase"] == BASE
            and table["newKanji"] == MEMBER and table["addedDirectGuards"] == ADDED_GUARDS
            and table["retainedDirectGuards"] == OLD_GUARDS
            and table["totalDeclaredDirectGuards"] == 17 and table["openUnguardedClaims"] == []
            and table["priorDecisionsPreservedNotRewritten"] is True
            and table["criterion"] and table["limits"],
            "Claim table summary differs")
    require(len(claims) == 15 and [row["id"] for row in claims] == [f"Q{i}" for i in range(1, 16)]
            and [row["pair"] for row in claims] == [[MEMBER, char] for char in OTHERS],
            "Finite claim inventory differs")
    root = ET.fromstring(kanjidic_raw)
    for row in claims:
        other = row["pair"][1]
        card = cards[other]
        guarded = row["id"] in GUARDED_IDS
        require(row["displayedLabels"] == [new["title"], card["title"]]
                and row["decision"] == ("conservative-direct-guard" if guarded else "no-guard")
                and row["declaredEndpointStatus"] == {
                    "newEndpoint": other in new["quiz_exclusions"],
                    "comparisonEndpoint": MEMBER in card.get("quiz_exclusions", []),
                    "symmetric": True, "nonTransitive": True}
                and (other in new["quiz_exclusions"]) is guarded
                and other not in old["quiz_exclusions"]
                and MEMBER not in card.get("quiz_exclusions", [])
                and row["withNewPromptAndOtherLabel"].strip()
                and row["withOtherPromptAndNewLabel"].strip() and row["residualLimit"].strip(),
                f"Disposition or declaring endpoint differs: {row['id']}")
        node = [item for item in root.iter("character") if item.findtext("literal") == other]
        require(len(node) == 1 and row["completeCharacterEnglishMeanings"]
                == [item.text for item in node[0].iter("meaning") if not item.attrib],
                f"Character meanings differ: {row['id']}")
        kinds = set()
        for source in row["sources"]:
            name = source["file"]
            if name == "jmdict-complete-records.xml":
                require(source["ent_seq"] in identities["jmdict"], f"Uncaptured family: {row['id']}")
            elif name == "kanjidic2-complete-records.xml":
                require(source["literal"] in {other, MEMBER}
                        and source["literal"] in identities["kanjidic2"], f"Uncaptured record: {row['id']}")
            elif name == "source-notes.json":
                require(source["sections"], f"Empty source-note binding: {row['id']}")
            else:
                require(name == f"comparison-cards/{other}.md", f"Unexpected source: {row['id']}")
            kinds.add(name)
        require({"jmdict-complete-records.xml", "kanjidic2-complete-records.xml",
                 f"comparison-cards/{other}.md"} <= kinds
                and any(s.get("literal") == other for s in row["sources"]),
                f"Incomplete source binding: {row['id']}")


def check_neutrality(packet_names, blob):
    responses, shared = {}, 0
    for name in [*packet_names, "packet-files.json"]:
        text = blob(PREFIX + name).decode("utf-8", "replace")
        hits = {family for family, pattern in FAMILY.items() if pattern.search(text)}
        if name == "response-a.md":
            require(hits == {"claude"}, "Response A is not Claude-only")
        elif name == "response-b.md":
            require(hits == {"gpt"}, "Response B is not GPT-only")
        elif name == "source-receipt-002.json":
            shared += 1
            neutral = json.loads(text)
            neutral.pop("admissionBindings")
            require(not any(p.search(json.dumps(neutral, ensure_ascii=False)) for p in FAMILY.values()),
                    "Family identity outside admission paths")
        else:
            shared += 1
            require(not hits, f"Family identity in shared file: {name}")
        if name.startswith("response-"):
            responses[name] = sha(blob(PREFIX + name))
    require(shared == 59 and len(responses) == 2, "Neutrality inventory differs")
    return responses


def check_log(name, log):
    text = log.decode("utf-8").replace("\r\n", "\n")
    lines = text.strip().splitlines()
    ok = {
        "lint": lines == ["kanji checked: 1, words checked: 1", "0 error(s), 0 warning(s)"],
        "quiz-safety": bool(lines) and lines[0].startswith("\u5507 (lips)  options: old | right | stone")
        and lines[-1] == "0 error(s), 0 warning(s)",
        "linkplan": text.strip() == LINKPLAN,
        "reading-exposure": all(value in text for value in EXPOSURE),
        "validate": text.strip() == "0 error(s)",
        "manifest": f"manifest.json: {RUNTIME_ENTRIES} files" in text and f"version {CONTENT_VERSION}" in text,
        "manifest-rebuild": f"manifest.json: {RUNTIME_ENTRIES} files" in text
        and f"version {CONTENT_VERSION}" in text,
        "unittest": bool(re.search(r"(?m)^Ran 431 tests in [0-9.]+s\n\nOK$", text)),
        "budget": text.startswith("{'files': "),
        "vocabulary": text.startswith("Vocabulary coverage: "),
    }[name]
    require(ok, f"Gate output differs: {name}")


def gate_commands(repo):
    lean = WS / "lean"
    return {name: [str(item) for item in arguments] for name, arguments in {
        "lint": [lean / "n1_batch_tool.py", "lint", "--base", BASE, "--no-jmdict", MEMBER],
        "quiz-safety": [lean / "quiz_safety.py", MEMBER],
        "linkplan": [lean / "n1_linkplan.py", "verify", BASE, "--remarks",
                     repo / ORIGINAL / "stale-remarks.json", MEMBER],
        "reading-exposure": [SCRATCH / "check_reading_b128.py"],
        "validate": [repo / "tools" / "validate.py"],
        "manifest": [repo / "tools" / "build_manifest.py"],
        "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
        "budget": [repo / "tools" / "check_content_budget.py"],
        "vocabulary": [repo / "tools" / "grammar_vocabulary.py", "check"],
        "manifest-rebuild": [repo / "tools" / "build_manifest.py"],
    }.items()}


def time(value):
    result = datetime.datetime.fromisoformat(value)
    require(result.tzinfo is not None, "Naive gate timestamp")
    return result


def verify_gates(mode, directory, summary_sha, head, repo, guard, not_before=None):
    directory = Path(directory)
    require({path.name for path in directory.iterdir()} == GATE_FILES, f"Gate files differ: {mode}")
    summary = json.loads(pin(directory / "summary.json", summary_sha))
    require(summary["batch"] == "128" and summary["revision"] == "reconciliation-001"
            and summary["mode"] == mode and summary["status"] == "PASS"
            and summary["parentCommit"] == PARENT and summary["publishedBase"] == BASE
            and summary["startingHead"] == head and summary["lintAndLinkplanBase"] == BASE
            and summary["checks"] == GATES and summary["manifestSha256"] == MANIFEST_SHA
            and summary["runnerSha256"] == RUNNER_SHA and summary["guardSha256"] == GUARD_SHA
            and summary["serial"] is True and summary["waitTimeoutSeconds"] == 0.1
            and summary["commonHelperSha256"] == COMMON_SHA
            and summary["cleanupTimeoutSecondsPerStage"] == 10
            and list(summary["logs"]) == GATES and memory_ok(summary["finalMemory"]),
            f"Wrong gate summary: {mode}")
    admission = json.loads(pin(directory / "admission.json"))
    require(admission == {"head": head, "parentCommit": PARENT, "publishedBase": BASE,
                          "mode": mode, "memory": admission["memory"]}
            and memory_ok(admission["memory"]), f"Gate admission differs: {mode}")
    commands, rows, latest = gate_commands(repo), [], not_before
    for name in GATES:
        declared = summary["logs"][name]
        raw = pin(directory / f"{name}.json", declared["receiptSha256"])
        log = pin(directory / f"{name}.log", declared["logSha256"])
        record = json.loads(raw)
        manifest_gate = name in ("manifest", "manifest-rebuild")
        require(record["gate"] == name and record["exitCode"] == 0
                and record["childExitCodeAfterCleanup"] == 0 and isinstance(record["childPid"], int)
                and Path(record["cwd"]) == repo and record["parentCommit"] == PARENT
                and record["publishedBase"] == BASE
                and record["logSha256"] == sha(log) and record["logBytes"] == len(log)
                and record["runnerSha256"] == RUNNER_SHA and record["commonHelperSha256"] == COMMON_SHA
                and record["guardSha256"] == GUARD_SHA and record["waitTimeoutSeconds"] == 0.1
                and record["cleanupTimeoutSecondsPerStage"] == 10
                and record["cleanupScope"] == CLEANUP_SCOPE
                and record["cleanupError"] is None and record["activeError"] is None
                and memory_ok(record["memory"])
                and record["manifestSha256"] == (MANIFEST_SHA if manifest_gate else None)
                and record["manifestReproducible"] is (name == "manifest-rebuild")
                and Path(record["command"][0]).name.lower() == "python.exe"
                and record["command"][1:] == ["-B", *commands[name]],
                f"Failed, weakened or changed gate: {mode}/{name}")
        started, finished = time(record["startedAt"]), time(record["completedAt"])
        require(finished >= started and (latest is None or started >= latest),
                f"Gate executions overlap or are out of order: {mode}/{name}")
        latest = finished
        check_log(name, log)
        rows.append({"gate": name, "receiptSha256": sha(raw), "logSha256": sha(log)})
        guard.check()
    require({row["gate"] for row in rows} == set(CHECKS), "Missing gate")
    return {"directory": str(directory), "summarySha256": summary_sha, "head": head, "gates": rows}, latest


def verify_preservation(mode, directory, summary_sha, head, names, history):
    directory = Path(directory)
    require({path.name for path in directory.iterdir()}
            == {"memory.json", "preserved-history.json", "summary.json"}, f"Preservation files differ: {mode}")
    summary = json.loads(pin(directory / "summary.json", summary_sha))
    expected = {
        "status": "PASS", "mode": mode, "parentCommit": PARENT, "publishedBase": BASE, "head": head,
        "runtimeChangedFromParent": [CARD], "runtimeAddedOrRemoved": [],
        "manifestMappedRuntimeEntries": RUNTIME_ENTRIES, "parentRuntimeEntriesUnchanged": RUNTIME_ENTRIES - 1,
        "allCandidateRuntimeHashesChecked": RUNTIME_ENTRIES,
        "supportWordAndGeometryRawBytesPreserved": True,
        "allOtherCardMetadataAndExactAllowedBodyEdits": True, "originalEvidenceFilesPreserved": 140,
        "originalProgressPreserved": True, "sharedNeutralFilesChecked": 59,
        "familyResponsesIsolated": True, "manifestSha256": MANIFEST_SHA,
        "contentVersion": CONTENT_VERSION, "producerSha256": PRODUCER_SHAS["preserve_reconciliation.py"],
    }
    require(all(summary.get(key) == value for key, value in expected.items())
            and sorted(summary["changedPaths"]) == sorted(names) and summary["limits"],
            f"Preservation summary differs: {mode}")
    require(memory_ok(json.loads(pin(directory / "memory.json"))), f"Preservation memory differs: {mode}")
    copied = json.loads(pin(directory / "preserved-history.json"))
    require(copied in (history, history["files"]), f"Preservation history differs: {mode}")
    return {"directory": str(directory), "summarySha256": sha(pin(directory / "summary.json")), "head": head}


def verify_content(config, repo, blob, previous, status, ids, guard):
    """Checks shared by the staged preflight and the signed successor."""
    parent_ids = tree_ids(config, PARENT)
    index_raw = pin(INDEX_VERIFICATION, INDEX_SHA)
    index = json.loads(index_raw)
    names = list(status)
    packet_raw = blob(PREFIX + "packet-files.json")
    packet = json.loads(packet_raw)
    packet_names = sorted(packet["files"])
    expected = {CARD, "manifest.json", NOTES, NEW_LEDGER, PREFIX + "packet-files.json",
                *(PREFIX + name for name in packet_names)}
    require(sha(packet_raw) == PACKET_FILES_SHA and packet["hashMode"] == "raw bytes; no normalization"
            and packet["excludes"] == ["packet-files.json"] and len(packet_names) == 60,
            "Packet inventory differs")
    require(set(names) == expected == set(index["files"]) and len(names) == 65
            and index["allStagedBytesEqualWorkspace"] is True and index["exactScope"] is True
            and all(status[path] == ("M" if path in {CARD, "manifest.json", NOTES} else "A") for path in names),
            "Unexpected changed-file inventory")
    require({path for path in ids if path.startswith(PREFIX)} == expected - {CARD, "manifest.json", NOTES, NEW_LEDGER},
            "Packet tree differs from inventory")
    signed = {}
    for path in names:
        raw = blob(path)
        require(ids[path] == index["files"][path]["gitBlob"]
                and sha(raw) == index["files"][path]["rawSha256"] == sha((repo / path).read_bytes()),
                f"Signed bytes differ from staged/worktree bytes: {path}")
        signed[path] = sha(raw)
        guard.check()
    for name in packet_names:
        raw = blob(PREFIX + name)
        require(sha(raw) == packet["files"][name]["sha256"] and len(raw) == packet["files"][name]["bytes"],
                f"Packet bytes differ: {name}")
        if name.startswith("producers/"):
            local = name.split("/", 1)[1]
            require(sha(raw) == PRODUCER_SHAS[local] == sha((PRODUCERS / local).read_bytes()),
                    f"Producer differs: {local}")
        elif name.startswith("author-gates-001/"):
            require(raw == (AUTHOR_GATES / name.split("/", 1)[1]).read_bytes(),
                    f"Packet author gate copy differs: {name}")
        elif name.startswith("execution-evidence/"):
            values = breaches(json.loads(raw))
            require(values and all(value is None for value in values), f"Execution memory breach: {name}")
        guard.check()
    require({name.split("/", 1)[1] for name in packet_names if name.startswith("producers/")}
            == set(PRODUCER_SHAS) and sum(name.startswith("author-gates-001/") for name in packet_names) == 22,
            "Packet producer or gate inventory differs")
    old_raw, new_raw = previous(CARD), blob(CARD)
    old, new = metadata(old_raw), metadata(new_raw)
    check_metadata(old, new)
    lines = check_edits(old_raw, new_raw, CARD_EDITS, "card")
    require(lines[13].startswith(b"quiz_exclusions: ") and lines[14] == b"---\r\n", "Card edit is not metadata/Notes")
    manifest_raw = blob("manifest.json")
    manifest = json.loads(manifest_raw)
    before, after = runtime(json.loads(previous("manifest.json"))), runtime(manifest)
    require(sha(manifest_raw) == MANIFEST_SHA and manifest["contentVersion"] == CONTENT_VERSION
            and before.keys() == after.keys() and len(after) == RUNTIME_ENTRIES
            and [path for path in after if before[path] != after[path]] == [CARD]
            and after[CARD] == sha(new_raw.replace(b"\r\n", b"\n")), "Runtime delta differs")
    for path in (f"words/{MEMBER}.md", f"strokes/{MEMBER}.json"):
        require(path not in status and ids[path] == parent_ids[path] and blob(path) == previous(path),
                f"Preserved runtime bytes changed: {path}")
    check_edits(previous(NOTES), blob(NOTES), NOTES_EDITS, "notes")
    old_ledger, ledger = json.loads(previous(OLD_LEDGER)), json.loads(blob(NEW_LEDGER))
    updates = {
        "status": "local-unreviewed-reconciled-authoring-candidate",
        "sourceEvidence": "batch-128-reconciliation/source-receipt-002.json",
        "comparisonEvidence": ["batch-128/baseline-gloss-scan.json", "batch-128/baseline-gloss-scan-002.json",
                               "batch-128-reconciliation/pair-dispositions.json"],
        "authorAudit": "batch-128-reconciliation/summary.md",
        "authorEvidence": "batch-128-reconciliation/author-evidence.json",
        "packetInventory": "batch-128-reconciliation/packet-files.json",
        "completeSourceVerification": "batch-128-reconciliation/source-verification-002.json",
        "runtimeCandidate": {"manifestSha256": MANIFEST_SHA, "contentVersion": CONTENT_VERSION,
                             "manifestMappedRuntimeEntries": RUNTIME_ENTRIES},
        "authorGates": {"status": "PASS", "summary": "batch-128-reconciliation/author-gates-001/summary.json",
                        "summarySha256": AUTHOR_GATES_SHA,
                        "committedChecks": "To be bound separately after signing; not claimed in advance."},
        "revision": "reconciliation-001", "parentCommit": PARENT,
        "supersedesWithoutOverwriting": "batch-128-progress.json",
        "addedDirectGuards": ADDED_GUARDS, "totalDirectGuards": 17,
    }
    require(OLD_LEDGER not in status and blob(OLD_LEDGER) == previous(OLD_LEDGER)
            and ledger == {**old_ledger, **updates} and ledger["membership"] == [MEMBER]
            and ledger["accounting"]["publishedPendingRecordsWithCards"] == 257
            and ledger["accounting"]["undelivered"] == 971
            and ledger["accounting"]["overallN1TaskComplete"] is False,
            "Ledger revision differs")
    for reference in ("sourceEvidence", "authorAudit", "authorEvidence", "packetInventory",
                      "completeSourceVerification"):
        require(PREFIX + updates[reference].split("/", 1)[1] in expected, f"Dangling ledger reference: {reference}")
    require(PREFIX + "author-gates-001/summary.json" in expected
            and sha(blob(PREFIX + "author-gates-001/summary.json")) == AUTHOR_GATES_SHA, "Author gate binding differs")
    history = json.loads(blob(PREFIX + "preserved-history.json"))
    originals = {path for path in parent_ids if path.startswith(ORIGINAL)} | {OLD_LEDGER}
    require(history["parentCommit"] == PARENT and history["allRawBytesMatchParent"] is True
            and set(history["files"]) == originals and len(originals) == 140
            and not originals & set(names), "Historical inventory differs")
    for path, item in history["files"].items():
        raw = blob(path)
        require(ids[path] == parent_ids[path] == item["gitBlob"] and sha(raw) == item["rawSha256"]
                and len(raw) == item["bytes"], f"History differs: {path}")
        guard.check()
    evidence = json.loads(blob(PREFIX + "author-evidence.json"))
    require(evidence["parentCommit"] == PARENT and evidence["publishedBase"] == BASE
            and evidence["authorGates"] == {"directory": str(AUTHOR_GATES), "summarySha256": AUTHOR_GATES_SHA,
                                            "checks": GATES}
            and evidence["manifestSha256"] == MANIFEST_SHA and evidence["contentVersion"] == CONTENT_VERSION
            and evidence["manifestMappedRuntimeEntries"] == RUNTIME_ENTRIES
            and evidence["runtimeChangedFromParent"] == [CARD] and evidence["originalFilesHashInventoried"] == 140,
            "Author evidence differs")
    receipt_raw = blob(PREFIX + "source-receipt-002.json")
    receipt = json.loads(receipt_raw)
    require(receipt["parentCommit"] == PARENT and receipt["publishedBase"] == BASE
            and receipt["originalReceipt"] == {"path": "source-receipt.json", "sha256": ORIGINAL_RECEIPT_SHA}
            and sha(blob(PREFIX + "source-receipt.json")) == ORIGINAL_RECEIPT_SHA
            and receipt["selectorMembership"] == {"path": "selector-membership.json",
                                                  "sha256": sha(blob(PREFIX + "selector-membership.json"))}
            and receipt["verification"] == {"path": "source-verification-002.json",
                                            "sha256": sha(blob(PREFIX + "source-verification-002.json"))}
            and receipt["recordCounts"] == {"jmdict": 50, "kanjidic2": 16}
            and receipt["producerSha256"] == PRODUCER_SHAS["finalize_reconciliation.py"]
            and set(receipt["admissionBindings"]) == set(ADMISSION_SHAS), "Source receipt differs")
    for key, digest in ADMISSION_SHAS.items():
        item = receipt["admissionBindings"][key]
        require(item["sha256"] == digest == sha(Path(item["path"]).read_bytes()), f"Admission binding changed: {key}")
    sources = restream.verify(blob, guard)
    identities = {kind: set(item["identities"]) for kind, item in sources.items()}
    require(len(identities["jmdict"]) == 50 and len(identities["kanjidic2"]) == 16
            and identities["kanjidic2"] == set(OTHERS + MEMBER), "Re-streamed record counts differ")
    require({name for name in packet_names if name.startswith("comparison-cards/")}
            == {f"comparison-cards/{char}.md" for char in MEMBER + OTHERS}, "Comparison card inventory differs")
    cards = {}
    for char in MEMBER + OTHERS:
        copied = blob(PREFIX + f"comparison-cards/{char}.md")
        require(copied == previous(f"kanji/{char}.md"), f"Comparison snapshot differs: {char}")
        if char != MEMBER:
            require(copied == blob(f"kanji/{char}.md") and f"kanji/{char}.md" not in status,
                    f"Comparison endpoint changed: {char}")
            cards[char] = metadata(copied)
    pairs_raw = blob(PREFIX + "pair-dispositions.json")
    check_claims(json.loads(pairs_raw), old, new, cards, identities,
                 blob(PREFIX + "kanjidic2-complete-records.xml"))
    responses = check_neutrality(packet_names, blob)
    require(sha(SCRATCH.joinpath("check_reading_b128.py").read_bytes()) == READING_SHA
            == sha(blob(ORIGINAL + "producers/check_reading_b128.py")), "Reading-exposure producer differs")
    return {
        "names": names, "signed": signed, "history": history, "after": after,
        "sources": {kind: {key: value for key, value in item.items() if key != "membership"}
                    for kind, item in sources.items()},
        "responses": responses, "packetSha256": sha(packet_raw), "receiptSha256": sha(receipt_raw),
        "pairsSha256": sha(pairs_raw), "indexSha256": sha(index_raw),
    }



def check_resume(directory, candidate):
    expected = {"handoff.json", "identity-signature.log", "operation.log",
                "execution-receipt.json", "resume-evidence.json", "resume-memory.json"}
    require({path.name for path in directory.iterdir()} == expected, "Handoff directory differs")
    evidence_raw = pin(directory / "resume-evidence.json",
                       "2c66492989abb6380444bd4c378ea06680730eab867cecfdc93b6a1366ad0c93")
    memory_raw = pin(directory / "resume-memory.json",
                     "041250032fdb852bbf840db872c71153f2dad61df3bee11672dc8bc741de6ca9")
    evidence = json.loads(evidence_raw)
    require(evidence["successor"] == candidate and evidence["authorizedRetryCount"] == 1
            and evidence["originalFailedAttemptPreserved"] is True
            and evidence["finalClean"] is True and memory_ok(json.loads(memory_raw)),
            "Recovery supplement scope or RAM evidence differs")
    names = {"reconciliation-sign-001/execution-receipt.json",
             "reconciliation-sign-002/result.json", "reconciliation-sign-002/execution-receipt.json",
             "reconciliation-retry-preflight-001.json", "reconciliation-stage-001/index-verification.json",
             "reconciliation-handoff-001/handoff.json"}
    require(set(evidence["bindings"]) == names, "Recovery binding inventory differs")
    bound = {}
    for name, item in evidence["bindings"].items():
        path = SCRATCH / name
        require(Path(item["path"]) == path, "Recovery binding path differs")
        bound[name] = json.loads(pin(path, item["sha256"]))
    result = bound["reconciliation-sign-002/result.json"]
    require(result["mode"] == "sign" and result["successor"] == candidate
            and result["parent"] == PARENT and result["publishedBase"] == BASE
            and result["clean"] is True and result["signatureStatus"] == "G"
            and result["signingFingerprint"] == result["primaryFingerprint"] == FINGERPRINT,
            "Recovery signed result differs")
    for attempt in ("001", "002"):
        receipt = bound[f"reconciliation-sign-{attempt}/execution-receipt.json"]
        require(receipt["mode"] == "sign" and memory_ok(receipt["memory"])
                and receipt["waitTimeoutSeconds"] == 0.1
                and receipt["cleanupTimeoutSecondsPerStage"] == 10
                and receipt["cleanupError"] is None
                and receipt["producerSha256"] == PRODUCER_SHAS["finish_reconciliation.py"],
                "Recovery signing execution differs")
        if attempt == "002":
            require(receipt["childExitCode"] == 0 and receipt["activeError"] is None,
                    "Signing retry did not succeed")
        else:
            require(receipt["childExitCode"] == 1
                    and receipt["activeError"].startswith("Deadline reached."),
                    "Original signing failure was relabeled")
    require(evidence["budgetLog"].encode("utf-8") == pin(COMMITTED_GATES / "budget.log").replace(b"\r\n", b"\n"),
            "Recovery budget differs from committed gate")
    return {"evidenceSha256": sha(evidence_raw), "memorySha256": sha(memory_raw),
            "bindings": evidence["bindings"], "authorizedRetryCount": 1,
            "originalFailedAttemptPreserved": True}


def check_handoff(handoff, handoff_path, candidate, owner, repo, config):
    directory = handoff_path.parent
    resume = check_resume(directory, candidate)
    execution = json.loads(pin(directory / "execution-receipt.json"))
    require(execution["mode"] == "handoff" and execution["childExitCode"] == 0
            and execution["activeError"] is None and execution["cleanupError"] is None
            and execution["producerSha256"] == PRODUCER_SHAS["finish_reconciliation.py"]
            and execution["memory"]["breach"] is None, "Handoff execution differs")
    signature = pin(directory / "identity-signature.log")
    require(signature == git(config, "show", "-s", "--format=%H%n%P%n%an%n%ae%n%cn%n%ce%n%G?%n%GF%n%GP%n%B",
                             candidate), "Signature evidence differs")
    pin(directory / "operation.log")
    identity = f"{owner} <{EMAIL}>"
    bindings = {name: {"path": str(repo / PREFIX / name), "sha256": None} for name in BINDINGS}
    require(set(handoff["bindings"]) == set(BINDINGS)
            and all(Path(handoff["bindings"][name]["path"]) == Path(bindings[name]["path"]) for name in BINDINGS),
            "Handoff binding inventory differs")
    expected = {
        "mode": "handoff", "successor": candidate, "parent": PARENT, "publishedBase": BASE, "clean": True,
        "author": identity, "committer": identity, "signatureStatus": "G",
        "signingFingerprint": FINGERPRINT, "primaryFingerprint": FINGERPRINT,
        "membership": [{"kanji": MEMBER, "sourceRow": 159}],
        "runtimeChangesFromParent": [CARD, "manifest.json"],
        "supportWordAndGeometryRawBytesPreserved": True,
        "addedDirectGuards": ADDED_GUARDS, "totalDirectGuards": 17,
        "authorGates": {"directory": str(AUTHOR_GATES), "summarySha256": AUTHOR_GATES_SHA},
        "packetInventorySha256": PACKET_FILES_SHA, "manifestSha256": MANIFEST_SHA,
        "contentVersion": CONTENT_VERSION, "noOpenUnguardedClaims": True,
        "publishedAccountingUnchanged": {"delivered": 257, "remaining": 971, "localDrafts": 1},
    }
    require(all(handoff.get(key) == value for key, value in expected.items())
            and Path(handoff["signatureEvidence"]) == directory / "identity-signature.log"
            and Path(handoff["worktree"]) == repo and Path(handoff["packet"]) == repo / PREFIX
            and Path(handoff["committedGates"]["directory"]) == COMMITTED_GATES
            and handoff["committedGates"]["checks"] == GATES
            and Path(handoff["preservation"]["directory"]) == COMMITTED_PRESERVATION
            and handoff["preservation"]["runtimeCount"] == RUNTIME_ENTRIES
            and handoff["preservation"]["unchangedFromParent"] == RUNTIME_ENTRIES - 1
            and len(handoff["limits"]) == 5 and all(handoff["limits"]), "Handoff fields differ")
    return resume


def preflight(output):
    output = Path(output).resolve()
    require(output.parent == REVIEW and not output.exists(), "Preflight output must be new under review")
    config = load_batch(128)
    repo = Path(config["repo"])
    require(config["candidate"] == PARENT and config["base"] == BASE, "Batch config differs")
    guard, _ = start_guard("B128 staged reconciliation preflight")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == PARENT
                and not git(config, "diff", "--name-only")
                and not git(config, "ls-files", "--others", "--exclude-standard"), "Staged state changed")
        content = verify_content(config, repo, lambda path: git(config, "show", f":{path}"),
                                 lambda path: git(config, "show", f"{PARENT}:{path}"),
                                 changed(config, None), tree_ids(config, None), guard)
        gates, _ = verify_gates("author", AUTHOR_GATES, AUTHOR_GATES_SHA, PARENT, repo, guard)
        preservation = verify_preservation("author", AUTHOR_PRESERVATION, AUTHOR_PRESERVATION_SHA, PARENT,
                                           content["names"], content["history"])
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preflight RAM guard breached")
    print(json.dumps(freeze_json(output, {
        "batch": 128, "status": "PASS", "mode": "staged-preflight", "parent": PARENT, "base": BASE,
        "changedFiles": content["names"], "stagedArtifacts": content["signed"],
        "runtimeEntries": len(content["after"]), "sources": content["sources"],
        "responses": content["responses"], "authorGates": gates, "authorPreservation": preservation,
        "memory": memory, "verifierSha256": sha(Path(__file__).read_bytes()),
        "limits": "Pre-signing only: no signed successor, committed gates, committed preservation or "
                  "handoff exist yet; this is not the reconciliation proof.",
    }), ensure_ascii=False))


def main():
    args = sys.argv[1:]
    if args[:1] == ["--staged-preflight"]:
        require(len(args) == 2, "usage: --staged-preflight NEW_OUTPUT_JSON")
        return preflight(args[1])
    require(len(args) == 3 and re.fullmatch(r"[0-9a-f]{40}", args[0])
            and re.fullmatch(r"[0-9a-f]{64}", args[2]), "usage: CANDIDATE HANDOFF_JSON HANDOFF_SHA256")
    candidate, handoff_path, handoff_sha = args[0], Path(args[1]).resolve(), args[2]
    require(handoff_path.name == "handoff.json" and handoff_path.parent.parent == SCRATCH,
            "Handoff must be a scratch-128 handoff.json")
    config = load_batch(128)
    repo = Path(config["repo"])
    require(config["candidate"] == PARENT and config["base"] == BASE, "Batch config differs")
    output = REVIEW / "reconciliation-001-independent-proof.json"
    require(not output.exists(), "Preserve existing proof")
    handoff = json.loads(pin(handoff_path, handoff_sha))
    guard, _ = start_guard("B128 signed reconciliation verification")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
                and not git(config, "status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate is not a clean HEAD")
        require("|".join(field.strip() for field in git(
                    config, "show", "-s", "--format=%P|%G?|%GF|%GP|%ae|%ce", candidate).decode().strip().split("|"))
                == f"{PARENT}|G|{FINGERPRINT}|{FINGERPRINT}|{EMAIL}|{EMAIL}", "Wrong direct parent or owner signature")
        git(config, "verify-commit", candidate)
        owner = git(config, "show", "-s", "--format=%an", PARENT).decode("utf-8").strip()
        message = git(config, "show", "-s", "--format=%an%n%cn%n%B", candidate)
        require(message.startswith(f"{owner}\n{owner}\n".encode("utf-8") + SUBJECT) and TRAILER in message,
                "Owner identity, subject or co-author trailer differs")
        committed_at = datetime.datetime.fromtimestamp(
            int(git(config, "show", "-s", "--format=%ct", candidate).decode().strip()), datetime.timezone.utc)
        resume = check_handoff(handoff, handoff_path, candidate, owner, repo, config)
        content = verify_content(config, repo, lambda path: git(config, "show", f"{candidate}:{path}"),
                                 lambda path: git(config, "show", f"{PARENT}:{path}"),
                                 changed(config, candidate), tree_ids(config, candidate), guard)
        for name in BINDINGS:
            require(handoff["bindings"][name]["sha256"] == content["signed"][PREFIX + name],
                    f"Handoff binding differs: {name}")
        author, author_end = verify_gates("author", AUTHOR_GATES, AUTHOR_GATES_SHA, PARENT, repo, guard)
        require(author_end <= committed_at + datetime.timedelta(seconds=1), "Author gates postdate the successor")
        committed, _ = verify_gates("committed", COMMITTED_GATES, handoff["committedGates"]["summarySha256"],
                                    candidate, repo, guard, max(author_end, committed_at))
        preservation = {
            "author": verify_preservation("author", AUTHOR_PRESERVATION, AUTHOR_PRESERVATION_SHA, PARENT,
                                          content["names"], content["history"]),
            "committed": verify_preservation("committed", COMMITTED_PRESERVATION,
                                             handoff["preservation"]["summarySha256"], candidate,
                                             content["names"], content["history"]),
        }
        require(git(config, "rev-parse", "HEAD").decode().strip() == candidate
                and not git(config, "status", "--porcelain=v1", "--untracked-files=all"), "Worktree changed")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Verification RAM guard breached")
    proof = {
        "batch": 128, "status": "PASS", "candidate": candidate, "parent": PARENT, "base": BASE,
        "signature": {"fingerprint": FINGERPRINT, "ownerVerified": True}, "worktreeClean": True,
        "runtimeChanged": [CARD], "runtimeEntries": len(content["after"]), "preservedRuntimeAndHistory": True,
        "manifestSha256": MANIFEST_SHA, "contentVersion": CONTENT_VERSION,
        "changedFiles": content["names"], "signedArtifacts": content["signed"],
        "stagedIndexVerificationSha256": content["indexSha256"],
        "packetInventorySha256": content["packetSha256"], "sourceReceiptSha256": content["receiptSha256"],
        "dispositionsSha256": content["pairsSha256"], "sources": content["sources"],
        "responses": content["responses"], "gateSets": {"author": author, "committed": committed},
        "preservation": preservation, "memory": memory, "handoff": str(handoff_path),
        "handoffSha256": handoff_sha, "addedDirectGuards": ADDED_GUARDS, "totalDirectGuards": 17,
        "resumeEvidence": resume,
        "conservativeGuardIds": list(GUARDED_IDS), "openUnguardedClaims": [],
        "reviewAccepted": False, "confirmationAccepted": False,
        "verifierSha256": sha(Path(__file__).read_bytes()),
        "limits": "Signed bytes, complete reb-aware source re-stream, exact card/notes/ledger edits, preserved "
                  "history and twenty bound host gates are verified. Author semantic dispositions still require "
                  "independent original-family confirmation; conservative guards retain disclosed linguistic "
                  "uncertainty. Not native/device, arbitrary-pool or publication acceptance.",
    }
    print(json.dumps(freeze_json(output, proof), ensure_ascii=False))


if __name__ == "__main__":
    main()
