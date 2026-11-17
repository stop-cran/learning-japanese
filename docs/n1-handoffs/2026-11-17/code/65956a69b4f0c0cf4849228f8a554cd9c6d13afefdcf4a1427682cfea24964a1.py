"""Prospective, source-bound B134 follow-up; old refusals/held results are never erased.

V5 transport/audit gates are retained. The only admitted new user turn is the exact
App-rendered forwarding of the newly received authorization plus frozen kickoff.
Claude reconsiders its own completely audited retained evidence; GPT reads every
source of its original 17-source dossier. Neither is a fresh initial review.
"""
import copy
import datetime as dt
import inspect
import json
import re
import sys
from pathlib import Path

from common import freeze_json, frozen, json_bytes, load_module, require, sha, start_guard, write_frozen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "revision-confirmation-runtime-repair-001" / "b134_revision_confirmation_v5.py"
PARENT_SHA = "ad100a8e18fdfa994d417318e58a3112bd61a135f766bc3932cf5a44901f1fe6"
AUTH = {"path": str(ROOT / "authorization-continuation-prep-001" / "authorization-event.jsonl"),
        "sha256": "4d69ed0c6e0476b38bba3e22b31b959178d417d8b1ecfaa7d29221660da167cb"}
SOURCE = {"id": "453fc328-b19a-4cc9-95a7-70f521c52b69", "revision": 3}
AUTH_TEXT = "Authorize bounded B134 follow-up reviews, superseding the earlier one-pass-only restriction"
HOLD = {"path": str(ROOT / "revision-confirmation-scope-hold-001" / "hold.json"),
        "sha256": "7818401b23e1c29522736cea57ab1d5118f9b69f6e3fe995a08d87c01fbc5683"}
CLAUDE_INDEX = {"path": str(ROOT / "revision-confirmation-runtime-repair-001" / "claude-evidence.json"),
                "sha256": "36b95162b8439030dee6e0ff4f1e297152aa5b09d13bd4d885a1f8868aa393be"}
PRIOR_PREFLIGHT = {
    "claude": {"path": str(ROOT / "revision-confirmation-claude-003" / "preflight.json"),
               "sha256": "21449899aa661939916b0c4d9edaf9617b6f488835b58244f6467a3153cd2887"},
    "gpt": {"path": str(ROOT / "revision-confirmation-gpt-002" / "preflight.json"),
            "sha256": "b59401edd077e186d937a57c07a0e16fcfea6fdbb4f76eabb47490ffe0ef227c"},
}
frozen(PARENT, PARENT_SHA)
parent = load_module("b134_authorized_pinned_v5", PARENT)
legacy = parent.legacy
ORIGINAL_MODULES = legacy.modules
ORIGINAL_PREFLIGHT = legacy.preflight
ORIGINAL_AUDIT = legacy.audit_snapshot
ORIGINAL_PREVIOUS_CLAUDE = legacy.previous_claude
check_native_create = parent.check_native_create
NORMALIZATION_NOTE = parent.parent.NORMALIZATION_NOTE
legacy.PINS["authorizedParentV5"] = (PARENT, PARENT_SHA)
legacy.PINS["actualAuthorization"] = (Path(AUTH["path"]), AUTH["sha256"])
legacy.PINS["scopeHold"] = (Path(HOLD["path"]), HOLD["sha256"])
legacy.PINS["heldClaudeEvidence"] = (Path(CLAUDE_INDEX["path"]), CLAUDE_INDEX["sha256"])


def block(text, tag):
    require(text.count("<" + tag + ">") == text.count("</" + tag + ">") == 1,
            "Missing/duplicate forwarded authorization block: " + tag)
    return json.loads(text.split("<" + tag + ">", 1)[1].split("</" + tag + ">", 1)[0])


def forwarded(data, kickoff):
    require(data.get("source") == "agent-" + legacy.COORDINATOR,
            "Forwarded authorization is not from this coordinator")
    text = data.get("transformedContent", "")
    require(block(text, "forwarded_user_message_source_json") == SOURCE
            and block(text, "forwarded_user_message_json") == AUTH_TEXT
            and block(text, "coordinator_instructions_json") == kickoff
            and data.get("content") == (
                "Forwarded user message:\n\n> " + AUTH_TEXT + "\n\nCoordinator instructions:\n\n" + kickoff),
            "Missing/wrong live user authorization or changed frozen coordinator instructions")
    return True


def authority():
    rows = legacy.parse_events(legacy.read(AUTH))
    require(len(rows) == 1 and rows[0]["id"] == "69e8afe9-c16a-4322-843f-ade61ab30a8e"
            and rows[0]["type"] == "user.message", "Not the actual received authorization event")
    row = rows[0]
    forwarded(row["data"], block(row["data"]["transformedContent"], "coordinator_instructions_json"))
    return row


def authorized_content(data, kickoff):
    return forwarded(data, kickoff)


def authorization_message(row, kickoff):
    authority()
    require(row["data"].get("agentMode") == "interactive", "Authorization delivered in wrong actual mode")
    require(dt.datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
            > dt.datetime.fromisoformat(authority()["timestamp"].replace("Z", "+00:00")),
            "Authorization cannot be applied retroactively")
    return forwarded(row["data"], kickoff)


def modules():
    auditor, structure, capacity, builder = ORIGINAL_MODULES()
    source = inspect.getsource(auditor.audit)
    before = "if content != kickoff:"
    after = "if not authorized_content(data, kickoff):"
    require(source.count(before) == 1, "Pinned underlying kickoff parser changed")
    auditor.authorized_content = authorized_content
    exec(compile(source.replace(before, after, 1), str(auditor.__file__), "exec"), auditor.__dict__)
    return auditor, structure, capacity, builder


def old_preflight(family):
    item = PRIOR_PREFLIGHT[family]
    legacy.read(item)
    return ORIGINAL_PREFLIGHT(Path(item["path"]))


def retained(family):
    """Verify every old semantic byte, including the refusal; never trim/rebrand it."""
    hold = legacy.value(HOLD)
    require(hold["status"] == "HOLD_REVIEWER_SCOPE_AUTHORIZATION_REQUIRED"
            and hold["originalObligationCount"] == 41 and hold["deliveryCredit"] == 0,
            "Historical scope hold changed")
    record, config, spec, chain = old_preflight(family)
    if family == "claude":
        index = legacy.value(CLAUDE_INDEX)
        accepted = legacy.value(hold["retainedClaudeAcceptance"])
        require(hold["retainedClaudeAcceptance"] == index["acceptance"]
                and accepted["producer"] == {"path": str(PARENT), "sha256": PARENT_SHA}
                and index["dispositions"] == {key: "DECLINE ACCEPTED" for key in ("F1", "O1", "O2", "O3")},
                "Held Claude identity/dispositions changed")
        previous = legacy.value(index["final"])
        audit = legacy.value(previous["audit"])
        raw_path = Path(previous["audit"]["path"]).parent / "events.jsonl"
        raw = frozen(raw_path, audit["eventsSha256"])
        legacy.modules = ORIGINAL_MODULES
        try:
            repeated = ORIGINAL_AUDIT(raw, record, config, chain, legacy.value(previous["admission"]))
        finally:
            legacy.modules = modules
        require(repeated[0]["chainRead"] == repeated[0]["chainRequired"] == len(chain["segments"])
                and repeated[2] == legacy.value(previous["structure"])
                and repeated[1] == legacy.value(previous["context"]),
                "Held Claude returned-byte audit no longer reproduces")
        for failed in index["failedAttempts"]:
            legacy.read(failed["rawEvents"])
            legacy.read(failed["auditMemory"])
        root = {"path": str(raw_path), "sha256": sha(raw)}
        own = {"index": index, "audit": repeated[0], "final": previous}
    else:
        root = hold["gptRawEvents"]
        raw = legacy.read(root)
        admission = legacy.value(hold["gptAdmission"])
        prefix = legacy.read(admission["prefix"])
        suffix_raw = legacy.read(hold["gptRefusalSuffix"])
        require(raw == prefix + suffix_raw and admission["preflight"] == PRIOR_PREFLIGHT["gpt"],
                "GPT refusal no longer extends its exact admitted prefix")
        rows = legacy.parse_events(suffix_raw)
        users = [r for r in rows if r["type"] == "user.message"]
        assistants = [r for r in rows if r["type"] == "assistant.message"]
        require(len(users) == len(assistants) == 1
                and users[0]["data"]["source"] == "agent-" + legacy.COORDINATOR
                and users[0]["data"]["content"] == admission["kickoff"]
                and assistants[0]["data"]["content"] == hold["gptResponse"]
                and not assistants[0]["data"].get("toolRequests")
                and not any(r["type"].startswith("tool.") for r in rows)
                and not Path(config["report"]).exists(), "Not the preserved no-read/no-report refusal")
        own = {}
    return root, raw, own


def verify_retained_prefix(record, raw):
    root, previous_raw, _ = retained(record["family"])
    spec = legacy.value(record["spec"])
    require(spec["continuation"]["priorEvents"] == root and raw.startswith(previous_raw),
            "Old held/refused semantic stream changed or was omitted")
    tail_raw = raw[len(previous_raw):]
    tail = legacy.parse_events(tail_raw) if tail_raw else []
    require(all(row["type"] in {
        "assistant.turn_end", "session.usage_checkpoint", "session.usage_record",
        "session.permissions_changed", "session.info", "session.warning", "hook.start", "hook.end"
    } for row in tail), "New/unadmitted semantic tail after retained hold/refusal")


def preflight(path):
    record, config, spec, chain = ORIGINAL_PREFLIGHT(path)
    family = record["family"]
    expected_kind = "same-claude-reconsideration" if family == "claude" else "same-gpt-full-dossier"
    require(spec["authorization"] == AUTH and config["authorization"] == AUTH
            and spec["run"] == "N1-B134-" + family.upper() + "-REVISION-002"
            and spec["continuation"]["kind"] == expected_kind
            and spec["continuation"]["priorPreflight"] == PRIOR_PREFLIGHT[family]
            and spec["continuation"]["originalObligationCount"] == 41
            and spec["continuation"]["oldEvidenceRemainsHeld"] is True
            and spec["continuation"]["authorizationIsProspective"] is True,
            "Missing/wrong prospective continuation contract")
    authority()
    root, _, _ = retained(family)
    require(spec["continuation"]["priorEvents"] == root, "Wrong retained semantic root")
    old_record, _, old_spec, old_chain = old_preflight(family)
    require(spec["obligations"] == old_spec["obligations"], "Own obligation inventory was changed")
    if family == "gpt":
        require(len(chain["sources"]) == len(old_chain["sources"]) == 17
                and legacy.reconstruct(chain) == legacy.reconstruct(old_chain),
                "GPT must receive every complete original source, byte for byte")
    else:
        _, _, own = retained(family)
        expected = sources_for(spec, old_record, old_chain, root, own)
        require(legacy.reconstruct(chain) == {name: raw for name, raw, _ in expected},
                "Claude reconsideration must retain every complete own evidence source and binding")
    return record, config, spec, chain


def sources_for(spec, old_record, old_chain, root, own):
    if spec["family"] == "gpt":
        return [(name, data, None) for name, data in legacy.reconstruct(old_chain).items()]
    index = own["index"]
    original = legacy.reconstruct(old_chain)
    binding = {
        "status": "PREVIOUS_COMPLETELY_READ_EVIDENCE_RETAINED_NOT_RETROACTIVELY_AUTHORIZED",
        "priorPreflight": PRIOR_PREFLIGHT["claude"], "priorEvents": root,
        "completeChain": old_record["chain"], "completeSources": old_chain["sources"],
        "segments": old_chain["segments"], "chainRead": own["audit"]["chainRead"],
        "chainRequired": own["audit"]["chainRequired"], "holdRemains": True,
        "originalObligationCount": 41,
        "limits": "Reconsider only your own retained evidence under the new prospective authorization. "
                  "Earlier raw NEEDS FIX and held CONFIRMED remain unchanged; F1 stays DECLINE ACCEPTED. "
                  "No source was truncated. Complete original returned bytes remain audit-bound; "
                  "zero compaction and exact retained prefix are required at admission and final audit."
    }
    return [
        ("own-prior/report.md", original["own-prior/report.md"], None),
        ("own-prior/adjudication.json", original["own-prior/adjudication.json"], None),
        ("own-prior/obligations.json", json_bytes(spec["obligations"]), None),
        ("own-revision/report.md", legacy.read(index["report"]), None),
        ("own-revision/adjudication.json", legacy.read(index["adjudication"]), None),
        ("own-revision/read-audit.json", legacy.read(own["final"]["audit"]), None),
        ("proof/retained-dossier.json", json_bytes(binding), None),
    ]


def prepare(spec_path, out):
    spec = json.loads(frozen(spec_path))
    family = legacy.identity(spec)
    require(spec["authorization"] == AUTH and spec["continuation"]["priorPreflight"] == PRIOR_PREFLIGHT[family]
            and spec["run"] == "N1-B134-" + family.upper() + "-REVISION-002",
            "Missing/wrong authorization or prior preflight")
    authority()
    target = legacy.output(out)
    guard, _ = start_guard("B134 prospective authorization preparation")
    try:
        legacy.prior_evidence(spec)
        legacy.actual_merge(spec, guard)
        old_record, old_config, old_spec, old_chain = old_preflight(family)
        root, raw, own = retained(family)
        require(spec["obligations"] == old_spec["obligations"], "Own obligations changed")
        spec["continuation"]["priorEvents"] = root
        saved_spec = freeze_json(target / "request.json", spec)
        sources = sources_for(spec, old_record, old_chain, root, own)
        _, _, _, builder = modules()
        chain = builder.build_chain(sources, target / "segments", target / "chain.json", guard, spec["run"])
        require(legacy.reconstruct(chain) == {n: b for n, b, _ in sources}, "Complete source reconstruction failed")
        report = target / "report" / "review.md"
        report.parent.mkdir()
        prompt = legacy.render_prompt(spec, chain, report, old_record["priorRawVerdict"])
        extra = (
            "\n## Prospective scope authorization\n"
            + AUTH_TEXT + "\nThis new authorization applies prospectively only. Earlier scope refusal/hold "
            "and all 41 original obligations remain preserved. Never upgrade the raw old verdict.\n"
            + ("This is same-Claude reconsideration of your own previously completely read and audited "
               "retained confirmation evidence, NOT a new initial review or a claim that the earlier "
               "pass was authorized. Read all new evidence-chain segments. Reconsider F1/O1/O2/O3 "
               "literally; the retained F1 disposition is DECLINE ACCEPTED, not RESOLVED. If retained "
               "source context is insufficient, report UNVERIFIED; do not recover it through extra reads.\n"
               if family == "claude" else
               "Your earlier no-read refusal remains unchanged and is not a review verdict. Under this "
               "new authorization read the entire existing 17-source dossier through this new chain.\n")
        )
        prompt_ref = write_frozen(target / "prompt.txt", (prompt + extra).encode("utf-8"))
        kickoff = (f"Read {prompt_ref['path']} using one view call with forceReadLargeFiles: true "
                   "and no view_range, then follow it exactly. Prospective authorized bounded follow-up only; "
                   "earlier refusal/held evidence remains unchanged.")
        write_frozen(target / "kickoff.txt", kickoff.encode("utf-8"))
        config = copy.deepcopy(old_config)
        config.update(run=spec["run"], prompt=prompt_ref["path"], kickoff=str(target / "kickoff.txt"),
                      report=str(report), chainManifest=str(target / "chain.json"), authorization=AUTH)
        files = [*old_config["files"], saved_spec, AUTH, HOLD, CLAUDE_INDEX, root,
                 legacy.ref(__file__), legacy.ref(PARENT), legacy.ref(target / "prompt.txt"),
                 legacy.ref(target / "kickoff.txt"), legacy.ref(target / "chain.json")]
        config["files"] = list({r["path"]: {k: r[k] for k in ("path", "sha256")} for r in files}.values())
        config_ref = freeze_json(target / "config.json", config)
        record = copy.deepcopy(old_record)
        record.update(run=spec["run"], spec={k: saved_spec[k] for k in ("path", "sha256")},
                      config={k: config_ref[k] for k in ("path", "sha256")},
                      chain=legacy.ref(target / "chain.json"), authorization=AUTH,
                      dossierBound=len((prompt + extra).encode("utf-8")) + sum(r["bytes"] for r in chain["segments"]),
                      continuation=spec["continuation"])
        freeze_json(target / "preflight.json", record)
        # Forecast uses the latest actual retained session, not a stale startup number.
        live = (Path.home() / ".copilot" / "session-state" / record["session"] / "events.jsonl").read_bytes()
        verify_retained_prefix(record, live)
        telemetry = legacy.context(legacy.parse_events(live), family, record["session"], record["dossierBound"])
        freeze_json(target / "readiness.json", {"status": "PREPARED_NOT_ADMITTED", "context": telemetry,
                                              "sources": len(chain["sources"]), "segments": len(chain["segments"]),
                                              "authorization": AUTH, "heldEvidenceStillHeld": True})
    finally:
        freeze_json(target / "preparation-memory.json", guard.finish())


def previous_claude(item, candidate, scope):
    ORIGINAL_PREVIOUS_CLAUDE(item, candidate, scope)
    accepted = legacy.value(item)
    require(accepted["authorization"] == AUTH and accepted["authorizationProspective"] is True
            and accepted["continuation"]["kind"] == "same-claude-reconsideration",
            "HELD/pre-authorization Claude result cannot admit GPT")


def derive(function, changes):
    source = inspect.getsource(function)
    for before, after in changes:
        require(source.count(before) == 1, "Pinned lifecycle adaptation anchor changed: " + before[:80])
        changed = source.replace(before, after, 1)
        require(changed.replace(after, before, 1) == source, "Lifecycle adaptation is not reversible")
        source = changed
    exec(compile(source, str(__file__), "exec"), legacy.__dict__)


# Keep the full V5 native/desktop transport and audit; change only the exact
# authorized kickoff predicate, never the raw events or their content.
source = inspect.getsource(parent.parent.audit_snapshot)
anchor = "    prefix_raw = legacy.read(admission[\"prefix\"])\n"
require(source.count(anchor) == 1, "Pinned V4 prefix predicate changed")
source = source.replace(anchor, '    verify_retained_prefix(record, legacy.read(admission["prefix"]))\n' + anchor, 1)
before = ('len(users) == 1 and users[0]["data"].get("source") == "agent-" + legacy.COORDINATOR\n'
          '            and users[0]["data"].get("content") == admission["kickoff"]')
require(source.count(before) == 1, "Pinned V4 kickoff predicate changed")
exec(compile(source.replace(before, 'len(users) == 1 and authorization_message(users[0], admission["kickoff"])', 1),
             str(__file__), "exec"), globals())
legacy.modules = modules
legacy.preflight = preflight
legacy.prepare = prepare
legacy.previous_claude = previous_claude
legacy.verify_retained_prefix = verify_retained_prefix
legacy.authorization_message = authorization_message
legacy.audit_snapshot = audit_snapshot
legacy.__file__ = __file__

admit_source = inspect.getsource(legacy.admit)
start = '        prior = value(record["priorFinal"])\n'
end = '        telemetry = context(events, record["family"], record["session"], record["dossierBound"])\n'
require(admit_source.count(start) == admit_source.count(end) == 1, "Pinned admission source changed")
removed = admit_source.split(start, 1)[1].split(end, 1)[0]
admit_source = admit_source.replace(start + removed, '        verify_retained_prefix(record, raw)\n', 1)
exec(compile(admit_source, str(__file__), "exec"), legacy.__dict__)

for function in (legacy.final, legacy.accept):
    source = inspect.getsource(function)
    anchor = '"priorRawVerdict": record["priorRawVerdict"],'
    require(anchor in source, "Pinned final/acceptance metadata anchor changed")
    source = source.replace(anchor, anchor + ' "authorization": spec["authorization"], '
                            '"authorizationProspective": True, "continuation": spec["continuation"],')
    if function.__name__ == "accept":
        anchor = '    confirmed = decision["verdict"] == "CONFIRMED"\n'
        extra = ('    require(decision.get("authorization") == spec["authorization"]\n'
                 '            and decision.get("heldEvidenceTreatment") == "retained-not-retroactively-authorized",\n'
                 '            "Separate prospective scope adjudication required")\n')
        require(source.count(anchor) == 1, "Pinned acceptance decision anchor changed")
        source = source.replace(anchor, extra + anchor, 1)
    exec(compile(source, str(__file__), "exec"), legacy.__dict__)


def main(argv=None):
    return legacy.main(argv)


if __name__ == "__main__":
    sys.exit(main())
