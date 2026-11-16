import re
from pathlib import Path
from common import COORDINATOR, require, load_module as load
HERE = Path(__file__).resolve().parent

def skeleton(run, commit, ids):
    dispositions = "\n".join(f"- {i} - <disposition> - <reason-and-evidence>" for i in ids)
    return f"""# B129 confirmation \u2014 {run}

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
    return f"""Perform ONE read-only confirmation of your own {acceptance_label} B129 {review_label}, under run {run}.
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
    run, commit, ids = "N1-B129-TEST-CONFIRM-002", "12345678", ["F1", "O1"]
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
