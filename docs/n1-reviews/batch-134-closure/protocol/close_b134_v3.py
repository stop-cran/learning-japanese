"""Assemble the cc374 B134 closure with two authorized same-reviewer confirmations.

Usage: close_b134_v3.py dry|real REQUEST_JSON OUTPUT
REQUEST_JSON is the closure134 request plus a "revision" block. The pinned v1 helpers
(through the pinned v2 external-input reader) collect the original, held and FRESH-003
history unchanged. Each confirmation is re-verified from its pinned acceptance: record
identities, literal tokens, the complete audited chain read, the exact admitted event
prefix, exactly one App-forwarded delivery of the actual user authorization after that
authorization and inside its admission window, an interactive delivered turn, receipts
and statically pinned producer ancestry. Raw events, audits, receipts and rosters remain
local. Confirmations add no publication or delivery credit.
"""
import copy
import datetime as dt
import json
import sys
from pathlib import Path

from b132_closure_records import UUID
from close_b132 import texts
from common import COORDINATOR, WS, freeze_json, frozen, json_bytes, load_module, require, sha, start_guard, write_frozen

TOOLS = Path(__file__).resolve().parent
PINS = {
    "close_b134_v2.py": "03a2eb2e767935dfe92d25cbc12136e0e41857a5560cf120db593dbf0c019744",
    "b134_revision_history.py": "3fb4c7f222d055794303223a0abb1d43afea6af84ab5b6d95bb836aa7e728eac",
    "b134_revision_progress.py": "545e499a57a2b611c6e97073a55b30be33738b1a6ab2bc34e82327a8e9e770cb",
}
for _name, _digest in PINS.items():
    frozen(TOOLS / _name, _digest)
import close_b134_v2 as v2

require(Path(v2.__file__).resolve() == TOOLS / "close_b134_v2.py", "Unexpected v2 module")
original = v2.original
history = load_module("b134_v3_pinned_revision_history", TOOLS / "b134_revision_history.py")
progress = load_module("b134_v3_pinned_revision_progress", TOOLS / "b134_revision_progress.py")

ROOT, HERE, REPO = original.ROOT, original.HERE, original.REPO
PRIOR, REVISED, ROLE = history.PRIOR, history.REVISED, history.ROLE
REAL_REPORT = HERE / "closure-v3-real-report-001.json"
FAMILIES = ("claude", "gpt")
RUNS = {family: "N1-B134-" + family.upper() + "-REVISION-002" for family in FAMILIES}
FRESH = {family: "N1-B134-" + family.upper() + "-FRESH-003" for family in FAMILIES}
ACCEPTANCES = {
    "claude": "86c82a358a68a05eae50842d45f98e5568bd013cbb1a758438bd4d042cc0cea8",
    "gpt": "c1fc8643366a1f7dd9c3f2dba849f8532e64cafc73a8533c4955f1521ccb739c",
}
CONTINUATIONS = {"claude": "same-claude-reconsideration", "gpt": "same-gpt-full-dossier"}
AUTH = {"path": str(ROOT / "authorization-continuation-prep-001" / "authorization-event.jsonl"),
        "sha256": "4d69ed0c6e0476b38bba3e22b31b959178d417d8b1ecfaa7d29221660da167cb"}
AUTH_EVENT = "69e8afe9-c16a-4322-843f-ade61ab30a8e"
SOURCE = {"id": "453fc328-b19a-4cc9-95a7-70f521c52b69", "revision": 3}
AUTH_TEXT = "Authorize bounded B134 follow-up reviews, superseding the earlier one-pass-only restriction"
ARRIVAL_SECONDS = 120
# Child first: every runtime must contain its parent's SHA-256 literally.
RUNTIMES = (
    ("authorization-runtime-004/b134_authorized_confirmation_v3.py",
     "bcaaaf90cb771a3b84bf31bbbd1f173846f4fb99e114ab052afc11c279756450"),
    ("authorization-runtime-003/b134_authorized_confirmation_v2.py",
     "b76bd7c306a7911c7bce6c31f159dfa396ee17eff8584c7eec847e48f82568fc"),
    ("authorization-runtime-002/b134_authorized_confirmation_v1.py",
     "65956a69b4f0c0cf4849228f8a554cd9c6d13afefdcf4a1427682cfea24964a1"),
    ("revision-confirmation-runtime-repair-001/b134_revision_confirmation_v5.py",
     "ad100a8e18fdfa994d417318e58a3112bd61a135f766bc3932cf5a44901f1fe6"),
    ("revision-confirmation-runtime-repair-001/b134_revision_confirmation_v4.py",
     "9457d59614d5d34ef22c2a2b1c7e5134cca3d098ee7abca94ec4c1f9e4819e38"),
    ("revision-confirmation-runtime-repair-001/b134_revision_confirmation_v3.py",
     "2b66f26b3604a79bf5fa59eed7e29f7ce83063c5966455a7c73fb7c4b8fa953c"),
    ("integration-confirmation-prep-001/selected-runtime-003/b134_revision_confirmation_v2.py",
     "7cd7c37e2f868584d6212336ec29fdd66576684d0e8ef0c6a899c6a8c5e6f125"),
    ("integration-confirmation-prep-001/selected-runtime-002/b134_integration_confirmation_v1.py",
     "4070171ab891062859a5df1e07d7f6ab76732c66832db353e08aacf271a45f61"),
)
PUBLISHED_RUNTIMES = 3
RT = {"rt4": ROOT / RUNTIMES[0][0], "rt3": ROOT / RUNTIMES[1][0], "rt2": ROOT / RUNTIMES[2][0],
      "rt1": ROOT / "authorization-runtime-001" / "b134_authorized_confirmation_v1.py"}
LOCAL_RUNTIMES = (
    ("authorization-runtime-001/b134_authorized_confirmation_v1.py",
     "2bd57bc4fbdd17295953996a0bd77ec68fefb786aa8d01122f23f2629b4d8035"),
    ("authorization-runtime-003/test_authorized_confirmation_v2.py",
     "206a99104b7663793d0ec90310f636ee512ed4fe66b2bd2870e3c32c84167966"),
    ("authorization-runtime-004/test_authorized_confirmation_v3.py",
     "6068214775ea7827af2ee412d73ee88672be631a5ada1967f074b31bf04a03aa"),
)
PRODUCERS = {"claude": "rt3", "gpt": "rt4"}
STEPS = {
    "claude": (("prepare", "authorization-claude-prepare-execution-002", "rt2"),
               ("admit", "authorized-claude-admit-exec-001", "rt2"),
               ("final", "authorized-claude-final-exec-003", "rt3"),
               ("accept", "authorized-claude-accept-exec-001", "rt3")),
    "gpt": (("prepare", "authorization-gpt-prepare-execution-002", "rt2"),
            ("admit", "authorized-gpt-admit-exec-001", "rt3"),
            ("final", "authorized-gpt-final-exec-002", "rt4"),
            ("accept", "authorized-gpt-accept-exec-001", "rt4")),
}
FREEZE = (ROOT / "authorized-receipt-freeze-001" / "freeze.json",
          "c6612e180711d825d3a639d653df4e848ed2de99179224b04ca20b215c682dc3")
# family, step, receipt folder, runtime, exact last log line (None: exit 0), published reason, output folder
ATTEMPTS = (
    ("claude", "prepare", "authorization-claude-prepare-execution-001", "rt1", None,
     "Superseded runtime-001 preparation; its preflight was never admitted, delivered or reviewed.",
     "authorized-claude-confirmation-001"),
    ("gpt", "prepare", "authorization-gpt-prepare-execution-001", "rt1", None,
     "Superseded runtime-001 preparation; its preflight was never admitted, delivered or reviewed.",
     "authorized-gpt-confirmation-001"),
    ("claude", "final", "authorized-claude-final-exec-001", "rt2",
     "ValueError: Authorization delivered in wrong actual mode",
     "Runtime-002 required an agentMode field that actual App-forwarded user.message events omit; "
     "runtime-003 instead requires the delivered turn's own turn_start to be interactive. No re-delivery.",
     "authorized-claude-final-001"),
    ("claude", "final", "authorized-claude-final-exec-002", "rt3",
     "ValueError: Writable frozen input: " + str(ROOT / RUNTIMES[1][0]),
     "Runtime-003 was still writable; the unchanged file was made read-only and the same audit rerun.",
     "authorized-claude-final-002"),
    ("gpt", "final", "authorized-gpt-final-exec-001", "rt3",
     "ValueError: Bounded returned-byte/read/write/completion audit failed",
     "Runtime-003 rejected the actual single apply_patch report write carried with LF-to-CRLF transport; "
     "runtime-004 binds exactly that transport and the same audit was rerun.",
     "authorized-gpt-final-001"),
)


def ref(path, digest):
    return {"path": str(path), "sha256": digest}


def read_ref(value):
    return original.read_review(value["path"], value["sha256"])


def load(value):
    return json.loads(read_ref(value))


def parse(raw):
    return [json.loads(line) for line in raw.decode("utf-8").splitlines()]


def stamp(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def block(text, tag):
    require(text.count("<" + tag + ">") == text.count("</" + tag + ">") == 1,
            "Missing/duplicate forwarded authorization block: " + tag)
    return json.loads(text.split("<" + tag + ">", 1)[1].split("</" + tag + ">", 1)[0])


def forwarded(data, kickoff):
    require(data.get("source") == "agent-" + COORDINATOR,
            "Forwarded authorization is not from this coordinator")
    text = data.get("transformedContent", "")
    require(block(text, "forwarded_user_message_source_json") == SOURCE
            and block(text, "forwarded_user_message_json") == AUTH_TEXT
            and block(text, "coordinator_instructions_json") == kickoff
            and data.get("content") == (
                "Forwarded user message:\n\n> " + AUTH_TEXT + "\n\nCoordinator instructions:\n\n" + kickoff),
            "Missing/wrong live user authorization or changed frozen coordinator instructions")


def authority(raw):
    rows = parse(raw)
    require(len(rows) == 1 and rows[0]["id"] == AUTH_EVENT and rows[0]["type"] == "user.message",
            "Not the actual received authorization event")
    data = rows[0]["data"]
    forwarded(data, block(data.get("transformedContent", ""), "coordinator_instructions_json"))
    return rows[0]


def check_delivery(events, prefix, admission, kickoff, auth_row):
    offset = admission["offset"]
    require(isinstance(offset, int) and 0 < offset == len(prefix)
            and prefix.endswith(b"\n") and events[:offset] == prefix,
            "Admission prefix is not the exact retained stream prefix")
    suffix = parse(events[offset:])
    users = [index for index, row in enumerate(suffix) if row["type"] == "user.message"]
    require(len(users) == 1, "Exactly one delivered authorization turn is required")
    row = suffix[users[0]]
    data = row["data"]
    require(data.get("agentMode", "interactive") == "interactive", "Authorization delivered in wrong actual mode")
    at, authorized, admitted = stamp(row["timestamp"]), stamp(auth_row["timestamp"]), stamp(admission["createdAt"])
    require(at > authorized, "Authorization cannot be applied retroactively")
    require(admission["messageMustArriveWithinSeconds"] == ARRIVAL_SECONDS
            and admitted <= at <= admitted + dt.timedelta(seconds=ARRIVAL_SECONDS),
            "Authorization was not delivered inside its admission window")
    forwarded(data, kickoff)
    turn, interaction = data.get("turnId"), data.get("interactionId")
    require(isinstance(turn, str) and turn and isinstance(interaction, str) and interaction,
            "Delivered authorization turn identity is missing")
    opened = [item for item in suffix[users[0] + 1:] if item["type"] == "assistant.turn_start"]
    require(opened and opened[0]["data"].get("turnId") == turn
            and opened[0]["data"].get("interactionId") == interaction
            and opened[0]["data"].get("agentMode") == "interactive",
            "The delivered authorization turn did not actually start in interactive mode")
    return {
        "secondsAfterAuthorization": round((at - authorized).total_seconds(), 3),
        "secondsAfterAdmission": round((at - admitted).total_seconds(), 3),
        "forwardedContentSha256": sha(data["content"].encode("utf-8")),
        "deliveredUserMessages": 1, "turnStartedInteractive": True,
    }, interaction


def check_request(request, own):
    require(set(request) == {"reviews", "revision", "resolution", "evidence", "protectedSources", "limits"},
            "Unexpected closure request fields")
    require(isinstance(request["reviews"], list)
            and [item["spec"]["family"] for item in request["reviews"]] == list(FAMILIES)
            and [item["spec"]["run"] for item in request["reviews"]] == [FRESH[f] for f in FAMILIES],
            "Both serial FRESH-003 reviews are required")
    revision = request["revision"]
    require(set(revision) == {"candidate", "priorSnapshot", "confirmations", "literalDispositionTokens",
                              "scopeProof", "gateProof", "scopeHold"}
            and revision["candidate"] == REVISED and revision["priorSnapshot"] == PRIOR,
            "Revision block differs")
    accepted = revision["confirmations"]
    require(list(accepted) == list(FAMILIES), "Two serial family confirmations are required")
    require(history.HELD_CLAUDE_SHA not in {value["sha256"] for value in accepted.values()},
            "A historical held acceptance cannot become prospective authorization")
    require(all(set(accepted[f]) == {"path", "sha256"} and accepted[f]["sha256"] == ACCEPTANCES[f]
                for f in FAMILIES), "Confirmation acceptances are not the pinned authorized results")
    tokens = revision["literalDispositionTokens"]
    require(list(tokens) == [RUNS[f] for f in FAMILIES]
            and all(list(tokens[RUNS[f]]) == list(history.OBLIGATIONS[f]) for f in FAMILIES),
            "Literal confirmation tokens differ")
    require(revision["scopeProof"]["sha256"] == history.PROOFS["scope"]
            and revision["gateProof"]["sha256"] == history.PROOFS["gates"]
            and revision["scopeHold"]["sha256"] == history.HOLD_SHA, "Revision proofs differ")
    evidence = {item["archivePath"]: item for item in request["evidence"]}
    require(len(evidence) == len(request["evidence"]), "Duplicate closure evidence path")
    for path, digest in (("protocol/close_b134_v2.py", PINS["close_b134_v2.py"]),
                         ("protocol/b134_revision_history.py", PINS["b134_revision_history.py"]),
                         ("protocol/b134_revision_progress.py", PINS["b134_revision_progress.py"]),
                         ("verification/revision-scope.json", history.PROOFS["scope"]),
                         ("verification/revision-gates.json", history.PROOFS["gates"]),
                         ("history/revision-scope-hold.json", history.HOLD_SHA)):
        require(path in evidence and evidence[path]["sha256"] == digest, "Missing pinned evidence: " + path)
    item = evidence.get("protocol/close_b134_v3.py")
    require(item is not None and item["sha256"] == sha(own) and read_ref(item) == own,
            "Closure must retain this authorized-confirmation assembler")
    return evidence


def check_tokens(family, tokens, adjudication, decision, structure, config, spec):
    obligations = list(history.OBLIGATIONS[family])
    require(list(tokens) == obligations
            and adjudication["dispositions"] == decision["dispositions"] == structure["dispositions"] == tokens
            and config["dispositionIds"] == obligations
            and [row["id"] for row in spec["obligations"]] == obligations,
            "Literal confirmation tokens differ from the adjudicated report")


def check_records(family, item, records):
    """Identity, acceptance, scope and authorization agreement across one confirmation."""
    run, session = RUNS[family], history.SESSIONS[family]
    acceptance, final, adjudication, decision = (records[k] for k in ("acceptance", "final", "adjudication", "decision"))
    preflight, spec, config, admission = (records[k] for k in ("preflight", "spec", "config", "admission"))
    audit, context, structure = records["audit"], records["context"], records["structure"]
    require(item["spec"]["session"] == session and item["spec"]["run"] == FRESH[family],
            "Confirmation reviewer differs from its own FRESH-003 reviewer")
    identity = {"run": run, "family": family, "session": session, "candidate": REVISED}
    require(all(record.get(key) == value for record in (acceptance, final, adjudication, decision, preflight, spec)
                for key, value in identity.items())
            and config["run"] == admission["run"] == audit["run"] == run
            and config["session"] == admission["session"] == audit["session"] == session
            and config["candidate"] == admission["candidate"] == audit["candidate"] == REVISED
            and config["expectedFamily"] == context["family"] == family,
            "Confirmation run, session, family or snapshot differs")
    scope = acceptance["scope"]
    require(isinstance(scope, str) and scope
            and all(record["scope"] == scope for record in
                    (final, adjudication, decision, preflight, spec, config, admission)),
            "Confirmation scope differs")
    require(acceptance["batch"] == final["batch"] == preflight["batch"] == original.BATCH
            and acceptance["mode"] == final["mode"] == preflight["mode"] == spec["mode"] == config["mode"] == "revision"
            and acceptance["verdict"] == adjudication["verdict"] == decision["verdict"] == "CONFIRMED"
            and final["confirmation"] == structure["confirmation"] == "CONFIRMED"
            and acceptance["confirmationAccepted"] is True and acceptance["reviewEvidenceAccepted"] is True
            and acceptance["acceptedNewFindings"] == acceptance["openClaimIds"] == []
            and adjudication["acceptedNewFindings"] == adjudication["openClaimIds"] == []
            and acceptance["priorRawVerdict"] == final["priorRawVerdict"] == adjudication["priorRawVerdict"]
            == preflight["priorRawVerdict"] == config["priorVerdict"] == "NEEDS FIX"
            and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and final["reviewAccepted"] is False and preflight["reviewAccepted"] is False
            and admission["reviewAccepted"] is False and preflight["preparedOnly"] is True
            and acceptance["publicationAccepted"] is final["publicationAccepted"]
            is adjudication["publicationAccepted"] is False
            and acceptance["deliveryCredit"] == 0,
            "Confirmation acceptance chain differs")
    require(all(record["authorization"] == AUTH for record in
                (acceptance, final, adjudication, decision, preflight, spec, config))
            and acceptance["authorizationProspective"] is final["authorizationProspective"]
            is adjudication["authorizationProspective"] is True
            and adjudication["heldEvidenceTreatment"] == "retained-not-retroactively-authorized",
            "Confirmation is not bound to the actual prospective authorization")
    continuation = acceptance["continuation"]
    require(continuation["kind"] == CONTINUATIONS[family]
            and all(record["continuation"] == continuation for record in (final, adjudication, preflight, spec)),
            "Confirmation continuation differs")
    producer = ref(RT[PRODUCERS[family]], {"rt3": RUNTIMES[1][1], "rt4": RUNTIMES[0][1]}[PRODUCERS[family]])
    require(acceptance["producer"] == final["producer"] == adjudication["producer"] == producer,
            "Confirmation producer differs")
    require(acceptance["report"] == final["report"] == adjudication["report"] == decision["report"]
            and acceptance["final"] == adjudication["final"] == decision["final"]
            and Path(acceptance["report"]["path"]) == Path(config["report"])
            and adjudication["reportReadCompletely"] is True and adjudication["rawAuditWasClean"] is True
            and adjudication["controlAdjudicationApplied"] is False
            and {key: adjudication[key] for key in decision} == decision,
            "Confirmation report, final or substantive decision differs")
    require(admission["status"] == "ADMITTED_FOR_ONE_COORDINATOR_MESSAGE_ONLY"
            and admission["preflight"] == final["preflight"]
            and preflight["config"]["path"] == str(Path(config["chainManifest"]).with_name("config.json"))
            and config["chainManifest"] == preflight["chain"]["path"]
            and config["coordinator"] == COORDINATOR
            and preflight["priorFinal"] == item["final"]
            and spec["prior"]["review"]["run"] == FRESH[family]
            and spec["prior"]["review"]["session"] == session
            and spec["prior"]["review"]["snapshot"] == PRIOR,
            "Confirmation preparation or admission differs")
    preservation = preflight["preservation"]
    require(preservation["status"] == "BOUND_ACTUAL_COORDINATOR_REVISION_PROOFS_ONLY"
            and preservation["candidate"] == REVISED and preservation["priorSnapshot"] == PRIOR
            and preservation["scopeProof"]["sha256"] == spec["scopeProof"]["sha256"] == history.PROOFS["scope"]
            and preservation["gateProof"]["sha256"] == spec["gateProof"]["sha256"] == history.PROOFS["gates"],
            "Confirmation revision proofs differ")
    profile = config["profile"]
    require(context["status"] == "PASS" and context["errors"] == [] and context["compactions"] == []
            and all(context["contextProfile"][key] == profile[key]
                    for key in ("selectedModel", "contextTier", "maxPromptTokens"))
            and 0 < context["actualPeakInputTokens"] < profile["maxPromptTokens"],
            "Confirmation context differs or compacted")
    require(structure["contract"] == "confirm-structure-v1" and structure["status"] == "PASS"
            and structure["errors"] == [] and structure["nonAccepting"] == []
            and structure["findings"] == 0 and structure["optionalPoints"] == 0,
            "Confirmation report structure differs")
    require(audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and audit["breaches"] == []
            and audit["unexpectedUserMessages"] == 0 and audit["final"] is True
            and audit["chainRead"] == audit["chainRequired"] == len(records["chain"]["segments"])
            and audit["readbackVerified"] is True and audit["reviewerIdle"] is True
            and audit["recordIncomplete"] is False,
            "Confirmation audit is incomplete")


def runtime_ancestry():
    raws = [original.read_review(ROOT / relative, digest) for relative, digest in RUNTIMES]
    for child, (_, parent_digest) in zip(raws, RUNTIMES[1:]):
        require(parent_digest.encode("ascii") in child, "Runtime ancestry pin differs")
    return raws


def command(runtime, step, *paths):
    return ["python", "-B", str(RT[runtime]), step, *(str(path) for path in paths)]


def receipt(folder, expected, success):
    path = ROOT / folder
    raw = original.read_review(path / "receipt.json")
    value = json.loads(raw)
    log = original.read_review(path / "output.log", value["logSha256"])
    require(value["command"] == expected and value["cleanupError"] is None
            and not value["memory"]["breach"] and (value["exitCode"] == 0) is success,
            "Execution receipt differs: " + folder)
    return value, log, [ref(path / "receipt.json", sha(raw)), ref(path / "output.log", sha(log))]


def local_tree(folder, published=()):
    path = ROOT / folder
    rows = []
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        if item in published:
            continue
        raw = original.read_review(item)
        rows.append({"path": str(item), "sha256": sha(raw), "bytes": len(raw)})
    return rows


def dedupe(rows):
    kept = {}
    for row in rows:
        key = str(Path(row["path"]).resolve())
        require(kept.setdefault(key, row)["sha256"] == row["sha256"], "Conflicting local retention: " + key)
    return list(kept.values())


def step_commands(family, records):
    request = ROOT / "authorization-continuation-prep-001" / ("request-" + family + ".json")
    preflight, admission = records["paths"]["preflight"], records["paths"]["admission"]
    final, decision = records["paths"]["final"], records["paths"]["decision"]
    return {
        "prepare": ("prepare", request, preflight.parent),
        "admit": ("admit", preflight, records["paths"]["observation"], admission.parent),
        "final": ("final", preflight, admission, final.parent),
        "accept": ("accept", final, decision, records["paths"]["acceptance"].parent),
    }


def gather(family, revision):
    refs = {"acceptance": revision["confirmations"][family]}
    records = {"acceptance": load(refs["acceptance"])}

    def follow(key, source, field=None):
        refs[key] = records[source][field or key]
        require(set(refs[key]) == {"path", "sha256"}, "Unexpected confirmation reference: " + key)
        records[key] = load(refs[key])

    follow("final", "acceptance")
    follow("adjudication", "acceptance")
    follow("decision", "adjudication", "substantiveDecisionInput")
    for key in ("preflight", "admission", "audit", "context", "structure"):
        follow(key, "final")
    for key in ("spec", "config", "chain"):
        follow(key, "preflight")
    follow("observation", "admission")
    refs["report"] = records["acceptance"]["report"]
    records["refs"], records["paths"] = refs, {key: Path(value["path"]) for key, value in refs.items()}
    return records


def collect(family, item, revision, auth_row):
    records = gather(family, revision)
    paths = records["paths"]
    check_records(family, item, records)
    check_tokens(family, revision["literalDispositionTokens"][RUNS[family]], records["adjudication"],
                 records["decision"], records["structure"], records["config"], records["spec"])
    if family == "gpt":
        require(records["observation"]["priorClaudeAcceptance"] == revision["confirmations"]["claude"],
                "GPT admission was not observed after the accepted Claude confirmation")
    audit = records["audit"]
    events = original.read_review(paths["audit"].parent / "events.jsonl", audit["eventsSha256"])
    require(len(events) == audit["eventsBytes"], "Confirmation event snapshot length differs")
    original.verify_audited_chain(records["chain"], audit, parse(events), "chain")
    prefix_ref = records["admission"]["prefix"]
    prefix = original.read_review(prefix_ref["path"], prefix_ref["sha256"])
    kickoff_raw = original.read_review(records["config"]["kickoff"])
    require(records["admission"]["kickoff"] == kickoff_raw.decode("utf-8"), "Admitted kickoff differs")
    delivery, interaction = check_delivery(events, prefix, records["admission"], records["admission"]["kickoff"],
                                           auth_row)
    return records, events, prefix, kickoff_raw, delivery, interaction


def add_confirmation(files, family, item, revision, auth_row, producers, guard):
    records, events, prefix, kickoff_raw, delivery, interaction = collect(family, item, revision, auth_row)
    guard.check()
    run, paths = RUNS[family], records["paths"]
    prefix_dir = "confirmations/" + run + "/"
    acceptance = records["acceptance"]
    entry = {
        "family": family, "run": run, "role": ROLE, "session": history.SESSIONS[family],
        "priorRun": FRESH[family], "priorSnapshot": PRIOR, "snapshot": REVISED, "mode": "revision",
        "scope": acceptance["scope"], "verdict": "CONFIRMED", "priorRawVerdict": "NEEDS FIX",
        "reviewAccepted": True, "confirmationAccepted": True, "originalReviewerConfirmation": False,
        "acceptedNewFindings": [], "openClaimIds": [],
        "dispositions": dict(revision["literalDispositionTokens"][run]),
        "authorizationProspective": True,
        "heldEvidenceTreatment": records["adjudication"]["heldEvidenceTreatment"],
        "continuationKind": acceptance["continuation"]["kind"],
        "publicationAccepted": False, "deliveryCredit": 0,
    }
    published = set()
    for key, name in (("report", "report.md"), ("final", "final.json"), ("acceptance", "acceptance.json"),
                      ("adjudication", "adjudication.json"), ("decision", "decision.json"),
                      ("context", "context.json"), ("structure", "structure.json"),
                      ("preflight", "preflight.json"), ("admission", "admission.json"),
                      ("config", "config.json"), ("spec", "request.json")):
        entry[key] = original.put(files, prefix_dir + name, read_ref(records["refs"][key]))
        published.add(paths[key])
    for key in ("prompt", "kickoff"):
        path = Path(records["config"][key])
        raw = kickoff_raw if key == "kickoff" else original.read_review(path)
        entry[key] = original.put(files, prefix_dir + key + ".txt", raw)
        published.add(path)
    entry["producer"] = producers[str(RT[PRODUCERS[family]])]
    entry["delivery"] = delivery
    retention = original.add_chain(files, run, records["preflight"]["chain"], guard)
    published.add(paths["chain"])
    local = [{"path": str(paths["audit"].parent / "events.jsonl"), "sha256": sha(events), "bytes": len(events)},
             {**records["admission"]["prefix"], "bytes": len(prefix)}]
    commands = step_commands(family, records)
    receipts = []
    for step, folder, runtime in STEPS[family]:
        value, _, refs = receipt(folder, command(runtime, *commands[step]), True)
        receipts.append({"step": step, "runtimeSha256": sha(original.read_review(RT[runtime])),
                         "receiptSha256": refs[0]["sha256"], "exitCode": value["exitCode"]})
        local.extend(refs)
        guard.check()
    for key in ("preflight", "admission", "final", "acceptance", "decision", "observation"):
        local.extend(local_tree(paths[key].parent.relative_to(ROOT), published))
    entry["executions"] = receipts
    return entry, local, retention, interaction


def non_accepted_attempts():
    rows, local = [], []
    for family, step, folder, runtime, failure, reason, out in ATTEMPTS:
        if step == "prepare":
            args = ("prepare", ROOT / "authorization-continuation-prep-001" / ("request-" + family + ".json"),
                    ROOT / out)
        else:
            confirmation, admit = ROOT / ("authorized-" + family + "-confirmation-002"), ROOT / (
                "authorized-" + family + "-admit-001")
            args = ("final", confirmation / "preflight.json", admit / "admission.json", ROOT / out)
        value, log, refs = receipt(folder, command(runtime, *args), failure is None)
        if failure is not None:
            lines = log.decode("utf-8").strip().splitlines()
            require(lines and lines[-1] == failure, "Failed attempt reason differs: " + folder)
        rows.append({
            "family": family, "run": RUNS[family], "step": step,
            "status": "SUPERSEDED_PREPARATION_NOT_REVIEW" if failure is None else "FAILED_ATTEMPT_NOT_ACCEPTED",
            "reason": reason, "runtimeSha256": sha(original.read_review(RT[runtime])),
            "receiptSha256": refs[0]["sha256"], "logSha256": refs[1]["sha256"], "exitCode": value["exitCode"],
            "reviewAccepted": False, "deliveryCredit": 0,
        })
        local.extend(refs)
        local.extend(local_tree(out))
    return rows, local


def check_freeze():
    raw = original.read_review(*FREEZE)
    value = json.loads(raw)
    require(value["status"] == "MADE_READ_ONLY_BYTES_UNCHANGED" and len(value["files"]) == 18,
            "Receipt freeze record differs")
    for row in value["files"]:
        original.read_review(row["path"], row["sha256"])
    return ref(*FREEZE)


def uuid_findings(files, allowed):
    found = []
    for name, raw in sorted(files.items()):
        unknown = {value.lower() for text in texts(name, raw) for value in UUID.findall(text)} - allowed
        found.extend({"file": name, "uuid": value} for value in sorted(unknown))
    return found


def evidence_ref(files, path, digest):
    require(path in files and sha(files[path]) == digest, "Missing archived proof: " + path)
    return {"path": path, "sha256": digest}


def assemble(mode, request_path, output, report_path, own):
    request_raw = original.read_review(request_path)
    request = json.loads(request_raw)
    check_request(request, own)
    guard, _ = start_guard("B134 cc374 authorized-confirmation closure")
    try:
        git = original.Git(REPO, original.RUNNER, guard)

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == REVISED
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Closure requires the clean revised snapshot")
            require(original.lineage(git, REVISED) > 0, "Missing signed reconciliation/correction lineage")

        clean()
        manifest = git("show", REVISED + ":manifest.json")
        progress_raw = git("show", original.CANDIDATE + ":" + original.PROGRESS)
        require(git("show", REVISED + ":" + original.PROGRESS) == progress_raw
                and (REPO / original.PROGRESS).read_bytes() == progress_raw
                and (REPO / "manifest.json").read_bytes() == manifest,
                "Revised manifest or original progress changed")
        base, files = original.load_originals()
        retentions = copy.deepcopy(base["chainRetention"])
        launch_hold, local = original.retain_launch_hold(files)
        fresh, original_claims = [], {}
        for item in request["reviews"]:
            entry, retained, retention = original.add_replacement(files, item, guard)
            fresh.append(entry)
            local.extend(retained)
            retentions[entry["run"]] = retention
        for family in original.INITIALS:
            _, refs, _, claims = original.actual_initial(family)
            original_claims[family] = {
                "report": original.ref_bytes(refs["report"]), "reportSha256": refs["report"]["sha256"],
                "claims": claims,
            }
        core_ref = {"path": str(original.CORE_ROOT / "fresh-independent-core-001.json"), "sha256": original.CORE_SHA}
        retentions["fresh-core"] = original.add_chain(files, "fresh-core", core_ref, guard)
        original.put(files, ".gitattributes", b"* -text\n")
        original.put(files, "verification/original-progress.json", progress_raw)
        for label, (relative, digest) in original.PROOFS.items():
            original.put(files, "verification/" + label + ".json", original.read_review(ROOT / relative, digest))
        for item in request["evidence"]:
            original.put(files, item["archivePath"], read_ref(item))
        original.put(files, "protocol/close_b134.py", frozen(v2.SOURCE, v2.SOURCE_SHA))
        original.put(files, "verification/fresh-local-retention.json", json_bytes({
            "files": local, "policy": "Raw audits, events, admissions, rosters and execution logs remain local.",
        }))

        auth_raw = original.read_review(AUTH["path"], AUTH["sha256"])
        auth_row = authority(auth_raw)
        runtimes = runtime_ancestry()
        producers = {
            str(ROOT / relative): original.put(files, "protocol/authorized-confirmation/" + relative, raw)
            for (relative, _), raw in zip(RUNTIMES[:PUBLISHED_RUNTIMES], runtimes)
        }
        confirmations, confirmation_local, interactions = [], [AUTH, check_freeze()], set()
        for family, item in zip(FAMILIES, request["reviews"]):
            entry, retained, retention, interaction = add_confirmation(
                files, family, item, request["revision"], auth_row, producers, guard)
            confirmations.append(entry)
            confirmation_local.extend(retained)
            retentions[entry["run"]] = retention
            interactions.add(interaction.lower())
        authorization_ref = original.put(files, "confirmations/authorization.json", json_bytes({
            "schemaVersion": 1, "batch": original.BATCH,
            "status": "ACTUAL_USER_AUTHORIZATION_APPLIED_PROSPECTIVELY",
            "authorizationText": AUTH_TEXT, "sourceRevision": SOURCE["revision"],
            "authorizationEventSha256": AUTH["sha256"], "authorizationTimestamp": auth_row["timestamp"],
            "deliveries": {entry["run"]: entry["delivery"] for entry in confirmations},
            "treatment": "Prospective only. Earlier refusals, the scope hold and the held Claude acceptance "
                         "remain historical evidence and are not retroactively authorized. Each confirmation "
                         "turn received exactly one App-forwarded copy of this user authorization with its "
                         "frozen coordinator kickoff, after the authorization and inside its admission window.",
            "rawEventRetention": "The authorization event and reviewer event streams remain local; "
                                 "only hashes and timing deltas are published.",
        }))
        for entry in confirmations:
            entry["authorization"] = authorization_ref
        attempts, attempt_local = non_accepted_attempts()
        attempts_ref = original.put(files, "history/authorized-attempts.json", json_bytes(attempts))
        for (relative, digest), raw in zip(RUNTIMES[PUBLISHED_RUNTIMES:], runtimes[PUBLISHED_RUNTIMES:]):
            confirmation_local.append({"path": str(ROOT / relative), "sha256": digest, "bytes": len(raw)})
        for relative, digest in LOCAL_RUNTIMES:
            confirmation_local.append(ref(ROOT / relative, sha(original.read_review(ROOT / relative, digest))))
        original.put(files, "verification/confirmation-local-retention.json", json_bytes({
            "files": dedupe(confirmation_local + attempt_local),
            "runtimeAncestry": [{"path": relative, "sha256": digest} for relative, digest in RUNTIMES],
            "policy": "Authorization and reviewer event streams, audits, admissions, observations, rosters, "
                      "receipts, logs, failed or superseded attempts and deeper runtime ancestry remain local. "
                      "Each runtime contains its parent's SHA-256; the producers are not re-executed here.",
        }))
        windows = set()
        sums_raw = original.read_review(original.CORE_ROOT / "packet" / "SHA256SUMS.json", original.PACKET_SHA)
        for name, digest in json.loads(sums_raw).items():
            raw = original.read_review(original.CORE_ROOT / "packet" / name, digest)
            if original.protected_source(name):
                original.add_protected(windows, raw, name.endswith((".html", ".htm")))
            guard.check()
        for item in request["protectedSources"]:
            path = Path(item["path"]).resolve()
            require(path.is_relative_to(WS), "Protected source escaped N1 workspace")
            original.add_protected(windows, frozen(path, item["sha256"]), path.suffix in (".html", ".htm"))
        require(windows, "Missing protected-source scan windows")
        original.put(files, "packet/SHA256SUMS.json", sums_raw)
        resolution_raw = read_ref(request["resolution"])
        resolution_ref = original.put(files, "resolution.json", resolution_raw)
        allowed = {COORDINATOR, original.AUTHOR, original.FAILED_SESSION, original.HELD_SESSION,
                   *original.METER_SESSIONS, SOURCE["id"], AUTH_EVENT, *interactions,
                   *(entry["session"] for entry in base["reviewLineage"] + fresh)}
        report = {"batch": original.BATCH, "mode": mode, "assemblyRequestSha256": sha(request_raw),
                  "confirmationRuns": [entry["run"] for entry in confirmations]}
        unknown = uuid_findings(files, allowed)
        if unknown:
            freeze_json(report_path, {**report, "status": "UNKNOWN_IDENTITIES", "uuidFindings": unknown})
            require(False, "Unknown identity must be investigated, not filtered; report preserved")
        adjustments = original.retain_overlapping_chains(files, windows, allowed, guard, retentions)
        original.put(files, "verification/chain-retention-adjustments.json", json_bytes(adjustments))
        uuids, leaks = original.publication_findings(files, windows, allowed, guard)
        checks = {"uuidFindings": len(uuids), "externalWindowFindings": len(leaks)}
        report.update(files=len(files) + 1, publicationChecks=checks, uuidFindings=uuids,
                      externalWindowFindings=leaks)
        freeze_json(report_path, report)
        require(not uuids and not leaks, "Publication retention failed; report preserved")
        closure = original.history(base, fresh, files, resolution_ref, request["limits"])
        closure.update(schemaVersion=2, reviewedSnapshot=REVISED, priorReviewedSnapshot=PRIOR,
                       reviewMode=history.MODE)
        closure["reviewLineage"].extend(confirmations)
        closure["confirmationRuns"] = [entry["run"] for entry in confirmations]
        closure["revisionProofs"] = {
            "scope": evidence_ref(files, "verification/revision-scope.json", history.PROOFS["scope"]),
            "gates": evidence_ref(files, "verification/revision-gates.json", history.PROOFS["gates"]),
        }
        closure["continuationHistory"] = {
            "scopeHold": evidence_ref(files, "history/revision-scope-hold.json", history.HOLD_SHA),
            "authorization": authorization_ref, "nonAcceptedAuthorizedAttempts": attempts_ref,
            "heldClaudeAcceptance": "retained-not-retroactively-authorized",
        }
        closure["nonAcceptedLaunches"] = [launch_hold]
        closure.update(publicationChecks=checks, chainRetention=retentions,
                       assemblyRequestSha256=sha(request_raw))
        resolution = json.loads(resolution_raw)
        history.validate_resolution(resolution, closure, REVISED, original_claims)
        closure_raw = json_bytes(closure)
        ledger = progress.closed_progress(json.loads(progress_raw), closure_raw, manifest, resolution,
                                          original_claims)
        clean()
        for name, raw in sorted(files.items()):
            write_frozen(output / name, raw)
            guard.check()
        write_frozen(output / "provenance.json", closure_raw)
        if mode == "real":
            path = REPO / original.PROGRESS
            require(path.read_bytes() == progress_raw, "Progress changed before replacement")
            path.chmod(0o644)
            path.write_bytes(json_bytes(ledger))
            path.chmod(0o444)
            require(frozen(path) == json_bytes(ledger), "Progress readback failed")
        print(json.dumps({**report, "status": "PASS", "closureSha256": sha(closure_raw),
                          "progressUpdated": mode == "real"}))
    finally:
        require(not guard.finish()["breach"], "Closure RAM breach")


def main(mode, request_path, output):
    report_path = REAL_REPORT if mode == "real" else output.with_name(output.name + "-report.json")
    require(mode in ("dry", "real") and not output.exists() and not report_path.exists(),
            "Preserve existing closure attempts")
    require((mode == "dry" and output.parent == HERE)
            or (mode == "real" and output == REPO / original.CLOSURE), "Unexpected closure destination")
    own = frozen(Path(__file__))
    original.read_review = v2.read_review
    try:
        assemble(mode, request_path, output, report_path, own)
    finally:
        original.read_review = v2.original_reader


if __name__ == "__main__":
    require(len(sys.argv) == 4, __doc__)
    main(sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())
