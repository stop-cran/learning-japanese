"""Preserve the exact native Windows report write, disk and full readback bindings.

Only the native create transport may expand LF to CRLF. The unchanged inherited
auditor's normalization note is retained, not suppressed or relabelled "exact".
Every other note still rejects admission to semantic adjudication. The parser
receives canonical line endings, while all archived and audited bytes stay raw.
"""
import datetime as dt
import inspect
import sys
from pathlib import Path

from common import frozen, load_module, require, sha

PARENT = Path(__file__).with_name("b134_revision_confirmation_v3.py")
PARENT_SHA = "2b66f26b3604a79bf5fa59eed7e29f7ce83063c5966455a7c73fb7c4b8fa953c"
frozen(PARENT, PARENT_SHA)
parent = load_module("b134_confirmation_pinned_native_create_v3", PARENT)
legacy = parent.legacy
legacy.PINS["nativeCreateV3"] = (PARENT, PARENT_SHA)


def transport_valid(stored, requested):
    return (stored == requested
            or (b"\r" not in requested and stored == requested.replace(b"\n", b"\r\n")))


source = inspect.getsource(parent.check_native_create)
before = 'Path(report).read_bytes() == args["file_text"].encode("utf-8")'
after = 'transport_valid(Path(report).read_bytes(), args["file_text"].encode("utf-8"))'
require(source.count(before) == 1, "Native create transport repair anchor changed")
derived = source.replace(before, after, 1)
require(derived.replace(after, before, 1) == source, "Transport repair is not reversible")
exec(compile(derived, str(__file__), "exec"), globals())

NORMALIZATION_NOTE = "Report on disk equals its single write after CRLF normalization"


def audit_snapshot(raw, record, config, chain, admission):
    prefix_raw = legacy.read(admission["prefix"])
    require(len(prefix_raw) == admission["offset"] and raw.startswith(prefix_raw),
            "Admission prefix changed")
    prefix = legacy.parse_events(prefix_raw)
    suffix = legacy.parse_events(raw[len(prefix_raw):])
    check_native_create(suffix, config["report"])
    users = [row for row in suffix if row["type"] == "user.message"]
    require(len(users) == 1 and users[0]["data"].get("source") == "agent-" + legacy.COORDINATOR
            and users[0]["data"].get("content") == admission["kickoff"],
            "Unexpected/missing kickoff or autopilot turn")
    created = dt.datetime.fromisoformat(admission["createdAt"])
    sent = dt.datetime.fromisoformat(users[0]["timestamp"].replace("Z", "+00:00"))
    require(0 <= (sent - created).total_seconds() < 120,
            "Kickoff was delivered outside fresh admission window")
    telemetry = legacy.event_envelope(prefix, suffix, record["family"], record["session"])
    auditor, _, _, _ = legacy.modules()
    audit = auditor.audit(suffix, config, chain, final=True, record_incomplete=False)
    native = [
        call for row in suffix if row["type"] == "assistant.message"
        for call in (row.get("data") or {}).get("toolRequests", [])
        if str(call.get("name", "")).removeprefix("functions.") == "create"
    ]
    binding_ok = (
        (audit["reportBinding"] == "exact" and audit["notes"] == [])
        or (audit["reportBinding"] == "line-endings-normalized" and len(native) == 1
            and audit["notes"] == [NORMALIZATION_NOTE])
    )
    require(audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and audit["breaches"] == []
            and binding_ok and audit["unexpectedUserMessages"] == audit["fetches"] == 0
            and audit["chainRead"] == audit["chainRequired"] == len(chain["segments"])
            and audit["writes"] == audit["readbacks"] == 1
            and audit["readbackVerified"] is True and audit["reviewerIdle"] is True
            and len(audit["messages"]) == 1,
            "Bounded returned-byte/read/write/completion audit failed")
    report = Path(config["report"])
    stored = report.read_bytes()
    audit["transportBinding"] = {
        "rule": "native-create-exact-or-lf-to-crlf-v1" if native else "exact-add-file",
        "storedSha256": sha(stored),
        "rawReadbackEqualsStoredBytes": audit["readbackVerified"],
        "originalAuditorBinding": audit["reportBinding"],
        "originalAuditorNotes": list(audit["notes"]),
    }
    if native:
        audit["transportBinding"]["requestedSha256"] = sha(
            native[0]["arguments"]["file_text"].encode("utf-8"))
        audit["transportBinding"]["hostEditKind"] = "create"
    report.chmod(0o444)
    canonical = frozen(report).decode("utf-8").replace("\r\n", "\n")
    require("\r" not in canonical, "Unsupported bare-CR report transport")
    structure = legacy.check_structure(canonical, record, chain, audit["messages"][0])
    require(structure["status"] == "PASS",
            "Report structure failed: " + "; ".join(structure["errors"]))
    return audit, telemetry, structure


legacy.audit_snapshot = audit_snapshot
legacy.__file__ = __file__


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    require(argv and argv[0] in ("admit", "final", "accept"),
            "This repair only operates on existing frozen follow-up preparations")
    return legacy.main(argv)


if __name__ == "__main__":
    sys.exit(main())
