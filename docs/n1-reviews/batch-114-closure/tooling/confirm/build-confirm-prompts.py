"""Freeze B114 confirmation prompts, kickoffs, audit configs and preflight. Writes only new ReadOnly files; launches nothing."""
import json
import stat
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from review_chain import digest  # noqa: E402

WORKSPACE = HERE.parent.parent
ORIGINAL = WORKSPACE / "review-packets" / "batch-114-8c2bdc27"
ORIGINAL_SHA = "eb6b1042060f561cd6ff49054d0e11533c15008ea0f6bbc064b07614b1701e15"
COORDINATOR = "2451b10d-02a9-46ab-82d5-d90993f0cb8b"
OUT = HERE / "prompts"
REPORTS = WORKSPACE / "reports-114"
TOOLING = [HERE.parent / "review_chain.py"] + [HERE / name for name in (
    "audit-confirm.py", "test-audit-confirm.py", "prepare-confirm-chain.py", "verify-confirm-chain.py",
    "build-confirm-prompts.py")]
USER_DIRECTION = ("Continue the existing full-scope N1 work with B114 from the published main, respecting the "
                  "necessary review, validation and resource gates.")
RUNS = [
    {"run": "N1-B114-CLAUDE-CONFIRM-001", "family": "claude", "session": "98c7bbce-f756-4954-8263-66f20c421c8c",
     "dispositions": "F1, F2, F3 and O1 to O7",
     "limits": "L1 to L6 need no disposition: record in Limits what remains unverified for them, without treating "
               "the absence of a code change as resolution."},
    {"run": "N1-B114-GPT-CONFIRM-001", "family": "gpt", "session": "c4b8c183-4098-4614-ad40-537b1d9dccad",
     "dispositions": "F1, F2 and F3",
     "limits": "O1 (none) and L1 to L6 need no disposition: record in Limits what remains unverified for the "
               "limits, without treating the absence of a code change as resolution."},
]

TEMPLATE = """Perform ONE independent confirmation of your own B114 initial review under run {run}. This is not a new first review or an implementation task; do not begin any other round. Establish every conclusion from evidence you open in this pass. Your initial report reaches you again through the chain below and is the record of your earlier points: do not rely on remembered observations from your earlier review instead of evidence read now.

Context: the repository owner's direction for this batch is, verbatim: "{direction}" Your assignment is only the read-only confirmation described here.

Revised snapshot (fix): {candidate}
Reviewed freeze: {freeze}
Confirmation packet: {packet}
Its packet-manifest.json SHA-256: {packet_sha}
Original packet: {original}
Its SHA256SUMS.json SHA-256: {original_sha}
Your initial report: {initial}
Its SHA-256: {initial_sha}
Sole report destination: {report} (absent at preflight)
Coordinator session: {coordinator}

HOW YOU RECEIVE THE INPUTS: read the chain only. You never open packet or report files directly. The coordinator verified every bound input against these hashes before building the chain; do not hash anything yourself.
Read all {segments} segments of the B114 {family} confirmation chain. Each part header states the source path (prefixed confirm-packet/, initial-report/ or original-packet/), the source SHA-256 and which segment lines equal which source lines; cite by source path and source line numbers. The last line of each segment gives the exact path of the next segment. Segment {segments} ends with "END OF CHAIN. Follow the run instruction's phase boundary.": this pass has one phase, so that line means the chain is complete and you proceed to analysis and the report. Segment 1 is:
{first}
Read segments in order, each with one view of the exact path printed at the end of the previous segment. Never use view_range; forceReadLargeFiles: true is permitted. Segments are under 16 KB and are returned whole. You may re-view a segment you have already reached.

THE CHAIN CONTAINS, in this order ({sources} sources):
1. confirm-packet/INSTRUCTIONS.md: the confirmation tasks and report contract (the start of segment 1).
2. initial-report/{initial_name}: your complete initial report.
3. confirm-packet/RESPONSE.md, then confirm-packet/CHANGES.md.
4. confirm-packet/diffs/fix.patch, diffs/changed-lines.txt and diffs/changed-files.txt.
5. All 15 revised cards, confirm-packet/snapshot/kanji/<card>.md: {members}. Six changed ({changed}), together with repository manifest.json; the other nine did not.
6. Counterpart cards from the original packet, original-packet/repo/kanji/<card>.md, unchanged at the revised snapshot: {counterparts}.
7. All ten confirmation checks, confirm-packet/checks/: {checks}.
8. confirm-packet/evidence/README.md, evidence/jmdict-cited-entries.xml and evidence/QuizBuilder.kt.
9. Original-packet context: rubric/copilot-instructions.md (the review contract), rubric/content-structure.instructions.md, repo/docs/content-format.md lines 1-139 only (kanji, quiz authoring and curated reading-question contracts; later lines are not part of the chain by design), evidence/kanjidic2-records.xml, evidence/jmdict-families.xml and evidence/title-index.txt (one KANJI-title line for each of the {index_lines} same-commit cards in code-point order; line 1 is "{index_first}" and line {index_lines} is "{index_last}").
The OLD text of the six changed cards is not included as separate files: diffs/fix.patch shows every removed and added line with context. Every other original-packet file (other cards, word articles, stroke data, the Joyo PDF and raw SVGs, other checks and evidence) is outside the permitted local inputs for this pass; disclose any you would have needed as a limit.

ACCESS RULES. These narrower rules govern any wider packet wording. In particular they replace INSTRUCTIONS.md's "Allowed local reads", its advice to read large files in ranges and its encouragement of public web sources. Any breach, wherever it falls in the run, voids the whole pass: its report is quarantined and not used. There is no retry. If you notice you have breached a rule, stop immediately and tell the coordinator exactly what happened.
1. EXACTLY ONE TOOL CALL PER RESPONSE. Wait for its result before the next response. Never place two or more tool calls in one response, even for independent files, and use no parallel wrapper or batch; a tool hint that you may batch view calls does not apply here.
2. The only tools you may call are view (rule 3), web_fetch (rule 5), one create or apply_patch (rule 6), send_session_message (rule 7) and, last, task_complete (rule 8). No other tool, including web search, todo or SQL trackers, memory, skills, ask-the-user and sub-agent tools.
3. Read local inputs only with view of one explicitly named file by absolute path, never a directory and never with view_range. The only allowed local inputs are (a) the chain segments, reached as described above, and (b) one readback of your report with forceReadLargeFiles: true. The sole delivery exception is the kickoff's initial full view of this instruction file, {prompt}, with forceReadLargeFiles: true and no view_range; do not read this file again. No other local path: in particular NOT any file under review-packets or reports-114 (not even the files the chain copies) and not the chain directory.
4. No shell/PowerShell/cmd, Python/scripts, search/grep/rg/glob, enumeration/listing/wildcards/recursion, corpus scans, agents, background jobs, browser/webview, JVM/Gradle/emulator/ADB, builds or temporary files. Open no other report, observation record, author ledger, audit record, session history, scratch file or live checkout, and no summary of any other reviewer's findings; do not look for them.
5. Up to three optional web_fetch calls IN TOTAL, to directly named public https reference URLs; no web search or browser. In the same response as each fetch, BEFORE the call, publicly state the URL and the reason in ordinary response text. Private reasoning and retrospective report text do not count.
6. The only write is the one report at the destination above, after every chain segment has been read. Use one create call if available; otherwise one apply_patch call containing exactly one Add File for that path is authorized. Do not revise or append it later. After the write, one complete readback view of the report (forceReadLargeFiles: true) is authorized.
7. Exactly ONE message to the coordinator in total: after the readback, one send_session_message to session {coordinator} with only session_id and message. The message has exactly two lines: line 1, the report's absolute path; line 2, "Confirmation: " followed by exactly one of CONFIRMED, NEEDS FIX or UNVERIFIED (the verdict of your report's Confirmation line) and nothing else. No findings, requests, hash or tool output in that message. Contact no other session.
8. After that message, stop. A single task_complete call is the only tool call permitted after it; none is permitted before it.
9. If required work cannot be completed within these bounds, report the limitation truthfully and stop. No extra prompt, retry or further pass is authorized.

TASKS. Follow INSTRUCTIONS.md's tasks and report contract within these rules.
- Dispositions: give one for each of {dispositions}, as RESPONSE.md requests, after verifying each yourself. RESPONSE.md and CHANGES.md are author claims to verify, not evidence. {limits}
- Read every changed card in full and check every changed hunk against all four facets: correctness, scoped coverage, consistency and quiz safety, comprehensibility. That includes the changes RESPONSE.md lists under "Changes that do not answer a point in your report". For every quiz_exclusions pair added in this revision, use the counterpart card and the title index to judge whether it is a real direct pair and not also a distractor, and whether each linked descriptive phrase matches the linked card's real title.
- Check the post-fix meaning options in checks/quiz-safety.txt and the mechanics in evidence/QuizBuilder.kt for every card of the batch, and the reading prompts in checks/reading-options.txt; say what these audits cannot show. They model limited pools only: not custom/caller-built or multi-borrow Starter behavior, Kotlin execution, native/phone acceptance, or compatibility with installed APK 5c000bd (predates quiz_exclusions). No Kotlin/JVM/emulator/phone execution occurred; do not turn host models or static code into native acceptance.
- Report new established defects only, without a quota. Do not re-raise a point you have dispositioned unless the revision itself is wrong. Do not force a CONFIRMED verdict: CONFIRMED only if every requested item is RESOLVED, DECLINE ACCEPTED or DISPUTE ACCEPTED and you established no new actionable defect. Disclose unresolved consequential claims accurately.
- Preserve dictionary entry/sense restrictions, spelling and register distinctions. Do not invent etymology or constituent readings, demand unrelated vocabulary, or treat historical completeness as the scope.
- In Scope, list the chain segment numbers you read (and any re-views) and every web_fetch URL with its purpose.
- Identify your actual model only if verifiable; otherwise disclose that execution-model identity is unverified.

Finish with exactly one report write, then one complete view readback (forceReadLargeFiles: true). Do not hash it: the coordinator will. Then send the one two-line message of rule 7 and stop; do not start further work.
"""


def frozen(path):
    return not Path(path).stat().st_mode & stat.S_IWRITE


def bound(path, expected=None):
    data = Path(path).read_bytes()
    assert frozen(path) and (expected is None or digest(data) == expected), path
    return {"path": str(path), "sha256": digest(data)}


def freeze(path, data):
    with path.open("xb") as stream:
        stream.write(data)
    path.chmod(stat.S_IREAD)
    return {"path": str(path), "sha256": digest(data), "bytes": len(data)}


def main():
    for tool in TOOLING:
        assert frozen(tool), tool
    sums = json.loads((ORIGINAL / "SHA256SUMS.json").read_bytes())
    bound(ORIGINAL / "SHA256SUMS.json", ORIGINAL_SHA)
    index = (ORIGINAL / "evidence" / "title-index.txt").read_bytes()
    assert digest(index) == sums["evidence/title-index.txt"]
    index = index.decode("utf-8").splitlines()
    OUT.mkdir()
    record = {"coordinator": COORDINATOR, "originalSumsSha256": ORIGINAL_SHA, "runs": []}
    for spec in RUNS:
        family = spec["family"]
        preflight_path = HERE / f"{family}-chain-preflight.json"
        preflight = json.loads(preflight_path.read_bytes())
        chain_path = Path(preflight["chainManifest"])
        chain_file = bound(chain_path, preflight["chainManifestSha256"])
        chain = json.loads(chain_path.read_bytes())
        for segment in chain["segments"]:
            bound(segment["path"], segment["sha256"])
        packet = Path(preflight["packet"])
        manifest = json.loads((packet / "packet-manifest.json").read_bytes())
        packet_file = bound(packet / "packet-manifest.json", preflight["packetManifestSha256"])
        for relative, entry in manifest["files"].items():
            bound(packet / relative, entry["sha256"])
        initial = Path(manifest["originalReport"])
        initial_file = bound(initial, preflight["initialReportSha256"])
        report = Path(manifest["report"])
        assert report.parent == REPORTS and report.name == f"confirm-{family}.md" and not report.exists()
        sources = [s["source"] for s in chain["sources"]]
        counterparts = [Path(s).stem for s in sources if s.startswith("original-packet/repo/kanji/")]
        checks = [Path(s).name for s in sources if s.startswith("confirm-packet/checks/")]
        changed = [Path(p).stem for p in manifest["changed"] if p.startswith("kanji/")]
        assert set(manifest["changed"]) == {f"kanji/{c}.md" for c in changed} | {"manifest.json"}
        prompt = OUT / f"confirm-{family}-114-001.txt"
        text = TEMPLATE.format(
            run=spec["run"], direction=USER_DIRECTION, candidate=manifest["candidate"], freeze=manifest["freeze"],
            packet=packet, packet_sha=preflight["packetManifestSha256"], original=ORIGINAL, original_sha=ORIGINAL_SHA,
            initial=initial, initial_sha=preflight["initialReportSha256"], report=report, coordinator=COORDINATOR,
            segments=len(chain["segments"]), family=family.upper() if family == "gpt" else family.capitalize(),
            first=chain["segments"][0]["path"], sources=len(sources), initial_name=initial.name,
            members=" ".join(manifest["members"]), changed=" ".join(changed), counterparts=" ".join(counterparts),
            checks=", ".join(checks), index_lines=len(index), index_first=index[0], index_last=index[-1],
            prompt=prompt, dispositions=spec["dispositions"], limits=spec["limits"])
        assert "{" not in text and "}" not in text and len(changed) == 6
        prompt_file = freeze(prompt, text.encode("utf-8"))
        kickoff_text = (f"Read {prompt} using one view call with forceReadLargeFiles: true and no view_range, "
                        "then follow its instructions. No other tool call may precede that read.")
        kickoff = freeze(OUT / f"kickoff-{family}-114-001.txt", kickoff_text.encode("utf-8"))
        files = [prompt_file, kickoff, chain_file, bound(preflight_path), packet_file, initial_file,
                 bound(ORIGINAL / "SHA256SUMS.json", ORIGINAL_SHA)] + [bound(tool) for tool in TOOLING]
        config = {"run": spec["run"], "kickoff": kickoff["path"], "prompt": prompt_file["path"],
                  "report": str(report), "coordinator": COORDINATOR, "expectedFamily": family,
                  "chainManifest": str(chain_path),
                  "files": [{"path": f["path"], "sha256": f["sha256"]} for f in files]}
        config_file = freeze(OUT / f"audit-config-{spec['run']}.json",
                             (json.dumps(config, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        record["runs"].append({"run": spec["run"], "family": family, "reviewerSession": spec["session"],
                               "prompt": prompt_file, "kickoff": kickoff,
                               "kickoffTrailingNewline": kickoff_text.endswith("\n"), "auditConfig": config_file,
                               "chainSegments": len(chain["segments"]), "chainSources": len(sources),
                               "report": str(report), "reportAbsent": not report.exists()})
    record["tooling"] = [bound(tool) for tool in TOOLING]
    record["note"] = ("Before each delivery, freeze the reviewer record's byte length and prefix SHA-256; the audit "
                      "covers only the slice after it and is VOID on any hash or ReadOnly drift.")
    freeze(OUT / "prompts-preflight.json", (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({r["run"]: [r["prompt"]["sha256"], r["kickoff"]["sha256"], r["auditConfig"]["sha256"]]
                      for r in record["runs"]}, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
