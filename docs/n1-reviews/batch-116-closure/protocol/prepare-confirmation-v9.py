"""Build a bounded B116 confirmation chain and prompt from an actual revised packet."""
import argparse
import hashlib
import importlib.util
import json
import re
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parent.parent
REPO = WORK / "rollout-recovered" / "learning-japanese"
ORIGINAL = WORK / "review-packets" / "batch-116-9e18d940-s1"
ORIGINAL_SHA = "c9978b0965138472de5147312c313d71e428a4a6864b67807f162ba60b5fd841"
COORDINATOR = "2451b10d-02a9-46ab-82d5-d90993f0cb8b"
sys.path.insert(0, str(HERE.parent))
from review_chain import build_chain  # noqa: E402

TOOL_PINS = {
    HERE / "audit-confirm.py": "c6ec99949ef19057f432c052df3293184c3866e65ba7387e148a39505a3b2c9e",
    HERE / "check-confirm-structure.py": "ad3a204757e872e54b81745a028d040e4510ce551046a63ec6b70fcb0bddd31d",
    WORK / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py":
        "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frozen(path, expected=None):
    data = path.read_bytes()
    require(not path.stat().st_mode & stat.S_IWRITE, f"Writable frozen input: {path}")
    require(expected is None or sha(data) == expected, f"Hash mismatch: {path}")
    return data


def save(path, data):
    with path.open("xb") as stream:
        stream.write(data)
    path.chmod(stat.S_IREAD)
    require(path.read_bytes() == data, f"Readback mismatch: {path}")
    return {"path": str(path), "sha256": sha(data)}


def skeleton(run, commit, ids):
    dispositions = "\n".join(f"- {i} - <disposition> - <reason-and-evidence>" for i in ids)
    return f"""# B116 confirmation \u2014 {run}

## Snapshot
Commit: {commit}
Model: <model-or-identity-unverified>

## Scope
Chain: <segments-read-and-re-views>
Fetches: <fetches>

## Dispositions
{dispositions}

## Verdicts
Correctness: <correctness-verdict>
Scoped coverage: <coverage-verdict>
Consistency and quiz safety: <consistency-verdict>
Comprehensibility: <comprehensibility-verdict>

## Confirmation
Verdict: <confirmation-verdict>
Basis: <basis>

## Findings
### F1: <short-title>
- Facet: <facet>
- Severity: <severity>
- Confidence: <confidence>
- Citations: <source>:<line-or-range>
- Evidence: <evidence>
- Required change: <required-change>

## Optional
### O1: <short-title>
- Facet: <facet>
- Severity: optional
- Confidence: <confidence>
- Citations: <source>:<line-or-range>
- Evidence: <evidence>
- Suggestion: <suggestion>

## Limits
- L1: <limit>
"""


def render_prompt(spec, packet, chain, prompt_path):
    run, commit, ids = spec["run"], packet["candidate"], spec["dispositionIds"]
    first = chain["segments"][0]["path"]
    open_initial = spec.get("basis") == "adjudicated-initial"
    held = spec.get("basis") == "held-confirmation"
    acceptance_label = "adjudicated" if open_initial or held else "accepted"
    followup = spec.get("basis", "initial") in ("confirmation", "held-confirmation")
    review_label = ("initial report with open claims" if open_initial else
                    "held previous confirmation" if held else
                    "adjudicated previous confirmation" if followup else "initial review")
    report_label = "previous confirmation" if followup else "initial"
    basis_explanation = ("The packet originalReport field names your prior confirmation report, "
                         "not a fresh initial review. Verify the author response to its findings, "
                         "optional points and limits against the actual new diff.\n" if followup else "")
    if open_initial:
        basis_explanation = (f"Your initial report remains {spec.get('priorVerdict', 'UNVERIFIED')} and held for open claims, not accepted "
                             "as a completed full-card review. This is a substantive same-reviewer follow-up "
                             "using new evidence and the actual revision. Reassess your prior D/E dispositions "
                             "and consequential limits as well as each numbered point; do not infer absence "
                             "of a sense from a short title or a compound-only argument. The prior report "
                             "and its hold are not rewritten or replaced by a claim of earlier acceptance.\n")
    if held:
        basis_explanation = (f"Your previous confirmation reported {spec['priorVerdict']}, but it is held for open "
                             f"claims {', '.join(spec['openClaimIds'])} and is not accepted. The packet "
                             "originalReport field names that prior confirmation report. The coordinator judged "
                             "the open claims consequential and recorded a gloss-overlap scan. This is a "
                             "substantive same-reviewer delta confirmation of the actual new revision. Verify the "
                             "author response to your numbered point, to each open claim and to each scan decision "
                             "against the actual diff and the supplied complete entries. A consequential comparison "
                             "that remains unverified cannot support CONFIRMED. The prior report and its hold are "
                             "not rewritten or replaced by a claim of earlier acceptance.\n")
    layout = skeleton(run, commit, ids)
    disposition_task = ("Give one disposition for each of\n  " + ", ".join(ids)
                        + "; limits need no disposition but must remain explicit." if ids else
                        "Your prior report has no numbered finding or optional\n"
                        "  item, so no disposition is due: leave the Dispositions section body empty, with no line\n"
                        "  at all (not even \"None.\"). Limits need no disposition but must remain explicit.")
    return f"""Perform ONE read-only confirmation of your own {acceptance_label} B116 {review_label}, under run {run}.
{basis_explanation}This is not a fresh initial review or an implementation task. Verify conclusions from sources read now.
The user's continuing task is completion of the N1 kanji cards. This assignment is only confirmation.

Reviewed freeze: {packet['freeze']}
Actual revised commit: {commit}
Scoped cards: {', '.join(spec['scope'])}
Your own {report_label} report: {packet['originalReport']}
Sole report destination: {packet['report']}
Coordinator: {COORDINATOR}

Read all {len(chain['segments'])} chain segments in order, starting with:
{first}
The NEXT SEGMENT line supplies the next exact absolute path. END OF CHAIN ends the only phase.
Every source part supplies its original path, SHA-256 and source-line/segment-line mapping.
The chain contains your own unchanged {report_label} report, the actual revised snapshot and diff,
author responses, fresh check outputs, and explicitly bounded source/comparison material.
Author responses and prior findings are hypotheses to verify, not evidence of their own correctness.
No other reviewer's report or held-run observations are supplied or authorized.

ACCESS RULES override wider packet wording, including advice to fetch sources or open packet files.
1. Exactly ONE tool call per response. Wait for its result. No parallel wrappers or batches.
2. The first call is the kickoff's forced full view of this prompt at {prompt_path}.
   Do not reread it. All further input reads are only view calls on reached chain segments,
   without view_range; forceReadLargeFiles true is allowed. Re-views of reached segments are allowed.
3. No other local reads, searches, directory listings, scripts, shell, browser, web_fetch, web search,
   agents, sessions, memory, SQL, builds, native/device commands or temporary files.
   No network fetches at all. If evidence is missing, disclose the limit rather than fetching.
4. After all segments, create the sole report with one apply_patch Add File (or one create call).
   Do not revise, append or rewrite it. Then one full view readback with forceReadLargeFiles true.
5. After readback, exactly one send_session_message with only session_id and message.
   session_id is {COORDINATOR}. The entire message is CONFIRMED, NEEDS FIX or UNVERIFIED,
   matching the Confirmation verdict; at most one trailing LF or CRLF is permitted.
   No other text or contact. After that message, stop; only one optional task_complete is permitted.
6. A breach invalidates this pass. Stop if you breach a rule; do not repair it with extra tools.
   Do not begin a further round or retry. Report unresolved consequential claims honestly.

TASKS
- Read your own full report and the scoped revised cards. {disposition_task}
- Check every changed line affecting the scoped cards, including changes not requested by you,
  against correctness, scoped coverage, consistency and quiz safety, and comprehensibility.
  Changes outside your scoped cards are context, not a claim of new full-card review.
- Verify direct exclusions using the actual counterpart articles and titles, including their
  ordinary secondary senses. Exclusions are symmetric direct pairs, not transitive.
  A different title, shared topic, compound status, or current option absence alone decides nothing.
  Keep semantic assessment and actual modeled runtime exposure separate.
- Verify the new meaning/reading options for the scoped cards and their supplied mechanics.
  Host models do not establish caller-built or multi-borrow pools, Kotlin execution,
  native/device acceptance or compatibility with the older installed APK.
- Check each author decline or dispute against actual evidence. Do not force agreement.
  Retain dictionary sense/spelling/register restrictions and no unsupported etymology.
- Report only new established defects, with no quota. Any material uncertainty stays explicit.

REPORT CONTRACT: confirm-structure-v1, checked mechanically before substantive adjudication.
Use the literal skeleton below without its code fence. Replace every placeholder.
Keep its eight level-2 headings exactly once, in order, and its field labels unchanged.
Within Confirmation, write exactly two nonblank physical lines: the Verdict field and the Basis field.
Keep all Basis reasoning on the Basis line. Do not add paragraphs, bullets or subheadings below it.
Use level-3 headings only for numbered Findings or Optional items. Indent continuation lines.
Each disposition is exactly RESOLVED, PARTIALLY RESOLVED, NOT RESOLVED, DECLINE ACCEPTED,
DECLINE REJECTED, DISPUTE ACCEPTED or DISPUTE REJECTED. Do not add or omit an ID.
Facet verdicts are CLEAN, NEEDS FIX or UNVERIFIED. Confirmation is CONFIRMED, NEEDS FIX or UNVERIFIED.
CONFIRMED requires accepting dispositions only (RESOLVED, DECLINE ACCEPTED, DISPUTE ACCEPTED),
no new finding, and no consequential unresolved claim. NEEDS FIX requires a new F item,
a NEEDS FIX facet or a non-accepting disposition. An established defect cannot be UNVERIFIED.
Every new F item's facet must be NEEDS FIX; every NEEDS FIX facet needs an F item or open disposition.
For Findings/Optional, replace the whole section body with "None." if there are no items.
Otherwise repeat its exact item layout, numbered from 1 without gaps, with all six fields.
Facet is exactly Correctness, Scoped coverage, Consistency and quiz safety, or Comprehensibility.
Finding severity is blocker, major or minor; optional severity is optional. Confidence is high, medium or low.
Every citation repeats the full SOURCE path and one line or contiguous range, separated by semicolons.
Use source line numbers, not segment numbers. No bracketed D/E labels or unsupported source paths.
Limits are "None." or consecutive "- L1: ...", "- L2: ..." lines. Disclose unread or unverified inputs.
Before the one write, internally check the complete draft against this layout and every required ID.

```text
{layout}```
"""


def self_test():
    checker = load("confirmation_checker", HERE / "check-confirm-structure.py")
    run, commit, ids = "N1-B116-TEST-CONFIRM-002", "12345678", ["F1", "O1"]
    text = skeleton(run, commit, ids)
    text = re.sub(r"## Findings\n.*?(?=## Optional)", "## Findings\nNone.\n\n", text, flags=re.S)
    text = re.sub(r"## Optional\n.*?(?=## Limits)", "## Optional\nNone.\n\n", text, flags=re.S)
    values = {"disposition": "RESOLVED", "confirmation-verdict": "CONFIRMED"}
    text = re.sub(r"<([^<>]+)>", lambda m: values.get(m[1], "CLEAN" if m[1].endswith("-verdict")
                                                    else "synthetic"), text)
    chain = {"sources": []}
    result = checker.check(text, run, commit, ids, chain, "CONFIRMED")
    require(result["status"] == "PASS", str(result))
    broken = text.replace("- O1 - RESOLVED - synthetic\n", "")
    require(checker.check(broken, run, commit, ids, chain, "CONFIRMED")["status"] == "FAIL",
            "Missing disposition was accepted")
    broken = text.replace("## Scope", "## Wrong")
    require(checker.check(broken, run, commit, ids, chain, "CONFIRMED")["status"] == "FAIL",
            "Wrong heading was accepted")
    print("3 confirmation skeleton checks passed")


def source_packet(spec, packet):
    binding = spec.get("sourcePacket")
    directory = Path(binding["path"]) if binding else ORIGINAL
    expected = binding["sha256"] if binding else ORIGINAL_SHA
    require(directory.is_absolute() and directory.parent == WORK / "review-packets",
            "Source packet must be an absolute review-packets child")
    require(str(directory) == packet["originalPacket"], "Source packet differs from packet originalPacket")
    sums = json.loads(frozen(directory / "SHA256SUMS.json", expected))
    return directory, expected, sums


def held_initial_bindings(accepted):
    bindings = {}
    for binding in accepted["mechanics"].values():
        frozen(Path(binding["path"]), binding["sha256"])
        bindings[binding["path"]] = binding["sha256"]
    execution = json.loads(frozen(Path(accepted["mechanics"]["execution"]["path"])))
    events = Path(accepted["mechanics"]["execution"]["path"]).parent / "events.jsonl"
    bindings[str(events)] = sha(frozen(events, execution["eventsSha256"]))
    if execution["status"] == "HOLD":
        binding = accepted["executionAdjudication"]
        proof = json.loads(frozen(Path(binding["path"]), binding["sha256"]))
        bindings[binding["path"]] = binding["sha256"]
        for field in ("phase1Audit", "phase1Adjudication"):
            item = proof[field]
            bindings[item["path"]] = sha(frozen(Path(item["path"]), item["sha256"]))
        prefix = Path(proof["phase1Audit"]["path"]).parent / "events.jsonl"
        bindings[str(prefix)] = sha(frozen(prefix, proof["phase1EventsSha256"]))
        for name, expected in (
            ("phase1_hold.py", "bcebabea31c01a60e5f56b0b54bf86edcb94cfaf239638eef94f5fd82301a00b"),
            ("review_chain.py", "2c02b506086b0698ccac49ead5ddfa87271b535f4deebbefdd9f28734bfb2109"),
        ):
            path = HERE.parent / name
            bindings[str(path)] = sha(frozen(path, expected))
    return bindings


def verify_known_execution_hold(accepted, execution):
    expected = "f1e119e80264e4b341a80e286e0e8bb9d7a8302b29d7fe1b7c4a806f5e2fab41"
    binding = accepted.get("executionAdjudication") or {}
    require(binding.get("sha256") == expected, "Unsupported execution HOLD adjudication")
    proof = json.loads(frozen(Path(binding["path"]), expected))
    require(proof["decision"] == "FINAL_EXECUTION_ACCEPTED_AFTER_PHASE1_ADJUDICATION",
            "Execution adjudication has another decision")
    require(accepted["run"] == proof["run"] == "N1-B116-CLAUDE-SUPERVISION-002"
            and accepted["session"] == proof["session"] == execution["session"]
            and accepted["candidate"] == "bb1d3856547ba5141c0e16212e5306b92648eaea"
            and accepted["scope"] == ["督"] and accepted["verdict"] == "NEEDS FIX"
            and accepted["report"]["sha256"] == "78bad2c1f43a69041f9b14a488c56271bf1e70f574a9fd3e6475cb402a985961",
            "Execution HOLD does not belong to this exact initial review")
    require(proof["finalAudit"] == accepted["mechanics"]["execution"], "Final audit binding differs")
    final_path = Path(proof["finalAudit"]["path"])
    require(json.loads(frozen(final_path, proof["finalAudit"]["sha256"])) == execution,
            "Final audit content differs")
    phase_path = Path(proof["phase1Audit"]["path"])
    phase_raw = frozen(phase_path, proof["phase1Audit"]["sha256"])
    phase = json.loads(phase_raw)
    require(phase["session"] == execution["session"], "Phase-1 reviewer differs")
    held_initial_bindings(accepted)
    gate = load("unchanged_phase1_hold", HERE.parent / "phase1_hold.py")
    reply = phase["messages"][0].encode("utf-8")
    refusal = gate.check(phase, phase_raw, phase_path, Path(proof["phase1Adjudication"]["path"]), reply)
    require(refusal is None, str(refusal))
    prefix = frozen(phase_path.parent / "events.jsonl", phase["eventsSha256"])
    events = frozen(final_path.parent / "events.jsonl", execution["eventsSha256"])
    require(events.startswith(prefix) and len(prefix) == proof["phase1EventsBytes"]
            and proof["phase1EventsSha256"] == phase["eventsSha256"]
            and proof["finalEventsSha256"] == execution["eventsSha256"]
            and proof["exactPrefixPreserved"] is True, "Phase-1 prefix was not preserved exactly")
    require(execution["status"] == "HOLD" and execution["final"] and not execution["breaches"]
            and not execution["recordIncomplete"] and execution["bootstrapVerified"]
            and execution["reviewerIdle"], "Final execution is otherwise incomplete")
    require(execution["unexpectedUserMessages"] == phase["unexpectedUserMessages"] == 5
            and execution["notes"] == phase["notes"] + [
                "Report on disk equals its single write after CRLF normalization"],
            "Execution has a new or unadjudicated HOLD reason")
    require(execution["coreRead"] == execution["coreRequired"] == 25
            and execution["extensionRead"] == execution["extensionRequired"] == 8
            and execution["writes"] == execution["readbacks"] == 1
            and execution["readbackVerified"] and execution["reportBinding"] == "line-endings-normalized"
            and execution["fetches"] == 0
            and execution["messages"] == [reply.decode("utf-8"), "NEEDS FIX"],
            "Final execution no longer matches the bounded adjudication")


def held_confirmation_gates(accepted):
    gates, bindings = {}, {}
    for field in ("finalAudit", "context", "structure"):
        binding = accepted[field]
        gates[field] = json.loads(frozen(Path(binding["path"]), binding["sha256"]))
        bindings[binding["path"]] = binding["sha256"]
    events = Path(accepted["finalAudit"]["path"]).parent / "events.jsonl"
    bindings[str(events)] = sha(frozen(events, gates["finalAudit"]["eventsSha256"]))
    scan = accepted.get("coordinatorScan") or {}
    for field in ("scan", "script"):
        if field in scan:
            item = scan[field]
            bindings[item["path"]] = sha(frozen(Path(item["path"]), item["sha256"]))
    return gates, bindings


def held_confirmation_bindings(accepted):
    return held_confirmation_gates(accepted)[1]


def verify_held_confirmation(spec, accepted):
    verdict = accepted.get("verdict")
    require(accepted.get("reportKind") == "confirmation" and verdict in ("CONFIRMED", "NEEDS FIX", "UNVERIFIED"),
            "Held basis is not a confirmation report with a recognized raw verdict")
    require(spec.get("priorVerdict") == verdict, "Spec relabels the prior verdict")
    require(accepted.get("status") == "HELD_OPEN_CLAIMS" and accepted.get("confirmationAccepted") is False
            and accepted.get("publicationAccepted") is False and accepted.get("reviewEvidenceAccepted") is True
            and accepted.get("openClaimIds") and spec.get("openClaimIds") == accepted["openClaimIds"],
            "Held confirmation is missing, accepted, or its open claims differ")
    require({claim["id"] for claim in accepted.get("openClaims", [])} == set(accepted["openClaimIds"]),
            "Open claims lack recorded reasons")
    raw = frozen(Path(accepted["report"]["path"]), accepted["report"]["sha256"]).decode("utf-8")
    raw = raw.replace("\r\n", "\n")
    require(re.findall(r"(?m)^## Confirmation\nVerdict: ([A-Z ]+)$", raw) == [verdict],
            "Raw confirmation verdict differs")
    limits = set(re.findall(r"(?m)^- (L\d+): ", raw))
    require(all(i in limits for i in accepted["openClaimIds"] if i.startswith("L")),
            "Open limit is absent from the raw report")
    gates, _ = held_confirmation_gates(accepted)
    execution = gates["finalAudit"]
    require(execution["session"] == spec["session"] == accepted["session"], "Execution belongs to another reviewer")
    require(execution["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and not execution["breaches"]
            and execution["fetches"] == 0 and execution["final"] and not execution["recordIncomplete"]
            and execution["bootstrapVerified"] and execution["reviewerIdle"]
            and execution["unexpectedUserMessages"] == 0 and execution["messages"] == [verdict]
            and execution["writes"] == execution["readbacks"] == 1 and execution["readbackVerified"]
            and execution["chainRead"] == execution["chainRequired"],
            "Prior execution breached the confirmation contract or is incomplete")
    require(execution["eventsSha256"] == accepted["eventsSha256"], "Adjudicated events differ")
    context = gates["context"]
    require(context["status"] == "PASS" and context["compactions"] == []
            and context["eventsSha256"] == execution["eventsSha256"]
            and context["events"] == str(Path(accepted["finalAudit"]["path"]).parent / "events.jsonl"),
            "Prior full-session context gate failed or covers another record")
    structure = gates["structure"]
    require(structure["status"] == "PASS" and structure["confirmation"] == verdict
            and structure["dispositions"] == accepted["acceptedDispositions"],
            "Prior structure gate failed or dispositions were relabeled")


def verify_prior_basis(spec, packet, accepted):
    basis = spec.get("basis", "initial")
    require(basis in ("initial", "confirmation", "adjudicated-initial", "held-confirmation"),
            "Unsupported prior-report basis")
    require(accepted["candidate"] == packet["freeze"], "Prior report covers another freeze")
    if basis == "initial":
        require(accepted.get("reviewAccepted") is True, "Initial review is not accepted")
        return
    require(accepted["session"] == spec["session"], "Follow-up is not the original reviewer")
    scope = accepted["scope"]
    scope = [scope] if isinstance(scope, str) else scope
    require(set(scope) == set(spec["scope"]), "Follow-up changes the adjudicated scope")
    if basis == "adjudicated-initial":
        verdict = accepted.get("verdict")
        require(accepted.get("reportKind") == "initial" and verdict in ("UNVERIFIED", "NEEDS FIX", "CLEAN"),
                "Open-claim basis is not an initial report with a recognized raw verdict")
        require(spec.get("priorVerdict", "UNVERIFIED") == verdict, "Spec relabels the prior verdict")
        raw = frozen(Path(accepted["report"]["path"]), accepted["report"]["sha256"]).decode("utf-8")
        require(re.findall(r"(?m)^## Overall verdict\nVerdict: ([A-Z ]+)$",
                           raw.replace("\r\n", "\n")) == [verdict], "Raw report verdict differs")
        require(accepted.get("status") == "HELD_OPEN_CLAIMS" and accepted.get("reviewAccepted") is False
                and accepted.get("reviewEvidenceAccepted") is True and accepted.get("openClaimIds"),
                "Open-claim hold is missing or misrepresented as accepted")
        gates = {}
        for gate in ("execution", "context", "structure"):
            binding = accepted["mechanics"][gate]
            gates[gate] = json.loads(frozen(Path(binding["path"]), binding["sha256"]))
        execution = gates["execution"]
        require(execution["session"] == spec["session"], "Execution belongs to another reviewer")
        if execution["status"] == "HOLD":
            verify_known_execution_hold(accepted, execution)
        else:
            require(execution["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK",
                    "Prior execution gate failed")
        require(not execution["breaches"] and execution["fetches"] == 0
                and execution["final"] and not execution["recordIncomplete"]
                and execution["bootstrapVerified"] and execution["reviewerIdle"],
                "Prior execution breached the review contract or is incomplete")
        require(gates["context"]["status"] == "PASS" and gates["context"]["compactions"] == []
                and gates["context"]["eventsSha256"] == execution["eventsSha256"]
                and gates["context"]["events"] == str(
                    Path(accepted["mechanics"]["execution"]["path"]).parent / "events.jsonl"),
                "Prior full-session context gate failed or covers another record")
        require(gates["structure"]["status"] == "PASS" and gates["structure"]["overall"] == verdict,
                "Prior structure gate failed or raw verdict was relabeled")
        held_initial_bindings(accepted)
        return
    if basis == "held-confirmation":
        verify_held_confirmation(spec, accepted)
        return
    confirmed = accepted.get("confirmationAccepted") is True
    evidence = accepted.get("reviewEvidenceAccepted") is True and accepted.get("verdict") == "NEEDS FIX"
    require(confirmed or evidence, "Previous confirmation has no accepted evidence")
    if not confirmed:
        raw = frozen(Path(accepted["report"]["path"]), accepted["report"]["sha256"])
        findings = set(re.findall(r"(?m)^### (F\d+):", raw.decode("utf-8")))
        require(findings == set(accepted["acceptedNewFindings"]),
                "Follow-up contains unaccepted findings")


def main(spec_path):
    spec = json.loads(frozen(spec_path))
    run = spec["run"]
    require(re.fullmatch(r"N1-B116-[A-Z0-9-]+-CONFIRM-\d{3}", run), "Invalid run")
    require(spec["family"] in ("claude", "gpt"), "Invalid family")
    for path, expected in TOOL_PINS.items():
        frozen(path, expected)
    packet_path = Path(spec["packet"]["path"])
    require(packet_path.parent == WORK / "review-packets", "Packet outside review-packets")
    manifest_path = packet_path / "packet-manifest.json"
    packet = json.loads(frozen(manifest_path, spec["packet"]["sha256"]))
    original_dir, original_sha, original_sums = source_packet(spec, packet)
    acceptance_path = Path(spec["acceptance"]["path"])
    accepted = json.loads(frozen(acceptance_path, spec["acceptance"]["sha256"]))
    verify_prior_basis(spec, packet, accepted)
    initial_path = Path(packet["originalReport"])
    require(str(initial_path) == accepted["report"]["path"], "Report is not this reviewer's accepted report")
    initial = frozen(initial_path, accepted["report"]["sha256"])
    ids = re.findall(r"(?m)^### ([FO]\d+):", initial.decode("utf-8"))
    require(ids == spec["dispositionIds"] and len(ids) == len(set(ids)), "Disposition IDs differ")
    require(spec["scope"] and set(spec["scope"]) <= set(packet["members"]), "Invalid card scope")
    if "card" in accepted:
        require(spec["scope"] == [accepted["card"]], "Confirmation expands the accepted card scope")
    report = Path(packet["report"])
    require(report.parent == WORK / "reports-116" and not report.exists(), "Report destination is not absent")
    git = lambda *args: subprocess.check_output(["git", "-c", "core.quotepath=false", "-C", str(REPO), *args])
    require(git("rev-parse", "HEAD").decode().strip() == packet["candidate"], "HEAD differs")
    require(not git("status", "--porcelain").strip(), "Dirty repository")
    subprocess.run(["git", "-C", str(REPO), "merge-base", "--is-ancestor",
                    packet["freeze"], packet["candidate"]], check=True)
    patch = git("diff", "--no-color", packet["freeze"], packet["candidate"], "--",
                ".", ":(exclude)manifest.json")
    require(patch == frozen(packet_path / "diffs" / "fix.patch"), "Packet diff is not the actual revision")

    chain_path, prompt_path = HERE / f"{run}-chain.json", HERE / f"{run}-prompt.txt"
    kickoff_path, config_path = HERE / f"{run}-kickoff.txt", HERE / f"{run}-config.json"
    preflight_path = HERE / f"{run}-preflight.json"
    directory = WORK / "review-chains" / run.lower()
    require(not any(p.exists() for p in (chain_path, prompt_path, kickoff_path, config_path,
                                         preflight_path, directory)), "Exclusive output exists")
    guard_module = load("confirmation_guard", list(TOOL_PINS)[-1])
    require(guard_module.available_ram() > 2 * 1024**3, "Requires more than 2048 MiB free RAM")
    guard = guard_module.RamGuard()
    guard.start()
    bindings = {str(spec_path): sha(frozen(spec_path)), str(acceptance_path): sha(frozen(acceptance_path)),
                str(manifest_path): sha(frozen(manifest_path)), str(initial_path): sha(initial),
                str(original_dir / "SHA256SUMS.json"): original_sha}
    if spec.get("basis") == "adjudicated-initial":
        bindings.update(held_initial_bindings(accepted))
    if spec.get("basis") == "held-confirmation":
        bindings.update(held_confirmation_bindings(accepted))
    try:
        report_prefix = ("prior-confirmation" if spec.get("basis") in ("confirmation", "held-confirmation")
                         else "initial-report")
        sources = [(f"{report_prefix}/{initial_path.name}", initial, None)]
        actual = {p.relative_to(packet_path).as_posix() for p in packet_path.rglob("*") if p.is_file()}
        require(actual == set(packet["files"]) | {"packet-manifest.json"}, "Packet file set differs")
        for relative, item in sorted(packet["files"].items()):
            guard.check()
            path = packet_path.joinpath(*relative.split("/"))
            require(path.resolve().is_relative_to(packet_path.resolve()), "Packet path traversal")
            data = frozen(path, item["sha256"])
            if relative.startswith("snapshot/"):
                actual_path = REPO.joinpath(*relative.split("/")[1:])
                require(data == actual_path.read_bytes(), f"Snapshot differs from revised checkout: {relative}")
            bindings[str(path)] = sha(data)
            sources.append((f"confirm-packet/{relative}", data, None))
        for relative in spec["originalSources"]:
            require(relative in original_sums, f"Unbound original source: {relative}")
            path = original_dir.joinpath(*relative.split("/"))
            data = frozen(path, original_sums[relative])
            bindings[str(path)] = sha(data)
            sources.append((f"original-packet/{relative}", data, None))
        require(len(sources) == len({s[0] for s in sources}), "Duplicate source")
        chain = build_chain(sources, directory, chain_path, guard, f"B116 {run} confirmation")
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM guard breached")
    prompt_data = render_prompt(spec, packet, chain, prompt_path).encode("utf-8")
    kickoff_data = (f"Read {prompt_path} using one view call with forceReadLargeFiles: true and no view_range, "
                    "then follow its instructions. No other tool call may precede that read.").encode("ascii")
    for path, data in ((prompt_path, prompt_data), (kickoff_path, kickoff_data)):
        save(path, data)
        bindings[str(path)] = sha(data)
    bindings[str(chain_path)] = sha(frozen(chain_path))
    bindings.update({str(p): expected for p, expected in TOOL_PINS.items()})
    for path in (Path(__file__), HERE.parent / "review_chain.py"):
        bindings[str(path)] = sha(frozen(path))
    config = {
        "run": run, "prompt": str(prompt_path), "kickoff": str(kickoff_path), "report": str(report),
        "coordinator": COORDINATOR, "expectedFamily": spec["family"], "chainManifest": str(chain_path),
        "completionContract": "entire-message-enum-v1", "reportStructureContract": "confirm-structure-v1",
        "dispositionIds": ids, "maxWebFetches": 0,
        "additionalAcceptanceChecks": "Require audit fetches == 0 and a passing full-session context/zero-compaction check. "
                                      "The inherited auditor alone permits up to three fetches; it does not enforce this zero cap.",
        "files": [{"path": path, "sha256": digest} for path, digest in bindings.items()],
    }
    config_binding = save(config_path, (json.dumps(config, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    preflight = {
        "run": run, "session": spec["session"], "candidate": packet["candidate"], "scope": spec["scope"],
        "config": config_binding, "kickoff": {"path": str(kickoff_path), "sha256": sha(kickoff_data)},
        "chain": {"path": str(chain_path), "sha256": sha(frozen(chain_path)), "segments": len(chain["segments"])},
        "sources": len(sources), "memory": memory,
        "launchPrecondition": "Fresh serial/resource admission and frozen pre-delivery event offset/prefix hash.",
        "acceptanceLimit": "Prepared only. No reviewer has received this prompt; no confirmation is inferred.",
    }
    save(preflight_path, (json.dumps(preflight, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(preflight, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.spec:
        main(args.spec)
    else:
        parser.error("Provide a frozen spec or --self-test")
