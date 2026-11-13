"""Freeze B114 run prompts, kickoffs, audit configs and preflight. Writes only new ReadOnly files; launches nothing."""
import json
import stat
import sys
from pathlib import Path

from review_chain import digest

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
PACKET = WORKSPACE / "review-packets" / "batch-114-8c2bdc27"
PACKET_SHA = "eb6b1042060f561cd6ff49054d0e11533c15008ea0f6bbc064b07614b1701e15"
CORE = HERE / "core-chain.json"
CORE_SHA = "3c475b16806a813bed1b142b6a73f88f623f6007d0673e6a27df06372289eab9"
REFERENCE = PACKET / "eligibility-reference.json"
REFERENCE_SHA = "706f0a7a945839f1177e20643cecb2b36888032bd4ff06cb68d9b7cb6a6a1526"
COORDINATOR = "2451b10d-02a9-46ab-82d5-d90993f0cb8b"
OUT = HERE / "prompts-114"
RUNS = [
    {"run": "N1-B114-CLAUDE-001", "family": "claude", "slug": "claude"},
    {"run": "N1-B114-GPT-001", "family": "gpt", "slug": "gpt"},
]
TOOLING = ["review_chain.py", "audit-review.py", "prepare-chain.py", "build-prompts-114.py",
           "test-review-chain.py", "test-review-audit.py", "test-prepare-extension.py"]
USER_DIRECTION = ("Continue the existing full-scope N1 work with B114 from the published main, respecting the "
                  "necessary review, validation and resource gates.")

TEMPLATE = """Perform ONE complete, independent first content review of B114 under run {run}, in TWO PHASES that together form one pass. Do not implement fixes, edit content or perform a confirmation round. Establish every conclusion from evidence you open in this pass.

Context: the repository owner's direction for this batch is, verbatim: "{direction}" Your assignment is only the read-only independent review described here.

Original packet (authoritative, immutable): {packet}
Snapshot: {snapshot}
Base: {base}
Packet SHA256SUMS.json: {packet_sha}
Sole report destination: {report} (absent at preflight)
Coordinator session: {coordinator}

HOW YOU RECEIVE THE PACKET: read chains only. You never open packet files directly.
- REQUIRED CHAIN (phase 1): read all {segments} segments of the B114 core chain. Each part header states the source path, the source SHA-256 and which segment lines equal which source lines; cite findings by source path and source line numbers. The last line of each segment gives the exact path of the next segment; segment {segments} ends with "END OF CHAIN". Segment 1 is:
{first}
- EXTENSION CHAIN (phase 2): the coordinator will mechanically build, in the same format, byte-exact copies of the D and E cards you request in phase 1, in your order, and send you its first-segment path.
Read segments in order, each with one view of the exact path printed at the end of the previous segment. Never use view_range; forceReadLargeFiles: true is permitted. Segments are under 16 KB and are returned whole. You may re-view a segment you have already reached.

Do not open, request or search for any review report, observation or audit record, author rationale, changed checkout, other packet, session history, or any summary of earlier work.

ACCESS RULES. These narrower rules govern any wider packet wording, including REVIEW.md's general access text. Any breach, wherever it falls in the run, voids the whole pass: its report and observations are quarantined and not used. There is no retry. If you notice you have breached a rule, stop immediately and tell the coordinator exactly what happened.
1. EXACTLY ONE TOOL CALL PER RESPONSE. Wait for its result before the next response. Never place two or more tool calls in one response, even for independent files, and use no parallel wrapper or batch.
2. Read local inputs only with view of one explicitly named file by absolute path, never a directory and never with view_range. The only allowed local inputs are (a) core-chain segments, reached as described above, (b) extension-chain segments, reached from the first-segment path the coordinator sends in phase 2, and (c) one readback of your report with forceReadLargeFiles: true. The sole delivery exception is the kickoff's initial full view of this instruction file, {prompt}, with forceReadLargeFiles: true and no view_range; do not read this file again. No other local path: in particular NOT any file under review-packets (including repo\\kanji cards; D and E cards reach you only through the extension chain) and not the chain directories.
3. No shell/PowerShell/cmd, Python/scripts, search/grep/rg/glob, enumeration/listing/wildcards/recursion, corpus scans, agents, background jobs, browser/webview, JVM/Gradle/emulator/ADB, builds or temporary files.
4. Up to three optional web_fetch calls IN TOTAL across both phases, to directly named public https reference URLs; no web search or browser. In the same response as each fetch, BEFORE the call, publicly state the URL and the reason in ordinary response text. Private reasoning and retrospective report text do not count.
5. The only write is the one report at the destination above, in phase 2, after every core and extension segment has been read. Use one create call if available; otherwise one apply_patch call containing exactly one Add File for that path is authorized. Do not revise or append it later. One readback view of the report is authorized.
6. Exactly two messages to the coordinator in total, each a send_session_message to session {coordinator} with only session_id and message: the phase-1 list message and the phase-2 completion message described below. The second message contains only the report path and a one-line verdict. No findings, requests, hash or tool output in that message. Contact no other session.
7. After the phase-2 message, stop. A single task_complete call is the only tool call permitted after it; none is permitted before it.
8. If required work cannot be completed within these bounds, report the limitation truthfully and stop. No extra prompt, retry or further pass is authorized.

REQUIRED READS: all {segments} core segments, in full. They contain, in this order:
A. Core: REVIEW.md and packet.json (read REVIEW.md first; it is the start of segment 1); rubric\\copilot-instructions.md and rubric\\content-structure.instructions.md; repo\\docs\\content-format.md lines 1-139 only (kanji, quiz authoring and curated reading-question contracts; later lines are not part of the chain by design); repo\\docs\\jlpt-levels.md; snapshot\\kanji cards for the fifteen new kanji ({new_cards}); snapshot\\strokes JSON for the fifteen new kanji; diffs\\existing.diff; the {words} changed snapshot\\words articles; all ten checks (lint, quiz-safety, linkplan, reading-exposure-final, unittest, validate, manifest, manifest-rebuild, budget, vocabulary); evidence source-metadata.json, kanjidic2-records.xml, jmdict-families.xml, dictionary-index.json, joyo-rows.json, shape-evidence.json and provenance.json.
B. The neutral title index, evidence\\title-index.txt (SHA-256 {index_sha}): one KANJI-title line for each of the {index_lines} same-commit cards in code-point order; a mechanically extracted index, not analysis or candidate suggestions. Confirm in the report that you read source lines 1-{index_lines}, that line 1 is "{index_first}" and line {index_lines} is "{index_last}".
C. All {slots} curated distractor slots ({distinct} distinct repo\\kanji copies; a card shared by several new cards appears once): {c_list}.
The raw stroke SVGs, the binary Joyo PDF and every other packet asset not in the chains are outside the permitted local inputs for this pass. Disclose them as unread.

PHASE 1 (selection). Read all {segments} core segments in full. Then select:
D. At most 40 collision-candidate cards, each neither a C distractor, a new card, nor an existing quiz_exclusions target of a new card. For each, name the new card(s) and the overlapping sense.
E. At most 10 cards that are existing quiz_exclusions targets of a new card whose text a conclusion relies on, each with the reason. {e_note}
Request only cards by kanji character; the coordinator includes only entries that exist as repo\\kanji\\<character>.md in the original packet and reports any nonexistent entry back verbatim, with no substitutes or hints.
ELIGIBILITY REFERENCE (exact bytes of the packet's eligibility-reference.json: mechanically extracted original frontmatter, in card order):
{reference}END ELIGIBILITY REFERENCE

Before sending your final D/E lists, check every entry against this reference. D must contain no new card, distractor, or quiz_exclusions target from any new card. E must contain only quiz_exclusions targets, and no new card or distractor. Each D line must name at least one actual new card and a nonempty overlapping sense after the colon.

Phase 1 ends with EXACTLY ONE send_session_message to the coordinator whose message contains ONLY the full numbered lists, one item per line, in this form and nothing else:
D1 <character> - <new card(s)>: <overlapping sense>
...
E1 <character> - <reason>
...
Write "D: none" or "E: none" if a list is empty. Number each list consecutively starting at 1. Then end your turn and wait; make no further tool call (including task_complete) until the coordinator's phase-2 message arrives. The lists are final: phase 2 cannot add any D or E entry. Disclose later-discovered unread candidates as limits.

PHASE 2 (review). The coordinator's single phase-2 message contains exactly: line 1, the extension first-segment path; then either "Missing entries: none", or "Missing entries:" followed by your request lines, verbatim, that have no repo\\kanji card in the packet. Missing entries get no substitute; disclose them as limits. Read the whole extension chain serially (an empty selection yields one segment without source parts), then analyse and write the report.

ANALYSIS AND REPORT:
Follow REVIEW.md's four facets and report contract: correctness, scoped coverage, consistency/quiz safety, comprehensibility. Number findings F1 onward, optional points O1 onward, limits L1 onward. Distinguish CLEAN, NEEDS FIX and UNVERIFIED. Identify consequential unverified claims; automated checks are not linguistic proof.
For each new card, compare each displayed title sense and ordinary secondary sense with the full index, including shared English head words/stems. Independently determine which direct exclusion pairs the contract requires. Exclusions are symmetric, not transitive.
For each C card, check its title against the index, meaning defensibility as an option, and reading overlap. For every D/E read, decide collision-needing-exclusion, already handled, or harmless; give evidence.
Check the fifteen link-only word-article changes in diffs\\existing.diff and the changed articles for correct targets and no unintended change. Review the stroke JSON only against the card, evidence and contract text you read; make no fresh visual geometry claim.
Include: the list of core-chain and extension-chain segment numbers you read (and any re-views); your phase-1 D/E lists, any nonexistent entries, and a table of EVERY D/E card actually read (character, displayed title, related new card, reason, disposition); per-card results for all fifteen new cards; and all identified but unread candidates with reasons in Limits.
Preserve dictionary entry/sense restrictions, spelling and register distinctions. Do not invent etymology or constituent readings, demand unrelated vocabulary, or treat historical completeness as the scope.
Reading audits model limited pools only: not custom/caller-built or multi-borrow Starter behavior, Kotlin execution, native/phone acceptance, or compatibility with installed APK 5c000bd (predates quiz_exclusions). JVM/emulator work remains on hold.
Identify your actual model only if verifiable; otherwise disclose that execution-model identity is unverified.

Finish with exactly one report write, then one complete view readback (forceReadLargeFiles: true). Do not hash it: the coordinator will. Send ONE phase-2 message to the coordinator containing exactly two lines: the report's absolute path, then a one-line verdict stating CLEAN, NEEDS FIX or UNVERIFIED. No findings, requests, hash or tool output in that message. Then stop; do not start further work.
"""


def frozen(path):
    return not Path(path).stat().st_mode & stat.S_IWRITE


def freeze(path, data):
    with path.open("xb") as stream:
        stream.write(data)
    path.chmod(stat.S_IREAD)
    return {"path": str(path), "sha256": digest(data), "bytes": len(data)}


def main():
    sums_bytes = (PACKET / "SHA256SUMS.json").read_bytes()
    assert digest(sums_bytes) == PACKET_SHA and frozen(PACKET / "SHA256SUMS.json")
    sums = json.loads(sums_bytes)
    for relative, expected in sums.items():
        path = PACKET / Path(relative)
        assert digest(path.read_bytes()) == expected and frozen(path), relative
    reference_bytes = REFERENCE.read_bytes()
    assert digest(reference_bytes) == REFERENCE_SHA and sums["eligibility-reference.json"] == REFERENCE_SHA
    reference = json.loads(reference_bytes)
    core_bytes = CORE.read_bytes()
    assert digest(core_bytes) == CORE_SHA and frozen(CORE)
    core = json.loads(core_bytes)
    for segment in core["segments"]:
        data = Path(segment["path"]).read_bytes()
        assert digest(data) == segment["sha256"] and frozen(segment["path"]) and len(data) < 16384
    packet = json.loads((PACKET / "packet.json").read_bytes())
    new = reference["newCards"]
    assert new == packet["newKanji"] and reference["otherRequiredCards"] == []
    index = (PACKET / "evidence" / "title-index.txt").read_bytes().decode("utf-8").splitlines()
    assert (len(index), index[0], index[-1]) == (packet["titleIndexLines"], packet["titleIndexFirst"], packet["titleIndexLast"])
    distractors = {c for row in reference["cards"] for c in row["distractors"]}
    targets = [c for row in reference["cards"] for c in row["quiz_exclusions"]]
    curated = list(dict.fromkeys(c for row in reference["cards"] for c in row["distractors"]))
    core_cards = [Path(s["source"]).stem for s in core["sources"] if s["source"].startswith("repo/kanji/")]
    assert core_cards == curated
    slots = sum(len(row["distractors"]) for row in reference["cards"])
    target_c = sorted(dict.fromkeys(c for c in targets if c in distractors))
    target_new = sorted(dict.fromkeys(c for c in targets if c in new))
    notes = []
    if target_c:
        notes.append(" ".join(target_c) + " are C cards (already in the required chain), not E.")
    if target_new:
        notes.append("Targets that are themselves new cards (" + " ".join(target_new) + ") are read from the required chain.")
    values = {
        "direction": USER_DIRECTION, "packet": str(PACKET), "snapshot": packet["candidate"], "base": packet["base"],
        "packet_sha": PACKET_SHA, "coordinator": COORDINATOR, "segments": len(core["segments"]),
        "first": core["segments"][0]["path"], "new_cards": " ".join(new), "words": len(packet["modifiedExisting"]),
        "index_sha": sums["evidence/title-index.txt"], "index_lines": len(index), "index_first": index[0],
        "index_last": index[-1], "slots": slots, "distinct": len(curated),
        "c_list": " / ".join(f"{row['card']}: {' '.join(row['distractors'])}" for row in reference["cards"]),
        "e_note": " ".join(notes) or "No quiz_exclusions target is a C card or a new card.",
    }
    reports = WORKSPACE / "reports-114"
    OUT.mkdir()
    reports.mkdir()
    record = {"reportsDirectory": str(reports), "reportsDirectoryCreatedEmpty": not any(reports.iterdir()),
              "packetManifestSha256": PACKET_SHA, "packetFilesVerified": len(sums), "coreManifest": str(CORE),
              "coreManifestSha256": CORE_SHA, "coreSegmentsVerified": len(core["segments"]),
              "referenceSha256": REFERENCE_SHA, "coordinator": COORDINATOR, "runs": []}
    for spec in RUNS:
        prompt = OUT / f"initial-{spec['slug']}-114-001.txt"
        report = reports / f"initial-{spec['slug']}.md"
        assert not report.exists() and not (WORKSPACE / "review-chains" / f"b114-{spec['run']}-extension").exists()
        text = TEMPLATE.format(run=spec["run"], report=report, prompt=prompt, reference="{REFERENCE}", **values)
        text = text.replace("{REFERENCE}", reference_bytes.decode("utf-8"))
        assert text.count(reference_bytes.decode("utf-8")) == 1 and "{" + "REFERENCE}" not in text
        prompt_record = freeze(prompt, text.encode("utf-8"))
        kickoff_text = (f"Read {prompt} using one view call with forceReadLargeFiles: true and no view_range, "
                        "then follow its instructions. No other tool call may precede that read.")
        kickoff = freeze(OUT / f"kickoff-{spec['slug']}-114-001.txt", kickoff_text.encode("utf-8"))
        files = [prompt_record, kickoff, {"path": str(CORE), "sha256": CORE_SHA},
                 {"path": str(REFERENCE), "sha256": REFERENCE_SHA},
                 {"path": str(PACKET / "SHA256SUMS.json"), "sha256": PACKET_SHA}]
        files += [{"path": str(HERE / name), "sha256": digest((HERE / name).read_bytes())} for name in TOOLING]
        config = {"run": spec["run"], "kickoff": kickoff["path"], "prompt": prompt_record["path"],
                  "report": str(report), "coordinator": COORDINATOR, "expectedFamily": spec["family"],
                  "coreManifest": str(CORE), "reference": str(REFERENCE),
                  "files": [{"path": f["path"], "sha256": f["sha256"]} for f in files]}
        config_record = freeze(OUT / f"audit-config-{spec['run']}.json",
                               (json.dumps(config, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        record["runs"].append({"run": spec["run"], "expectedFamily": spec["family"], "prompt": prompt_record,
                               "kickoff": kickoff, "kickoffTrailingNewline": kickoff_text.endswith("\n"),
                               "auditConfig": config_record, "report": str(report), "reportAbsent": True})
    record["tooling"] = [{"path": str(HERE / name), "sha256": digest((HERE / name).read_bytes()),
                          "readOnly": frozen(HERE / name)} for name in TOOLING]
    record["note"] = "Tooling must be ReadOnly before any audit; audits VOID on any hash or ReadOnly drift."
    freeze(OUT / "prompts-preflight.json", (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({r["run"]: [r["prompt"]["sha256"], r["kickoff"]["sha256"], r["auditConfig"]["sha256"]]
                      for r in record["runs"]}, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
