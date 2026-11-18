"""Verify the signed B133 reconciliation-003 delta, exact runtime preservation and ten committed gates.

Successor of verify_b133_teaching_revision_v3.py for the third owner-signed reconciliation: the parent is
reconciliation-002 d7d6cff9 (lineage depth 3 from the reviewed candidate). Only kanji/滝.md changes
teaching: 酒 is appended to quiz_exclusions; the unsupported 滝水 gloss is replaced in the first Meaning
paragraph and in the 液 Note; one 酒 Note bullet follows the 液 bullet; and the 滝水 citation is inserted in
the metadata block. Records live under docs/n1-sources/batch-133-reconciliation-003/.
"""
import difflib
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from run_b133_closure_checks import BASE, CANDIDATE, ORDER, REPO, lineage
from verify_b131_gate_evidence_v2 import memory_ok
from verify_b133_gates_v2 import commands, verify_execution, verify_launcher, verify_reading_output
from verify_b133_packet import RUNNER
from verify_b133_payload import runtime_entries
from verify_b133_sources import Git
from verify_b133_teaching_revision_v2 import HELPERS, inventory_files

ROOT = WS / "scratch-133"
PARENT = "d7d6cff92afe8220c16a5daa76f1c3f00a2bef30"
HANDOFF = ROOT / "teaching-reconciliation-003"
OUT = ROOT / "review" / "teaching-revision-verification-004"
PREFIX = "docs/n1-sources/batch-133-reconciliation-003/"
EARLIER_PREFIXES = ("docs/n1-sources/batch-133-reconciliation/", "docs/n1-sources/batch-133-reconciliation-002/",
                    "docs/n1-sources/batch-133/")
ARTICLE = "kanji/滝.md"
ADDITIONS = ["酒"]
CITATION = "[滝水](https://kotobank.jp/word/滝水)"
OLD_SENTENCE = "日本国語大辞典 additionally records an abbreviation of 滝水, water from a waterfall."
OLD_GLOSS = "water from a waterfall"
MEANING_START = "[滝](../words/滝.md) たき is a waterfall."


def norm(text):
    return " ".join(text.split())


def bullets(block):
    parts = ("\n" + block).split("\n- ")
    return parts[0], ["- " + part for part in parts[1:]]


def verify_article(before, after):
    before, after = (raw.decode("utf-8").replace("\r\n", "\n") for raw in (before, after))
    line = re.search(r"(?m)^quiz_exclusions: \[([^\]]*)\]$", before)
    require(line is not None, "Original exclusions missing")
    old = [value.strip() for value in line[1].split(",")]
    require(old[-1] == "液" and not set(old) & set(ADDITIONS), "Parent exclusions differ")
    expected = before.replace(line[0], "quiz_exclusions: [" + ", ".join(old + ADDITIONS) + "]", 1)
    require(after.count("## Notes\n") == expected.count("## Notes\n") == 1
            and after.count("Metadata: ") == before.count("Metadata: ") == 1,
            "Notes/citation boundary is ambiguous")
    e_head, e_notes = expected.split("## Notes\n", 1)
    a_head, a_notes = after.split("## Notes\n", 1)
    e_paras, a_paras = e_head.split("\n\n"), a_head.split("\n\n")
    require(len(e_paras) == len(a_paras), "Head paragraph structure changed")
    changed = [i for i, (x, y) in enumerate(zip(e_paras, a_paras)) if x != y]
    require(len(changed) == 1 and e_paras[changed[0]].startswith(MEANING_START),
            "Revision changed teaching outside the first Meaning paragraph")
    old_para, new_para = norm(e_paras[changed[0]]), norm(a_paras[changed[0]])
    require(old_para.endswith(OLD_SENTENCE), "Parent Meaning sentence differs")
    prefix = old_para[:-len(OLD_SENTENCE)]
    tail = new_para[len(prefix):]
    require(new_para.startswith(prefix) and OLD_GLOSS not in tail and "滝水 たきすい" in tail
            and "sake" in tail and "not taught" in tail, "Meaning replacement differs from the admitted scope")
    e_body, e_meta = e_notes.split("\nMetadata: ", 1)
    a_body, a_meta = a_notes.split("\nMetadata: ", 1)
    e_lead, e_items = bullets(e_body)
    a_lead, a_items = bullets(a_body)
    require(e_lead == a_lead, "Notes lead changed")
    k = [i for i, item in enumerate(e_items) if item.startswith("- [液](液.md)")]
    require(len(k) == 1, "Parent 液 bullet missing")
    k = k[0]
    require(len(a_items) == len(e_items) + 1 and a_items[:k] == e_items[:k]
            and a_items[k + 2:] == e_items[k + 1:], "Notes bullets outside 液/酒 changed")
    liquid, sake = norm(a_items[k]), norm(a_items[k + 1])
    require(liquid.startswith("- [液](液.md)") and OLD_GLOSS not in liquid
            and "Not every liquid is a waterfall" in liquid and "not taught as meaning liquid generally" in liquid,
            "液 Note differs from the admitted scope")
    require(sake.startswith("- [酒](酒.md)") and "たきすい" in sake and "たきみず" in sake
            and "ろうすい" in sake and "not taught as meaning alcohol" in sake,
            "酒 Note differs from the admitted scope")
    old_lines, new_lines = e_meta.split("\n"), a_meta.split("\n")
    ops = [op for op in difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False).get_opcodes()
           if op[0] != "equal"]
    require(len(ops) == 1 and ops[0][0] == "insert"
            and CITATION in "\n".join(new_lines[ops[0][3]:ops[0][4]]),
            "Metadata changed other than one inserted 滝水 citation block")
    require(CITATION not in before and after.count(CITATION) == 1, "The 滝水 citation is not newly present")
    require(OLD_GLOSS not in norm(after), "The unsupported 滝水 gloss remains")
    return {"added": ADDITIONS, "meaningBefore": old_para, "meaningAfter": new_para,
            "liquidNote": liquid, "sakeNote": sake,
            "insertedMetadata": new_lines[ops[0][3]:ops[0][4]],
            "notesBeforeSha256": sha(e_notes.encode()), "notesAfterSha256": sha(a_notes.encode())}


def check_summary(summary, admission, revision, manifest_sha, wrapper_sha, runner_sha):
    require(admission["head"] == revision and admission["parent"] == PARENT
            and admission["originalBatchBase"] == BASE and admission["mode"] == "committed",
            "Committed gate admission binds another snapshot")
    memory_ok(admission["memory"])
    require(summary["status"] == "PASS" and summary["mode"] == "committed"
            and summary["head"] == revision and summary["parent"] == PARENT
            and summary["originalBatchBase"] == BASE and summary["checks"] == ORDER
            and summary["serial"] is True and summary["manifestSha256"] == manifest_sha
            and summary["runnerSha256"] == wrapper_sha and summary["originalRunnerSha256"] == runner_sha
            and set(summary["logs"]) == set(ORDER),
            "Committed gate summary differs; inspect schema rather than substitute defaults")
    memory_ok(summary["memory"])


def main(revision, summary_path, inventory_sha, wrapper_name):
    require(re.fullmatch(r"[0-9a-f]{40}", revision) and not OUT.exists(), "Use a fresh exact revision")
    require(summary_path.parent.parent == HANDOFF, "Use the actual handoff committed-gate directory")
    guard, _ = start_guard("B133 signed revision verification v4")
    captured, articles = {}, {}
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == revision
                and git("show", "-s", "--format=%P", revision).decode().strip() == PARENT
                and not git("status", "--porcelain=v1", "--untracked-files=all")
                and lineage(git, revision) == 3, "Revision is not a clean owner-signed child of d7d6cff9")
        blob = lambda name, commit=revision: git("show", commit + ":" + name)
        before, after = blob(ARTICLE, PARENT), blob(ARTICLE)
        articles[ARTICLE] = {**verify_article(before, after), "beforeSha256": sha(before), "afterSha256": sha(after)}
        captured["articles/滝-before.md"] = before
        captured["articles/滝-after.md"] = after
        current_raw, previous_raw = blob("manifest.json"), blob("manifest.json", PARENT)
        current, previous = (runtime_entries(json.loads(raw)) for raw in (current_raw, previous_raw))
        require(current.keys() == previous.keys() and len(current) == 8745
                and {p for p in current if current[p] != previous[p]} == set(articles),
                "Unexpected runtime delta")
        for path, (digest, binary) in current.items():
            raw = (REPO / path).read_bytes()
            require(binary == previous[path][1]
                    and sha(raw if binary else raw.replace(b"\r\n", b"\n")) == digest,
                    "Actual runtime differs: " + path)
            guard.check()
        inventory_raw = blob(PREFIX + "inventory.json")
        require(sha(inventory_raw) == inventory_sha, "Signed reconciliation-003 inventory differs")
        inventory = inventory_files(json.loads(inventory_raw))
        names = git("diff", "--name-only", "-z", PARENT, revision).decode().strip("\0").split("\0")
        require(set(names) == {*articles, "manifest.json", PREFIX + "inventory.json"}
                | {PREFIX + name for name in inventory}, "Changed path inventory differs")
        require(not any(name.startswith(EARLIER_PREFIXES) for name in names),
                "An earlier batch-133 record was rewritten")
        for name, entry in inventory.items():
            raw = blob(PREFIX + name)
            require(sha(raw) == entry["sha256"] and len(raw) == entry["bytes"]
                    and sha((REPO / (PREFIX + name)).read_bytes()) == entry["sha256"],
                    "Signed inventory differs: " + name)
            guard.check()
        signed = {}
        for name in HELPERS:
            raw = blob("docs/n1-sources/batch-133/producers/" + name)
            require((ROOT / name).read_bytes() == raw
                    and blob(PREFIX + "producers/original/" + name) == raw, "Executed gate helper differs: " + name)
            signed[name] = sha(raw)
        wrapper = blob(PREFIX + "producers/" + wrapper_name)
        require((HANDOFF / wrapper_name).read_bytes() == wrapper, "Executed gate wrapper differs")
        summary_raw, admission_raw = frozen(summary_path), frozen(summary_path.parent / "admission.json")
        summary, admission = json.loads(summary_raw), json.loads(admission_raw)
        check_summary(summary, admission, revision, sha(current_raw), sha(wrapper), signed["run_133_gates.py"])
        captured["committed-gates/summary.json"] = summary_raw
        captured["committed-gates/admission.json"] = admission_raw
        receipts, logs = {}, {}
        for name in ORDER:
            for suffix, key in (("json", "receiptSha256"), ("log", "logSha256")):
                raw = frozen(summary_path.parent / (name + "." + suffix), summary["logs"][name][key])
                captured["committed-gates/" + name + "." + suffix] = raw
            receipt = json.loads(captured["committed-gates/" + name + ".json"])
            require(receipt["gate"] == name and receipt["base"] == BASE and receipt["cwd"] == str(REPO)
                    and receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
                    and receipt["cleanupError"] is None and receipt.get("activeError") is None
                    and not receipt["memory"]["breach"]
                    and receipt["runnerSha256"] == signed["run_133_gates.py"]
                    and receipt["logSha256"] == summary["logs"][name]["logSha256"],
                    "Failed or unbound committed gate: " + name)
            receipts[name] = receipt
            logs[name] = captured["committed-gates/" + name + ".log"].decode()
        verify_execution(receipts, commands(), signed["common_133.py"])
        verify_launcher(receipts, logs, signed["bounded_launch_133.py"])
        keys = json.loads(blob("docs/n1-sources/batch-133/reading-keys.json"))["testedKeys"]
        latent = verify_reading_output(logs["reading-exposure"], keys)
        require(latent == 1 and receipts["manifest-rebuild"]["manifestReproducible"] is True
                and all(receipts[name]["manifestSha256"] == sha(current_raw)
                        for name in ("manifest", "manifest-rebuild")), "Reading/manifest outcomes differ")
        captured["teaching.patch"] = git("diff", "--no-color", PARENT, revision, "--", ARTICLE)
        captured["cumulative-teaching.patch"] = git("diff", "--no-color", CANDIDATE, revision, "--",
                                                    "kanji/琴.md", "kanji/鉛.md", "kanji/滝.md")
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Verification changed tree")
        result = {
            "batch": 133, "status": "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY",
            "candidate": revision, "parent": PARENT, "reviewedFreeze": CANDIDATE, "base": BASE,
            "lineageDepth": 3, "changedPaths": names,
            "manifestSha256": sha(current_raw), "contentVersion": json.loads(current_raw)["contentVersion"],
            "runtimeEntries": len(current), "runtimeChanged": sorted(articles),
            "unchangedRuntimeEntries": len(current) - len(articles), "articles": articles,
            "committedGates": ORDER, "gateWrapperSha256": sha(wrapper), "signedHelpers": signed,
            "supplementalReadingKeys": keys, "latentCollisions": latent,
            "signedInventorySha256": sha(inventory_raw), "signedInventoryFiles": len(inventory),
            "reviewAccepted": False, "publicationAccepted": False,
            "capturedExecutionFiles": {name: write_frozen(OUT / name, raw) for name, raw in captured.items()},
            "limits": "The Meaning/Note/citation wording requires separate substantive inspection; this proves the "
                      "bounded structural delta relative to d7d6cff9, all actual runtime hashes and signed serial "
                      "gates, not semantic agreement. One latent reading collision remains; no arbitrary/custom/"
                      "multiple-borrow, Kotlin/native/device, rendering, publication or whole-set acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Revision verification RAM breach")
    result["memory"] = memory
    result["verifierSha256"] = sha(frozen(Path(__file__)))
    print(freeze_json(OUT / "verification.json", result))


if __name__ == "__main__":
    require(len(sys.argv) == 5, "REVISION COMMITTED_GATE_SUMMARY INVENTORY_SHA256 WRAPPER_NAME")
    main(sys.argv[1], Path(sys.argv[2]), sys.argv[3], sys.argv[4])
